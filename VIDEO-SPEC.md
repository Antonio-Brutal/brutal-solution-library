# Brutal.ai Article Video Spec

One short demo video per article: a silent, elegant, brand-aesthetic animation of the article's central workflow, problem, or crux. High-status and restrained — never gimmicky. Format matches the live blog's existing embed (native MP4 `<video>` with poster).

## Pipeline (proven in pilot)

Keys: `source /private/tmp/claude-502/-Users-antonio-marques-Documents-Claude-Projects-Brutal-Articles/a4398d1d-3a2d-4ca2-9dac-066edf9a7fbb/scratchpad/keys.env`
Scripts: same scratchpad, `bin/bfl.sh` (FLUX keyframe) and `bin/seedance.sh` (video; pass image path as 3rd arg for image-to-video).

1. **Keyframe** — `bfl.sh <tmp>/<slug>-keyframe.png "<keyframe prompt>"` (FLUX 1.1 pro, 1280×704).
2. **LOOK at the keyframe** (Read the PNG). Off-brand, cluttered, contains text/figures → adjust prompt, regenerate. Max 2 attempts, then keep the better one.
3. **Animate** — `seedance.sh <tmp>/<slug>-raw.mp4 "<animation prompt>" <keyframe.png>` (Seedance 2.5, 720p, 5s, camera fixed).
4. **Review** — extract 3 frames (`ffmpeg -vf "select='eq(n\,0)+eq(n\,60)+eq(n\,110)'" -vsync vfr`), LOOK at them. Warped line-work or chaotic motion → regenerate once with a calmer prompt.
5. **Finalize** —
   - `ffmpeg -i raw.mp4 -an -c:v copy articles/media/<slug>.mp4` (strip audio; silent by design)
   - `ffmpeg -i articles/media/<slug>.mp4 -frames:v 1 -q:v 3 articles/media/<slug>-poster.jpg`
6. **Embed** — in the article, directly BEFORE the `## How it works` heading (or the article's equivalent section), matching the live site's pattern:

```html
<video src="media/<slug>.mp4" poster="media/<slug>-poster.jpg" controls playsinline preload="none" width="1280" height="720"></video>
```

One italic caption line beneath it, e.g. `*The matching flow: every document becomes structured data; only exceptions reach a human.*`

## Prompt formula

**Keyframe (FLUX):** start from this base, then describe the article's mechanism scene:
"Wide technical schematic illustration on a near-black dark navy background, thin white circuit-like line-work, small glowing lime-green (yellow-green chartreuse) dots along the paths, elegant premium minimal tech aesthetic, vector style, high contrast, no text, no letters, no numbers, no logos, no human figures"

Scene = the article's crux as a mechanism (funnel for ingestion, comparator for matching, lattice for scoring, manifold for routing...). One clear left-to-right flow. Density like a fine circuit board — intricate but composed.

**Animation (Seedance i2v):** "Animate this static schematic: small glowing lime-green pulses travel smoothly left to right along the white lines; [one article-specific motion beat, e.g. 'one pulse diverts into the side loop, pauses, then rejoins']; all line-work remains perfectly static and crisp; camera fixed; subtle seamless-loop motion; no text."

## Rules

- Emphasize LIME green (#bbf451 family — yellow-green), not emerald/teal.
- No text anywhere in the scene (AI-garbled lettering is an instant tell). Labels live in the article, not the video.
- No metrics, no client references, no people, no offices, no stock-footage vibes.
- Silent audio track stripped. 5 seconds, 720p, camera fixed.
- Every video gets human review of extracted frames before finalize.
