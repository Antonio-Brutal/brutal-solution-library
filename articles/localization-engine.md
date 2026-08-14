# Our Localization Engine Ships Fewer Translations Than It Rejects

> Why a meaningful share of interface strings cannot be translated into Polish by anyone at any budget, and what changed when the pipeline started filing bugs against the source code instead of guessing.

![Flow diagram: source strings carry their interface context through a glossary-enforcement gate into translation, with a native-reviewer node prioritising the most visible strings before release](graphics/localization-engine.svg)

## Some strings cannot be translated, only rewritten in English first

A meaningful share of the strings in any interface cannot be translated into some target languages at all, by any translator, at any budget. They can only be rewritten in English first, and until someone does that, every translation of them is a guess that will be wrong in a way the reviewer cannot fix.

Our customer is a consumer app expanding across Europe: nine live languages, more queued, thousands of interface strings, a release train that ships weekly, and the process almost everybody starts with. Export the changed strings to a spreadsheet, email it to a pool of freelancers, wait days, paste the results back, ship.

The obvious failure there is missing context. "Free" means one thing on a pricing page and something unrelated beside a booking slot, and a spreadsheet row cannot tell a translator which one it is. Capturing the screen, the component and a rendered crop alongside every string solves that, and it was the easy half of the work.

The half that mattered was the strings that context cannot rescue. Our pipeline's most valuable output turned out to be a list of defects filed against the source code, not a set of translations.

## Six plural categories, and a source language that knows about two

CLDR defines six plural categories, zero, one, two, few, many and other, and languages select different subsets. Arabic exercises all six. Polish and Russian use one, few, many and other. English uses two.

An English source string written as a singular and a plural literally does not contain enough forms to be expanded into Polish. When the plural choice lives in application code, as an if-statement selecting between two literals, the target language has nowhere to put its remaining forms and no translator can add them without editing the source. The bug sits upstream of the translation, in a language nobody is translating.

Grammatical case compounds it. A Slavic sentence interpolating a name usually requires that name in the instrumental or the genitive, so a variable slot filled with a nominative string produces a sentence that is wrong in a way no character-count check will ever catch.

A translatable string is one whose meaning, grammatical number, and grammatical role are fully determined by the string and its metadata. A string that acquires its meaning from where it happens to render, or its plural form from an English if-statement, is a defect in the source code.

We will not machine-translate a string assembled by concatenation. Those go back to the developer as defects, because a sentence stitched together in code has no grammatical structure to preserve, and every language with case or gender agreement breaks on it. The fix is one message with named variable slots and declared plural rules, which costs a developer minutes and a translator nothing.

## Pseudolocalization runs on every pull request, before a translator exists

Every pull request renders the interface in a pseudolocale, so expansion breakage is found before a translator has been paid to discover it. Source strings are transformed mechanically: accented characters throughout, length padded to the expansion a verbose target language produces, and visible boundary markers at each end.

The boundary markers are what make concatenation visible. A sentence assembled from three fragments renders as three bracketed pieces on screen, which is unarguable in a code review. Anything still rendering as plain unaccented English is a hardcoded string that never reached the resource file.

Every source string is also fingerprinted at build time, so when the English changes, all nine translations are flagged stale immediately with a diff of what moved. That single mechanism ends the state where a product speaks last quarter's copy everywhere except its home market.

## We widen the component; we do not shorten the sentence

The first pipeline had one rule about length: no string may exceed the character budget of the component it renders in. It obeyed that rule, and the obedience was the failure. German strings met the budget by being abbreviated into clipped, telegraphic forms that fitted the button. Native reviewers rejected them as brand damage, and they were right: the output satisfied every check we had written and was worse than the freelancer spreadsheet it replaced.

So we inverted the escalation. When a string cannot meet its budget inside the tone specification, the engine does not compress it. It opens a layout ticket against the component, with a rendered screenshot of the overflow attached, and a designer decides whether the sentence changes or the component widens.

