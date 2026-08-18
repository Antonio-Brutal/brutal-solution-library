# Two Funders Ask the Same Question, and Both Answers Are Correct

> Each grant agreement fixes its own indicator definitions, windows and exchange-rate rules, so this engine stores no converted figures and computes every reported number from raw records at render time.

![Flow diagram: programme data and field notes converge, then fan out through per-funder template mappings into drafted narratives whose figures remain traced back to source](graphics/funder-report-automation.svg)

## The warehouse with one true number, and why it lasted a single cycle

We built a warehouse holding one canonical figure per indicator, with each donor's report as a filtered view on top. Buried in that design is a claim about the world: that an indicator has one true value. The claim survived a single reporting cycle.

The nonprofit delivers programmes across a dozen countries on money from institutional donors, government agencies and private foundations. Every grant ends in a document: quarterly narratives, interim reports triggered by a milestone, final reports that release the last tranche. The material those documents need already exists, spread across a monitoring database, a finance ledger, and the field notes of the people who were there.

The warehouse broke not on counting but on money and dates. A training paid in local currency, invoiced across an eligibility boundary and converted once at the bank rate on the payment date, disagreed with the donor's mandated rate and with the finance ledger at the same time. Because we had stored the converted value rather than the transaction, we could not reproduce either figure.

That failure changed the primary object of the system. Two funders asking the same question about the same quarter are entitled to two different, equally correct numbers, because each grant agreement fixes its own indicator definition, eligibility window and currency convention. The number is not a stored value. It is a function evaluated from a contract against raw records.

## Means of verification: the provenance column donors already made you fill in

Every logframe obliges the grantee to declare a means of verification for each indicator, which means donors mandated a provenance column long before anyone called it data lineage. Attendance registers, signed training records, clinic registers, photographs of a delivered asset: the column exists, agreed, in the approved proposal.

Almost nobody populates it with anything actionable. It is completed once at design stage with a category name, and by reporting time the figure in the narrative has no link to the register that produced it. The obligation is discharged on paper and abandoned in practice.

We treated that column as the engine's output contract. Every figure in a draft carries the means of verification the grant agreement names, resolved down to actual records: which registers, over which dates, at which sites, entered by whom. Clicking the number opens the evidence. Nothing more elaborate was needed to make the reports auditable, because the donor had already specified what auditable meant.

## Two correct answers to how many people you reached

"People reached" is not one quantity, and an organisation reporting it as one is guessing which of its contracts it is breaching. One donor counts a person who attended a single session and another excludes them. One requires disaggregation by age band and district. One reports on the grant anniversary, another on the calendar year, a third on a fiscal year matching neither.

Donor definition of record: the version of an indicator's calculation, disaggregation, eligibility window and exchange-rate convention that one specific grant agreement fixes. Under it, people reached is not a quantity in the organisation, it is a quantity in a contract, and two donors asking for it in the same quarter are asking two different questions.

Indicator computations are therefore versioned definitions executed against raw participant records, not filters over a precomputed roll-up. When a donor revises its template mid-grant, the definition gains a new version with an effective date, and reports already submitted continue to reproduce under the version in force when they were signed.

We refuse to build the consolidated cross-donor beneficiary total that executives ask for on day one. Summing figures computed under incompatible contractual definitions does not produce a bigger truth. It produces a number that is wrong for every reader and defensible to none.

<img src="motion/funder-report-automation.svg" alt="Animated schematic: pulses travel the flow described above, pausing where a human decides." width="1200" height="630">

*Every funder wants it differently. The programme data underneath stays the same.*

## InforEuro, the eligibility boundary, and the conversion we should never have stored

European Commission grant agreements specify the conversion convention for costs incurred in other currencies, typically the InforEuro monthly accounting rate for the month of the expense rather than the bank rate on the date a payment cleared. Costs falling outside the eligibility period are ineligible regardless of when they were paid.

Those two rules together are why a stored converted amount is a liability rather than a convenience. Conversion depends on the month the cost was incurred, eligibility depends on the same date, and the bank rate that actually hit the account depends on treasury timing no donor cares about. One stored figure cannot satisfy the ledger and the grant agreement at once.

So we stopped storing converted amounts anywhere in the system. Every amount is held in its transaction currency with its transaction date, and conversion happens at render time under the requesting donor's stated convention. The reported figure travels with six things attached: source amount, currency, date, rate, rate source and result. Any reader can recompute it, and so can we, three years later, with an auditor in the room.

## Field notes are evidence, and three sentences stays three sentences

Numbers describe scale; field notes describe what happened, and they carry most of what a programme officer actually reads. Why attendance dipped in March. The partner clinic that lost its nurse. The equipment that never cleared customs.

The engine parses trip reports, monitoring visits and partner updates into discrete observations, each attached to an activity, a place and a date, each keeping a pointer to the passage and the author it came from. If a programme officer wrote three sentences about a flooded school, three sentences is what the layer holds and three sentences is what the narrative may use.

The drafting layer can only use what the evidence layer collected, and that constraint is the whole mechanism keeping the narrative honest. Where a template asks for something the record does not contain, the draft leaves an explicit gap naming what is missing and who would know. An unanswered question is a task. A fluent paragraph of nothing is a liability.

## Under-delivery reported is a conversation, under-delivery smoothed is a finding

The machine drafts and people attest. The programme lead signs the narrative, because the question there is whether this is a truthful account of what was done. Finance signs the figures against the accounts, because that is a different question with different failure modes. Both approvals attach to a specific document version, and nothing exports until both are in place.

The engine has no submission rights of any kind. It does not send anything to a donor, does not estimate a missing indicator, does not resolve a discrepancy between programme and finance systems on its own, and does not soften an unflattering result into gentler language.

Where two sources disagree, both values travel into the draft with the reason for the gap. A workshop invoiced in one month and delivered in the next is a timing difference rather than an error, and saying so before submission turns it into a conversation with a programme officer. Discovering it a year later, during an audit, turns it into a finding. Reported under-delivery costs one difficult call; smoothed under-delivery costs the grant.

## Common questions

### Can we get one total for people reached across all our donors?

Not from this engine, and the reason is contractual rather than technical. Each grant agreement fixes its own definition, eligibility window and disaggregation, so adding figures computed under incompatible rules produces a total that is wrong for every reader. We produce each donor's figure separately, each reproducible, each carrying the definition it was computed under.

### What happens when a donor changes its indicator definition mid-grant?

The definition gains a new version with an effective date. Reports drafted afterwards use the new version, while reports already signed continue to reproduce under the version in force when they were submitted. The grants team owns and edits those definitions directly, which matters when someone asks who decided what a number meant.

### How does it handle exchange rates across currencies?

Amounts are stored in the currency and on the date of the transaction and never converted at rest. Conversion happens when a report renders, under the convention that donor's agreement specifies, such as the InforEuro monthly accounting rate for the month of the expense. Every converted figure carries its source amount, date, rate and rate source.

### Does it write the narrative or only the numbers?

Both, but only from material staff already wrote. Field notes are parsed into dated observations tied to specific activities, and the narrative is assembled from those. Where the template asks for something nobody documented, the draft leaves a named gap rather than filling it, and the programme lead signs the result including any edits.

## Does reporting season pull your best people out of the field?

A quarter spent hunting figures across three systems, reconciling numbers that were never contractually meant to agree, is the price of storing figures instead of computing them. We build these engines so every reported number can be recomputed from raw records under the donor's own rules, years after submission, with its means of verification attached. Tell us what your donors ask for.
