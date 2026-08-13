# Metrics Policy — publication readiness

These articles describe representative engagements. No figure in them is a documented, audited result. Publishing invented precision ("83% reduction", "€1.2M saved", "team of nine") as if measured is a credibility risk for Brutal and is not acceptable.

The fix is NOT to delete every number — that guts the writing. The fix is to replace **false precision** with **honest magnitude**.

## Rules

1. **Delete the `<!-- PLACEHOLDER METRICS ... -->` comment entirely.** No production notes, TODOs, or editorial asides survive into the final file. The published article must contain nothing but publishable prose and asset embeds.

2. **Convert precise counts to magnitudes.**
   - "roughly 45,000 shipments a year" → "tens of thousands of shipments a year"
   - "around 6,000 invoices a month" → "thousands of supplier invoices a month"
   - "a finance team of nine" → "a finance team you could fit around one table"
   - "hundreds of thousands of SKUs from thousands of suppliers" → keep (already a magnitude, not a claim)

3. **Convert precise performance claims to qualitative statements.**
   - "more than 80% of invoices match without a human" → "the large majority of invoices match and post without a human touching them"
   - "12 minutes average handling time" → "handling time ran well into double-digit minutes"
   - "resolution takes under 3 minutes" → "resolution takes minutes, because the investigation is already done"
   - "PR merges rose from 35 to 93 per month" → "merge throughput roughly doubled"

4. **Never invent a currency figure, percentage improvement, or ROI multiple.** If one exists in a draft, remove the number and keep the direction ("cost per document fell sharply").

5. **Keep numbers that are structural, not performance claims.** Layer counts ("a four-layer loop"), time windows that define the process ("month-end close"), and industry-standard facts are fine. "A 400-page operating manual" is fine — it characterizes the problem, not Brutal's result.

6. **Preserve voice.** These edits must read as deliberate authorial choice, not redaction. "The large majority" is a confident sentence. "A significant percentage (exact figure TBD)" is not. Never leave a bracket, a placeholder, or a hedge like "up to X%".

7. **Preserve the argument.** If removing a number leaves a sentence pointless, rewrite the sentence around the mechanism instead of the metric.

## Acceptance check per file

- Zero HTML comments in the file.
- Zero occurrences of: TODO, TBD, FIXME, XXX, placeholder, [ ], (exact figure, replace with.
- Zero occurrences of the build tokens `GRAPHIC_EMBED` and `VIDEO_EMBED` — these are scaffolding used while drafting ahead of the assets, and they pass a naive TODO grep, so they must be checked for by name.
- Every asset path referenced in the file resolves to a file that exists on disk.
- No bare percentage claims about Brutal's results.
- No invented currency amounts.
- Article still opens with `# Title`, `> subtitle`, then the graphic embed; video embed still sits above `## How it works`.
- Word count stays within 1,150–1,500.
