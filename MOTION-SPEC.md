# Motion Spec — animated schematics

## Why this replaces generated video

Three rounds of prompt engineering against FLUX + Seedance produced, at best, a 20% pass rate. The failure modes were persistent and unfixable by prompting: 3D-shaded objects, circuit boards and microchips, glowing perspective grid floors, lens flare, LED-matrix dot blocks, and garbled pseudo-text. Generated video cannot be held to a brand system, because nothing in the pipeline is under our control.

The 30 hero schematics in `articles/graphics/` are already exactly right. Animating them is deterministic: same mechanism as the article, same palette, same line weights, zero possibility of a stray glyph or a lens flare. It is also ~100× smaller and infinitely crisp.

**The animated SVG is the primary deliverable.** Raster MP4/GIF are derived from it for platforms that cannot take SVG.

## What the animation does

Motion must be restrained and legible — it exists to show the flow of the mechanism, not to decorate.

1. **Travelling pulses.** Small lime dots move along the schematic's existing flow paths, left to right, using `<animateMotion>` bound to those paths by reference. Do not invent new geometry.
2. **Staggered starts.** Pulses on parallel paths start at different offsets (`begin="0.4s"`, `1.1s`, …) so the piece breathes instead of marching in lockstep.
3. **The human node breathes.** The lime-ringed decision node gets a slow opacity or radius pulse (approx 2.4s cycle) so the eye lands on it.
4. **The exception path behaves differently.** Where the schematic has a rejected/flagged/held branch, its pulse either stops at the terminal or pauses before rejoining — the article's argument, made visible.
5. **Everything else stays perfectly still.** Structure never moves, fades, or redraws.

## Hard rules

- Total loop length exactly **6s**, seamless: state at t=6 must equal t=0. Use `repeatCount="indefinite"` and `dur="6s"` (or an exact divisor: 2s, 3s).
- Never add text, never change the palette, never add glow beyond the existing filter.
- Never modify the static geometry. Animation is additive only — new `<animateMotion>`, `<animate>`, `<set>` elements plus, at most, new `<circle>` pulse dots.
- Respect reduced motion: wrap animations so `@media (prefers-reduced-motion: reduce)` freezes them (`animation-play-state` for CSS; for SMIL, a CSS rule hiding the moving dots is acceptable).
- Output must remain a single self-contained SVG file, `viewBox` only, ids still slug-prefixed.

## Files

- `articles/graphics/<slug>.svg` — static (unchanged; used as OG image)
- `articles/motion/<slug>.svg` — animated version, embedded in the article
- `articles/media/<slug>.mp4` / `.gif` — raster fallbacks rendered from the animated SVG

## Raster rendering

Render deterministically with headless Chrome. To avoid one browser launch per frame, lay out N frozen copies of the SVG in a grid on one page — each copy advanced with `svgRoot.setCurrentTime(i * step)` — screenshot once, then slice the grid into frames and encode with ffmpeg. 72 frames at 12fps over 6s.
