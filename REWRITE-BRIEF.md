# Rewrite Brief — kill the sameness, kill the slop, earn the citation

This supersedes the structural parts of `STYLE-BRIEF.md`. The voice (first-person plural, confident, mid-formality) still holds. Everything about *shape* changes.

## What went wrong

Thirty articles were written to one template, so we produced one article thirty times. Measured across the corpus:

- 26 of 30 used the identical aphorism "They don't have an X problem. They have a *Y* problem."
- 13 of 30 contained the sentence "The human role shifts from..."
- All 30 used the same three section headings: "What we built", "How it works", "Why this generalizes".
- 468 em dashes.

Read alone, each piece is fine. Read together, they blur. That is a structural failure, not a writing failure, and the fix is structural.

## Rule 1: No em dashes. None.

Not one, in any article, ever. Replace each with the punctuation the sentence actually needs: a comma, a colon, a semicolon, a full stop, or parentheses. Often the best fix is two sentences. Never substitute a hyphen or " - ".

## Rule 2: The banned-phrase list

Delete on sight. These are the tells that make writing read as machine-produced:

- "It's not just X, it's Y" and every variant of that construction
- "Here's the thing", "The truth is", "Let's be honest", "Make no mistake"
- "In today's landscape", "In an era of", "As we move forward", "The reality is"
- "delve", "leverage" as a verb, "robust", "seamless", "unlock", "empower", "supercharge", "game-changer", "transformative", "revolutionise", "at scale" used as filler
- "It's important to note", "It's worth noting", "That said" as a paragraph opener
- Rule-of-three lists used for rhythm rather than because there are exactly three things
- Rhetorical question followed immediately by its own answer, more than once per article
- Any sentence that restates the thesis in different words. Say it once, properly.
- Hedging stacks: "may potentially", "could arguably", "in some cases might"

## Rule 3: Every article needs a spine that no other article could have

Before writing, decide the one thing this piece is *about* that would be factually wrong if pasted into any of the other 29. Then build the article around it.

The spine is usually one of:
- **A domain constraint nobody outside the industry knows.** Demurrage clocks in freight. Coverage triggers in claims. Jurisdictional divergence in HR policy. Recipe yield drift in kitchens.
- **A counterintuitive finding.** The thing that surprised us when we built it.
- **A specific failure.** What we tried first, why it did not work, what we changed. This is the strongest single move available and almost nothing else signals real experience as effectively.
- **A design argument we will defend.** Take a position. Say what we refuse to build and why.

Test before submitting: pick your three sharpest paragraphs. If any of them could sit inside another article in this library with the nouns swapped, it is not specific enough.

## Rule 4: Vary the structure. Do not reuse the old skeleton.

Headings must be written for *this* article, in its own vocabulary. "What we built" and "Why this generalizes" are banned as headings; cover that ground under headings that say something. Aim for 4 to 6 sections and vary how you open:

- open on a concrete scene at a specific moment in the working day
- open on the wrong solution that everyone tries first
- open on a constraint that makes the obvious approach illegal or impossible
- open on a number that reframes the problem
- open on a flat, arguable claim and spend the piece earning it

Rotate these deliberately. Adjacent articles in the index must not open the same way.

## Rule 5: Write for AI citation (GEO/AEO)

AI answer engines cite passages they can lift whole. Optimise for extractability without sounding like a manual:

- **One self-contained claim per paragraph.** A paragraph that only makes sense after reading the previous one cannot be quoted. Front-load the claim, then support it.
- **Answer the question in the first sentence under a heading**, then elaborate. Never build to the point across three paragraphs.
- **Use precise, checkable nouns.** "Three-way matching against the purchase order and the goods-receipt note" is citable. "Advanced document processing" is not.
- **Define the term you own.** Each article should define at least one concept crisply enough to be quoted as a definition. Put the definition in its own short paragraph.
- **Include one comparison or decision rule** the reader could act on, for example when this approach is wrong and what to use instead.
- **End with a short FAQ**, heading `## Common questions`, containing 3 to 4 real questions a buyer asks, each answered in 40 to 70 words, each answer self-contained. Questions must be phrased the way someone would actually type or say them.

## Rule 6: Keep the honesty rules

Unchanged and non-negotiable: no invented percentages, currency figures or ROI claims; magnitudes only; no named clients; no production notes; and every article still states plainly what the system is not permitted to decide.

## Structure of the finished file

```
# Title
> Standfirst, one sentence
<hero graphic embed>          (leave the existing embed line untouched)
... opening section, heading written for this article ...
... 3 to 5 further sections ...
<animated schematic embed>    (leave the existing embed line and its caption untouched)
## Common questions
### question?
answer
## <closing heading, phrased as a direct question to the reader>
two or three sentences, ending in an invitation to talk
```

Length: 1,300 to 1,700 words including the FAQ. Keep both existing media embeds exactly where they are, byte-identical, including alt text and caption.

## Rule 7: break the machine rhythm

AI-drafted prose has a rhythm detectors and readers both pick up, separate from word choice. The corpus audit found it everywhere. These rules apply to every article and every future edit:

1. **"Rather than" is rationed.** Corpus count was 205, roughly seven per article; no human does that. Maximum three per article. Replace with "instead of", "not", restructure, or plain assertion.
2. **Twin-sentence antithesis is rationed.** "Receipt is notice. Reading is not." is a fine sentence; three per section is a metronome. Keep at most two per article, flatten the rest into ordinary sentences.
3. **Vary the lists.** "Cannot A, cannot B, cannot C" triples everywhere: make some lists two items, some four, break some into prose, interrupt one with an aside.
4. **Not every paragraph earns a mic drop.** Let some paragraphs end on a plain fact. The aphorisms that survive gain force from the quiet around them.
5. **Allow human texture.** Per article, one or two parenthetical asides (this is what parentheses are for), one or two honest hedges ("in practice", "on the accounts we saw", "more often than not"), an occasional sentence starting with And or But. Paragraph lengths should visibly vary: a one-sentence paragraph beside a six-sentence one.
6. **Thin the intensifiers.** "Exactly", "precisely", "deliberately" carry force only when scarce.
7. **Never fake humanity.** No injected typos, no grammar errors, no manufactured rambling. Facts, structure and honesty rules stay untouched. The goal is prose a careful human editor would actually produce, which is also the prose that scores least machine-made.
