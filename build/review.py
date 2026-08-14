#!/usr/bin/env python3
"""Single-file review page: all 30 articles rendered exactly as they will appear on the blog,
with graphics and videos inlined. Navigation chrome is the only thing added."""
import base64, os, re, html as H, importlib.util

ROOT = "/Users/antonio.marques/Documents/Claude Projects/Brutal Articles"
ART = os.path.join(ROOT, "articles")
WEB = "/private/tmp/claude-502/-Users-antonio-marques-Documents-Claude-Projects-Brutal-Articles/a4398d1d-3a2d-4ca2-9dac-066edf9a7fbb/scratchpad/web30"
OUT = os.path.join(ROOT, "review-all-30.html")


def _load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, "build", name + ".py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


brand = _load("brand")
ORDER = _load("build").ORDER


def inline_assets(inner, slug):
    """Swap asset paths for data URIs so the page stands alone."""
    svg = open(os.path.join(ART, "graphics", slug + ".svg"), encoding="utf-8").read()
    svg = re.sub(r"<\?xml[^>]*\?>", "", svg).strip()
    b64svg = base64.b64encode(svg.encode()).decode()
    inner = inner.replace(f"../graphics/{slug}.svg", "data:image/svg+xml;base64," + b64svg)
    inner = inner.replace(f"graphics/{slug}.svg", "data:image/svg+xml;base64," + b64svg)

    poster = base64.b64encode(open(os.path.join(ART, "media", slug + "-poster.jpg"), "rb").read()).decode()
    for pre in ("../media/", "media/"):
        inner = inner.replace(f"{pre}{slug}-poster.jpg", "data:image/jpeg;base64," + poster)

    motion = open(os.path.join(ART, "motion", slug + ".svg"), encoding="utf-8").read()
    motion = re.sub(r"<\?xml[^>]*\?>", "", motion).strip()
    b64m = base64.b64encode(motion.encode()).decode()
    for pre in ("../motion/", "motion/"):
        inner = inner.replace(f"{pre}{slug}.svg", "data:image/svg+xml;base64," + b64m)
    return inner


def build():
    cards, toc = [], []
    for i, (slug, title, cust, cat) in enumerate(ORDER, 1):
        p = os.path.join(ART, slug + ".md")
        if not os.path.exists(p):
            continue
        inner, real_title, _ = brand.render_article(open(p, encoding="utf-8").read(), slug)
        inner = inline_assets(inner, slug)
        toc.append(f'<a href="#{slug}"><span class="tn">{i:02d}</span>'
                   f'<span class="tt">{H.escape(real_title)}</span>'
                   f'<span class="tc">{H.escape(cat)}</span></a>')
        cards.append(f'<article id="{slug}"><div class="container">'
                     f'<div class="meta"><span>{H.escape(cat)}</span><span>{H.escape(cust)}</span></div>'
                     f'{inner}<a class="totop" href="#top">Back to index</a>'
                     f'</div></article><hr class="sep">')

    chrome = """
.rhero{padding:5rem 1.5rem 2rem;border-bottom:1px solid #1d293d}
.rhero-in{max-width:72rem;margin:0 auto}
.rhero h1{font-size:2.25rem;margin:0 0 1rem}
.rhero p{color:#90a1b9;max-width:66ch;margin:0;font-size:1rem}
.rhero b{color:#9de500;font-weight:700}
.toc{max-width:72rem;margin:0 auto;padding:1.75rem 1.5rem 2.5rem;display:grid;
 grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:.35rem}
.toc a{display:flex;gap:.7rem;align-items:baseline;text-decoration:none;padding:.5rem .7rem;
 border-radius:.6rem;border:1px solid transparent}
.toc a:hover{border-color:#1d293d;background:rgba(15,23,43,.5)}
.tn{color:#62748e;font-family:ui-monospace,Menlo,monospace;font-size:.7rem}
.tt{color:#cad5e2;font-size:.85rem}
.toc a:hover .tt{color:#fff}
.tc{margin-left:auto;color:#9de500;font-size:.6rem;font-weight:700;text-transform:uppercase;
 letter-spacing:.1em;opacity:.75}
article{padding:4rem 1.5rem 2rem}
.sep{border:0;border-top:1px solid #1d293d;margin:0}
.totop{display:inline-block;margin-top:3.5rem;color:#62748e;text-decoration:none;font-size:.7rem;
 font-weight:700;text-transform:uppercase;letter-spacing:.1em}
.totop:hover{color:#9de500}
@media(max-width:820px){.toc{grid-template-columns:1fr}.rhero h1{font-size:1.75rem}}
"""
    page = f"""<title>Brutal.ai — 30 Articles for Review</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&display=swap" rel="stylesheet">
<style>{brand.ARTICLE_CSS}{chrome}</style>
<a id="top"></a>
<div class="rhero"><div class="rhero-in"><h1>Solution Library — Review</h1>
<p><b>30</b> articles, each rendered exactly as it will appear on the blog, with its schematic and
demo loop in place. All publication-ready: no production notes, no invented metrics, no named clients.
Jump to any piece below.</p></div></div>
<nav class="toc">{''.join(toc)}</nav>
{''.join(cards)}"""
    open(OUT, "w", encoding="utf-8").write(page)
    print(f"built {len(cards)} articles -> {OUT} ({os.path.getsize(OUT)/1024/1024:.1f} MB)")


if __name__ == "__main__":
    build()
