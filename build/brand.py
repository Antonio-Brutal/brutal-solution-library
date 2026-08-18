#!/usr/bin/env python3
"""Brutal.ai article rendering — mirrors the live blog's markup and typography.

Extracted from https://brutal.ai/en/blog/ai-content-engine. Every rule below corresponds
to a Tailwind class on the live page; the class string is quoted beside it.
"""
import re
import markdown

# exact tokens from brutal.ai production CSS
BG = "#050608"
LIME_400 = "#9de500"   # h1, h3
LIME_300 = "#bbf451"
SLATE_300 = "#cad5e2"  # body copy
SLATE_400 = "#90a1b9"  # subtitle
SLATE_500 = "#62748e"  # meta, captions
SLATE_800 = "#1d293d"  # media borders
SLATE_900 = "#0f172b"  # media bg, CTA panel

ARTICLE_CSS = f"""
:root{{--bg:{BG};--lime:{LIME_400};--lime3:{LIME_300};--s300:{SLATE_300};--s400:{SLATE_400};
--s500:{SLATE_500};--s800:{SLATE_800};--s900:{SLATE_900}}}
*{{box-sizing:border-box}}
html{{-webkit-text-size-adjust:100%}}
body{{margin:0;background:var(--bg);color:var(--s300);
 font-family:'Space Grotesk',ui-sans-serif,system-ui,-apple-system,'Helvetica Neue',Arial,sans-serif;
 -webkit-font-smoothing:antialiased}}
/* article: "px-6 pt-32 pb-24" + "container mx-auto max-w-3xl" */
article{{padding:8rem 1.5rem 6rem}}
.container{{max-width:48rem;margin:0 auto}}
/* h1: "mt-8 text-3xl font-black uppercase leading-tight tracking-tight text-lime-400 md:text-5xl" */
h1{{margin:2rem 0 0;font-size:1.875rem;line-height:1.25;font-weight:900;text-transform:uppercase;
 letter-spacing:-.025em;color:var(--lime)}}
/* subtitle: "mt-6 text-lg text-slate-400 md:text-xl" */
.subtitle{{margin:1.5rem 0 0;font-size:1.125rem;line-height:1.6;color:var(--s400)}}
/* meta: "mt-8 flex ... text-xs font-bold uppercase tracking-widest text-slate-500" */
.meta{{margin:2rem 0 0;display:flex;flex-wrap:wrap;align-items:center;gap:.5rem .75rem;
 font-size:.75rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--s500)}}
.meta span:not(:last-child):after{{content:"";display:inline-block;width:3px;height:3px;
 border-radius:50%;background:var(--s500);margin-left:.75rem;vertical-align:middle}}
/* body: "text-base md:text-lg leading-relaxed text-slate-300 my-5" (first para "mt-10") */
p{{font-size:1rem;line-height:1.75;color:var(--s300);margin:1.25rem 0}}
.prose>p:first-of-type{{margin-top:2.5rem}}
/* h2: "text-2xl md:text-3xl font-bold uppercase tracking-tight text-white mt-16 mb-5" */
h2{{font-size:1.5rem;font-weight:700;text-transform:uppercase;letter-spacing:-.025em;color:#fff;
 margin:4rem 0 1.25rem}}
/* h3: "text-xl md:text-2xl font-bold text-lime-400 mt-12 mb-4" */
h3{{font-size:1.25rem;font-weight:700;color:var(--lime);margin:3rem 0 1rem}}
/* pull quote: "my-12 border-y-2 border-lime-400/30 py-8 text-xl md:text-2xl italic ... text-white" */
blockquote{{margin:3rem 0;padding:2rem 0;border-top:2px solid rgba(157,229,0,.3);
 border-bottom:2px solid rgba(157,229,0,.3);font-size:1.25rem;font-style:italic;
 line-height:1.375;color:#fff}}
blockquote p{{margin:0;font-size:inherit;color:inherit;line-height:inherit}}
/* figure: "my-14"; media: "w-full rounded-2xl border border-slate-800 bg-slate-900" */
figure{{margin:3.5rem 0}}
figure img,figure video{{width:100%;height:auto;display:block;border-radius:1rem;
 border:1px solid var(--s800);background:var(--s900)}}
/* figcaption: "text-sm text-slate-500 text-center italic mt-3 mb-10" */
figcaption{{font-size:.875rem;color:var(--s500);text-align:center;font-style:italic;
 margin:.75rem 0 2.5rem}}
/* lists: "my-5 ml-5 list-disc space-y-3 marker:text-lime-400" */
ul,ol{{margin:1.25rem 0;padding-left:1.25rem}}
ul{{list-style:disc}}
li{{font-size:1rem;line-height:1.75;color:var(--s300);margin-bottom:.75rem}}
li::marker{{color:var(--lime)}}
strong{{color:#fff;font-weight:700}}
em{{font-style:italic}}
a{{color:var(--lime)}}
::selection{{background:{LIME_400};color:{BG}}}
/* mono section kickers, echoing the schematic labels */
.kicker{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.7rem;font-weight:700;
 letter-spacing:.18em;color:var(--s500);margin:4rem 0 .4rem}}
.kicker+h2{{margin-top:0}}
/* definition callout */
.defcard{{margin:2.75rem 0;border:1px solid rgba(157,229,0,.3);border-left:3px solid var(--lime);
 border-radius:.75rem;background:rgba(15,23,43,.5);padding:1.4rem 1.6rem}}
.deflabel{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.65rem;font-weight:700;
 letter-spacing:.18em;color:var(--lime);margin:0 0 .6rem}}
.defcard p{{margin:0;font-size:1rem;line-height:1.7;color:#e2e8f0}}
.defcard strong{{color:#fff}}
/* FAQ accordions */
.faq details{{border-top:1px solid var(--s800)}}
.faq details:last-of-type{{border-bottom:1px solid var(--s800)}}
.faq summary{{cursor:pointer;list-style:none;display:flex;gap:.9rem;align-items:baseline;
 padding:1.15rem 0;font-weight:600;color:#fff;font-size:1.05rem}}
.faq summary::-webkit-details-marker{{display:none}}
.faq summary::before{{content:"+";color:var(--lime);font-weight:700;flex:0 0 auto;
 font-family:ui-monospace,Menlo,monospace}}
.faq details[open] summary::before{{content:"−"}}
.faq details>p{{margin:0 0 1.3rem;color:var(--s300)}}
/* closing CTA: "mt-20 rounded-2xl border border-lime-400/30 bg-slate-900/60 p-8 md:p-10" */
.cta{{margin-top:5rem;border-radius:1rem;border:1px solid rgba(157,229,0,.3);
 background:rgba(15,23,43,.6);padding:2rem}}
.cta h2{{margin:0;font-size:1.5rem;font-weight:900;text-transform:uppercase;
 letter-spacing:-.025em;color:#fff}}
.cta p{{margin:1rem 0 0}}
.cta .btn{{margin-top:2rem;display:inline-block;background:var(--lime);color:#050608;
 font-weight:700;text-transform:uppercase;letter-spacing:.05em;font-size:.875rem;
 padding:.85rem 1.6rem;border-radius:.6rem;text-decoration:none}}
@media(min-width:768px){{
 h1{{font-size:3rem}} .subtitle{{font-size:1.25rem}}
 p,li{{font-size:1.125rem}} h2{{font-size:1.875rem}} h3{{font-size:1.5rem}}
 blockquote{{font-size:1.5rem}} .cta{{padding:2.5rem}} .cta h2{{font-size:1.875rem}}
}}
"""


