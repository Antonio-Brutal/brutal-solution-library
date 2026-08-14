# A Screening Engine That Measures Whether Its Human Oversight Is Real

> How we built high-volume candidate screening for a staffing agency placing industrial and logistics workers, and why the number we watch hardest is how often a hire comes from below the shortlist cut.

![Flow diagram: CVs are parsed and scored against recruiter-defined criteria with an audit trail citing every score; the recruiter decides who advances to interviews, and parse failures are flagged for human review](graphics/candidate-screening-engine.svg)

## A ranked list is a decision, whoever clicks the button

Nobody in high-volume recruiting builds a machine that rejects candidates, so the automated-decision debate is aimed at a system that does not exist. The real hazard is quieter. A reviewer works down a ranked list from the top, stops when the shifts are filled, and never reaches the evidence that would have changed the order. A human clicked every button. The sort made the decision.

Rank-position compliance is the tendency of a reviewer to act on the order a system produced rather than on the evidence behind it. It is the genuine automated-decision risk in screening, and unlike most fairness concerns it is directly measurable: the share of hires originating below the shortlist cut.

The agency we built this for places candidates into industrial and logistics roles: warehouse operators, forklift drivers, line technicians, delivery crews. Thousands of applications a month reach a recruiting team that can give each one a few seconds. The industry measures its skim in seconds rather than minutes, and that is a description rather than an exaggeration.

That skim leaves no record and produces nothing anyone could audit for fairness, which is the bar a screening system has to clear: more consistent than a tired glance, more accountable afterwards, and explicit about what it may never decide.

## There is no such thing as a forklift licence, and Driver CPC expires when nobody is looking

There is no statutory forklift licence in the United Kingdom. PUWER 1998 and the L117 approved code of practice require adequate training plus site-specific and truck-specific familiarisation, refresher intervals are guidance rather than expiry dates, and the certificate a candidate holds is issued by an accrediting body such as RTITB, ITSSAR, AITT or NPORS. Clients still write "valid forklift licence, in date" into the criteria, because that is how the yard talks.

A genuine expiry does exist, in the place recruiters rarely look. Driver CPC requires 35 hours of periodic training every five years under Directive 2003/59/EC, and it lapses independently of the vocational licence category, so a candidate can hold a perfectly valid category C entitlement and still be unlawful to place behind a wheel.

The phrase "RTITB counterbalance, 2019" on a CV is an accurate description of a real qualification, and the extractor we built first scored it badly against the criterion "valid forklift licence, in date". It was hunting for the word licence and an expiry date. Neither exists for that qualification, so candidates lost points for describing their certification correctly.

Criteria became typed objects with resolvers. A truck-category criterion resolves against accrediting-body names and category codes and asks whether refresher training is due; a driver-entitlement criterion checks the CPC cycle separately from the licence category. The client still writes the criterion in their own words, and the resolver decides what that phrase means in the paperwork that exists.

## The scorer was rewarding good writing, so we took the CV away from it

The second failure was harder to see, because nothing looked broken. Candidates with longer, better-written documents were outscoring candidates with identical evidence for the same criterion. The whole CV sat in context at scoring time, and prose quality was leaking into the judgement.

We split scoring in two. An extraction pass reads the document and pulls evidence spans for each criterion, recording where each was found. A scoring pass then sees only those spans and the criterion text, with the source document removed from context entirely. A scorer that cannot see the CV cannot be impressed by it.

Parsing failures never become silent rejections. Applications arrive as polished PDFs, ancient Word templates, photographs of paper CVs and job-board exports in several languages, and anything the parser cannot read confidently goes to a human queue. Someone who can drive a reach truck should not lose work to a formatting choice.

<img src="motion/candidate-screening-engine.svg" alt="Animated schematic: pulses travel the flow described above, pausing where a human decides." width="1200" height="630">

*Evidence lights the criteria that it supports. The ranking is visible, and the decision stays human.*

## Photographs and dates of birth never reach a model

