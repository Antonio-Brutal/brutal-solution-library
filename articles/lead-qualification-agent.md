# An Agent That Qualifies Inbound Before a Rep Opens the Email

> How we built an inbound qualification agent for a B2B industrial manufacturer, and why the same approach matters for any company whose best lead is currently sitting unread in a shared inbox.

![Flow diagram: inbound leads pass through enrichment into a scoring lattice defined by the sales team, then route to the right rep with a drafted first touch awaiting approval](graphics/lead-qualification-agent.svg)

## The problem: the good lead arrives looking exactly like the bad ones

Most B2B sales teams don't have a lead-volume problem. They have a *sorting* problem.

Our customer manufactures industrial equipment sold into factories and processing plants across Europe — long sales cycles, technical buyers, deals that are specified over months and installed over quarters. Their inbound channel is a contact form, a general sales address, and a stream of trade-show scans. What arrives through it is a name, a company, and one sentence of free text.

That sentence is the entire problem. "Interested in your equipment" might be a student writing a dissertation, a competitor doing research, a supplier hoping to sell them something, or a maintenance engineer at a large processing group who has been told to replace a production line this financial year. All four look identical in the inbox. The only way to tell them apart is to research the company — website, sector, plant locations, recent announcements — which is a solid quarter-hour of tab-opening nobody does dozens of times a week.

So the sorting happened by proxy, badly. Reps skimmed for a recognizable company name, and anything from a domain nobody knew went to the bottom — in industrial markets a specific and expensive error, because the recognizable names are often mature accounts and the unfamiliar ones are frequently the manufacturer expanding capacity. Meanwhile leads sat for days — the rep who could have answered was travelling, or it was unclear whose territory the lead belonged to, and an unclear owner means no owner.

The cost is not the wasted hours. It is that the response arrives long after the moment of intent has passed. Someone who filled in a form on Tuesday afternoon was, at that moment, actively comparing suppliers. By Friday they are further along, with someone else. In a market where one line replacement anchors a multi-year relationship, arriving fourth is the same as not arriving.

## What we built

An agent that processes every inbound lead the moment it arrives: enriching it from public sources, scoring it against an ideal customer profile the sales team wrote themselves, routing it to the right rep by rules the sales leadership owns, and drafting a first-touch reply for that rep to review and send.

The design principle we insisted on is that the sales team owns the judgment and the agent owns the legwork. The ICP is not a model artifact or a learned propensity score. It is a plain-language document the head of sales and the regional leads wrote, that anyone can read, and that any of them can edit on a Tuesday afternoon and see take effect immediately. When a score looks wrong, the answer is never "that's what the model thinks." It is a specific criterion, in a document with an author, that a human can argue with and change.

And the agent never disqualifies anyone. Low-scoring leads are not deleted, hidden or silently binned; they go to a visible nurture queue that any rep can search and pull from. The machine sorts. People decide.

<img src="motion/lead-qualification-agent.svg" alt="Animated schematic: pulses travel the flow described above, pausing where a human decides." width="1200" height="630">

*Fit and intent are scored against an ICP the sales team wrote, not one the model invented.*

*Raw inbound is enriched, weighed against the sales team's own criteria, and routed — with the rep approving every word that goes out.*

## How it works

### Layer 1: Enrichment from public sources

The moment a lead lands, the agent builds a picture of the company behind the email domain: what it makes, which sector it operates in, roughly how large it is, where its sites are, whether it has announced an expansion, what it has been hiring for. Job postings are unusually informative in industrial markets — a plant advertising for process technicians is a plant preparing to run more line time.

Two rules govern this layer. Everything comes from sources a rep could have opened themselves, and every enriched field carries its link, so a rep can check the claim in one click. And unknown is a permitted value. When the agent cannot establish a company's sector or size with confidence, the field stays empty and says so. An enrichment layer that guesses is worse than no enrichment layer, because it manufactures confidence in a score built on top of it.

### Layer 2: Fit and intent scoring against an ICP the sales team wrote

Fit is scored against the ICP document: the sectors this equipment suits, the production characteristics that make it a fit, the plant scale below which the economics don't work, the geographies where the company can actually service an installation. Intent is scored separately, from the lead's own words and behavior — the specificity of the enquiry, whether a timeline or a technical requirement is mentioned, whether they asked about a particular product line.

Keeping the two apart matters. A perfect-fit company with a vague enquiry is a relationship to build patiently. A poor-fit company with an urgent, specific request is often someone else's opportunity, and knowing that early is worth as much as a qualified lead. Every score itemizes its reasoning criterion by criterion, with the enrichment evidence attached, so a rep reads why in seconds rather than trusting a number.

### Layer 3: Routing by rules the sales leadership owns

Routing is the least glamorous layer and the one that recovered the most value. The agent applies the rules the business already has: territory, product line, existing account ownership, distributor and channel-conflict rules, key-account exceptions. It applies them consistently, in seconds, at three in the morning and during the trade-show week when everyone is out of the office.

It does not invent routing rules, and it does not resolve genuine ambiguity. When a lead could legitimately belong to two territories, or touches an account another team already works, it goes to a human duty desk with the conflict spelled out. Guessing an owner in an organization with channel partners is how you damage a partner relationship, and no amount of speed is worth that.

### Layer 4: First-touch drafting, with hard limits on what a draft may say

The rep receives a drafted reply written in their own voice, referencing what the enrichment established, answering the specific question asked, and proposing a concrete next step. Most of the work of a good first response is having read up on the company, and that reading is already done.

The rep edits and sends. Nothing is ever sent automatically — not to a lead, not to a partner, not to anyone. And the drafting layer operates under an explicit prohibition list that is enforced structurally, not stylistically: it has no access to the pricing system, and it may not quote a price, commit a lead time, confirm a technical specification, or make any statement about compliance or certification. In industrial sales those sentences are commercial commitments, and in some markets contractual ones. A first-touch email is an invitation to a conversation; the moment it becomes a quotation it belongs to a human with the authority to make that promise. So we built it so that it cannot accidentally become one.

## Why this generalizes

The pattern is any business where inbound is high in volume, wildly mixed in quality, and expensive to research one lead at a time. Specialty chemicals and laboratory equipment distributors run exactly this funnel, with the same problem that the unfamiliar domain is often the best account. Commercial construction and engineering services firms field enquiries where the sorting question — is this project real, is it funded, is it in our region — is answerable from public information nobody has time to gather. Freight and logistics providers quoting inbound shipping requests face the same mix of serious buyers and idle enquiries arriving through one form.

In every one of them the same division works. The agent does the reading, the enrichment and the routing at machine speed and machine consistency. The sales team writes the definition of a good customer, keeps it visible, and makes every call that touches a relationship or a commitment.

## Is your best inbound lead sitting unread right now?

If your reps are sorting inbound by which company names they recognize, the leads worth the most are the ones being ignored longest. We build qualification agents around an ICP your sales team writes and can edit, with routing rules you own and every outbound word approved by a person. Tell us what your inbound looks like on a normal Monday.
