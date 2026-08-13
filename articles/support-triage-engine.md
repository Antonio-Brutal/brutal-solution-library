# A Support Engine That Drafts the Reply Before the Agent Opens the Ticket

> How we built a triage and draft-reply engine for a subscription e-commerce brand serving customers in several languages, and why the same approach matters for any high-volume B2C support operation.

![Flow diagram: a stack of inbound tickets moves through classification and intent routing, context assembly, and on-brand drafting into an approval and earned-autonomy step where a human approves each reply before it is sent; hard cases escalate along a separate path.](graphics/support-triage-engine.svg)

## The problem: the same few dozen questions, thousands of times a month

Most support teams don't have a volume problem. They have a *repetition* problem.

Our customer is a subscription e-commerce brand shipping physical products to customers across Europe — thousands of tickets a month, arriving in several languages. Read through a week of those tickets and the pattern is impossible to miss: the overwhelming majority are variations on the same few dozen questions. Where is my order. I moved, change my delivery address. Pause my subscription for a month. Skip the next box. The card on file expired. Swap the flavor, the language, the punctuation — the questions barely change.

None of these questions is hard. Every one of them has a known answer that already lives in a system the company owns: the order management platform knows exactly where the parcel is, the subscription platform knows the billing state, the help desk knows what this customer asked last time. The support agent's actual job, ticket after ticket, was to be the integration layer between those systems — open four tabs, find the customer, read the history, and type out an answer they had typed a hundred times before. This time in Italian.

The repetition had costs well beyond the hours. A first response took most of a working day to arrive, because tickets sat in language-specific queues waiting for the right agent to come online. Hiring support agents who write well in Polish and Portuguese is genuinely difficult, so coverage was thinnest exactly where the brand was growing fastest. The brand voice drifted, because a support floor under time pressure will write one version of the same answer per agent. And the genuinely hard tickets — the shipment that arrived damaged twice, the customer cancelling a gift subscription for someone who passed away — waited in the same queue behind "where is my order," handled by agents too rushed to give them the care they deserved.

## What we built

We built an engine that reads every inbound ticket, works out what the customer wants, pulls the context needed to answer, and writes a complete draft reply — in the customer's language, in the brand's voice, grounded in that customer's actual order and subscription data. The agent reviews the draft, edits it if anything is off, and sends it with one click.

One rule shaped the entire design: the machine never sends anything unsupervised at first. Every reply passes through a human. Autonomy is not a launch feature — it is earned, intent by intent, as the system proves its accuracy where the stakes are lowest. That rule is what made the support team trust the system enough to actually use it, and it is what makes the eventual automation safe rather than reckless.

<video src="media/support-triage-engine.mp4" poster="media/support-triage-engine-poster.jpg" controls playsinline preload="none" width="1280" height="720"></video>

*Volume funnels into intent, context merges in, and the hard cases keep their own path.*

## How it works

### Layer 1: Classification and intent routing

Every inbound message — email, contact form, chat transcript — is classified against an intent taxonomy we built from the brand's own ticket history. The top intents cover the large majority of ticket volume, and that concentration is what makes the economics work. You don't need to automate everything. You need to automate the head of the distribution and route the tail to humans gracefully.

Classification also detects the language, reads the sentiment, and catches messages carrying more than one request — "where is my order, and also pause my subscription" is two intents, not one, and answering only the first is how you generate a follow-up ticket. Every classification carries a confidence score. High-confidence tickets flow into the drafting pipeline. Low-confidence tickets, and anything touching a sensitive category — legal language, safety complaints, a customer who is visibly upset — route straight to a human queue with a note explaining why the machine stepped aside.

### Layer 2: Context assembly

Before a single word is drafted, the system gathers what an experienced agent would look up by hand: current order status and carrier tracking from the order management system, subscription and billing state from the subscription platform, and the customer's previous tickets from the help desk. All of it is assembled into a compact context bundle attached to the ticket.

This layer is the difference between a useful draft and a polite non-answer. "Where is my order" answered with real tracking data — your parcel left our warehouse on Tuesday and is expected Thursday — closes the ticket. The same question answered with "we're looking into it" creates a second ticket and an annoyed customer. The model is never asked to remember facts about the customer; it is handed them, fresh, every single time. That is also why the drafts don't hallucinate order numbers: they never have to invent what they've been given.

### Layer 3: On-brand drafts in the customer's language

The brand's tone of voice is encoded as an explicit, versioned instruction set — not vibes, rules. How to greet a customer. What the product is called and never called. The right formality register per language, because the correct level of formality in German is not the correct level in Spanish. And a hard list of things a draft may never contain: promises about carrier delivery times, refund commitments beyond the published policy, anything that reads like legal advice.

Drafts are generated directly in the customer's language, grounded in the context bundle from the layer below. When the brand team updates the tone guide, the instruction set is updated with it — which means the company's support voice across every language it serves is now maintained in one place instead of inside every agent's head.

### Layer 4: Approval, escalation, and earned autonomy

The agent's screen shows three things side by side: the ticket, the assembled context, and the draft. Approve, edit, or reject — for most tickets it is one click and done. Every edit is logged and reviewed, because an edit is the most honest feedback signal there is: it marks the exact spot where the machine's answer and a human's judgment diverged.

Escalation is a first-class path, not a failure mode. The hard cases land with a human early, carrying the full context bundle with them, so the agent starts from understanding rather than from tab one. The human role shifts from assembling answers to judging them.

And this is where autonomy gets earned. When an intent runs for several weeks at a near-zero edit rate — "where is my order" got there quickly — it becomes a candidate for auto-send. A human makes the promotion decision, one intent at a time, and any intent drops back to full review the moment quality slips. Within months, a first response on drafted intents stopped being something a customer waited most of a day for and became something that arrived while the question was still fresh — not because agents typed faster, but because the queue stopped being sorted by language and started being sorted by how much judgment a ticket actually needs.

## Why this generalizes

Nothing in this architecture is specific to subscription boxes. The pattern it exploits is: high ticket volume, a short list of intents covering most of it, answers that already live in your systems of record, and a brand voice worth protecting across languages. That describes mobility apps, where "where is my driver" and "refund this trip" dominate the queue. It describes ticketing platforms drowning in "the event was rescheduled" and "change the name on my ticket." It describes telcos, food delivery, parcel networks — any high-volume B2C support operation where the questions are predictable and the answers are sitting in a database nobody has connected to the inbox.

The teams that get this right won't answer tickets faster. They'll stop treating most tickets as work for humans at all — while keeping humans firmly in charge of everything that deserves one.

## Drowning in the same few dozen questions?

If your support team can predict tomorrow's tickets before they arrive, the drafting is already automatable — the only real question is how quickly your systems can feed it context. We build these engines approval-first, with autonomy earned intent by intent. Tell us.
