# An Incident Copilot That Reads the Logs While Your Engineers Fight the Fire

> How we built an incident-response copilot for a fintech engineering organization, and why the same approach matters for any team running systems people depend on around the clock.

![Flow diagram: alerts, deploys and logs converge onto one incident timeline; runbooks are retrieved with citations back to the events that summoned them, and the remediation branch ends at a closed valve the system cannot cross](graphics/incident-response-copilot.svg)

## The problem: the first minutes of an incident go to assembly, not repair

Most engineering teams don't have an incident problem. They have a *context assembly* problem.

Our customer runs payments and lending infrastructure across several European markets: dozens of services, a permanent on-call rotation, and the uptime expectations that come with holding other people's money. The engineers are good and the tooling is modern. Every serious incident still began the same way — a page at an unkind hour, followed by an entirely manual reconstruction of reality.

That reconstruction looks like this. The alert says error rates are climbing on one service. The engineer opens the dashboard, then the log platform, then the deploy history, then the feature-flag console, then the channel where somebody mentioned two hours ago that a dependency was being upgraded. None of those systems know about each other. The engineer is the join key. Somewhere in that sequence sits the fact that explains everything — a config change, an expired certificate, a partner API quietly returning malformed responses — and the only way to find it is to check all seven places while holding the result in your head.

Then there are the runbooks. They existed, and they were genuinely good, written by people who had been through it before. They were also spread across a wiki, a repository, and a folder somebody exported once. Searching for the right one under pressure is its own small crisis, and the worst outcome is not failing to find it. It is finding the version that stopped being true two migrations ago.

Meanwhile, the person running the incident has a second full-time job: telling everyone else what is happening. Support needs to know what to say to customers. Compliance needs to know whether this is reportable, and in payments, reportable comes with a clock attached. Executives want a sentence they can repeat. So the most context-loaded person in the room stops thinking about the outage in order to write status updates, and the quality of both jobs drops.

The postmortem is the last casualty. Days later, somebody reconstructs the timeline from memory and a channel scrollback that reads like a group chat during a house fire — because that is what it was. The most valuable artifact of the whole incident is the sequence of what actually happened, and it is the one that decays fastest.

## What we built

A copilot that sits in the incident channel and does the assembly work continuously, from the first alert to the published postmortem. It pulls alerts, metrics, log anomalies, deploys and flag changes into a single timeline. It retrieves the runbooks that match what it is seeing, with citations. It maintains a rolling summary of what is known, what is not, and what has already been tried. It drafts the status updates. When the incident closes, it writes the first postmortem draft from the timeline it recorded rather than from anyone's recollection.

One rule defines the architecture: the copilot never takes remediation actions. It cannot restart a service, roll back a deploy, flip a feature flag, scale a cluster, or fail over a region. That is not a policy written into a prompt — it is a property of the credentials it holds. Every integration is read-only, so there is no write path to production, and therefore no instruction, no jailbreak and no clever chain of reasoning that can produce one. Every action taken during an incident is taken by a named human who chose to take it.

We are firm about this because the failure modes are not symmetrical. A copilot that summarizes badly costs an engineer a minute of attention. A copilot that acts badly turns a degraded service into an outage, during the exact window when the humans are too busy to notice what it did.

<img src="motion/incident-response-copilot.svg" alt="Animated schematic: pulses travel the flow described above, pausing where a human decides." width="1200" height="630">

*Runbooks and log signals converge into a live picture. The copilot never touches remediation.*

*Signals converge into one timeline, runbooks arrive with citations, and every action stays with a human.*

## How it works

### Layer 1: Signal aggregation into one timeline

The moment an incident is declared, the copilot begins assembling a chronological record: alert transitions, error-rate and latency movements, deployments and rollbacks, configuration and feature-flag changes, infrastructure events, and the log anomalies it detects against each service's normal shape. Everything carries a timestamp, a source, and a link back to the system it came from.

This is deliberately mechanical work, and it is exactly the work humans do worst under adrenaline. The copilot is not diagnosing here. It is answering the question every incident actually starts with — what changed, and when — before anyone has to ask it out loud.

### Layer 2: Runbook retrieval with citations

Against that live picture, the copilot retrieves the runbooks and past incident records that match the symptoms, and it surfaces them the way a good colleague would: the relevant section, quoted, with a link to the source and the date it was last edited. Age is displayed as prominently as content, because a two-year-old runbook is a hypothesis, not an instruction.

When nothing matches, it says nothing matches. The copilot does not compose plausible-sounding recovery steps out of general knowledge about distributed systems, and it never generates a command for someone to paste into production. Retrieval is grounded in the organization's own documented procedures or it does not happen — an invented runbook step is the most dangerous sentence this system could possibly produce.

### Layer 3: Live incident summarization and drafted updates

The copilot maintains a running summary in three parts: what we know, what we don't, and what has been tried. Engineers joining thirty minutes late read that instead of scrolling. It also drafts the outbound communications — the customer-facing status note, the internal update, the escalation summary — each written for its audience and grounded only in the recorded timeline.

Nothing leaves the room without approval. The incident commander reviews and sends every external update, and the compliance team makes every regulatory notification decision. The copilot can point out that an event looks like it may meet a reporting threshold, and it does, early. It never makes that determination. In a regulated environment, the difference between flagging a possible obligation and deciding one is the entire distinction between a helpful tool and an unauthorized filing.

### Layer 4: A postmortem drafted from the timeline that actually happened

When the incident is resolved, the copilot produces the first postmortem draft: the reconstructed sequence, detection and mitigation moments, customer impact as evidenced in the data, and the open questions the timeline raises. It writes contributing factors as questions rather than conclusions — "the deploy at this time preceded the error spike; was it causal?" — because a machine reading a timeline can spot correlation and has no business asserting cause.

The engineers who ran the incident own the analysis, the conclusions and the action items. What changes is where they start. Instead of spending the first two hours rebuilding a timeline from scrollback, they start from an accurate record and spend that time thinking about why. The human role shifts from reconstructing what happened to judging what it means.

## Why this generalizes

Nothing here is specific to payments. The pattern is: systems that must stay up, signals scattered across tools that don't talk to each other, institutional knowledge in documents nobody can find under pressure, and an obligation to explain yourself afterwards. That is e-commerce platform operations through peak trading, where every minute of degradation is measurable and the postmortem goes to the board. It is telecom network operations, where the timeline is the regulatory artifact. It is hospital IT and clinical systems, where the stakes of an unattended automated action are the reason a read-only copilot is the only responsible design.

In all of them, the same division of labor holds. The machine reads everything, remembers precisely, and drafts. The humans diagnose, decide, act, and speak.

## Still writing postmortems from memory?

If your incidents begin with twenty minutes of tab-opening and end with a timeline nobody can fully reconstruct, the assembly work is already automatable — and it is the part your engineers should never have been doing at 3am. We build incident copilots read-only by design, with every action and every external word left to a human. Tell us what your last bad night looked like.
