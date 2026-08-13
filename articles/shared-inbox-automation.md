# A Shared Inbox That Triages Itself

> How we built shared-inbox automation for a property management company handling thousands of tenant emails a month, and why the same approach matters for any operations team that lives in a shared inbox.

![Flow diagram: one wide shared-inbox channel arrives at an urgency gate where a single bright pulse breaks onto a fast express rail while the rest sort through an entity-resolution grid; the resolved stream forks into a work-order nozzle feeding the maintenance system and a draft-reply rail passing a lime-ringed node where the property manager approves before replies go out.](graphics/shared-inbox-automation.svg)

## The problem: triage by whoever opens the inbox first

Most operations teams don't have an email problem. They have a *triage* problem.

Our customer is a property management company running a portfolio of several thousand units, with thousands of tenant emails a month landing in a single shared inbox. Maintenance requests, billing questions, lease queries, complaints about the neighbors, questions about parking spots — all of it, one address, one undifferentiated stream.

The triage protocol was simple: whoever opened the inbox first dealt with what they found. Which meant a burst pipe flooding a ground-floor flat sat in the same list as a question about visitor parking, in arrival order, until someone happened to read it. Emails got claimed by being opened, so some were answered twice by two different property managers and some were answered by no one, each manager assuming another had it. Every maintenance request that did get handled had to be retyped by hand into the maintenance system — several minutes of transcription per request, tenant details copied field by field. And the first pass through the overnight pile consumed the better part of a property manager's morning before any actual property management happened.

None of this was anyone's fault. The inbox was doing exactly what inboxes do: presenting everything in the order it arrived, with no opinion about what any of it means. The expensive judgment of experienced property managers was being spent on sorting, not solving.

## What we built

We built an engine that reads every email as it arrives, classifies what it is and how urgent it is, works out which tenant, unit, and contract it concerns, creates work orders in the maintenance system automatically, and drafts a reply for the property manager to review and send.

The shared inbox is still there — nobody had to change where they work. But it stopped being a pile and became a queue: sorted by urgency and type, each message arriving pre-labeled, pre-matched to a tenant, and carrying a draft answer. Nothing is sent and no work order is dispatched to a contractor without a human looking at it first. The property managers kept every decision. They just stopped doing the sorting.

<video src="media/shared-inbox-automation.mp4" poster="media/shared-inbox-automation-poster.jpg" controls playsinline preload="none" width="1280" height="720"></video>

*Urgency takes the express rail. Everything else resolves to a tenant, a unit, a work order.*

## How it works

### Layer 1: Classification and urgency detection

Every inbound email is classified along two independent axes. The first is type: maintenance request, billing question, lease query, move-in or move-out logistics, complaint, general question. The second is urgency — and keeping it separate matters, because a burst pipe is not a parking question, even though both arrive as "maintenance." Water where it shouldn't be, the smell of gas, no heating in January, a door that won't lock: these patterns are flagged as urgent from the message content and context, not from whether the tenant thought to write URGENT in the subject line. Tenants in a genuine emergency rarely write tidy emails.

Attachments are read as part of the message, because tenants photograph problems more often than they describe them well. A blurry photo of water pooling under a boiler carries more signal than the two lines of text above it. Urgent items trigger an immediate notification to the on-duty manager; everything else lands in the queue in priority order.

### Layer 2: Entity resolution

The second question is deceptively hard: who is this, and which unit are they writing about? Tenants write from personal addresses that were never registered. Partners write on behalf of leaseholders. People move units within the portfolio and keep using the same email. A message signed "Anna, Flat 12" is useless until you know which building.

The engine resolves identity from converging signals — sender address matched against tenant records, names in signatures, unit and building references in the text, postal addresses, lease references — and attaches a confidence score to the match. High-confidence matches proceed automatically; ambiguous ones are presented to the manager with candidates ranked, one click to confirm. This layer is the least glamorous part of the system and the most essential: every downstream action, from the work order to the draft reply, is only as correct as the answer to "which tenant, which unit, which contract."

### Layer 3: Automated work-order creation

Maintenance requests — the largest single category in the inbox — used to end their journey there and start again, retyped, in the maintenance system. Now the engine creates the work order directly: category, unit, problem description distilled from the tenant's message, urgency level, photos attached, tenant contact details filled in.

Duplicates are handled at this layer too. When the lift breaks, three tenants report it within the hour; that becomes one work order with three linked reporters, not three contractor callouts. For routine issues, the property manager approves the drafted work order before it is dispatched. For urgent ones, the order is created and flagged immediately — the manager's review happens in parallel with the response, not in front of it.

### Layer 4: Draft replies for the property managers

Every email gets a draft reply built from what the system now knows. A maintenance request gets an acknowledgment with the work order reference and the expected next step. A billing question gets a reply grounded in the actual account state. A lease query gets an answer that points to the relevant clause of that tenant's actual contract, not a generic policy statement.

The manager reviews, edits where judgment is needed, and sends. Nothing leaves the inbox unsupervised — the human role shifts from typing every reply from scratch to deciding whether the prepared one is right. Most of the time it is, and the minutes saved on the routine messages are spent where they belong: on the angry tenant, the tricky lease negotiation, the judgment calls no draft can make.

## Why this generalizes

The shared inbox is the default operating system of an enormous number of teams, and it fails them all the same way. Logistics customer service desks fielding "where is my container" next to genuine exception alerts. Clinic front desks where an appointment reschedule sits in the same stream as a message describing symptoms that shouldn't wait. University admissions offices buried under deadline questions while time-sensitive transcript issues age quietly in the pile.

The shape is always identical: one address the world writes to, a small set of message types behind the apparent chaos, structured systems sitting next to the inbox that nobody has connected to it, and urgency scattered randomly through the stream. Wherever that shape exists, the same four layers apply — classify, resolve, act in the system of record, draft the reply — with a human approving every action that touches the outside world.

## Still triaging a shared inbox by hand?

If your team's morning starts with someone reading a pile of email to figure out what matters, you are paying expert salaries for sorting work a machine now does better. We build inbox engines that triage, match, and draft — and leave every send to your people. Tell us.
