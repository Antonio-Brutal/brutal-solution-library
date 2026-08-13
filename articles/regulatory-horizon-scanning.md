# How We Built a Regulatory Horizon-Scanning System for a Payments Fintech

> How we built a regulatory horizon-scanning system for a payments fintech operating across multiple European markets, and why the same approach matters for any business whose rulebook is written by someone else.

![Flow diagram: distant source beacons feed a change-detection comparator where an old and new version overlay and the difference glows lime, then an impact-mapping lattice routes the change and an officer confirms before it fans out to distinct owner terminals, each with a deadline](graphics/regulatory-horizon-scanning.svg)

## One compliance officer, a rulebook in every market

One compliance officer. A spread of European jurisdictions. Dozens of official sources that publish whenever they feel like it. The payments fintech we worked with was licensed across multiple markets, which meant its rulebook was written and rewritten by a national regulator in each of them, plus the European supervisory authorities, plus the official journals where the actual legal text lands. One person tracked all of it: regulator newsletters, consultation papers, guideline updates, a browser folder of bookmarks, and a reading load that ran well into double-digit hours a week.

Most regulated companies don't have a compliance problem. They have a *detection* problem. The controls were sound. The policies were current — as far as anyone knew. The weakness was upstream of all of it: knowing, reliably and promptly, when the rules had moved. And detection ran through a single person's reading stamina.

She was good at it. That was part of the problem. Because she was good at it, nobody worried about it, and because nobody worried about it, the process stayed what it was: one diligent professional scanning feeds and PDFs, always slightly afraid of the one she missed. Miss a consultation paper and the company loses its chance to shape a rule that will constrain the product for years. Miss a guideline update and a control drifts quietly out of date until an auditor — or worse, an incident — finds it.

There is a second cost, less visible. Reading is not actually the job. The job is what happens after the reading: deciding whether a change applies, which controls and policies it touches, who needs to act, and by when. The scanning was consuming exactly the hours that assessment and follow-through needed.

## What we built

We built a horizon-scanning system that monitors the official sources, detects what actually changed, explains each change in plain language, maps it to the internal controls, policies, and product features it touches, and routes it to a named owner with a deadline.

The thesis fits in one sentence: the system turns regulatory change from a reading problem into a work-assignment problem. The compliance officer stopped being a human news feed. She now supervises a pipeline — reviewing the system's assessments and correcting its routing instead of producing everything from scratch — and the bulk of that reading time came back to her.

It is worth saying what the system is not. It does not interpret the law, and it does not decide what the company should do about a change — those calls stay with the humans who are qualified and accountable for them. It makes sure the right human sees the right change, with the right context, in time to act.

<video src="media/regulatory-horizon-scanning.mp4" poster="media/regulatory-horizon-scanning-poster.jpg" controls playsinline preload="none" width="1280" height="720"></video>

*Change arrives from many sources, gets compared against what stood before, and lands on an owner.*

## How it works

### Component 1: Source monitoring

The system watches dozens of official sources: national regulator websites across every licensed market, official journals, European supervisory authority publications, and open consultation feeds. The engineering here is unglamorous and essential. Regulators do not publish tidy APIs. They replace PDFs at the same URL, restructure guideline pages without notice, and sometimes announce a substantive change only in a press release.

The monitoring layer checks these sources continuously, normalizes every publication into a common format, and deduplicates aggressively — the same amendment surfacing in two newsletters and one official journal is one item of work, not three. Nothing gets discarded silently; anything the system cannot classify lands in a review queue rather than a void.

### Component 2: Change detection and summarization

Finding new documents is the easy part. Knowing what changed is the hard part, and it is where the manual process bled the most hours. Regulators routinely republish a sixty-page guideline in order to amend two paragraphs, and the reader is left to find them.

The system diffs each new version against the previous one and produces a plain-language summary of the difference — a summary of the *change*, not a summary of the document. "The updated guideline extends incident-reporting obligations from major incidents to significant near-misses; reporting windows are unchanged" is a sentence someone can act on. Every summary links back to the exact passages it came from, because a compliance officer should never be asked to take a machine's word for anything.

### Component 3: Impact mapping

A summary is knowledge. Compliance runs on consequences. The third layer maintains a register that links regulatory topics to the internal artifacts they govern: controls, policies, procedures, and product features. When a change lands, the system maps it against the register and states the blast radius: this update touches the outsourcing register, the incident-response policy, and the merchant-onboarding flow in more than one market.

We built that register in working sessions with the compliance officer, and it deserves the same observation we make in most of our projects: the map already existed — in her head. She could tell you from memory which policy a given guideline fed. The register made that map explicit, which means it now survives holidays, handovers, and resignations.

### Component 4: Owner routing with deadlines

The last layer is where reading becomes work. Every relevant change becomes a task with a named owner and a deadline taken from the regulatory calendar itself — consultation closing dates, transposition deadlines, dates of entry into force. Assignment happens while the change is still news rather than at the next quarterly review, and every task is tracked to closure.

The compliance officer reviews each assessment before it ships: confirming relevance, adjusting the impact mapping, redirecting the owner if the system chose wrong. Her role shifts from reading everything to deciding whether the system's reading is correct. A side effect worth naming: the pipeline produces a complete audit trail — what arrived, who was told, what they did about it — which is precisely the kind of record regulators like to be shown.

## Why this generalizes

Nothing in this architecture is specific to payments. Medical device manufacturers track MDR guidance and notified-body communications across the same kind of ragged source landscape. Food producers track labeling and safety standards that shift country by country. Crypto platforms face a rulebook that is being written in real time, in public, across a dozen venues at once.

Any regulated business shares the shape: the rules are written elsewhere, published unevenly across many sources, and carry real consequences for the one you miss. The sources change, the register contents change — the system does not. And in most of these companies, detection is the unfunded function: teams are staffed to assess and remediate, while finding out lands by default on whoever reads the most newsletters.

Over the next few years, the gap between these two postures will widen. Companies that treat regulatory change as assigned, deadlined work will absorb it as routine; companies that treat it as reading will keep discovering changes at audit time, when the options are worst and the explanations are hardest.

## What's your plan for the regulatory change you haven't seen yet?

If regulatory monitoring at your company is one diligent person and a folder of bookmarks, you have a single point of failure reading as fast as they can. We build the system that watches, explains, and assigns — so your experts spend their time on the response, not the reading. How does regulatory change reach your team today? Tell us.
