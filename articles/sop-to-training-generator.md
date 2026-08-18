# A Generator That Splits a 400-Page Manual Into Training Proportionate to the Job

> Food-hygiene law requires training commensurate with what each person actually does, which makes splitting a 400-page manual by role a legal act rather than a formatting choice.

![Flow diagram: a bound operating manual fans into role-mapped modules with assessments, and a currency loop regenerates affected modules whenever the underlying policy changes](graphics/sop-to-training-generator.svg)

## Four hundred pages, and a legal standard that says "commensurate with their work activity"

Four hundred pages of operating manual is an unsorted legal obligation. Until every procedure is assigned to the role that performs it, the network is carrying that obligation rather than discharging it.

Regulation (EC) No 852/2004, Annex II, Chapter XII requires food business operators to ensure that food handlers are supervised and instructed or trained in food hygiene matters commensurate with their work activity, and that those responsible for HACCP procedures have received adequate training. The wording is the point. The law names no certificate, no syllabus and no number of hours. It names proportionality to what the person actually does.

An inspector tests that standard by asking one member of staff about one task. A manual organised by system rather than by role is evidence of documentation, not evidence of training, and the gap between the two becomes visible only when somebody in an apron is asked a question nobody ever specifically taught them.

The franchise network we built this for spans several countries: hundreds of locations, most owner-operated, most of the frontline staff in their first job or their third this year. The manual is genuinely good, refined over two decades, and it answers almost every question a new employee will have. Almost nobody has opened it, because it was written for the network rather than for the nineteen-year-old on their first shift.

## Onboarding by oral tradition drifts one hire at a time

When the written standard is unreadable at the point of work, onboarding reverts to oral tradition, and oral tradition drifts one hire at a time. New starters learn from whoever is on shift, which means they learn that person's version: the shortcuts, the local habits, the step somebody dropped years ago because it seemed unnecessary.

Across hundreds of owner-operated locations that produces hundreds of dialects of one standard. Nobody is lying. Each retelling simply loses the part that looked least useful, which is frequently the part that exists for a legal reason.

Head office had tried the obvious fix and built modules by hand. The effort covered a handful of roles before it collapsed, because the moment a policy changes, every module touching it becomes quietly wrong. Training that ages badly is worse than no training, because staff learn to distrust all of it at once.

## Some of the manual mapped to no role, and some roles did not exist in every country

The mapping stage produced the uncomfortable surprise, before we had generated a single module. A substantial part of the manual mapped to no role at all: procedures nobody currently performs, standards written for an equipment generation since replaced, sections addressed to a head-office function that no longer exists. Another set of procedures mapped cleanly to a role that did not exist in two of the countries.

Nobody had been able to see either fact while the manual was a single document, because a four-hundred-page bound object presents as complete on weight alone. Only when every procedure must be assigned to a named role in a named country does the unassignable residue become countable, and that residue is a finding about the business rather than about the document.

The mechanics underneath are plain. The manual is decomposed into atomic units, each an individual procedure, policy, standard or safety rule anchored to its exact location in the source. Role definitions come from the operations team rather than from the model: shift lead, front of house, kitchen, opener, closer, franchise owner. The system proposes the mapping and an operations lead reviews it once per manual revision, moving any unit between roles. That review is where a person makes the judgement that matters most: who genuinely needs to know this.

<img src="motion/sop-to-training-generator.svg" alt="Animated schematic: pulses travel the flow described above, pausing where a human decides." width="1200" height="630">

*One manual, many roles. When the policy changes, the affected modules regenerate.*

## Questions built from decision points, not from paragraphs

A pass mark on the earliest version of the assessment proved that somebody could quote the manual back to us. It proved nothing else. Those questions were generated from the module prose, so they tested recall of phrasing, and staff who passed still got the task wrong on the floor, because a person can reproduce a clause on allergen segregation and still put the wrong tongs back in the wrong tray.

