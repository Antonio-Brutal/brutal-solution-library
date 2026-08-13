#!/usr/bin/env python3
"""Build the single-file review page: all 30 articles, full text, inline graphic + video."""
import base64, json, os, re, html as H
import markdown

ROOT = "/Users/antonio.marques/Documents/Claude Projects/Brutal Articles"
ART = os.path.join(ROOT, "articles")
WEB = "/private/tmp/claude-502/-Users-antonio-marques-Documents-Claude-Projects-Brutal-Articles/a4398d1d-3a2d-4ca2-9dac-066edf9a7fbb/scratchpad/web30"
OUT = os.path.join(ROOT, "review-all-30.html")

import importlib.util
spec = importlib.util.spec_from_file_location("b", os.path.join(ROOT, "build", "build.py"))
b = importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
ORDER = b.ORDER


def inline_svg(slug):
    s = open(os.path.join(ART, "graphics", slug + ".svg"), encoding="utf-8").read()
    s = re.sub(r"<\?xml[^>]*\?>", "", s).strip()
    for i in set(re.findall(r'id="([^"]+)"', s)):
        if not i.startswith(slug):
            s = s.replace(f'id="{i}"', f'id="{slug}-{i}"')
            s = s.replace(f"url(#{i})", f"url(#{slug}-{i})")
            s = s.replace(f'href="#{i}"', f'href="#{slug}-{i}"')
    return s


def build():
    md = markdown.Markdown(extensions=["extra", "sane_lists"])
    cards, toc = [], []
    for i, (slug, title, cust, cat) in enumerate(ORDER, 1):
        p = os.path.join(ART, slug + ".md")
        if not os.path.exists(p):
            continue
        src = open(p, encoding="utf-8").read()
        # pull the graphic + video out of the flow; we render them ourselves
        src = re.sub(r"!\[[^\]]*\]\(graphics/[^)]+\)", "", src)
        src = re.sub(r"<video[^>]*></video>", "", src)
        md.reset()
        body = md.convert(src)
        vid = base64.b64encode(open(os.path.join(WEB, slug + ".mp4"), "rb").read()).decode()
        toc.append(f'<a href="#{slug}"><span class="tn">{i:02d}</span>{H.escape(title)}'
                   f'<span class="tc">{H.escape(cat)}</span></a>')
        cards.append(f"""
<section id="{slug}">
  <div class="shead"><span class="num">{i:02d}</span>
    <div><h2>{H.escape(title)}</h2><p class="cust">{H.escape(cust)} &middot; {H.escape(cat)}</p></div>
    <a class="top" href="#top">top</a></div>
  <div class="assets">
    <figure><figcaption>hero graphic</figcaption><div class="svgwrap">{inline_svg(slug)}</div></figure>
    <figure><figcaption>video</figcaption>
      <video controls loop muted playsinline preload="none" src="data:video/mp4;base64,{vid}"></video></figure>
  </div>
  <div class="prose">{body}</div>
</section>""")

    css = """
:root{--bg:#050608;--panel:#0a0d12;--ink:#f8fafc;--muted:#90a1b9;--dim:#62748e;--lime:#bbf451;--line:#1e293b}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:'Space Grotesk','Helvetica Neue',Arial,sans-serif;line-height:1.7}
.hero{padding:64px 32px 36px;border-bottom:1px solid var(--line)}
.hin{max-width:1200px;margin:0 auto}
h1{font-size:38px;margin:0 0 12px;letter-spacing:-.025em}
.hin>p{color:var(--muted);max-width:72ch;margin:0}
.n{color:var(--lime)}
.toc{max-width:1200px;margin:0 auto;padding:28px 32px 8px;display:grid;
     grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:6px}
.toc a{display:flex;gap:10px;align-items:baseline;color:var(--muted);text-decoration:none;
       font-size:13px;padding:7px 10px;border-radius:6px;border:1px solid transparent}
.toc a:hover{color:var(--ink);border-color:var(--line);background:var(--panel)}
.tn{color:var(--dim);font-family:ui-monospace,Menlo,monospace;font-size:11px}
.tc{margin-left:auto;color:var(--lime);font-size:10px;letter-spacing:.06em;opacity:.8}
main{max-width:1200px;margin:0 auto;padding:20px 32px 100px}
section{border-top:1px solid var(--line);padding:52px 0 8px;scroll-margin-top:16px}
.shead{display:flex;gap:16px;align-items:flex-start;margin-bottom:26px}
.num{color:var(--dim);font-family:ui-monospace,Menlo,monospace;font-size:13px;padding-top:6px}
.shead h2{margin:0;font-size:26px;letter-spacing:-.02em}
.cust{margin:4px 0 0;color:var(--muted);font-size:13px}
.top{margin-left:auto;color:var(--dim);font-size:12px;text-decoration:none}
.top:hover{color:var(--lime)}
.assets{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-bottom:34px}
figure{margin:0}
figcaption{color:var(--dim);font-size:10px;letter-spacing:.16em;margin-bottom:8px}
.svgwrap svg,video{width:100%;height:auto;display:block;border-radius:8px;border:1px solid var(--line);background:#000}
.prose{max-width:74ch}
.prose h1{font-size:27px;margin:0 0 14px;letter-spacing:-.02em}
.prose blockquote{margin:0 0 26px;padding:0;border:0;color:var(--muted);font-size:17px}
.prose h2{font-size:20px;margin:36px 0 12px}
.prose h3{font-size:16px;margin:26px 0 10px;color:var(--lime)}
.prose p{font-size:16px;margin:0 0 16px}
.prose em{color:var(--muted)}
@media(max-width:900px){.assets{grid-template-columns:1fr}.toc{grid-template-columns:1fr}}
"""
    page = f"""<title>Brutal.ai — 30 Articles for Review</title>
<style>{css}</style>
<a id="top"></a>
<div class="hero"><div class="hin"><h1>Brutal.ai — 30 articles</h1>
<p>Every article in full, each with its hero schematic and demo loop. <span class="n">{len(cards)}</span> pieces,
all publication-ready: no production notes, no invented metrics, no named clients.
Press play on any video. Jump to any piece below.</p></div></div>
<nav class="toc">{''.join(toc)}</nav>
<main>{''.join(cards)}</main>"""
    open(OUT, "w", encoding="utf-8").write(page)
    print(f"built {len(cards)} articles -> {OUT} ({os.path.getsize(OUT)/1024/1024:.1f} MB)")


if __name__ == "__main__":
    build()
