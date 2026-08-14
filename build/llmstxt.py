#!/usr/bin/env python3
"""Generate llms.txt for the solution library.

llms.txt is a proposed convention giving AI crawlers a clean, structured map of a site's
content, in place of parsing rendered HTML. Cheap to produce, and the GEO skill treats its
absence as a gap.
"""
import os, re, importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ART = os.path.join(ROOT, "articles")

spec = importlib.util.spec_from_file_location("b", os.path.join(ROOT, "build", "build.py"))
b = importlib.util.module_from_spec(spec); spec.loader.exec_module(b)


def standfirst(slug):
    s = open(os.path.join(ART, slug + ".md"), encoding="utf-8").read()
    m = re.search(r"^>\s?(.+)$", s, re.M)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""


def main():
    by_cat = {}
    for slug, title, cust, cat in b.ORDER:
        if os.path.exists(os.path.join(ART, slug + ".md")):
            by_cat.setdefault(cat, []).append((slug, title, cust))

    out = ["# Brutal.ai Solution Library", "",
           "> Engineering write-ups on AI systems and internal-improvement work built for "
           "client companies. Each covers one system: the bottleneck it removes, its architecture, "
           "and where a human stays in the decision loop. Customers are described by type rather "
           "than named.", "",
           "Figures in these articles are stated as magnitudes rather than measured results, "
           "because they describe representative engagements. They contain no percentage claims, "
           "currency amounts or ROI multiples.", ""]

    for cat in sorted(by_cat):
        out.append(f"## {cat}")
        for slug, title, cust in by_cat[cat]:
            out.append(f"- [{title}](https://brutal.ai/en/blog/{slug}): {standfirst(slug)} "
                       f"Customer type: {cust}.")
        out.append("")

    out += ["## About", "",
            "- [Brutal.ai](https://brutal.ai): AI engineering consultancy. We build document "
            "intelligence, governed analytics, agent systems and internal tooling, and we keep "
            "humans on the decisions that matter.", ""]

    path = os.path.join(ROOT, "dist", "llms.txt")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write("\n".join(out))
    print(f"llms.txt -> {path} ({len(by_cat)} categories, "
          f"{sum(len(v) for v in by_cat.values())} articles)")


if __name__ == "__main__":
    main()
