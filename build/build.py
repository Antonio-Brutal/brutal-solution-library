#!/usr/bin/env python3
"""Build the publishable export: brand-styled HTML for every article, an index, and the asset tree.

Usage:  python3 build/build.py            # builds into dist/
"""
import os, re, shutil, html as htmlmod, importlib.util
_spec = importlib.util.spec_from_file_location("brand", os.path.join(os.path.dirname(os.path.abspath(__file__)), "brand.py"))
brand = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(brand)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ART = os.path.join(ROOT, "articles")
DIST = os.path.join(ROOT, "dist")

# ---- ordered catalogue -------------------------------------------------------
ORDER = [
    ("invoice-matching-engine", "AI Invoice Ingestion & Three-Way Matching", "Mid-market freight forwarder", "Finance operations"),
    ("support-triage-engine", "Support Triage & Draft-Reply Engine", "Subscription e-commerce brand", "Customer operations"),
    ("rfp-response-engine", "RFP & Tender Response Engine", "Engineering services contractor", "Revenue"),
    ("contract-review-copilot", "Contract Review Copilot", "Commercial real-estate group", "Legal & compliance"),
    ("claims-document-intelligence", "Claims Document Intelligence", "Regional P&C insurer", "Finance operations"),
    ("catalog-enrichment-engine", "Product Catalog Enrichment Engine", "Long-tail marketplace", "Revenue"),
    ("meeting-to-crm-pipeline", "Meeting-to-CRM Pipeline", "Professional services firm", "Revenue"),
    ("conversation-qa-full-coverage", "100% Conversation QA", "Outsourced contact centre", "Customer operations"),
    ("shared-inbox-automation", "Shared-Inbox Automation", "Property management company", "Customer operations"),
    ("financial-close-automation", "Financial Close Copilot", "Multi-entity hospitality group", "Finance operations"),
    ("field-service-reporting", "Voice-to-Report Field Documentation", "Industrial maintenance provider", "Field operations"),
    ("analytics-agent-slack", "Governed Analytics Agent in Slack", "B2B scale-up", "Data"),
    ("sop-knowledge-assistant", "SOP Knowledge Assistant", "Multi-location franchise network", "Knowledge"),
    ("candidate-screening-engine", "High-Volume Candidate Screening", "Staffing & recruiting agency", "Revenue"),
    ("regulatory-horizon-scanning", "Regulatory Horizon Scanning", "Payments fintech", "Legal & compliance"),
    ("demand-forecasting-explainability", "Demand Forecasting Buyers Trust", "Specialty retail chain", "Data"),
    ("churn-early-warning", "Churn Early-Warning & Save Orchestration", "Subscription media company", "Revenue"),
    ("localization-engine", "Multilingual Localization Engine", "Consumer app scaling across Europe", "Knowledge"),
    ("incident-response-copilot", "Incident-Response Copilot", "Fintech engineering organisation", "Engineering"),
    ("sop-to-training-generator", "SOP-to-Training Generator", "Franchise network", "Knowledge"),
    ("lead-qualification-agent", "Inbound Lead Qualification Agent", "B2B industrial manufacturer", "Revenue"),
    ("competitive-price-monitoring", "Competitive Price Monitoring", "Consumer electronics retailer", "Data"),
    ("ticket-mining-knowledge-base", "Ticket-Mining Knowledge Base", "Enterprise IT services provider", "Knowledge"),
    ("supplier-onboarding-risk", "Supplier Onboarding & Risk Screening", "Manufacturing procurement team", "Legal & compliance"),
    ("clinical-documentation-assistant", "Clinical Intake & Documentation Assistant", "Physiotherapy clinic chain", "Field operations"),
    ("funder-report-automation", "Funder Report Automation", "International nonprofit", "Knowledge"),
    ("menu-inventory-intelligence", "Menu & Inventory Intelligence", "Multi-site restaurant group", "Data"),
    ("ad-creative-iteration", "Ad Creative Iteration Engine", "DTC consumer brand", "Revenue"),
    ("hr-policy-case-assistant", "HR Policy & Case Assistant", "Mid-size enterprise HR team", "Knowledge"),
    ("portfolio-reporting-automation", "Portfolio Reporting Automation", "Private-equity operating team", "Finance operations"),
]

