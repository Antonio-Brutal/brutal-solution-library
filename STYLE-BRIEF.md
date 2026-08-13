# Brutal.ai Blog Style Brief

Derived from the two live posts (`ai-content-engine`, `semantic-layer-modern-data-stack`). Every article in this project follows this brief.

## Voice

- First-person plural throughout: "we built", "our thesis", "we lived this".
- Confident assertions, no hedging. Forward-looking claims are fine ("Over the next 18 months, the businesses that...").
- Mid-formality: accessible to a business reader, technical terms explained in one clause, no acronym soup.
- Sentence rhythm: mix short punchy statements (5–8 words) with longer technical explanations. Open sections with the punchy one.
- Minimal humor, delivered as understated frustration ("Your most expensive analysts spend half their time answering 'can you just pull that number for me?'").
- Aphoristic problem-framing near the top: "Most companies don't have an X problem. They have a *Y* problem."
- Direct address sparingly: "You have data." Rhetorical questions allowed once or twice.
- Human-in-the-loop is a recurring theme: "The human role shifts from doing X to deciding whether the result is correct."

## Structure (in order)

1. **Title**: descriptive + capability ("An AI Engine That Creates and Optimizes Its Own Content", "How We Built ...").
2. **Subtitle**: "How we built X for [generalized customer], and why the same approach matters for any [broader category]."
3. **The problem section** — heading names the real bottleneck. Punchy framing, describe the manual status quo concretely.
4. **What we built** — one section, plain description of the system.
5. **How it works** — named layers/components (3–5), each with its own sub-heading ("Layer 1: Ingestion from the source" style). This is the technical core.
6. **Why this generalizes** — lift from the specific customer to the category. Name 1–2 adjacent industries where the same shape applies.
7. **Closing CTA** — heading is a direct question to the reader ("Sitting on years of data nobody trusts?", "Running a brand across dozens of locations?"). Two or three sentences, end with an invitation: "Tell us."

## Customers

- **Never name a customer.** Describe them concretely but generically: "a European freight forwarder moving roughly 40,000 shipments a year", "a hospitality group operating 40 properties across three countries".
- Give the customer enough texture (size, geography, volume) that the story feels lived, not hypothetical.

## Metrics

- Use numbers sparingly — 3 to 5 per article, mostly volumes and time (hours per week, documents per month), not revenue claims.
- Every number used must be listed in an HTML comment at the very top of the file:
  `<!-- PLACEHOLDER METRICS — replace with real figures before publishing: ... -->`
- Keep numbers conservative and plausible. No "10x" claims.

## Length & format

- 1,200–1,500 words.
- Markdown: `#` title, `> ` blockquote for the subtitle, `##` sections, `###` for layers/components.
- No emoji, no bullet-point-only sections — prose carries the argument, bullets only for genuine lists.
