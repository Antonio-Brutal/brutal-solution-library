#!/usr/bin/env python3
"""Publication preflight. Run against a frozen tree before any export or push.

Exits non-zero if any article is not publication-ready.
"""
import os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ART = os.path.join(ROOT, "articles")

FORBIDDEN = ["TODO", "TBD", "FIXME", "XXX", "placeholder", "PLACEHOLDER",
             "GRAPHIC_EMBED", "VIDEO_EMBED", "exact figure", "replace with",
             "Lorem ipsum", "[ ]"]

# Voice failures. The em dash is banned outright; the rest are the phrases that make
# writing read as machine-produced. See REWRITE-BRIEF.md.
BANNED_VOICE = ["—", "It's not just", "Here's the thing", "The truth is",
                "Let's be honest", "Make no mistake", "In today's", "In an era of",
                "It's important to note", "It's worth noting", "delve", "leverage",
                "seamless", "game-changer", "supercharge", "unlock the power",
                "They have a *", "human role shifts", "revolutioni"]

HEADINGS = {}


def main():
    files = sorted(glob.glob(os.path.join(ART, "*.md")))
    problems = []
    HEADINGS.clear()

    for p in files:
        name = os.path.basename(p)
        s = open(p, encoding="utf-8").read()

        for tok in FORBIDDEN:
            if tok in s:
                problems.append(f"{name}: forbidden token {tok!r}")

        for tok in BANNED_VOICE:
            n = s.count(tok)
            if n:
                label = "em dash" if tok == "—" else repr(tok)
                problems.append(f"{name}: banned phrasing {label} x{n}")

        # citability: the FAQ block is the most quotable part of the page
        if "## Common questions" not in s:
            problems.append(f"{name}: no '## Common questions' FAQ block")
        else:
            faq = s.split("## Common questions", 1)[1]
            faq = faq.split("\n## ", 1)[0]
            qs = re.findall(r"^### .+$", faq, re.M)
            if not (3 <= len(qs) <= 4):
                problems.append(f"{name}: FAQ has {len(qs)} questions, expected 3-4")

        # heading reuse across the corpus is what made the library read as one article
        for h in re.findall(r"^## (.+)$", s, re.M):
            if h.strip() != "Common questions":
                HEADINGS.setdefault(h.strip(), []).append(name)

        if "<!--" in s:
            problems.append(f"{name}: HTML comment present")

        for m in re.finditer(r"\b\d+(?:\.\d+)?\s?%", s):
            problems.append(f"{name}: numeric percentage {m.group(0)!r}")

        for m in re.finditer(r"[€$£]\s?[\d,.]+\s?(?:k|m|bn|million|billion)?", s, re.I):
            problems.append(f"{name}: currency figure {m.group(0)!r}")

        # alt text must describe the diagram, not carry the design brief
        for a in re.findall(r"!\[([^\]]*)\]", s):
            if re.search(r"#[0-9a-fA-F]{6}|opacity|viewBox|px\b|stroke", a):
                problems.append(f"{name}: alt text contains design-brief detail")
            if len(a) > 400:
                problems.append(f"{name}: alt text {len(a)} chars, too long to be read aloud")
            if not a.strip():
                problems.append(f"{name}: empty alt text")

        if not s.startswith("# "):
            problems.append(f"{name}: does not open with '# ' title")
        if "\n> " not in s:
            problems.append(f"{name}: no '> ' subtitle line")
        if len(re.findall(r"^## ", s, re.M)) < 4:
            problems.append(f"{name}: fewer than 4 top-level sections")

        # every referenced asset must exist
        refs = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", s) + re.findall(r'(?:src|poster)="([^"]+)"', s)
        for r in refs:
            if not os.path.exists(os.path.join(ART, r)):
                problems.append(f"{name}: missing asset {r}")
        if not any(r.startswith("graphics/") for r in refs):
            problems.append(f"{name}: no hero graphic embed")
        if 'src="motion/' not in s:
            problems.append(f"{name}: no animated schematic embed")

        # prose word count: strip embeds, alt text, HTML tags and captions so we measure
        # what a reader actually reads, not the markup around it
        prose = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", s)
        prose = re.sub(r"<[^>]+>", "", prose)
        w = len(prose.split())
        if not (1250 <= w <= 1800):
            problems.append(f"{name}: prose word count {w} outside 1250-1800")

    for h, users in sorted(HEADINGS.items()):
        if len(users) > 1:
            problems.append(f"heading reused across {len(users)} articles: {h!r} ({', '.join(users[:4])}"
                            + (", ..." if len(users) > 4 else "") + ")")

    print(f"preflight: {len(files)} articles checked")
    if problems:
        print(f"FAILED — {len(problems)} problem(s):")
        for x in problems:
            print("  -", x)
        return 1
    print("PASS — all articles publication-ready")
    return 0


if __name__ == "__main__":
    sys.exit(main())
