# A Close Copilot That Reconciles the Numbers and Drafts the Story

> How we built a financial close copilot for a multi-country hospitality group, and why the same approach matters for any multi-entity business.

![Flow diagram: parallel entity rails converge into a reconciliation enclosure where pairs lock; an unmatched rail drops through a siding to a lime-ringed controller-reviews node and rejoins, variance narratives draft from the matched data, and a sequential close checklist leads to the closed ledger, with an audit trail running underneath the whole flow](graphics/financial-close-automation.svg)

## The close that never really ends

Month-end close is supposed to be an event. For most multi-entity businesses it is a season.

The customer that brought us this problem is a hospitality group operating dozens of properties across several countries, each property its own legal entity with its own bank accounts, its own property management system, and its own local tax quirks. Every month, the group finance team faced the same mountain: reconcile bank statements against the property management system against the general ledger, for every entity, in several currencies. Then explain the variances — why is food-and-beverage margin down at one property, why did payroll spike at another — before the consolidated numbers could go to leadership.

The close ran for weeks. Which meant the team spent the bulk of every month looking backward, assembling reconciliation spreadsheets and chasing property accountants for explanations. By the time leadership saw a variance, the month that caused it was already history. The group's most senior controllers — people hired for their judgment — spent the bulk of their time as ticket collectors: pull this statement, tie out that account, email this property manager again. And because the work was manual, it was also fragile. Every reconciliation lived in a spreadsheet on someone's drive, every explanation in an email thread, and every audit season began with an archaeology project to reconstruct how last year's numbers were actually assembled.

Most multi-entity businesses believe they have a reporting problem. They don't. They have an *assembly* problem. The numbers exist. The explanations exist, scattered across property managers' heads and inboxes. What takes weeks is the manual assembly of both into something an auditor and a CFO can trust. Assembly is mechanical. Mechanical work is automatable.

## What we built

We built a close copilot that runs the mechanical layer of the close continuously, not just at month-end. It matches transactions across bank feeds, the property management systems, and the ledger as they occur. It drafts the first version of every variance narrative — the actual prose explaining why a number moved — from the transaction detail underneath. It orchestrates the close checklist across every entity, so the team always knows what is done, what is blocked, and who owns the blocker. And it keeps a complete audit trail of every match, every adjustment, and every narrative revision.

The controllers still close the books. But their role shifted from assembling the close to reviewing it — from building reconciliation spreadsheets to judging whether the system's reconciliation and its explanation are correct. That is the recurring pattern in everything we build: the human moves from doing the work to deciding whether the work is right.

<video src="media/financial-close-automation.mp4" poster="media/financial-close-automation-poster.jpg" controls playsinline preload="none" width="1280" height="720"></video>

*Entity ledgers converge, matched pairs lock, and only the unreconciled drops to a controller.*

## How it works

### Layer 1: Transaction matching across bank, PMS, and ledger

Every entity's bank feed, property management system, and general ledger stream into a matching engine that ties the three together at transaction level — tens of thousands of transactions per property per month: this card settlement batch equals these folio payments equals this ledger entry, net of fees. Hospitality makes this genuinely hard — a single guest stay can touch room revenue, city taxes, F&B, and a third-party booking commission, settled days apart across processors. The engine matches what it can with full confidence, flags what it can't, and — critically — does this daily. Unreconciled items surface within a day of occurring, not weeks after month-end, when the person who could explain them still remembers.

### Layer 2: Variance narratives, first draft

This is the layer that changed how the team works. When a line moves materially against budget or prior period, the system drafts the explanation a controller would otherwise have to construct by hand: F&B margin at a given property fell because banquet volume dropped while a fixed supplier contract kept costs flat — with the specific transactions and contracts cited underneath. The draft is grounded entirely in the matched data from Layer 1; the system writes down what the transactions show, and only what they show. Controllers edit, correct, or reject the draft. In the common case they confirm it and move on; in the interesting cases, the draft is the starting point for a real conversation with the property. Either way, no controller opens a blank document late at night anymore. Writing the first draft was always the slowest part of the close, because it required a human to go spelunking through the detail. Now the spelunking is done before the human arrives.

### Layer 3: Close-checklist orchestration

A close across dozens of entities is a project with hundreds of tasks per cycle, laced with dependencies: intercompany eliminations wait on entity-level reconciliations, consolidation waits on eliminations, the tax pack waits on everything. The copilot runs this as a live dependency graph. Every task has an owner, a state, and its upstream blockers made explicit. When a property accountant completes a reconciliation, everything downstream unblocks automatically and the next owner is notified. The group controller no longer discovers late in the cycle that one entity's bank reconciliation stalled in its first days — the graph shows it the moment it happens, and shows exactly what it is holding up.

### Layer 4: The audit trail

Everything the system does is recorded: which transactions were matched and under what rule, which narrative was drafted from which data, who edited it, who approved it, and when. When the auditors arrive, the answer to "how do you know this number is right" is no longer a folder of spreadsheets and a controller's recollection — it is a traceable chain from the reported figure down to the source transactions. The audit trail is not a compliance afterthought bolted onto the system. It is the reason controllers can trust the automation at all: nothing happens that cannot be inspected and reversed.

## Why this generalizes

The hospitality group is a specific shape of a general problem: many entities, heterogeneous source systems, one set of books, and a close whose length is set by manual assembly rather than accounting complexity.

Franchise groups live the identical structure — dozens of operating entities, each with a point-of-sale system and a bank account, rolling up to a brand-level P&L. Private equity portfolio operations face it with more heterogeneity, closing across acquired companies that each brought their own ERP. Retail chains face it at store level, with the same daily settlement-matching problem across processors. In each case the instinct is to solve it with headcount or with a multi-year ERP consolidation. The copilot approach is faster and less invasive: leave the source systems alone, automate the matching and the narrative assembly above them, and give the controllers a close they review instead of a close they build.

The businesses that get there first won't just close faster. They will make decisions on numbers that are weeks fresher than their competitors' — every month, compounding.

## How long does it take you to close the books?

If your month-end runs in weeks, and your best finance people spend those weeks assembling spreadsheets instead of exercising judgment, the assembly layer can be automated without replacing a single source system. We build close copilots end to end — matching, narratives, orchestration, audit trail. Tell us.
