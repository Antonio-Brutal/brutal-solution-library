# How We Built a Contract Review Copilot for a Skeleton-Crew Legal Team

> How we built a contract review copilot for the in-house legal team of a commercial real-estate group, and why the same approach matters for any team that reviews agreements against a standard it carries around in its head.

![Flow diagram: leases, contracts, and NDAs enter clause extraction, pass through the playbook made explicit, deviation flagging, and redlines with rationale, and a lawyer decides — accept, edit, or reject — before the redline goes out](graphics/contract-review-copilot.svg)

## The bottleneck is reading, not judgment

A legal team you could count on one hand. Hundreds of contracts a year. That was the in-house legal function of a commercial real-estate group we worked with: lease agreements, service contracts, and NDAs flowing in from asset managers, facilities teams, and brokers across the portfolio — and every single one read line by line. Not because every contract was dangerous, but because there was no way to know which ones were without reading them.

Most in-house legal teams don't have a judgment problem. They have a *reading* problem. The judgment — knowing which indemnity language is acceptable, when a break option is worth fighting for, what a reasonable liability cap looks like on a facilities contract — was excellent and fast. What consumed the week was the mechanical work of getting to the point where judgment could be applied: reading forty pages of counterparty paper to find the handful of clauses that actually mattered.

The manual routine looked like this. A first pass on an incoming lease ate the better part of a morning. The lawyer read every clause, compared it against a standard that existed nowhere except in her head, marked up a Word document, and typed out comments explaining why the indemnity language was unacceptable — comments she had written, in slightly different words, dozens of times before. When one lawyer went on holiday, everyone else's queue swelled, and a large share of the institutional memory went offline with the out-of-office reply.

Here is what struck us in the first workshop: the team already had a playbook. Ask any of the lawyers about assignment clauses and you would get, without hesitation, the preferred position, two acceptable fallbacks, the walk-away line, and a war story about the negotiation that shaped each one. None of it was written down anywhere. The playbook existed. It just wasn't explicit.

## What we built

We built a contract review copilot that reads every incoming contract, extracts and classifies its clauses, compares each one against the team's own negotiation playbook, flags every deviation from the standard, and proposes redlines with the rationale attached. The lawyer reviews flags instead of reading documents cold. Nothing goes back to a counterparty without a lawyer's sign-off — the human role shifts from reading every line to deciding whether the machine's reading is correct.

It is worth being clear about what the system is not. It is not a chatbot that answers legal questions, and it is not a substitute for a lawyer's judgment on a novel deal. It is a first-pass reviewer that applies, tirelessly and consistently, the positions the lawyers themselves wrote down.

<img src="motion/contract-review-copilot.svg" alt="Animated schematic: pulses travel the flow described above, pausing where a human decides." width="1200" height="630">

*Clauses run against the playbook. What deviates diverts, and a lawyer decides what to do about it.*

## How it works

### Component 1: Clause extraction and classification

Contracts arrive as PDFs and Word files, on counterparty paper at least as often as on the group's own templates. The first layer segments each document into clauses and classifies them against a taxonomy of a few dozen clause types that matter in this practice: indemnities, liability caps, assignment and change of control, break options, rent review mechanisms, service levels, insurance obligations, confidentiality, termination rights.

Counterparty paper is messy — sometimes deliberately so. The indemnity you care about is a sub-paragraph buried in "General Provisions", and the liability cap is split across two schedules. Classification therefore works on what a clause does, not on what its heading says. The output is a structured map of the document: every commitment, obligation, and right, sorted by type.

### Component 2: The playbook, made explicit

This is the heart of the system, and the least technical part of the project. For each clause type, the playbook records the team's preferred position, its fallback positions, and its walk-away terms — written by the lawyers themselves, in working sessions where we mostly asked questions and typed. We did not impose an external standard, license a clause library, or scrape precedent from the internet. The standard was already there, applied consistently for years. It just lived in the heads of the people applying it.

This is a theme we keep meeting in our work: the most valuable step in building an AI system is often making explicit what was implicit. The document that came out of those sessions would have been worth the effort even if no software had followed — it is an onboarding manual, a continuity plan, and a negotiation standard in one. And the playbook remains a living document the lawyers own. When a hard negotiation changes their view of an acceptable cap, they edit the playbook, and every future review inherits the change.

### Component 3: Deviation flagging

With clauses classified and the playbook explicit, comparison becomes tractable. Each extracted clause is checked against the corresponding playbook position, and the differences are stated plainly: "This indemnity clause differs from your standard in three ways: it is uncapped, it extends to indirect losses, and it survives termination indefinitely."

Flags are graded, because not every deviation deserves the same attention. A clause matching the preferred position passes with a note. A clause landing within a fallback position is flagged with the fallback it matches, so the lawyer knows what has already been conceded. A clause beyond the walk-away line goes to the top of the queue. The lawyer opens a contract and sees a triaged list of deviations, not forty pages of undifferentiated text.

### Component 4: Suggested redlines with rationale

For every flag, the system proposes a redline — replacement language drawn from the playbook — together with the rationale, phrased the way the team phrases it. The lawyer can accept the redline as-is, edit it, or reject it. The rationale matters as much as the new language: it is the explanation that goes back to the counterparty, so it has to be negotiation-ready, not a generic note about risk.

The accept-edit-reject decisions are also a signal. When a lawyer keeps rewording the same proposed clause the same way, that is the playbook asking to be updated, and the update takes a minute. A first pass that used to eat a morning is now a short, focused review of what the system flagged. The judgment is untouched; the reading has been delegated.

## Why this generalizes

Nothing in this system is specific to real estate. The same shape fits any team of expert reviewers facing a steady volume of documents and carrying its standard in its head.

Procurement teams reviewing supplier terms against purchasing policy have a playbook — payment terms, liability, data protection, exit rights — that almost never exists in writing. HR teams handling employment contracts and severance agreements across jurisdictions have one too. So does every in-house legal team carrying a department's workload with a handful of people, which in our experience describes most in-house legal teams.

The move is identical in every case: make the standard explicit, let the machine do the comparing, and keep the human on the judgment calls no standard can make. The experts stop being the bottleneck and become what they always should have been — the authors of the standard and the final word on the exceptions.

## Staring at a contract pile only you can review?

If your team reads every agreement line by line because the standard lives in someone's head, that standard is your most valuable unwritten asset. We help teams write it down, then build the system that applies it — so your experts spend their time deciding, not reading. What does your review pile look like this week? Tell us.
