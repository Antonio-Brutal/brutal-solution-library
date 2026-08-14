# QA That Reads Every Conversation, Not One in Fifty

> How we built full-coverage conversation QA for an outsourced contact center running support for several consumer brands, and why the same approach matters for any operation where conversations carry quality or compliance risk.

![Flow diagram: a broad sheet of every conversation across voice, chat, and email flows into a scoring lattice fed from above by the rubric as code; scored pulses collect into per-team coaching channels on the right, while a calibration loop below routes through a lime-ringed node where humans audit the scorer and feed refinements back into the lattice.](graphics/conversation-qa-full-coverage.svg)

## The problem: quality management by lottery

Most contact centers don't have a quality problem. They have a *visibility* problem.

Our customer is an outsourced contact center — a BPO running customer support for several consumer brands, handling tens of thousands of conversations a month across voice, chat, and email. Like almost every operation of its kind, quality assurance worked by sampling: a QA team you could fit around one table pulled conversations more or less at random, listened or read, and scored each one by hand against the client's scoring rubric. Sampling landed where sampling always lands: about one conversation in fifty. The other forty-nine were never read by anyone except the agent and the customer.

Think about what lives in the conversations nobody reads. The agent who quietly mishandles every cancellation request, and won't appear in a sample for weeks. The compliance disclosure a client contractually requires on every call — certified as "monitored" on the strength of a sample that thin. The new refund policy that half the floor misunderstood, invisible until the complaints arrive. Coaching built on a handful of random data points per agent per month. And feedback that lands weeks after the conversation happened, when neither the agent nor anyone else remembers the call.

Sampling was never a methodology. It was a compromise with the cost of human reading, and everyone in the industry has quietly agreed to pretend otherwise. For a BPO the stakes are doubled: quality scores are contractual, clients audit them, and a quality miss discovered by the client before the operator is how accounts get lost.

## What we built

We built a system that ingests every conversation across every channel, scores each one against the same rubric the analysts used, attaches cited evidence to every score, and turns the results into coaching digests for every agent and team — continuously, not quarterly.

The QA analysts did not disappear from this picture. They moved up a level. Instead of sampling conversations, they now audit the scorer: reviewing machine-scored conversations, catching disagreements, and refining the rubric until human and machine judgments converge. Sampling became calibration. It is the same expertise, pointed at a far more leveraged target.

<img src="motion/conversation-qa-full-coverage.svg" alt="Animated schematic: pulses travel the flow described above, pausing where a human decides." width="1200" height="630">

*Every conversation carries a pulse, not a sampled few. The loop underneath is calibration.*

## How it works

### Layer 1: Transcript ingestion across channels

Voice calls are transcribed with speaker separation, so the system knows who said what and when. Chat logs and email threads are normalized into the same canonical conversation format, because a scoring rubric shouldn't care which channel a conversation happened on. Each conversation is joined with its metadata — brand, agent, queue, handle time, outcome codes, customer satisfaction score where one exists — producing one clean, queryable record per conversation.

This layer sounds mundane and is anything but. Every downstream judgment inherits its quality from the transcript. Getting speaker attribution right, handling crosstalk, stitching a chat that dropped and resumed — this is the unglamorous engineering that decides whether the scores can be trusted at all.

### Layer 2: The rubric as code

Every client scorecard already existed — as a PDF written for human interpretation. "Agent demonstrates empathy." "Agent follows the identification procedure." Useful guidance for a trained analyst; useless as a specification.

We translated the client's scorecard — every criterion on it — into evaluable form: each one with a precise definition, explicit pass and fail conditions, worked examples, and documented edge cases, all agreed line by line with the QA team. The process surfaced ambiguities that had quietly caused analyst disagreement for years. What counts as a greeting on chat? Does empathy require specific phrasing or acknowledged emotion? Writing the rubric as code forced answers to questions the PDF allowed everyone to skip.

The rubric is versioned. When a client changes their scorecard, the criteria change deliberately, with a date and a diff — and every score records which rubric version produced it.

### Layer 3: Scoring with cited evidence

Every conversation is scored on every criterion — and no score is allowed to exist without evidence. A passing empathy score links to the exact utterance where the agent acknowledged the customer's frustration. A failed compliance criterion links to the precise moment in the call where the mandatory disclosure should have happened and didn't. Click the score, land on the moment.

This rule — no naked scores — is what makes the system auditable rather than oracular. An agent who disputes a score doesn't argue with a number; they look at the cited moment and the criterion definition, and the disagreement resolves in minutes. It is also what makes the scores actionable for compliance: a critical fail now pages a team lead within minutes of the conversation ending, with the evidence attached, instead of surfacing in a report weeks later.

### Layer 4: Coaching digests

Raw scores at full coverage would drown everyone. So the system distills them. Each agent gets a short weekly digest: what improved, the one recurring miss that matters most, and two or three cited examples from their own conversations to review. Team leads get the aggregate view — which criteria the team struggles with, which agents are trending down before it becomes a problem, which new policy is being fumbled across the whole floor rather than by one person.

Coaching conversations changed shape. They used to start from one sampled call and a debate about whether it was representative. They now start from a pattern across a month of an agent's actual work, with the receipts attached.

### Layer 5: Calibration — humans audit the scorer

Every week, the QA analysts review a slice of machine-scored conversations — a few hundred a month, deliberately weighted toward low-confidence scores and disputed ones. Where the analyst disagrees with the machine, the disagreement is logged and traced back: was the transcript wrong, was the criterion ambiguous, was the model wrong? Each root cause has a fix, and most fixes are rubric refinements that improve every future score.

The human role shifts from reading conversations to deciding whether the reader can be trusted. A handful of analysts sampling a sliver of the traffic could never see the operation. The same handful, calibrating a scorer that reads everything, effectively can.

## Why this generalizes

Any operation where conversations carry risk or coaching value has this same shape. Internal support teams that gave up on QA entirely because they never had analysts to begin with. Sales organizations that want every discovery call scored for methodology adherence and risky claims, not just the deals that closed. And regulated industries — collections, insurance, financial advice — where conversation monitoring is legally mandatory and sampling has always been an uncomfortable compromise that everyone hoped a regulator wouldn't examine too closely.

Anywhere humans review a sample because reviewing everything was impossible, the constraint has quietly disappeared. The rubric, the evidence discipline, and the calibration loop are what turn that raw capability into something an operation can actually run on.

## What's hiding in the forty-nine you never read?

Every sampled QA program is an admission that most of what your customers experience goes unexamined. We build scoring systems that read everything, cite their evidence, and keep your analysts in charge of the judging. Tell us.
