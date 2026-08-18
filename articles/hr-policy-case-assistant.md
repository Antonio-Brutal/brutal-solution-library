# An HR Assistant That Cites the Clause and Cannot Tell You Who Asked

> Under German co-determination a per-person question log is the regulated object, so the analytics store holds cohorts only and the sensitive routes never invoke a model at all.

![Flow diagram: jurisdiction-layered policies feed a retrieval lattice that returns cited answers, while sensitive topics take a separate branch that bypasses drafting entirely and goes straight to a person](graphics/hr-policy-case-assistant.svg)

## In one market, the log file is the illegal part

In a co-determined market, the record of who asked the question is the regulated object, not the answer. Section 87(1)(6) of the German Works Constitution Act gives the works council a co-determination right over the introduction and use of technical devices that are suited to monitor employee behaviour or performance. Suitability is the test. Intent is irrelevant, and a system that logs which employee asked which question is suited to monitoring whether or not anyone ever reads the log.

The employer has several thousand people across a handful of European countries, served by an HR function small enough that everyone knows everyone else's calendar. The policies exist and they are good: a group handbook, country addenda covering what differs by jurisdiction, works council agreements in one market, a separate leave policy in another. What employees actually use is the shared inbox and whoever sits nearest, and the overwhelming majority of what arrives there has a documented answer that gets typed out again by hand.

HR asked for an assistant over the handbook with a question log behind it, and every component of that request is reasonable on its own. In this employer's largest market, the log is the part that stops the project.

## Co-determination is a veto, not a privacy preference

Co-determination is not a setting you can respect more or less. Deploying a covered system requires a negotiated works agreement, and those agreements typically forbid individual-level evaluation outright, which means an admin toggle marked "disable per-user analytics" satisfies nothing. The capability is the problem. A switch implies someone with the rights to flip it.

A second clock runs alongside it. The EU Whistleblower Directive 2019/1937 requires acknowledgement of an internal report within seven days and feedback within three months, and it protects the reporting person's identity. A protected disclosure that lands in a general HR question log is both a confidentiality breach and a statutory deadline nobody started.

Those two facts push in the same direction: per-person analytics had to become impossible in the design rather than switchable in the settings, and the sensitive routes had to leave the assistant entirely.

## The question log we built and the one we were allowed to keep

We built an identity-linked question log first, because it made everything downstream easy. Routing knew who to hand a question to. Entitlement scoping was a lookup. The gap map, the set of questions the assistant could not answer from policy, turned out to be the most useful thing the system produced, and it assembled itself when every question carried a person.

The works council review in one market stopped the rollout before a single employee had used it. An identifiable record of who asked about parental leave, sick pay or notice periods is precisely what the co-determination right covers, and negotiating the works agreement that would have permitted it would have taken longer than the build.

So we rebuilt around two stores. An ephemeral session store holds identity only for the duration of a single answer, long enough to scope the response to the right country, entity and contract type, and it is gone when the answer is delivered. A separate analytics store keeps the question text, the jurisdiction and whether the question was answered, with no identifier attached and a minimum cohort size enforced before any cut of it will render. Escalations leave both stores and enter the case system, where identity is necessary and access is controlled like any other case file.

The gap map survived the rebuild. Read as a set, unanswered questions show where policy is missing, ambiguous, or written in language nobody can act on, and none of that reading requires knowing who asked.

<img src="motion/hr-policy-case-assistant.svg" alt="Animated schematic: pulses travel the flow described above, pausing where a human decides." width="1200" height="630">

*Answers cite their source. Sensitive cases bypass drafting entirely and go straight to a person.*

## A generation-free path for the questions that deserve a person

On the sensitive list, the system produces nothing at all. Harassment, discrimination, bullying, retaliation, whistleblowing, safety concerns, health and disability disclosures, mental health, grievances, terminations, pay disputes, and anything in which the employee names another person: no answer, no draft, no suggestion. The employee gets a named person and a time, and a whistleblowing route starts its seven-day acknowledgement clock at intake rather than whenever someone opens the inbox.

