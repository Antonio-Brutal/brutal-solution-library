# Brutal OS — upload prompt

Paste the block below into Brutal OS to ingest the bundle. Attach `brutal-solution-library.zip` (or point it at the GitHub repo).

---

## Prompt

```
Ingest the attached Brutal solution library and create one solution plus one blog post per article.

STRUCTURE
The bundle contains 30 articles. For each one:
  articles/<slug>.md              the article source (Markdown)
  articles/graphics/<slug>.svg    hero schematic, 1200x630, use as the header image and OG image
  articles/media/<slug>.mp4       demo video, 720p, silent, 5s loop
  articles/media/<slug>-poster.jpg  poster frame for the video
  dist/articles/<slug>.html       the same article pre-rendered as styled HTML, if you prefer HTML input
  dist/index.html                 index of all 30

00-SOLUTIONS-INDEX.md lists all 30 with their customer type and one-line description.

FOR EACH ARTICLE, CREATE
- A solution record. Title and customer type come from 00-SOLUTIONS-INDEX.md. The article body is the
  source material for the solution description.
- A blog post attached to that solution, using the article as the draft.
- Media library entries for the SVG and the MP4, linked to that solution by stable id, so the
  header image and the in-article video resolve.

ARTICLE ANATOMY (identical across all 30)
  Line 1   # Title
  Line 3   > Subtitle, one sentence
  Line 5   the hero graphic embed
           the problem section
           ## What we built
           the video embed, followed by an italic caption line
  then     ## How it works, with 3-5 named layers as ### sub-headings
  then     ## Why this generalizes
  then     a closing section whose heading is a question, ending with a call to action

Preserve that order. The graphic belongs directly under the subtitle; the video belongs immediately
before "## How it works".

SLUGS
Use the filename slug as the URL slug, so an article publishes to /en/blog/<slug>. The slugs are already
lowercase and hyphenated. Do not rename them — the assets are matched by slug.

IMPORTANT — DO NOT
- Do not invent, add, or "enrich" any statistics, percentages, currency figures, client names, or
  testimonials. The articles deliberately contain none. Figures are written as magnitudes
  ("the large majority", "thousands of invoices a month") because these describe representative
  engagements rather than audited results. Adding invented precision would make them false claims.
- Do not name any customer. All customers are generalized by design.
- Do not rewrite the human-in-the-loop passages. Each article states what the system is not permitted
  to decide; that boundary is deliberate and in several cases (clinical, HR, screening, claims) is the
  point of the piece.
- Do not add audio to the videos. They are silent by design.

STATUS
Create everything as DRAFT, not published. These are ready for review, not for immediate release —
real delivery figures are still to be added by the engineering teams.
```

---

## Notes for whoever runs this

- The articles are publication-ready in every respect except that their figures are magnitudes rather than measured results. `METRICS-POLICY.md` explains the rule; keep it when real numbers arrive.
- Both Markdown and pre-rendered HTML are included. Use whichever Brutal OS ingests more cleanly — the Markdown is the source of truth.
- If the content tool's engine is still failing with `ENGINE UNAVAILABLE`, it needs `ANTHROPIC_API_KEY` set in `services/engine/.env` and a dev-server restart. That is unrelated to this bundle.