CVs in several European markets routinely carry a photograph and a date of birth, and both are stripped at parse time, before any model sees the document. Nationality and marital status, where a template invites them, go the same way.

Under Annex III of the EU AI Act, a system used to filter applications and evaluate candidates sits in the high-risk employment category. Our design assumption is that everything this system does will one day be read back to us by somebody with a legitimate grievance, which changes what you are willing to store and what you are willing to infer.

Every score links to the spans that produced it, and a score of nothing shows what the system searched for and failed to find, which is the case a recruiter should check by hand. When a candidate, a client or a regulator asks why someone sat where they sat, the answer is retrievable per criterion.

No candidate is rejected by this system. It may not reject, may not remove anyone from view, and may not decide who is interviewed.

## Pull-up rate: how we test whether the human oversight is real

We measure the share of hires that originated below the shortlist cut, and we call it the pull-up rate. It is the honest test of whether human oversight is real, because oversight that never changes an outcome is indistinguishable from none.

The interface exists to make pull-ups cheap. Below-cut candidates sit one click away, ranked, with their evidence displayed and the criterion they missed named, so a recruiter can act on what the CV does not say: the depot is a short walk from an address the system read as a long commute.

When the pull-up rate flattens toward nothing over a sustained period, we treat it as a defect and go looking. Either the criteria are wrong, the evidence is too slow to read under time pressure, or the cut has quietly become the decision. None of the available fixes is to conclude that the ranking was right all along.

One decision rule before anyone builds anything: if you receive a handful of applications per role, do not. A written scorecard and a human reading every application beats a screening engine on fairness and on cost. This shape earns its place when applications arrive faster than qualified people can read them and somebody will eventually ask you to justify the order.

## The number we refuse to compute

We will not compute a single overall candidate score. A composite number is the artefact that gets pasted into a client email and becomes the decision, and it is unarguable in a way that per-criterion evidence is not. A recruiter can dispute "no evidence found for cold-storage experience" and win the argument with a line from page two. Nobody disputes a number out of a hundred.

We will not infer anything nobody asked for. No culture fit, no personality read, no seniority inferred from tone. Criteria come from the recruiters and the job spec, in plain language, and anyone who has to defend them can read and contest them. A criterion that turns out to be a proxy for something it should not be is a visible line in a configuration, which you can argue with and change.

What the agency receives per role is a ranked shortlist, per-criterion evidence for every candidate on and below it, and interview questions aimed at the gaps: a certification listed with no accrediting body named, or a break in dates after a logistics role. The interview is where a person's future gets decided, by a person.

## Common questions

### Our clients want one score out of a hundred. Why will you not produce it?

Because a composite score travels: pasted into an email, quoted in a meeting, treated as the decision, while the evidence behind it stays in the system. Per-criterion results travel too, and they can be argued with: a client can challenge a missing certification and be shown the line that answers it.

### Is a screening system like this high-risk under the EU AI Act?

Annex III places systems used to filter applications and evaluate candidates in the high-risk employment category, so plan for it from the first design meeting. In practice that means documented criteria, retained evidence behind every score, records of human decisions, and no inferred attributes. Your legal team owns the classification; we build so their answer is defensible.

### What happens to candidates who fall below the shortlist?

Nothing is discarded. They stay ranked and one click away, with their evidence and the criteria they missed on display, and recruiters pull them up regularly. We measure how often that happens, because a shortlist nobody reaches past is making the decisions. That measurement is a standing report, not a launch-day check.

### How do you handle certifications that have no expiry date?

By modelling the certification that exists rather than the one clients describe. A truck-category criterion resolves against accrediting-body names and category codes and asks whether refresher training is due. A driver entitlement checks the Driver CPC cycle separately from the licence category, since CPC lapses on its own schedule and makes an otherwise valid driver unlawful to place.

## Is your shortlist a recommendation, or is it the decision?

If nobody has hired from below the cut in months, the ranking is deciding and the review is ceremony. That is measurable this quarter, from data you already hold. Tell us how your shortlists get built, and we will tell you what to measure first.
