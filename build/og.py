#!/usr/bin/env python3
"""Branded OG share cards: left panel with kicker + title, schematic filling the right.
Rendered deterministically with headless Chrome at 1200x630."""
import os, re, subprocess, tempfile, importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ART = os.path.join(ROOT, "articles")
OUT = os.path.join(ROOT, "dist", "og")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

spec = importlib.util.spec_from_file_location("b", os.path.join(ROOT, "build", "build.py"))
b = importlib.util.module_from_spec(spec); spec.loader.exec_module(b)

TPL = """<!doctype html><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
<style>
*{margin:0;box-sizing:border-box}
body{width:1200px;height:630px;background:#050608;overflow:hidden;display:flex;
 font-family:'Space Grotesk','Helvetica Neue',Arial,sans-serif}
.panel{width:470px;flex:0 0 470px;padding:52px 44px;display:flex;flex-direction:column;
 justify-content:space-between;border-right:1px solid #1d293d;position:relative;z-index:2;
 background:#050608}
.kick{font-family:ui-monospace,Menlo,monospace;font-size:15px;font-weight:700;
 letter-spacing:.18em;color:#62748e}
.kick b{color:#9de500}
.title{font-size:%TS%px;line-height:1.12;font-weight:700;text-transform:uppercase;
 letter-spacing:-.02em;color:#f8fafc}
.meta{font-family:ui-monospace,Menlo,monospace;font-size:13px;letter-spacing:.14em;
 color:#62748e;text-transform:uppercase}
.meta b{color:#9de500;font-weight:700}
.art{flex:1;position:relative;background:#050608}
.art svg{position:absolute;height:630px;width:auto;left:50%;top:0;transform:translateX(-50%)}
.scrim{position:absolute;inset:0;background:linear-gradient(90deg,#050608 0,rgba(5,6,8,0) 18%);z-index:1}
</style>
<body>
<div class="panel">
 <div class="kick">BRUTAL<b>.AI</b> // SOLUTION LIBRARY</div>
 <div class="title">%TITLE%</div>
 <div class="meta"><b>%CAT%</b><br>%CUST%</div>
</div>
<div class="art"><div class="scrim"></div>%SVG%</div>
</body>"""


def main():
    os.makedirs(OUT, exist_ok=True)
    for slug, _, cust, cat in b.ORDER:
        mdp = os.path.join(ART, slug + ".md")
        if not os.path.exists(mdp):
            continue
        title = open(mdp, encoding="utf-8").readline().strip().lstrip("# ")
        svg = open(os.path.join(ART, "graphics", slug + ".svg"), encoding="utf-8").read()
        svg = re.sub(r"<\?xml[^>]*\?>", "", svg)
        ts = 44 if len(title) < 55 else (38 if len(title) < 75 else 33)
        html = (TPL.replace("%TITLE%", title).replace("%CAT%", cat.upper())
                   .replace("%CUST%", cust).replace("%SVG%", svg).replace("%TS%", str(ts)))
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as t:
            t.write(html); page = t.name
        png = os.path.join(OUT, slug + ".png")
        subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                        "--window-size=1200,630", "--virtual-time-budget=4000",
                        f"--screenshot={png}", f"file://{page}"],
                       check=True, capture_output=True)
        os.unlink(page)
        print("og:", slug)


if __name__ == "__main__":
    main()