Over the following quarter, more components were widened than strings were retranslated, and that ratio is the whole argument. A layout built to English word lengths is a design decision nobody ever consciously made, and compression was hiding it inside the translation budget where no designer could see it.

<img src="motion/localization-engine.svg" alt="Animated schematic: pulses travel the flow described above, pausing where a human decides." width="1200" height="630">

*Strings carry their context through translation. The glossary is enforced, not suggested.*

## The glossary is enforced twice, and the second time is programmatic

The glossary is injected as a constraint at generation time and then checked against the output programmatically, because a rule that is only ever a prompt is a suggestion. A translation using a banned term or the wrong register fails the check and is regenerated or escalated rather than quietly shipping.

Per language it holds product nouns and feature names with their approved translation, a never-translate list, the wrong-but-tempting alternatives that are explicitly banned, the formality register, and constructions to avoid. Formality carries real consequences: the choice between du and Sie, tu and vous, je and u changes how the product feels, and no freelancer should be making it per string, in isolation, on a Tuesday.

The glossary is owned by the brand team and versioned like code. Change an entry and every affected string in every language is re-queued, so the brand voice lives in one file rather than inside nine translators' heads.

## Reviewers stop translating and start legislating

Reviewers are a finite resource, so the queue is ordered by impressions multiplied by risk class rather than by arrival. The first onboarding screen, the paywall and the errors people hit when a payment fails are reviewed by an in-market native speaker every time. A tooltip in an advanced setting that sits inside the glossary and passes every check publishes and is reviewed later.

Each reviewer sees the source string, the context screenshot, the glossary entries applied and the engine's own flags. Their job is to judge, then to classify: every edit is recorded as a glossary entry, a tone-specification amendment, or a genuine one-off. Edits that repeat become rules, so the same correction is never made twice.

That reclassification changes the job. A native speaker with product judgment is wasted retyping sentences and valuable deciding what the brand sounds like in their language.

## Consent copy does not auto-publish, at any confidence

One class of copy never publishes without a named human, at any model confidence and at any traffic volume: legal terms, consent and privacy language, refund and cancellation policy, pricing and billing copy, and safety and accessibility instructions. Those carry regulatory weight that varies by market, so they route to an in-market reviewer, with counsel where the market requires it.

Routing is enforced by the risk class attached to the string, not by a reviewer remembering to be careful on a Friday afternoon. The class is set where the string is defined and travels with it, so skipping review requires an explicit change to the source rather than a lapse in attention.

Build this when your release train ships faster than a human review cycle can follow it. If you publish a marketing site in two languages a few times a quarter, a translation memory and a good agency will serve you better, and that is where the money should go.

## Common questions

### Can we just machine-translate everything and have someone check it afterwards?

Checking afterwards catches the wrong class of error. The failures that matter are structural: a plural form the source could not express, a name interpolated in the wrong grammatical case, a sentence concatenated in code. Each of those has to be fixed in the source string before translation happens, which is why the pipeline files them as defects rather than sending them to a reviewer.

### How many of our strings are actually defective?

More than any team expects, and you can find out in a day. Run pseudolocalization over your existing build and count the strings that overflow their component, the ones rendering as several bracketed fragments, and the ones still appearing in unaccented English. That is a real defect list against your own code, produced before you commission a single translation.

### Won't developers push back on localization filing bugs against them?

Less than you would think, once the ticket arrives with a rendered screenshot and a one-line fix. The pushback we see comes from vague quality complaints months after a release. A pull-request check that fails immediately, on the code someone is actively writing, reads as a build error rather than as criticism from another department.

### What about languages we have not launched yet?

They are the reason to start early. A source string that satisfies the definition above can be sent to a new language on the day you sign the market. A concatenated, English-shaped one has to be rewritten first, and every existing translation of it re-done. Fixing the source is the part of this work that compounds.

## How old is the copy your product speaks in its ninth language?

If nobody can answer that quickly, the translations are not the part that is broken. We build localization pipelines that capture context automatically, enforce the brand as versioned rules, and send the impossible strings back to engineering where they can actually be fixed. Tell us how many languages you are behind, and we will show you what your own build already knows.