So we rewrote generation to work from the procedure's branch conditions instead. Every question now sits on a real decision point in the source procedure, with that procedure's other conditions supplied as the distractors. The allergen question is no longer "what does the policy state" but "a customer asks whether the sauce contains nuts and the prep sheet is missing, what do you do", and the wrong answers are the other branches the same procedure defines.

A candidate question with no branch behind it is discarded automatically. That rule costs volume and buys the only thing an assessment is for: evidence that the person chooses correctly when the choice appears.

## The gap list is the most valuable output, and nobody asked for it

When a role needs an answer the manual does not contain, the generator raises the gap rather than filling it. It does not supply plausible industry practice, because an unsourced instruction inserted into training is how a network acquires a standard nobody approved and cannot defend.

Each gap names the role, the task, the countries where it applies and the point in the workflow where the module would otherwise have to invent something. Collected, they are the things the network assumed everyone knew and never wrote down. Nobody asked for that list. It is now the output the operations team reads first, because every line on it is a place where the floor has already been improvising.

## Completion is evidence; certification is a signature

The system records completion and never competence, and that is a franchisor liability question as much as a training-law one.

Completion evidence is not certification. A training system may record that a named person was shown a specific version of a specific procedure and how they answered. It may not record that they are competent to perform it. Competence is attested by a qualified human, and a system that quietly converts the first into the second is manufacturing a legal record nobody signed.

A franchisor that certifies a franchisee's employees is asserting a degree of control over those employees that it spends considerable effort elsewhere denying, in a record that is written down and dated.

These limits are wired into the publish path rather than written into guidance. Modules covering food safety, workplace safety and alcohol service cannot be published by any path except a named compliance owner's approval. The system may not mark anyone as certified, may not decide which roles exist, may not fill a gap the manual leaves open, and may not publish any version of any module to any location without a named human approving that version.

## When the policy changes, we can name who was trained on the old version

Policy changes are made once, in the manual, and the currency loop is why the system does not rot. When a section is edited, the generator identifies every module and question derived from it, regenerates them, and produces a diff of what changed. An operations lead reviews that diff and approves the publish. Nothing reaches staff automatically.

On approval the network gets two things it never had. Updated training reaches the floor within days of a policy change rather than never, and head office can name which people, at which locations, still hold the superseded version.

That second list is what an inspection turns on. "We updated the manual" is a statement about a document. "These named people at these sites were shown this version of this procedure on these dates" is a statement about training, which is what the regulation asked for.

## Common questions

### Does this replace our food hygiene certification?

No. It records completion evidence: that a named person was shown a specific version of a specific procedure on a specific date, and how they answered the checks. Certification remains a signature from a qualified human trainer, as the law in these markets requires. The two records sit side by side and are deliberately never merged into one status field.

### What happens when the manual does not answer something a role needs?

The generator raises the gap instead of filling it. It will not supply industry-standard practice, because an unsourced instruction inside training becomes a standard the network never approved. The gap goes to the operations team naming the role, the task and the countries affected, and the module publishes without that section rather than with an invented one.

### Our manual is out of date in places. Does it have to be fixed first?

No, and the mapping stage is the fastest audit of it you will get. Our first run found a substantial part of the manual mapping to no role at all, and a set of procedures mapping to a role that did not exist in two countries. Neither was visible while the manual was one bound document.

### How quickly does training reflect a policy change?

Days rather than never, and the constraint is human review rather than generation. Editing the source section regenerates every module and question derived from it and produces a diff of what changed. An operations lead approves the publish. The system then names everyone still holding the superseded version, by person and by location.

## Is your training a document or a demonstration?

If your standards live in four hundred pages organised by system, your frontline training is oral tradition and your evidence of it is a signature on a page nobody read. We build these generators source-anchored, role-mapped and approval-gated, so what a person is shown is proportionate to what they do. Tell us what your onboarding looks like on a normal Monday.
