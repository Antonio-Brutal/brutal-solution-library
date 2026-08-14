#!/usr/bin/env python3
"""Raster renderer for the animated schematics (MOTION-SPEC.md).

Takes an animated SVG with a 6s seamless SMIL loop and produces a deterministic
MP4 + GIF, using exactly ONE headless-Chrome launch per video.

Technique (grid mode, the default)
----------------------------------
72 copies of the SVG are laid out in a 9x8 grid with zero gaps and no page
margin, each copy at half scale (600x315), giving a 5400x2520 page. An inline
script walks the copies and freezes copy i at t = i * 6/72 via
``setCurrentTime()`` + ``pauseAnimations()`` (plus the Web Animations API for
any CSS-driven motion, so stagger delays survive). One screenshot, then the PNG
is sliced into 72 frames and encoded, upscaled back to 1200x630.

Every copy is id-namespaced before embedding, otherwise the 72 inline SVGs would
share ids in one HTML document and all `url(#glow)` / `href="#pulse"` /
`<mpath>` references would collapse onto the first copy.

Safety net: after slicing, the frames are hashed. If the freeze did not take
(all tiles identical), the renderer automatically falls back to `perframe` mode
(one Chrome launch per frame) and says so loudly. Force either with --mode.

Usage
-----
    python3 build/render_motion.py articles/motion/<slug>.svg
    python3 build/render_motion.py articles/motion/*.svg --outdir articles/media
    python3 build/render_motion.py --selftest

Outputs <outdir>/<slug>.mp4, <outdir>/<slug>.gif, <outdir>/<slug>-poster.jpg.
"""

from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
DURATION = 6.0          # loop length, seconds (MOTION-SPEC hard rule)
FRAMES = 72             # 72 frames over 6s
FPS = 12                # 72 / 6
OUT_W, OUT_H = 1200, 630
TILE_W, TILE_H = 600, 315   # half scale
COLS, ROWS = 9, 8           # 9 * 8 = 72
GIF_W, GIF_H = 800, 420

DEFAULT_OUTDIR = os.path.join(ROOT, "articles", "media")


# --------------------------------------------------------------------------
# SVG preparation
# --------------------------------------------------------------------------

def _root_tag_span(svg: str) -> tuple[int, int]:
    """Return (start, end) offsets of the opening <svg ...> tag, quote-aware."""
    start = svg.index("<svg")
    i = start + 4
    quote = None
    while i < len(svg):
        ch = svg[i]
        if quote:
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
        elif ch == ">":
            return start, i + 1
        i += 1
    raise ValueError("unterminated <svg> tag")


def strip_prolog(svg: str) -> str:
    """Drop the XML declaration / doctype so the SVG can be inlined in HTML."""
    svg = re.sub(r"^\s*<\?xml[^>]*\?>\s*", "", svg)
    svg = re.sub(r"^\s*<!DOCTYPE[^>]*>\s*", "", svg, flags=re.I)
    return svg.strip()


ID_ATTR_RE = re.compile(r'\bid\s*=\s*"([^"]*)"')
TIMING_ATTR_RE = re.compile(r'\b(begin|end)\s*=\s*"([^"]*)"')


def namespace_ids(svg: str, prefix: str) -> str:
    """Rewrite every id and every reference to it with `prefix`.

    Covers id="", url(#id), href/xlink:href="#id", CSS selectors inside <style>,
    and SMIL syncbase timing values such as begin="foo.end+0.4s".
    """
    ids = [i for i in set(ID_ATTR_RE.findall(svg)) if i]
    if not ids:
        return svg

    svg = ID_ATTR_RE.sub(
        lambda m: 'id="%s%s"' % (prefix, m.group(1)) if m.group(1) in ids else m.group(0),
        svg,
    )

    alt = "|".join(re.escape(i) for i in sorted(ids, key=len, reverse=True))
    # #id anywhere it is a real reference (url(#x), href="#x", CSS "#x{...}")
    svg = re.sub(r"(?<![\w\-])#(%s)(?![\w\-])" % alt,
                 lambda m: "#%s%s" % (prefix, m.group(1)), svg)

    idset = set(ids)

    def fix_timing(m: re.Match) -> str:
        attr, value = m.group(1), m.group(2)
        parts = []
        for tok in value.split(";"):
            stripped = tok.strip()
            head = re.match(r"^([\w\-]+)\.", stripped)
            if head and head.group(1) in idset:
                stripped = prefix + stripped
            parts.append(stripped)
        return '%s="%s"' % (attr, ";".join(parts))

    return TIMING_ATTR_RE.sub(fix_timing, svg)


