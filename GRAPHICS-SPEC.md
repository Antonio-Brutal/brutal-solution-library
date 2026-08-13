# Brutal.ai Article Hero Graphic Spec — v2 (BRAND CORRECTED)

v1 copied the internal content tool's cream/brutalist look. WRONG. The real Brutal.ai brand (from brutal.ai's live CSS and the reference schematic) is: near-black navy, thin white engineering line-work, lime glow accents, quiet lowercase Space Grotesk labels. Think: an elegant circuit/signal-flow schematic drawn by a hardware engineer with taste, not a boxes-and-arrows slide.

## Reference

The canonical example: an email-triage schematic — chaotic glowing input strands converge through a funnel ("Ingestion"), pass through an isometric box containing logic gates and a small neural mesh ("Classification"), then fan out through manifold splitters to clean output nozzles ("Routing" → "assigned desk"). Lime pulses travel along white paths. Sparse lowercase labels. No headline, no wordmark, no metrics.

## Palette (from brutal.ai production CSS — exact values)

- Background: `#050608` (fill the full canvas; optional radial vignette to `#020618` at edges)
- Line-work: `#f8fafc` at 1–1.5px stroke; secondary detail lines at 40–60% opacity
- Muted labels / faint structure: `#90a1b9`, `#62748e`
- Accent lime (glow dots, pulses, filled flow-arrows, highlight rings): `#bbf451` primary, `#9de500` deep, `#d8f999` bright core
- Nothing else. No cream, no sage, no rust, no white card fills.

## Typography

- Space Grotesk: `font-family="'Space Grotesk', 'Helvetica Neue', Arial, sans-serif"`
- Labels lowercase or sentence case, NOT uppercase. 18–24px. Stage names in `#f8fafc` beneath the diagram; input/output words (e.g. "invoices", "ledger") in `#90a1b9` at the sides.
- 3–6 labels total. No title, no kicker, no wordmark, no numbers, no client names.

## Composition

- Canvas: `viewBox="0 0 1200 630"`, self-contained SVG (no external refs).
- Left→right signal flow: many messy input strands (curved paths with glowing lime dots) → 2–4 processing mechanisms → ordered outputs.
- Each stage is drawn as a MECHANISM, not a labeled box: converging wire bundles, funnels/nozzles, logic-gate clusters, small neural meshes, isometric extruded enclosures, manifold splitters, valve gates. Pick metaphors that match the article's actual layers.
- Density target: 60–120 drawn elements. Intricate but breathable — generous dark space around the machinery. This must NOT look simplistic.
- Glow: SVG filter (feGaussianBlur, stdDeviation 3–6) behind lime dots and 1–2 lime filled swoosh arrows. Layer a small bright core (`#d8f999`) over a blurred halo (`#bbf451`).
- The article's human-decision point: one lime-ringed node with a quiet lowercase label (e.g. "human approves"), integrated into the flow — understated, not a highlighted box.
- Isometric depth on ONE element max (the core processing enclosure), drawn with parallel offset lines like the reference.

## Process requirements

- Overwrite the existing file at `articles/graphics/<slug>.svg` (embeds already point there — do not change article markdown paths, but DO update alt text if the scene changed).
- Validate: `xmllint --noout`.
- Render to PNG at 1200×630 (headless Chrome or rsvg) and LOOK at it. Check: label legibility, no overlaps, glow visible against `#050608`, composition balanced. Iterate at least once before finishing.
