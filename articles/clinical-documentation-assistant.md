# A Documentation Assistant That Drafts the Note and Waits for the Clinician

> How we built pre-visit summarization and structured note drafting for a physiotherapy clinic chain, and why the same approach matters for any practice where the record is a legal document.

![Flow diagram: intake and session capture feed a note drafted to the clinic template, which stops at a clinician sign-off node; no path continues into the record without it](graphics/clinical-documentation-assistant.svg)

## The problem: the note gets written twice, and the second time is at night

Most clinics don't have a documentation problem. They have a *re-entry* problem.

Our customer is a physiotherapy clinic chain running dozens of sites, with clinicians seeing patients back to back from early morning to early evening. Before each appointment, the information that would make the session better already exists. The patient filled in an intake questionnaire the night before. A referral letter arrived as a scanned PDF. Previous session notes sit in the record, written by three clinicians across two sites. Reading all of that properly takes longer than the gap between two appointments.

So clinicians do what clinicians everywhere do. They skim the top of the intake form, rely on memory and a two-line handover, and promise themselves they will read the referral later. Then the session runs, and the note has to be written. Typing during the session means looking at a screen while a patient describes their pain — bad care, and bad data, because you capture what is easy to type rather than what matters. Typing afterwards means competing with the next patient, already in the waiting room. So the notes pile up and get written in the evening, from memory, hours after the thing they describe.

Everything about that is expensive. Detail decays fast; a note written at nine at night is a summary of a summary. Structure drifts, because a tired clinician writes the shortest note that will pass, and the fields that matter for continuity and for reimbursement are the first to collapse into "as before, progressing well." And the clinicians themselves — the scarce, hard-to-hire resource the entire business runs on — spend the tail of every working day doing data entry.

## What we built

We built an assistant that does the reading and the typing, and nothing else.

Before the appointment, it reads the intake questionnaire, the referral, and the previous notes, and produces a short pre-visit summary the clinician can absorb in the time it takes to walk from the door to the treatment table. During the session, with the patient's consent, it captures what is said. Afterwards, it drafts a structured note into the clinic's own template — same fields, same order, same vocabulary — and puts that draft in front of the clinician for review.

Then it stops. The draft is not a record. It is a proposal, sitting in a holding area outside the patient file, and it stays there until a named clinician reads it, edits whatever needs editing, and signs it. Nothing the system produces enters the medical record without that signature. The system does not diagnose, does not grade severity, does not suggest a treatment plan, and does not decide what happens next. It writes down what the clinician did and said, in the format the clinic requires, and waits.

<video src="media/clinical-documentation-assistant.mp4" poster="media/clinical-documentation-assistant-poster.jpg" controls playsinline preload="none" width="1280" height="720"></video>

*The note is drafted from the session. Nothing reaches the record without the clinician.*

## How it works

### Layer 1: The data boundary, drawn before anything else

We designed the data handling before we designed a single feature, because in a clinical setting that ordering is the whole difference between a system a clinic can adopt and one its legal counsel will refuse.

The rules are architectural, not policy documents. Patient data stays inside the clinic's own processing environment. Recordings are transient — captured, transcribed, destroyed on a fixed schedule, never accumulated into a corpus. Nothing patient-identifiable trains a model. Access follows the same clinical need-to-know rules the record system already enforces, so the assistant cannot show a clinician anything they could not open themselves. Consent is captured per session and genuinely revocable: withdraw it and capture stops, the audio goes, and the clinician writes the note the old way with no penalty.

Every one of those constraints is enforced in the pipeline, not in a training slide. That is why this is Layer 1 and not an appendix.

### Layer 2: Pre-visit intake summarization

The pre-visit summary is short by design — a clinician reading a screen for ninety seconds is not going to read a page. It pulls together the intake form, the referral, and previous sessions, and surfaces the handful of things that change how the next thirty minutes should go: mechanism of injury, the reported pain pattern, current medication and relevant history, what was tried last time and how the patient responded.

Every line is traceable. Tap a statement and you see its source — this sentence from the intake form, that one from the referral letter, this from a note written three weeks ago. The assistant does not interpret the clinical picture and does not flag concerns; it assembles what is already on file so the clinician arrives having read it, rather than intending to.

### Layer 3: In-session capture that doesn't compete with the patient

Capture runs in the background, with visible consent and an obvious stop. There is no screen to look at, nothing to click, no prompts, no live suggestions — a clinician glancing at a monitor mid-session is precisely the behavior we set out to remove. The assistant is a passive listener, and the session belongs to the two people in the room.

Clinicians can mark the record verbally, the way they already talk during a session. Stating what they are testing, what they observe, and what the patient reports is normal practice; it also gives the drafting layer clean anchors to build a structured note around. The best capture, it turns out, asks clinicians to change almost nothing about how they work.

### Layer 4: Structured drafting into the clinic's own template

A generic clinical summary is useless to this business. The note has to land in the clinic's template, with its fields, in its house vocabulary, at the length its auditors and insurers expect.

So the drafting layer maps the session onto that template field by field: subjective report, objective findings as stated by the clinician, treatment delivered, patient response, plan as the clinician described it. Where a field has no support in the session, the draft leaves it empty and says so. It never smooths a gap over with plausible clinical language — an invented range of motion is far worse than a blank one, because a blank field asks a question and a fluent one closes it. Measurements and exercise prescriptions carry through verbatim, or not at all.

### Layer 5: Sign-off, and what the machine may not decide

The review screen shows three things: the draft, the source of each statement, and the fields left blank. The clinician edits freely and signs. The signature is attributable and timestamped — the record shows a human author who takes responsibility for the content, with the assistant's involvement logged behind it.

Unsigned drafts expire rather than linger. There is no bulk approve, because a bulk approve button is how sign-off quietly becomes a formality. And the boundary is enforced in the system, not merely discouraged: the assistant does not write a diagnosis, does not propose or alter a treatment plan, does not modify a signed note, and does not push anything to a patient, a referrer, or an insurer. Every edit is retained, because edits show exactly where the drafting is weak.

## Why this generalizes

The shape is any practice where a qualified professional produces a regulated record as a byproduct of skilled work with a person in front of them. Dental groups have this problem with an even more rigid chart structure. Veterinary chains have it with a talkative owner and a patient who says nothing. Occupational health and community care providers have it with the added burden that their notes go to third parties who each want a different format.

In every case, the same division of labor holds. The machine reads what already exists and writes down what happened. The clinician decides what it means, what to do about it, and whether the record is true. That last decision is not a checkbox on the way to automation. It is the point.

## Are your clinicians writing notes at nine at night?

If the people you hired for their clinical judgment are spending the end of every day on data entry, the documentation is the bottleneck — not the caseload. We build these systems boundary-first: patient data handled as an architectural constraint, and no note in the record without a clinician's signature. Tell us what your template looks like.