def size_root(svg: str, w: int, h: int) -> str:
    """Force explicit width/height on the root <svg> (viewBox is preserved)."""
    start, end = _root_tag_span(svg)
    tag = svg[start:end]
    if "viewBox" not in tag:
        raise SystemExit("SVG has no viewBox; MOTION-SPEC requires viewBox-only sizing")
    tag = re.sub(r'\s(width|height)\s*=\s*"[^"]*"', "", tag)
    tag = tag[:-1].rstrip()
    if tag.endswith("/"):
        tag = tag[:-1].rstrip()
    tag += ' width="%d" height="%d" preserveAspectRatio="xMidYMid meet">' % (w, h)
    return svg[:start] + tag + svg[end:]


FREEZE_JS = """
function freezeAll() {
  var svgs = document.querySelectorAll('#grid > svg');
  for (var i = 0; i < svgs.length; i++) {
    var svg = svgs[i], t = TIMES[i];
    try { svg.setCurrentTime(t); svg.pauseAnimations(); svg.setCurrentTime(t); } catch (e) {}
    // CSS / Web-Animations motion: seek the same instant, keeping stagger delays.
    if (svg.getAnimations) {
      var anims = svg.getAnimations({ subtree: true });
      for (var j = 0; j < anims.length; j++) {
        try { anims[j].currentTime = t * 1000; anims[j].pause(); } catch (e) {}
      }
    }
  }
  document.documentElement.setAttribute('data-frozen', svgs.length);
}
freezeAll();
document.addEventListener('DOMContentLoaded', freezeAll);
window.addEventListener('load', freezeAll);
"""


def build_page(svg_source: str, times: list[float], cols: int,
               tile_w: int, tile_h: int) -> str:
    """One HTML page holding len(times) id-namespaced copies, each frozen."""
    body = strip_prolog(svg_source)
    copies = []
    for i in range(len(times)):
        copy = namespace_ids(body, "f%02d-" % i)
        copies.append(size_root(copy, tile_w, tile_h))
    return (
        "<!doctype html><html><head><meta charset=\"utf-8\"><title>motion grid</title>"
        "<style>"
        "html,body{margin:0;padding:0;border:0;background:#020618;overflow:hidden;}"
        "#grid{display:grid;grid-template-columns:repeat(%d,%dpx);"
        "grid-auto-rows:%dpx;gap:0;line-height:0;font-size:0;width:%dpx;}"
        "#grid>svg{display:block;width:%dpx;height:%dpx;}"
        "</style></head><body><div id=\"grid\">%s</div>"
        "<script>var TIMES=%s;%s</script></body></html>"
        % (cols, tile_w, tile_h, cols * tile_w, tile_w, tile_h,
           "".join(copies), json.dumps([round(t, 6) for t in times]), FREEZE_JS)
    )


# --------------------------------------------------------------------------
# Chrome
# --------------------------------------------------------------------------

def chrome_screenshot(html_path: str, png_path: str, w: int, h: int,
                      verbose: bool = False) -> None:
    if not os.path.exists(CHROME):
        raise SystemExit("Google Chrome not found at %s" % CHROME)
    cmd = [
        CHROME, "--headless", "--disable-gpu",
        "--screenshot=%s" % png_path,
        "--window-size=%d,%d" % (w, h),
        "--hide-scrollbars",
        "--force-device-scale-factor=1",
        "--disable-extensions",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-features=DialMediaRouteProvider,Translate",
        "--virtual-time-budget=4000",
        "--run-all-compositor-stages-before-draw",
        "file://%s" % html_path,
    ]
    if verbose:
        print("  chrome:", " ".join(cmd[:1] + cmd[-1:]))
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if not os.path.exists(png_path) or os.path.getsize(png_path) == 0:
        raise SystemExit("Chrome produced no screenshot.\n%s\n%s"
                         % (proc.stdout[-2000:], proc.stderr[-2000:]))


# --------------------------------------------------------------------------
# Slicing
# --------------------------------------------------------------------------