CSS = brand.ARTICLE_CSS + """
.sitebar{position:sticky;top:0;z-index:10;background:rgba(5,6,8,.92);backdrop-filter:blur(8px);
 border-bottom:1px solid #1d293d;padding:1rem 1.5rem}
.sitebar-in{max-width:72rem;margin:0 auto;display:flex;align-items:center;gap:1rem}
.brandmark{font-weight:900;text-transform:uppercase;letter-spacing:-.02em;color:#fff;
 text-decoration:none;font-size:1rem}
.brandmark span{color:#9de500}
.backlink{margin-left:auto;color:#62748e;text-decoration:none;font-size:.75rem;
 font-weight:700;text-transform:uppercase;letter-spacing:.1em}
.backlink:hover{color:#9de500}
/* index */
.ihero{padding:7rem 1.5rem 3rem}
.ihero-in{max-width:72rem;margin:0 auto}
.ihero h1{font-size:2.25rem;margin:0 0 1rem}
.ihero p{max-width:60ch;color:#90a1b9;margin:0}
.igrid{max-width:72rem;margin:0 auto;padding:2rem 1.5rem 7rem;display:grid;gap:.75rem}
.irow{display:grid;grid-template-columns:2.5rem 1fr 15rem 9rem;gap:1.25rem;align-items:center;
 padding:1.1rem 1.25rem;border:1px solid #1d293d;border-radius:1rem;background:rgba(15,23,43,.4);
 text-decoration:none;color:inherit}
.irow:hover{border-color:rgba(157,229,0,.5);background:rgba(15,23,43,.7)}
.irow .n{color:#62748e;font-family:ui-monospace,Menlo,monospace;font-size:.8rem}
.irow .t{font-weight:700;color:#fff;font-size:1rem}
.irow .c{color:#90a1b9;font-size:.8rem}
.irow .g{color:#9de500;font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em}
@media(max-width:820px){.irow{grid-template-columns:2rem 1fr}.irow .c,.irow .g{display:none}
 .ihero h1{font-size:1.75rem}}
"""

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | Brutal.ai</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{og}">
<meta property="og:type" content="article">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&display=swap" rel="stylesheet">
<style>{css}</style></head>
<body>
<nav class="sitebar"><div class="sitebar-in">
 <a class="brandmark" href="../index.html">BRUTAL<span>.AI</span></a>
 <a class="backlink" href="../index.html">All solutions</a>
</div></nav>
<article><div class="container">
<div class="meta"><span>{cat}</span><span>{cust}</span></div>
{inner}
</div></article>
</body></html>"""


def main():
    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    os.makedirs(os.path.join(DIST, "articles"))
    shutil.copytree(os.path.join(ART, "graphics"), os.path.join(DIST, "graphics"))
    shutil.copytree(os.path.join(ART, "media"), os.path.join(DIST, "media"))
    shutil.copytree(os.path.join(ART, "motion"), os.path.join(DIST, "motion"))

    built = []
    for i, (slug, title, cust, cat) in enumerate(ORDER, 1):
        p = os.path.join(ART, slug + ".md")
        if not os.path.exists(p):
            print("  !! missing", slug); continue
        src = open(p, encoding="utf-8").read()
        inner, real_title, desc = brand.render_article(src, slug, asset_prefix="../")
        out = PAGE.format(title=htmlmod.escape(real_title), desc=htmlmod.escape(desc),
                          og="../media/%s-poster.jpg" % slug, css=CSS, inner=inner,
                          cust=htmlmod.escape(cust), cat=htmlmod.escape(cat))
        open(os.path.join(DIST, "articles", slug + ".html"), "w", encoding="utf-8").write(out)
        built.append((i, slug, title, cust, cat))

    rows = "\n".join(
        f'<a class="irow" href="articles/{s}.html"><span class="n">{i:02d}</span>'
        f'<span class="t">{htmlmod.escape(t)}</span>'
        f'<span class="c">{htmlmod.escape(c)}</span>'
        f'<span class="g">{htmlmod.escape(g)}</span></a>'
        for i, s, t, c, g in built)
    idx = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Brutal.ai — Solution Library</title><style>{CSS}</style></head><body>
<nav class="sitebar"><div class="sitebar-in"><a class="brandmark" href="index.html">BRUTAL<span>.AI</span></a></div></nav>
<div class="ihero"><div class="ihero-in"><h1>Solution Library</h1>
<p>{len(built)} engineering write-ups. Each one covers a system we build: the bottleneck it removes,
the architecture, and where the human stays in the loop. Every article ships with a hero schematic and a short demo loop.</p>
</div></div><div class="igrid">{rows}</div></body></html>"""
    open(os.path.join(DIST, "index.html"), "w", encoding="utf-8").write(idx)
    print(f"built {len(built)} articles into dist/")
    return len(built)


if __name__ == "__main__":
    main()
