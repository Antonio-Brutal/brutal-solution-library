# An Analytics Agent in Slack That Can't Make Numbers Up

> How we built a governed analytics agent for a B2B scale-up, and why the same approach matters for any company past the dashboard-sprawl stage.

![Flow diagram: plain-language questions drop into a governed SQL generation chamber that sits atop a wide semantic-layer lattice feeding it from below, answers exit as chart clusters, and one flagged question loops through a data-team-defines node back into the lattice as a new definition](graphics/analytics-agent-slack.svg)

## The queue behind the dashboards

The data team had done everything right. The B2B scale-up we worked with had a data team you could name from memory, a properly modeled warehouse, and a semantic layer — the layer where a metric like "active customer" is defined once, in one governed place, instead of five slightly different ways across five dashboards. There were dashboards for every department, refreshed on schedule, documented and maintained.

And still the queue: dozens of ad-hoc requests a week, most of them opening with some variant of "can you just pull that number for me?"

Most data teams don't have a tooling problem. They have a *queue* problem. Dashboards answer the questions somebody predicted six months ago. Real questions arrive with one extra filter, one different cut, one date range nobody predicted. When that happens, the business user has two options: learn SQL and the warehouse's table names, or ask the data team. They ask the data team.

The math is grim on both sides. Turnaround on a routine request was measured in days, while the meeting that needed the number was happening that afternoon — so people guessed, reused the figure from last quarter's deck, or decided without it. Meanwhile some of the company's most expensive analytical talent spent half its week operating as a query service, pulling numbers a machine could have pulled, instead of doing the analysis it was hired for.

## What we built

We built an analytics agent that lives in Slack. Anyone in the company can ask a question in plain language; the agent generates SQL strictly against the semantic layer, runs it, and posts the answer back into the thread as a chart or table — together with the exact definition it used.

The constraint is the product. The agent can only use metrics the data team has defined. It cannot write free-form SQL against raw tables, and it cannot invent a definition of "active customer" — it can only use the one that exists. The data team stays in the loop where it matters: not approving every answer, which would recreate the queue, but owning every definition an answer can be built from.

We've written before about semantic layers and why a warehouse without one is a pile of tables rather than a source of truth. This system is the payoff of that groundwork, and we'll be blunt about the dependency: it only works *because* of the governance. Point the same agent at an ungoverned warehouse and it will produce wrong numbers with total confidence — find five revenue-like tables, pick one, write fluent SQL, and format a beautiful chart of the wrong answer. The semantic layer is what makes self-serve safe.

<img src="motion/analytics-agent-slack.svg" alt="Animated schematic: pulses travel the flow described above, pausing where a human decides." width="1200" height="630">

*The agent sits on top of the governed layer. It cannot invent a definition, only use one.*

## How it works

### Component 1: Question intake in Slack

The questions were already happening in Slack; the agent went to them rather than asking users to visit yet another tool. People ask in a shared channel or by direct message, in ordinary language: "how many active customers did we add in Q2, by region?"

When a question is ambiguous, the agent asks one clarifying question — "rolling 30 days or calendar quarter?" — rather than silently picking an interpretation. And because conversations live in threads, context carries: "same thing, but enterprise accounts only" works as a follow-up, exactly the way it would with a colleague.

Meeting people where they already work did more for adoption than any launch announcement. There was no login to remember and no interface to learn; the first time someone watched a teammate get a chart in a thread, they had learned the whole product.

### Component 2: Governed SQL generation

This is the core layer. The semantic layer holds many dozens of governed metrics and dimensions — revenue measures, customer counts, pipeline stages, usage metrics — each with a single owned definition. The agent composes its queries exclusively from these building blocks. No raw-table access, no improvised joins, no on-the-fly definitions.

When someone asks for a number that has no definition, the agent says exactly that, and names the nearest metric that does exist. That refusal is a feature, not a limitation. A system that sometimes says "that metric doesn't exist yet" can be trusted when it answers; a system that always answers cannot.

### Component 3: Charts and tables back in the thread

Answers render where the question was asked: a chart when the question implies a trend or comparison, a table when it implies a list. Every answer states the definition and filters it used — "Active customers: accounts with a paid subscription and at least one product login in the last 30 days; trials excluded."

That one detail changed more behavior than any other. When the definition travels with the number, arguments stop being "whose number is right" and become "is this the right definition" — a better argument, and one the data team can settle once, in the semantic layer, for everyone. Analysts who want to verify can expand the generated query; nothing is hidden.

### Component 4: The feedback loop

Wrong or ambiguous answers do not vanish into a thread. Any user can flag a response; every flag becomes a ticket for the data team; and the resolution, in most cases, is a new or refined metric definition in the semantic layer. A question the agent couldn't answer this month becomes a metric it answers correctly next month.

This inverts how the semantic layer grows. Instead of speculative upfront modeling, it expands along the grain of the questions people actually ask. The data team's role shifts from answering questions to defining the terms in which questions get answered — governance becomes the day job, and the query-pulling is delegated to the machine. The routine requests largely stop reaching an analyst at all, and an answer that used to take days now arrives while the question is still on the screen.

## Why this generalizes

This pattern fits any company past the dashboard-sprawl stage — and most companies with a data team are past it. The warehouse exists. The BI tool is licensed. The dashboards have multiplied beyond anyone's ability to name them. And the questions still route to humans, because the last step between a business user and a trustworthy number was never the visualization. It was the definition.

The order of operations is the whole lesson. Governance first, agent second. Bolting a language model onto an ungoverned warehouse doesn't democratize data; it industrializes the production of confident wrong numbers — faster answers, worse decisions. If the semantic layer isn't in place yet, that is the project to start with. The agent that comes after is almost the easy part, and it is what finally makes the unglamorous definitional work visible to the whole company.

## How long is your data-request queue right now?

If your analysts spend their week fielding "quick pulls" while the dashboards gather dust, the missing piece isn't a smarter chatbot — it's governed definitions and an agent constrained to use them. We build both, in that order. What did someone ask your data team for this morning? Tell us.