def _have_pillow() -> bool:
    try:
        import PIL  # noqa: F401
        return True
    except ImportError:
        return False


def slice_grid(png_path: str, frame_dir: str, count: int, cols: int,
               tile_w: int, tile_h: int) -> list[str]:
    """Cut the grid screenshot into `count` frame PNGs. Pillow, else ffmpeg."""
    os.makedirs(frame_dir, exist_ok=True)
    paths = [os.path.join(frame_dir, "frame%03d.png" % i) for i in range(count)]

    if _have_pillow():
        from PIL import Image
        with Image.open(png_path) as sheet:
            sheet = sheet.convert("RGB")
            need_w, need_h = cols * tile_w, ((count + cols - 1) // cols) * tile_h
            if sheet.width < need_w or sheet.height < need_h:
                raise SystemExit(
                    "screenshot is %dx%d, expected at least %dx%d - Chrome clipped the grid"
                    % (sheet.width, sheet.height, need_w, need_h))
            for i, out in enumerate(paths):
                x, y = (i % cols) * tile_w, (i // cols) * tile_h
                sheet.crop((x, y, x + tile_w, y + tile_h)).save(out)
        return paths

    # Fallback: ffmpeg crop, one invocation per tile.
    for i, out in enumerate(paths):
        x, y = (i % cols) * tile_w, (i // cols) * tile_h
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", png_path,
             "-vf", "crop=%d:%d:%d:%d" % (tile_w, tile_h, x, y),
             "-frames:v", "1", out])
    return paths


def frame_hashes(paths: list[str]) -> list[str]:
    return [hashlib.sha1(open(p, "rb").read()).hexdigest() for p in paths]


# --------------------------------------------------------------------------
# Encoding
# --------------------------------------------------------------------------

def run(cmd: list[str], verbose: bool = False) -> None:
    if verbose:
        print("  $", " ".join(cmd))
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit("command failed: %s\n%s" % (" ".join(cmd), proc.stderr[-3000:]))


def encode_mp4(frame_dir: str, out_path: str, scale: bool, verbose: bool) -> None:
    vf = ["-vf", "scale=%d:%d:flags=lanczos" % (OUT_W, OUT_H)] if scale else []
    run(["ffmpeg", "-y", "-loglevel", "error",
         "-fflags", "+bitexact",
         "-framerate", str(FPS), "-start_number", "0",
         "-i", os.path.join(frame_dir, "frame%03d.png")]
        + vf +
        ["-c:v", "libx264", "-crf", "20", "-preset", "slow",
         "-pix_fmt", "yuv420p", "-an",
         "-flags:v", "+bitexact", "-map_metadata", "-1",
         "-movflags", "+faststart",
         out_path], verbose)


def encode_gif(frame_dir: str, out_path: str, tmpdir: str, verbose: bool) -> None:
    palette = os.path.join(tmpdir, "palette.png")
    src = os.path.join(frame_dir, "frame%03d.png")
    scale = "scale=%d:%d:flags=lanczos" % (GIF_W, GIF_H)
    run(["ffmpeg", "-y", "-loglevel", "error",
         "-framerate", str(FPS), "-start_number", "0", "-i", src,
         "-vf", "%s,palettegen=stats_mode=diff" % scale, palette], verbose)
    run(["ffmpeg", "-y", "-loglevel", "error",
         "-framerate", str(FPS), "-start_number", "0", "-i", src,
         "-i", palette,
         "-lavfi", "%s[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle" % scale,
         "-loop", "0", out_path], verbose)


def encode_poster(frame_dir: str, out_path: str, verbose: bool) -> None:
    run(["ffmpeg", "-y", "-loglevel", "error",
         "-i", os.path.join(frame_dir, "frame000.png"),
         "-vf", "scale=%d:%d:flags=lanczos" % (OUT_W, OUT_H),
         "-frames:v", "1", "-q:v", "3", out_path], verbose)


# --------------------------------------------------------------------------
# Frame production
# --------------------------------------------------------------------------

def frames_grid(svg_source: str, times: list[float], workdir: str,
                tile_w: int, tile_h: int, verbose: bool) -> tuple[list[str], str]:
    html = build_page(svg_source, times, COLS, tile_w, tile_h)
    html_path = os.path.join(workdir, "grid.html")
    with open(html_path, "w", encoding="utf-8") as fh:
        fh.write(html)
    sheet = os.path.join(workdir, "grid.png")
    chrome_screenshot(html_path, sheet, COLS * tile_w, ROWS * tile_h, verbose)
    frame_dir = os.path.join(workdir, "frames")
    paths = slice_grid(sheet, frame_dir, len(times), COLS, tile_w, tile_h)
    return paths, frame_dir


def frames_perframe(svg_source: str, times: list[float], workdir: str,
                    verbose: bool) -> tuple[list[str], str]:
    """Fallback: one full-size Chrome launch per frame. Slow but bulletproof."""
    frame_dir = os.path.join(workdir, "frames_pf")
    os.makedirs(frame_dir, exist_ok=True)
    paths = []
    for i, t in enumerate(times):
        html = build_page(svg_source, [t], 1, OUT_W, OUT_H)
        html_path = os.path.join(workdir, "single%03d.html" % i)
        with open(html_path, "w", encoding="utf-8") as fh:
            fh.write(html)
        out = os.path.join(frame_dir, "frame%03d.png" % i)
        chrome_screenshot(html_path, out, OUT_W, OUT_H, verbose and i == 0)
        paths.append(out)
        if verbose:
            print("  frame %02d/%d" % (i + 1, len(times)), end="\r", flush=True)
    if verbose:
        print()
    return paths, frame_dir


# --------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------

ANIM_RE = re.compile(r"<(animate|animateMotion|animateTransform|set)\b|@keyframes|animation\s*:",
                     re.I)


def has_animation(svg: str) -> bool:
    return bool(ANIM_RE.search(svg))


def render(svg_path: str, outdir: str, mode: str = "auto", keep_temp: bool = False,
           poster: bool = True, tile_scale: str = "half", verbose: bool = False) -> dict:
    svg_path = os.path.abspath(svg_path)
    slug = os.path.splitext(os.path.basename(svg_path))[0]
    svg_source = open(svg_path, encoding="utf-8").read()
    os.makedirs(outdir, exist_ok=True)

    if not has_animation(svg_source):
        raise SystemExit("no animation found in %s (<animate*>/<set>/CSS @keyframes) - "
                         "this is a static schematic, not a motion file" % os.path.basename(svg_path))

    tile_w, tile_h = (TILE_W, TILE_H) if tile_scale == "half" else (OUT_W, OUT_H)
    step = DURATION / FRAMES
    times = [i * step for i in range(FRAMES)]

    workdir = tempfile.mkdtemp(prefix="render_motion_%s_" % slug)
    try:
        used_mode = "grid" if mode in ("auto", "grid") else "perframe"
        if used_mode == "grid":
            paths, frame_dir = frames_grid(svg_source, times, workdir,
                                           tile_w, tile_h, verbose)
            uniq = len(set(frame_hashes(paths)))
            if uniq < 2:
                if mode == "grid":
                    raise SystemExit(
                        "grid freeze produced %d unique frames - setCurrentTime() did not "
                        "take. Re-run with --mode perframe." % uniq)
                print("  !! grid freeze failed (%d unique frames) - "
                      "falling back to per-frame Chrome launches" % uniq)
                used_mode = "perframe"
        if used_mode == "perframe":
            paths, frame_dir = frames_perframe(svg_source, times, workdir, verbose)
            uniq = len(set(frame_hashes(paths)))

        if uniq < 2:
            raise SystemExit("all %d frames are identical - the SVG is not animating "
                             "or the freeze technique is broken" % FRAMES)
        if uniq < FRAMES * 0.5:
            print("  warning: only %d/%d frames are unique - motion may be too subtle "
                  "or the loop is shorter than %gs" % (uniq, FRAMES, DURATION))

        upscale = (used_mode == "grid" and (tile_w, tile_h) != (OUT_W, OUT_H))
        mp4 = os.path.join(outdir, slug + ".mp4")
        gif = os.path.join(outdir, slug + ".gif")
        encode_mp4(frame_dir, mp4, scale=upscale, verbose=verbose)
        encode_gif(frame_dir, gif, workdir, verbose)
        result = {"slug": slug, "mode": used_mode, "tile_scale": tile_scale,
                  "unique_frames": uniq, "mp4": mp4, "gif": gif}
        if poster:
            jpg = os.path.join(outdir, slug + "-poster.jpg")
            encode_poster(frame_dir, jpg, verbose)
            result["poster"] = jpg
        if keep_temp:
            result["workdir"] = workdir
        return result
    finally:
        if keep_temp:
            print("  temp kept: %s" % workdir)
        else:
            shutil.rmtree(workdir, ignore_errors=True)


TEST_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630">
  <defs>
    <path id="t-track" d="M 80 500 C 300 120, 900 120, 1120 500" fill="none"/>
  </defs>
  <rect width="1200" height="630" fill="#020618"/>
  <use href="#t-track" stroke="#f8fafc" stroke-width="2" opacity="0.5"/>
  <circle cx="80" cy="500" r="6" fill="#f8fafc" opacity="0.6"/>
  <circle cx="1120" cy="500" r="6" fill="#f8fafc" opacity="0.6"/>
  <circle r="18" fill="#bbf451">
    <animateMotion dur="6s" repeatCount="indefinite" rotate="auto">
      <mpath href="#t-track"/>
    </animateMotion>
  </circle>
  <circle cx="600" cy="560" r="26" fill="none" stroke="#bbf451" stroke-width="3">
    <animate attributeName="r" values="26;34;26" dur="2s" repeatCount="indefinite"/>
  </circle>
</svg>
"""


def selftest(outdir: str, mode: str, tile_scale: str, verbose: bool) -> int:
    tmp = tempfile.mkdtemp(prefix="render_motion_selftest_")
    svg = os.path.join(tmp, "selftest-dot.svg")
    with open(svg, "w", encoding="utf-8") as fh:
        fh.write(TEST_SVG)
    print("selftest SVG: %s" % svg)
    res = render(svg, outdir, mode=mode, poster=False, tile_scale=tile_scale,
                 verbose=verbose)
    print(json.dumps(res, indent=2))
    print("inspect: %s" % res["mp4"])
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        description="Render animated SVGs (6s SMIL loop) to deterministic MP4 + GIF.")
    ap.add_argument("svg", nargs="*", help="animated SVG file(s)")
    ap.add_argument("-o", "--outdir", default=DEFAULT_OUTDIR,
                    help="output directory (default: articles/media)")
    ap.add_argument("--mode", choices=["auto", "grid", "perframe"], default="auto",
                    help="auto (grid, fall back to per-frame), grid, or perframe")
    ap.add_argument("--tile-scale", choices=["half", "full"], default="half",
                    help="grid tile size: half = 600x315 tiles upscaled on encode "
                         "(default, 5400x2520 screenshot); full = native 1200x630 tiles, "
                         "crisper hairlines, 10800x5040 screenshot")
    ap.add_argument("--no-poster", dest="poster", action="store_false",
                    help="skip the <slug>-poster.jpg still")
    ap.add_argument("--keep-temp", action="store_true", help="keep the working directory")
    ap.add_argument("--selftest", action="store_true",
                    help="render a built-in travelling-dot SVG and report frame uniqueness")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args(argv)

    if not shutil.which("ffmpeg"):
        raise SystemExit("ffmpeg not found on PATH")

    if args.selftest:
        return selftest(args.outdir, args.mode, args.tile_scale, args.verbose)

    targets: list[str] = []
    for pattern in args.svg:
        hits = sorted(glob.glob(pattern)) if any(c in pattern for c in "*?[") else [pattern]
        targets.extend(hits)
    if not targets:
        ap.error("no input SVG given (or --selftest)")

    failures = 0
    for path in targets:
        if not os.path.exists(path):
            print("missing: %s" % path)
            failures += 1
            continue
        print("rendering %s" % os.path.basename(path))
        try:
            res = render(path, args.outdir, mode=args.mode, keep_temp=args.keep_temp,
                         poster=args.poster, tile_scale=args.tile_scale,
                         verbose=args.verbose)
        except SystemExit as exc:
            print("  FAILED: %s" % exc)
            failures += 1
            continue
        print("  mode=%s tile=%s unique_frames=%d/%d"
              % (res["mode"], res["tile_scale"], res["unique_frames"], FRAMES))
        for key in ("mp4", "gif", "poster"):
            if key in res:
                print("  %s -> %s (%.1f KB)"
                      % (key, res[key], os.path.getsize(res[key]) / 1024))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
