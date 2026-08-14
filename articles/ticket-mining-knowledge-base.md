# A Knowledge Base Mined From Ten Years of Resolved Tickets

> How we built a self-maintaining knowledge base and a deflection assistant for an enterprise IT services provider, and why the same approach matters for any organization whose best answers are buried in closed tickets.

![Flow diagram: an archive of closed tickets is clustered into article trunks, each tethered by provenance threads back to its source tickets; stale and contradictory entries divert to an owner before anything publishes](graphics/ticket-mining-knowledge-base.svg)

## The problem: the answer exists, it just was never written down twice

Most service desks don't have a knowledge problem. They have a *distillation* problem.

Our customer is an enterprise IT services provider running service desks for large corporate clients across several countries. Their ticketing system holds a decade of history — millions of resolved tickets, each one a question somebody asked and an answer that actually worked. It is the most complete record of how their business solves problems, and nobody could use it.

The official knowledge base, meanwhile, was a few hundred articles produced during a documentation push years earlier. Many described systems that had since been replaced, policies that had since changed, and steps that no longer matched the console anyone was looking at. Engineers stopped trusting it, so they stopped searching it. They searched raw ticket history instead, or asked the one colleague who remembered — which meant the knowledge base decayed further, because nothing rots faster than documentation nobody reads.

The costs compound quietly. The same incident gets solved from scratch by three engineers in three months, each spending an hour rediscovering what a fourth engineer wrote down in a resolution note in 2019. Expertise concentrates in individuals, which is fine until they take annual leave and lovely until they resign. New engineers take months to become useful, not because the work is hard but because the map is in other people's heads. And writing articles is always the task that loses: it competes with a live queue, and the live queue always wins.

## What we built

We built a system that reads the resolution history, finds the problems that genuinely recur, drafts a knowledge article for each one with links back to the tickets behind every step, watches for articles going stale or contradicting each other, and answers questions from the published set with citations.

The boundary is simple and it holds everywhere. The machine drafts; a named human publishes. Every article has an owner — a senior engineer in that domain — who approves it before it can be seen by anyone and stays on record as the person accountable for it. Nothing synthesized reaches an engineer or an end user without that signature.

<img src="motion/ticket-mining-knowledge-base.svg" alt="Animated schematic: pulses travel the flow described above, pausing where a human decides." width="1200" height="630">

*Years of resolutions become articles that know exactly where they came from.*

*Resolutions cluster into recurring problems, synthesis pulls them into drafts with provenance, and nothing publishes without an owner's approval.*

## How it works

### Layer 1: Resolution mining and clustering

The first job is reading a ticket properly, which means separating what the user reported from what actually fixed it. Resolution notes are written in haste for the person closing the ticket, and the real signal is scattered across comments, internal notes, attachments and linked change records. A note reading "same as last time, applied the workaround" is a pointer, not an answer, and the system has to follow it.

Before anything is synthesized, everything is redacted: credentials, tokens, hostnames, personal data, and client-identifying details. Tenancy is enforced structurally — knowledge mined from one client's tickets never reaches another client's assistant unless it is generic and has been explicitly approved for the shared library. In a multi-client service business that is not a nice-to-have, it is the contract.

Clustering then groups tickets by problem and fix rather than by keyword. This distinction is the whole layer. One symptom with three different underlying causes must become three articles; collapsing them into one produces a document that is wrong two-thirds of the time and confidently so. Clusters are prioritized by how often they recur and how recently, so the drafting queue reflects what is actually costing the desk hours this quarter.

### Layer 2: Article synthesis with provenance

Each cluster becomes a draft in the house structure: symptom, environment it applies to, cause, verified steps, how to confirm the fix worked, and when to escalate instead.

Every step cites the tickets it came from. Provenance is the entire game here, because it changes the review question. The owner is not asked "does this sound plausible?" — they are shown that these eleven tickets produced this step, and asked whether they agree. Where a cluster contains genuine disagreement, the draft says so and puts the choice to the owner rather than smoothing it into a false consensus.

Synthesis also tags steps that are privileged or destructive: restarting a production service, resetting credentials, editing a registry, deleting profile data. That tag is metadata carried by the article itself, and the layer above depends on it.

### Layer 3: Freshness and contradiction detection

A knowledge base is not a project, it is a population with a mortality rate. Articles die when a system is decommissioned, a client policy changes, or a vendor patch makes step four unnecessary. The system watches for that continuously.

The strongest signal is divergence: new resolutions in a cluster where engineers are doing something different from what the published article says. Others are softer — change records touching the systems an article covers, the article's own citations aging, engineers quietly editing steps, or users who received a cited answer and came back anyway.

When two articles give conflicting instructions for the same symptom, the system does not pick a winner. It opens a review task for both owners with the conflicting passages and the evidence behind each. Deciding which runbook is correct is an engineering judgment with operational consequences, and a model that resolves it silently is a model that will eventually be silently wrong. Stale articles are flagged and demoted in the assistant's ranking, never deleted — quiet deletion is how a good article that nobody had time to review disappears forever.

### Layer 4: A deflection assistant that cites its answers

The assistant answers from published articles only. If nothing published covers the question, it says so and routes to a human with a summary of the request and what it searched. There is no approximate answer, no improvised third option, no synthesis on the fly from raw tickets. An assistant that guesses about production systems is worse than no assistant at all.

Every answer shows the articles it used, as links. End users click them more than anyone expected; engineers click them constantly, because for an engineer the citation is the real product.

The privileged tag from Layer 2 becomes an architectural boundary here. Steps marked privileged or destructive are never handed to an end user. The assistant gives the safe portion, then opens a ticket routed to an engineer with the full article attached. That rule lives in the article metadata and the routing logic, not in a prompt politely asking a model to be careful.

Questions the assistant could not answer become a ranked queue of knowledge gaps. It is the most honest content roadmap the organization has ever had, because it is built from what people actually asked rather than from what someone assumed should be documented. The human role shifts from answering the same question repeatedly to owning the answer once.

## Why this generalizes

The pattern is any organization where doing the work already produces a written record of the fix. Field service for medical devices and industrial equipment is the same picture with different documents: decades of service reports describing symptoms, causes and repairs, sitting in a system used only for billing. Software companies run it inside their own support desks, where the answer to a customer's question was written last month in a thread nobody indexed. Internal shared service centres for HR, payroll and finance answer the same few hundred questions every year, with the correct answers scattered across a decade of email.

In each case the archive is not a compliance artifact. It is a knowledge base that has already been written and never assembled — and assembling it is a machine's job, while standing behind it stays a person's.

## Sitting on a decade of tickets nobody can search?

If your best documentation is a resolution note somebody typed at the end of a long shift, you already own the knowledge base — it just hasn't been written yet. We build these systems provenance-first, with a named owner behind every published article. Tell us what your ticket history looks like.