def render_article(md_text, slug, asset_prefix=""):
    """Markdown -> the live blog's article markup.

    Returns (inner_html, title, subtitle). The first blockquote is the standfirst
    (rendered as .subtitle, matching the live page) rather than a pull quote.
    """
    src = md_text

    # title
    m = re.match(r"#\s+(.+)", src)
    title = m.group(1).strip() if m else slug
    src = re.sub(r"^#\s+.+\n", "", src, count=1)

    # standfirst
    m = re.search(r"^>\s?(.+?)(?:\n(?!>)|\Z)", src, re.M | re.S)
    subtitle = ""
    if m:
        subtitle = re.sub(r"\s*\n>\s?", " ", m.group(1)).strip()
        src = src.replace(m.group(0), "", 1)

    if asset_prefix:
        src = src.replace("](graphics/", f"]({asset_prefix}graphics/")
        src = src.replace('src="media/', f'src="{asset_prefix}media/')
        src = src.replace('src="motion/', f'src="{asset_prefix}motion/')
        src = src.replace('poster="media/', f'poster="{asset_prefix}media/')

    # closing CTA: last h2 whose text is a question
    cta = None
    heads = list(re.finditer(r"^##\s+(.+)$", src, re.M))
    if heads and heads[-1].group(1).strip().endswith("?"):
        h = heads[-1]
        cta = (h.group(1).strip(), src[h.end():].strip())
        src = src[:h.start()].rstrip()

    md = markdown.Markdown(extensions=["extra", "sane_lists"])
    body = md.convert(src)

    # wrap standalone media in <figure>, promoting the italic line beneath into a caption
    def figurize(html):
        """Wrap each media element in <figure>, absorbing a following italic line as its
        caption. Single pass per media type so an already-wrapped element is never re-wrapped
        (which would push the caption outside the figure). markdown may or may not wrap a raw
        <video> block in a <p>, so both forms are matched."""
        def wrap(m):
            media, cap = m.group("media"), m.group("cap")
            inner = media + (f"<figcaption>{cap}</figcaption>" if cap else "")
            return f"<figure>{inner}</figure>"

        for media_re in (r"(?P<media><video\b.*?</video>)", r"(?P<media><img\b[^>]*>)"):
            pattern = (r"(?:<p>\s*)?" + media_re + r"(?:\s*</p>)?"
                       r"(?:\s*<p><em>(?P<cap>.*?)</em></p>)?")
            html = re.sub(pattern, wrap, html, flags=re.S)
        return html

    body = figurize(body)

    # definition callout: promote the article's owned definition to a styled card.
    STOP = {"The","A","An","It","We","That","This","So","But","And","In","On","Under",
            "One","Every","Nothing","Most","Our","Your","Their","Two","Three","Four","Five",
            "Because","Underneath","Whatever","Whether","Where","When","Once","While"}
    VERBS = (" is ", " are ", " was ", " means ", " sits ", " travels ", " comes ", " runs ")
    def defcard(m):
        term, rest = m.group(1), m.group(2)
        if (term.split()[0] in STOP or len(term) > 48 or len(term.split()) > 5
                or any(v in f" {term} " for v in VERBS)):
            return m.group(0)
        defcard.n += 1
        if defcard.n > 1:
            return m.group(0)
        return (f'<div class="defcard"><div class="deflabel">DEFINITION</div>'
                f'<p><strong>{term}:</strong> {rest}</p></div>')
    defcard.n = 0
    # only the body above the FAQ is eligible; FAQ answers are not definitions
    _split = body.find("<h2>Common questions</h2>")
    if _split == -1:
        body = re.sub(r"<p>([A-Z][A-Za-z0-9' -]{2,48}): (.*?)</p>", defcard, body, flags=re.S)
    else:
        head, tail = body[:_split], body[_split:]
        head = re.sub(r"<p>([A-Z][A-Za-z0-9' -]{2,48}): (.*?)</p>", defcard, head, flags=re.S)
        body = head + tail

    # FAQ accordions: h3/p pairs after the Common questions heading become <details>
    def faqify(m):
        block = m.group(1)
        block = re.sub(r"<h3>(.*?)</h3>\s*<p>(.*?)</p>",
                       r"<details><summary>\1</summary><p>\2</p></details>", block, flags=re.S)
        return f'<h2>Common questions</h2><div class="faq">{block}</div>'
    body = re.sub(r"<h2>Common questions</h2>(.*?)(?=<h2|\Z)", faqify, body, count=1, flags=re.S)

    # mono kickers numbering the sections
    kick = {"n": 0, "total": len(re.findall(r"<h2>", body))}
    def kicker(m):
        kick["n"] += 1
        return f'<div class="kicker">// {kick["n"]:02d}</div>{m.group(0)}'
    body = re.sub(r"<h2>", kicker, body)

    cta_html = ""
    if cta:
        md.reset()
        cta_body = md.convert(cta[1])
        cta_html = (f'<div class="cta"><h2>{cta[0]}</h2>{cta_body}'
                    f'<a class="btn" href="https://brutal.ai/en/contact">Talk to us</a></div>')

    inner = (f'<h1>{title}</h1>'
             f'<p class="subtitle">{subtitle}</p>'
             f'<div class="prose">{body}</div>{cta_html}')
    return inner, title, subtitle