Generation-free path: a route through the system on which no model is invoked at all. The classifier's only output is a routing decision, and the employee receives a named person and a time rather than a drafted answer. A prompt can be talked into answering; a code path that never calls a model cannot.

The classifier is deliberately over-inclusive, tuned knowing it would send routine questions to humans, because the opposite error is the one that causes harm. Sensitivity here is a property of the route, not a warning appended to an answer.

## One clause, one country, one version, or silence

Routine questions get an instant answer with a citation to the exact clause in the exact document version, in the asker's jurisdiction, or they get no answer at all. We refuse to answer from general employment knowledge, because a model's generic understanding of parental leave is an average of the internet and the employee in front of it is governed by one agreement in one country. An answer scoped to the wrong entity is not partially right. It is wrong, delivered with confidence.

Precedence between sources is declared rather than inferred. Handbooks, country addenda, works council agreements and policy memos carry different authority, and a local agreement overrides the group handbook in the market it covers because a human said so, not because a model read the tone. Every source carries its scope: which entity, which country, which contract types, effective from when and superseded when. Documents are chunked along their own structure, because a leave table split down the middle is a wrong answer waiting for someone to ask.

We also refuse to build the dashboard. No view of this system can rank, segment or single out individuals by what they asked, in any market, including the ones with no works council at all. Building it once for a permissive jurisdiction means the capability exists everywhere.

If your handbook is not versioned and scoped by jurisdiction, an assistant on top of it is a faster way to give wrong answers, and the policy register is the project to do first.

## What a case summary is forbidden to conclude

For cases already in human hands, the case layer assembles what a business partner would otherwise rebuild by hand: a chronological timeline of the thread, the policy sections implicated, what was agreed, and what remains outstanding against the statutory and internal deadlines that apply. Feedback dates under the Whistleblower Directive are tracked as dates, not as intentions.

It produces a summary and never a conclusion. It does not propose an outcome, assess credibility, suggest a disciplinary step, or score anything about a person, because a machine-generated suggestion anchors a judgment that has to stay independent. Every summary is marked as drafted, reviewed before it enters the case record, and never sent to the employee.

The decisions the system may not make are named and enforced in code rather than in a prompt: it may not decide that a sensitive matter is routine, may not answer without a citation, may not produce a per-person view of question activity, and may not close a case.

## Common questions

### Will our works council approve this?

That is a negotiation, and the architecture is what makes it short. There is no identity-linked question log to argue about, no per-person view to restrict, and a minimum cohort size enforced before any analytics cut renders. Councils ask first what is stored and who can see it, and answering "nothing at the person level" changes that conversation from months to weeks.

### What stops it from answering something it should escalate?

The escalation path never invokes a model, so there is no prompt to talk around. The classifier's only job on that route is to decide where the question goes, and it is tuned to over-escalate. A routine question sent to a person costs a few minutes. A harassment report answered by a machine costs considerably more than that, and it cannot be taken back.

### Can we still see what employees are asking about?

Yes, as cohorts and never as people. You get question text, jurisdiction and whether policy answered it, aggregated above a minimum cohort size. That is enough to see that one country's leave policy generates repeated confusion or that a new expense rule is unreadable. It is not enough to work out who asked, which is the point.

### How does it handle countries with different rules for the same policy?

Every source is ingested with its scope and precedence attached, and answers are retrieved within the asker's country, entity and contract type. Where a local works agreement overrides the group handbook, that ordering is declared by HR operations, not inferred. If nothing in the asker's jurisdiction covers the question, the assistant says so and routes it rather than borrowing another country's clause.

## Do you know what your HR inbox is being asked, without knowing who asked?

Business partners running a lookup service for policies they wrote, while the serious cases queue behind the expense questions: that split is fixable without building a monitoring device in the process. We design these boundary-first: cited answers where policy is clear, a named person for everything that deserves one, and no per-person record to negotiate over. Tell us which markets you operate in and what lands in your inbox.
