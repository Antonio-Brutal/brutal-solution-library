# Brutal.ai — Solution Library

Thirty engineering write-ups covering AI systems and internal-improvement work, one per solution, each with a hero schematic and a short demo loop.

**Live index:** open `dist/index.html`.

## What's here

```
articles/            30 source articles in Markdown
  graphics/          30 hero schematics (SVG, 1200×630)
  media/             30 demo videos (MP4, 720p, silent) + poster frames
dist/                built HTML — one page per article plus an index
  og/                30 branded share cards (1200x630 PNG), one per article
build/
  build.py           Markdown → styled HTML export
  review.py          single-file review page with everything inlined
  preflight.py       publication gate — run before every export
00-SOLUTIONS-INDEX.md  the catalogue
STYLE-BRIEF.md       voice and structure spec
GRAPHICS-SPEC.md     the visual system for the schematics
VIDEO-SPEC.md        the video pipeline and prompt formula
METRICS-POLICY.md    what may and may not be claimed
```

## The articles

Each follows the same shape: name the real bottleneck, describe what was built, walk the named layers of the architecture, generalise to adjacent industries, then invite a conversation. Human-in-the-loop is a through-line rather than a disclaimer — every piece names who approves what, and what the system is not permitted to decide.

Customers are described concretely but generically ("a mid-market European freight forwarder", "a regional property and casualty insurer"). No real client is named anywhere in the corpus.

## Figures — read this before publishing

**These articles describe representative engagements, not audited results.** Figures have been written as honest magnitudes ("the large majority", "thousands of invoices a month") rather than invented precision. There are no percentage claims, no currency amounts, and no ROI multiples anywhere in the corpus, by policy — see `METRICS-POLICY.md`.

When real numbers become available from delivery teams, they replace the magnitude phrasing and become genuine, defensible claims. Until then, nothing here overstates what was measured.

## Assets

Schematics are self-contained SVG on `#050608` with white line-work and lime accents, sized 1200×630 so they double as OG images. Every `id` is slug-prefixed, so any number of them can be inlined on one page without collisions.

Diagram loops are silent five-second 720p clips, each with a poster frame and a true GIF alternative under `articles/media/gif/`. They embed as `autoplay loop muted playsinline` so they behave like a GIF — no controls, no click to start — because they are diagrams rather than something the reader chooses to watch. Prefer the MP4 over the GIF where the platform allows it: same loop at roughly half the weight and noticeably sharper, since GIF caps at 256 colours and these are subtle gradients on near-black.

They carry no text by design. Generated lettering is unreliable and reads as fake, so every label lives in the article and the schematic instead. `VIDEO-SPEC.md` records the prompt discipline this requires — describe geometry, never objects, since object nouns like *panel*, *dial* or *matrix* pull the model toward labelled instrument panels that arrive covered in garbled glyphs.

## Rebuilding

```bash
python3 build/preflight.py    # gate: fails if anything is not publication-ready
python3 build/build.py        # -> dist/
python3 build/review.py       # -> review-all-30.html (single file, everything inlined)
```

`preflight.py` checks every article for production notes, forbidden tokens, numeric percentage claims, currency figures, design-brief alt text, structural integrity, prose length, and that every referenced asset resolves on disk. It exits non-zero on any failure — wire it into CI if these move into a real pipeline.