def build_schema(title, subtitle, slug, cust, cat, body_html):
    """Article + FAQPage JSON-LD. AI answer engines lean on structured data when
    deciding what to cite, and the FAQ block is the most quotable part of the page."""
    import json as _json, re as _re

    faqs = []
    m = _re.search(r"<h2[^>]*>Common questions</h2>(.*?)(?=<h2|\Z)", body_html, _re.S | _re.I)
    if m:
        block = m.group(1)
        pairs = _re.findall(r"<summary>(.*?)</summary>\s*<p>(.*?)</p>", block, _re.S) or \
                _re.findall(r"<h3[^>]*>(.*?)</h3>\s*<p>(.*?)</p>", block, _re.S)
        for q, a in pairs:
            faqs.append({
                "@type": "Question",
                "name": _re.sub(r"<[^>]+>", "", q).strip(),
                "acceptedAnswer": {"@type": "Answer",
                                   "text": _re.sub(r"<[^>]+>", "", a).strip()},
            })

    graph = [{
        "@type": "Article",
        "headline": title,
        "description": subtitle,
        "about": {"@type": "Thing", "name": cat},
        "audience": {"@type": "Audience", "audienceType": cust},
        "image": f"https://brutal.ai/images/blog/{slug}.png",
        "author": {"@type": "Organization", "name": "Brutal.ai", "url": "https://brutal.ai"},
        "publisher": {"@type": "Organization", "name": "Brutal.ai", "url": "https://brutal.ai"},
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"https://brutal.ai/en/blog/{slug}"},
        "inLanguage": "en",
    }]
    if faqs:
        graph.append({"@type": "FAQPage", "mainEntity": faqs})

    return ('<script type="application/ld+json">'
            + _json.dumps({"@context": "https://schema.org", "@graph": graph},
                          ensure_ascii=False, separators=(",", ":"))
            + "</script>")
