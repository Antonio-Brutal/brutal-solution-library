#!/usr/bin/env python3
"""Build the publishable export: brand-styled HTML for every article, an index, and the asset tree.

Usage:  python3 build/build.py            # builds into dist/
"""
import os, re, shutil, html as htmlmod
import markdown

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

CSS = """
:root{--bg:#050608;--panel:#0a0d12;--ink:#f8fafc;--muted:#90a1b9;--dim:#62748e;--lime:#bbf451;--line:#1e293b}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
     font-family:'Space Grotesk','Helvetica Neue',Arial,sans-serif;line-height:1.7;
     -webkit-font-smoothing:antialiased}
.wrap{max-width:760px;margin:0 auto;padding:64px 24px 96px}
.back{display:inline-block;color:var(--muted);text-decoration:none;font-size:13px;margin-bottom:40px}
.back:hover{color:var(--lime)}
h1{font-size:40px;line-height:1.15;letter-spacing:-.025em;margin:0 0 20px;font-weight:700}
blockquote{margin:0 0 36px;padding:0;border:0;color:var(--muted);font-size:19px;line-height:1.6}
h2{font-size:25px;letter-spacing:-.015em;margin:52px 0 16px;font-weight:600}
h3{font-size:18px;margin:36px 0 12px;font-weight:600;color:var(--lime)}
p{margin:0 0 20px;font-size:17px}
em{color:var(--ink);font-style:italic}
img,video{width:100%;display:block;border-radius:8px;margin:32px 0;background:#000;border:1px solid var(--line)}
video+p em,img+p em{color:var(--dim);font-size:14px}
a{color:var(--lime)}
ul,ol{margin:0 0 20px;padding-left:22px}li{margin-bottom:8px;font-size:17px}
footer{margin-top:72px;padding-top:28px;border-top:1px solid var(--line);color:var(--dim);font-size:13px}
/* index */
.hero{border-bottom:1px solid var(--line);padding:72px 24px 40px}
.hero-in{max-width:1100px;margin:0 auto}
.hero h1{font-size:44px;margin-bottom:14px}
.hero p{color:var(--muted);max-width:68ch}
.grid{max-width:1100px;margin:0 auto;padding:40px 24px 96px;display:grid;gap:14px}
.row{display:grid;grid-template-columns:44px 1fr 200px 150px;gap:18px;align-items:center;
     padding:18px 20px;border:1px solid var(--line);border-radius:10px;background:var(--panel);
     text-decoration:none;color:inherit}
.row:hover{border-color:var(--lime)}
.num{color:var(--dim);font-family:ui-monospace,Menlo,monospace;font-size:13px}
.ttl{font-weight:600;font-size:16px}
.meta{color:var(--muted);font-size:13px}
.tag{color:var(--lime);font-size:12px;letter-spacing:.06em}
@media(max-width:760px){.row{grid-template-columns:36px 1fr}.meta,.tag{display:none}}
"""

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — Brutal.ai</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{og}">
<meta property="og:type" content="article">
<style>{css}</style></head>
<body><div class="wrap">
<a class="back" href="../index.html">&larr; All solutions</a>
{body}
<footer>Brutal.ai — {cust} &middot; {cat}</footer>
</div></body></html>"""


def convert(slug):
    src = open(os.path.join(ART, slug + ".md"), encoding="utf-8").read()
    # assets sit one level up from articles/<slug>.html inside dist
    src = src.replace("](graphics/", "](../graphics/")
    src = src.replace('src="media/', 'src="../media/').replace('poster="media/', 'poster="../media/')
    md = markdown.Markdown(extensions=["extra", "sane_lists"])
    body = md.convert(src)
    # subtitle: first blockquote paragraph
    m = re.search(r"<blockquote>\s*<p>(.*?)</p>", body, re.S)
    desc = re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else ""
    return body, desc


def main():
    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    os.makedirs(os.path.join(DIST, "articles"))
    shutil.copytree(os.path.join(ART, "graphics"), os.path.join(DIST, "graphics"))
    shutil.copytree(os.path.join(ART, "media"), os.path.join(DIST, "media"))

    built = []
    for i, (slug, title, cust, cat) in enumerate(ORDER, 1):
        p = os.path.join(ART, slug + ".md")
        if not os.path.exists(p):
            print("  !! missing", slug); continue
        body, desc = convert(slug)
        out = PAGE.format(title=htmlmod.escape(title), desc=htmlmod.escape(desc),
                          og="media/%s-poster.jpg" % slug, css=CSS, body=body,
                          cust=htmlmod.escape(cust), cat=htmlmod.escape(cat))
        open(os.path.join(DIST, "articles", slug + ".html"), "w", encoding="utf-8").write(out)
        built.append((i, slug, title, cust, cat))

    rows = "\n".join(
        f'<a class="row" href="articles/{s}.html"><span class="num">{i:02d}</span>'
        f'<span class="ttl">{htmlmod.escape(t)}</span>'
        f'<span class="meta">{htmlmod.escape(c)}</span>'
        f'<span class="tag">{htmlmod.escape(g)}</span></a>'
        for i, s, t, c, g in built)
    idx = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Brutal.ai — Solution Library</title><style>{CSS}</style></head><body>
<div class="hero"><div class="hero-in"><h1>Brutal.ai — Solution Library</h1>
<p>{len(built)} engineering write-ups. Each one covers a system we build: the bottleneck it removes,
the architecture, and where the human stays in the loop. Every article ships with a hero schematic and a short demo loop.</p>
</div></div><div class="grid">{rows}</div></body></html>"""
    open(os.path.join(DIST, "index.html"), "w", encoding="utf-8").write(idx)
    print(f"built {len(built)} articles into dist/")
    return len(built)


if __name__ == "__main__":
    main()
