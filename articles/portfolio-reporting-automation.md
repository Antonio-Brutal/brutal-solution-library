# A Reporting Engine That Turns Books That Disagree Into One Monthly Pack

> How we built a portfolio reporting engine for a private-equity operating team, and why the same approach matters for any group reporting across companies that keep their books differently.

![Flow diagram: five portfolio companies with differently kept books pass through individual mapping combs onto one shared chart of accounts, then into metric computation and a reporting pack gated by an operating partner](graphics/portfolio-reporting-automation.svg)

## The problem: the first two weeks of every month

Most operating teams don't have a reporting problem. They have a *translation* problem.

Our customer is a mid-market private-equity firm with a portfolio in the low double digits — manufacturers, distributors, a couple of software businesses across several countries — and an operating team small enough to fit in one room. Every month, that team produces a reporting pack per company: the numbers, the variances, the operational metrics, the commentary. The packs feed the investment committee, the board meetings, and eventually the LPs.

Every company keeps its books differently, and none of them is wrong to. One runs a mature ERP with a chart of accounts refined over twenty years. One runs entry-level software where half the analysis lives in the memo field. Two use the same system configured in incomparable ways. Each has its own definition of gross margin, its own view of what belongs in cost of sales, its own habits around accruals, and its own statutory obligations pulling the accounts somewhere the investor's view never goes.

So the first two weeks of every month went to translation. Someone downloads a trial balance, opens the mapping spreadsheet, remaps the accounts, recalculates the metrics the fund defines rather than the ones the company reports, chases a controller about a line that moved, writes the commentary, formats the pack. Then does it again for the next company. And again.

The consequences are worse than the hours. Numbers arrive late enough that operating partners are reacting to a quarter that has already happened. Comparability is fragile — when a company adds a general ledger account and nobody updates the mapping, the number silently changes meaning and the trend line lies without anyone noticing. Every version of the mapping lives in a workbook on somebody's laptop, so when an analyst leaves, part of the fund's reporting logic leaves too. And the people hired to improve businesses spend half of every month doing data entry.

## What we built

We built an engine that runs the translation layer. It pulls each portfolio company's raw finance and operations data, maps it into the fund's common chart of accounts using rules the team owns and can read, computes every metric against one definition, drafts the variance narrative from the underlying detail, and assembles the pack.

Nothing ships without a human. The operating partner responsible for a company reviews and signs off every pack before it goes anywhere — to the investment committee, to a board, to an LP. The engine's job is to have the arithmetic, the mapping, and the first draft of the story done before that partner sits down. The judgment call about what a number means, and whether the fund is willing to stand behind it, stays exactly where it was.

<video src="media/portfolio-reporting-automation.mp4" poster="media/portfolio-reporting-automation-poster.jpg" controls playsinline preload="none" width="1280" height="720"></video>

*Companies that keep their books differently converge on one chart of accounts.*

*Different books converge on one chart of accounts; the pack waits for a signature before it moves.*

## How it works

### Layer 1: Per-company ingestion and mapping

Each company connects the way it can: an API into the accounting system where one exists, a scheduled export where it doesn't, a defined file drop for the businesses whose finance function is one person and a spreadsheet. We do not ask companies to change systems. Replacing a portfolio company's ERP to improve fund reporting is a two-year project that solves the wrong problem.

The mapping from each company's chart of accounts to the fund's common chart is explicit, versioned, and owned by a named person on the finance side. The system proposes mappings for new accounts — it is good at recognising that "Freight Out — Region 2" belongs with distribution costs — but it never activates one on its own. An unmapped account is an exception that goes to a human, and until that human resolves it, the affected company's pack carries a visible flag. Silent mapping is the single most dangerous thing this kind of system can do: it produces a pack that looks complete, reconciles to nothing, and is believed.

Operational data comes through the same door. Headcount, units shipped, bookings, utilisation — the metrics that explain the financials — are ingested and tied to the same period boundaries, because a margin discussion without volume is guesswork.

### Layer 2: Metric computation against one definition

The fund's metric definitions live in one place, in language a human can read: how gross margin is calculated, what belongs in adjusted EBITDA, how recurring revenue is recognised, how net working capital is derived. Every company's numbers are computed from the mapped data using those definitions, so that when two businesses show the same metric, they mean the same thing.

Adjustments are where this gets serious. Add-backs, normalisations, and one-off exclusions are the most consequential and most contested numbers in private equity, and the engine treats them accordingly: it applies only the adjustment policies the fund has agreed, records which policy produced each adjustment, and refuses to invent new ones. A cost that looks non-recurring but matches no existing policy is raised as a question for the CFO and the operating partner, not quietly stripped out. The machine computes agreed treatments. It does not decide what counts as exceptional.

### Layer 3: Variance narrative drafting

When a line moves materially against budget, forecast, or prior period, the engine drafts the explanation an analyst would otherwise assemble by hand — and grounds it entirely in the detail underneath. Gross margin fell at one company because a product mix shift toward a lower-margin line coincided with a raw material price increase, with the specific accounts and volumes cited beneath the sentence. Where the portfolio company has submitted its own commentary, that is carried through and attributed, not paraphrased into the fund's voice.

The most valuable output of this layer is the admission of ignorance. When a number moves and nothing in the data explains it, the draft says so and names the question to ask the controller. An unexplained variance surfaced on day two is a phone call. The same variance discovered in a board meeting is an incident.

### Layer 4: Pack assembly and the operating-partner review gate

The pack renders itself — the standard exhibits in the standard order, per company and consolidated — and lands with the responsible operating partner as a draft, everything a human should look at already flagged: unmapped accounts, adjustments awaiting a decision, unexplained variances, incomplete submissions.

The gate is real. A pack does not leave the system unsigned, and it cannot be signed while blocking exceptions are open. Exceptions are never silently excluded from the totals to make a pack render cleanly; an incomplete pack states what is missing, because a pack that quietly drops what it couldn't handle is worse than one that arrives a day late. Every figure traces back through its metric definition and its mapping to the source trial balance line, so the answer to "where does this come from" is a path, not a recollection. And every partner edit is captured — a corrected narrative is the clearest available signal of where the engine's reading of a business and a partner's understanding of it diverge.

## Why this generalizes

The shape is any group that reports across entities it did not design: acquired companies, franchised operators, local subsidiaries — businesses that keep their own books for their own good reasons and must still roll up into one comparable view.

Acquisitive multi-brand groups live this exactly, absorbing a new chart of accounts with every deal and postponing the ERP consolidation that never quite happens. Family offices face it across an even wider spread of asset types and reporting standards. And large franchisors run it in reverse — hundreds of independent operators submitting numbers in whatever form their bookkeeper prefers, into a brand-level view needed monthly.

In all three, the instinct is a system migration or another analyst. Both are slow, and neither addresses the constraint. Leave the source systems alone, automate the translation layer above them, and keep sign-off where the accountability already sits.

## How much of your month goes to remapping the same accounts?

If your pack is assembled by hand from a dozen sets of books, your operating team's most productive fortnight each month goes to translation, and the numbers reach decision-makers already stale. We build these mapping-first, exception-visible, and signed by a human before anything leaves the building. Tell us what your month-end looks like.
