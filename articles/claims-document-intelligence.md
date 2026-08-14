# An AI System That Reads the Claim File So the Adjuster Can Decide It

> How we built claims document intelligence for a regional property and casualty insurer, and why the same approach matters for any operation where decisions wait on reading.

![Flow diagram: scattered claim documents and photos funnel through intake and an evidence-extraction lattice, align against a policy-terms grid for coverage cross-check, and condense into one brief rail that ends at an open node — the adjuster decides, the system never does](graphics/claims-document-intelligence.svg)

## Adjusters are paid to decide. They spend their days reading.

A claims file is a pile of paper wearing a case number. First notice of loss forms, photos of the damage, contractor repair estimates, police reports, medical bills, correspondence — all of it arriving as unstructured attachments in whatever shape the policyholder, the body shop, or the police department happened to produce.

The customer that brought us this problem is a regional property and casualty insurer handling thousands of claims a month. Their adjusters are experienced, licensed professionals whose job is judgment: what does the policy cover, is this estimate reasonable, does the evidence hold together. But a typical claim file runs to dozens of documents, and before an adjuster can exercise any judgment, someone has to read all of it — find the damage description buried in the FNOL narrative, pull the line amounts out of a photographed repair estimate, cross-reference the police report's account against the policyholder's. By the insurer's own reckoning, its adjusters spent more of their working hours reading and re-reading documents than doing anything else, and the backlog grew every time a storm rolled through. The re-reading matters as much as the reading: documents trickle in over days or weeks, so an adjuster returns to the same file again and again, rebuilding the mental picture from scratch on each visit.

Most insurers describe this as a claims capacity problem and respond by hiring more adjusters. It isn't a capacity problem. It is a *preparation* problem. The decision itself — covered or not, pay this much or contest — takes an experienced adjuster minutes once the facts are assembled. What consumes the hours is assembling the facts. And assembling facts from documents is precisely what AI now does well, while deciding claims is precisely what it should not do.

## What we built

We built a claims document intelligence system that reads everything so the adjuster reads only what matters. It normalizes the intake — every attachment, every format — extracts the evidence from each document, cross-checks the claim against the actual policy terms, and assembles an adjuster brief in which every single statement cites the source document it came from.

One design principle governed the whole build, and we held to it without exception: the system never decides a claim. It does not approve, deny, or reserve. It prepares the decision, completely, and puts a human in front of it. This is not a limitation we tolerated; it is the architecture we chose. Claims decisions carry regulatory weight, contractual weight, and human weight. The correct role for the machine is to make the decider faster and better informed — the human role shifts from excavating the file to judging it.

<img src="motion/claims-document-intelligence.svg" alt="Animated schematic: pulses travel the flow described above, pausing where a human decides." width="1200" height="630">

*Scattered evidence becomes one cited brief. The final node stays open: the adjuster decides.*

## How it works

### Layer 1: Intake normalization

Everything that arrives — emailed photos, scanned FNOL forms, faxed police reports, PDFs from repair networks, voicemail transcriptions — is converted into a single normalized claim file. Each item is classified by type, deduplicated, timestamped, and attached to the right claim even when the sender forgot the claim number and referenced a name and a date instead. Nothing is discarded and nothing is retyped. The adjuster stops being the person who reconstructs the file from an inbox; the file assembles itself as evidence arrives.

### Layer 2: Evidence extraction

Each normalized document is mined for the facts a claims decision runs on. From photos: what is damaged, how severely, and whether the visible damage is consistent with the described cause of loss. From repair estimates: line items, labor rates, and totals — even when the estimate is a photograph of a printout on a contractor's clipboard. From police reports: parties, location, the reporting officer's account. From the FNOL: the policyholder's narrative and its stated timeline. Every extracted fact carries two things — a confidence score, and a pointer to the exact document and passage it came from. Weak extractions are flagged as weak, never silently smoothed over.

### Layer 3: Coverage cross-check

Facts alone don't frame a decision; the policy does. This layer reads the claim against the policyholder's actual policy — the specific form, endorsements, limits, deductibles, and exclusions in force on the date of loss, not a generic product description. It surfaces the questions an adjuster would otherwise dig for: the loss date sits inside the policy period; water damage of this type touches this exclusion; the estimate total crosses this sub-limit. The output is deliberately framed as flags and citations, not conclusions. The system says "this exclusion may apply, here is the clause, here is the evidence that triggered the flag" — and stops there. Deciding whether the exclusion actually applies is the adjuster's job, and the system is built so it cannot creep into it.

### Layer 4: The adjuster brief

Everything converges into a single brief: what happened, what the evidence shows, what the policy says, and where the open questions are — with every statement footnoted to its source document, so verification is one click rather than a search through the whole stack of attachments. Inconsistencies get their own section: the estimate that includes a room no photo shows, the police report timeline that disagrees with the FNOL. The brief is ready almost as soon as the last document lands. And because claims evolve, the brief evolves with them: when a supplementary estimate or a late police report arrives, the brief updates and marks what changed, so each return visit to a file starts from an accurate picture instead of a stale one. The adjuster opens the file and starts where they used to finish: at the judgment.

## Why this generalizes

Strip away the insurance vocabulary and the shape is this: decisions of consequence, made by trained professionals, throttled by the reading of heterogeneous documents. That shape is everywhere.

Warranty processing is the nearest neighbor — claims, receipts, photos of failed parts, coverage terms, and technicians spending their time on paperwork triage instead of failure analysis. Travel insurance runs the same loop with booking confirmations, medical certificates, and airline correspondence. Lending operations may be the largest instance of all: underwriters reading bank statements, pay slips, and contracts to assemble a credit picture before the credit decision — which, like the claims decision, should stay human.

In every one of these, the automation target is the same and so is the boundary. Automate the reading, the extraction, and the cross-checking. Keep the decision with a person, and hand that person a brief where every fact shows its source. Businesses that draw the line there get the speed of automation and keep the accountability of human judgment — and their professionals finally spend their hours on the work they were hired for.

## Watching a claims backlog grow?

If your adjusters — or underwriters, or warranty teams — spend most of their day reading documents instead of making the decisions you actually pay them for, the reading can be lifted off them without taking the decision away from them. We build systems like this end to end, from intake to brief. Tell us.
