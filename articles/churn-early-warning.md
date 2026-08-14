# A Churn Model That Learned the Wrong Lesson From a Price Rise

> Why our best-calibrated risk score was confidently wrong about an entire market, and what changed when we stopped asking one number to describe two unrelated processes.

![Flow diagram: product and billing signals feed a risk-scoring lattice that emits reason codes; each reason routes to a different save action, and outcomes return to retrain the selector](graphics/churn-early-warning.svg)

## An accurate score, wired to the one action that already existed

Our customer is a subscription media company operating across several European markets, with a subscriber base in the millions and a mix of monthly and annual plans, and they already had a churn dashboard. Monthly, with cohort curves and breakdowns by plan and tenure, accurate and well built, describing decisions that had finished weeks earlier. We built a score to catch those decisions while they were still forming.

A score fixes the timing and leaves everything else exactly where it was. It tells you who is at risk this week rather than which cohort decayed last quarter, but if the only action wired to it is the discount that already sits at the cancel door, an earlier score simply buys the same blunt thing sooner and hands money to people who were staying anyway.

Someone whose playback stutters on the living-room TV every evening does not want money off. Someone who opens the app, searches, finds nothing and closes it again wants to be shown the thing they would actually watch, which no score produces on its own.

Ours was well calibrated. It was also confidently wrong about a whole market.

## A price rise disturbs the SCA exemption, and the model learns the wrong lesson

The score flagged a large risk cohort that had decided nothing at all. Their renewals were failing because a price change had disturbed the payment path the subscriptions relied on, and the model was reading those failures as cancellations.

Under PSD2 strong customer authentication, the first payment of a recurring series is authenticated by the cardholder, and subsequent merchant-initiated transactions at a fixed amount ride an exemption path that does not require the subscriber to be present. Change the recurring amount and that assumption is disturbed. Issuers may soft-decline, or push an authentication challenge to a cardholder who is nowhere near the app, and the transaction fails on a card that is entirely valid.

What the model had actually learned was that a price change predicts a payment failure, not that a price change predicts a cancellation. Acting on it would have posted retention discounts to subscribers who wanted to keep paying us and needed a card re-authentication prompt instead, which is both expensive and slightly insulting in the same message.

We removed payment failures from the behavioural target entirely.

Involuntary churn is a payments event, not a retention event. The subscriber has made no decision, and the correct intervention is a credential update rather than an offer. Any churn model that includes failed payments in its target is estimating two unrelated processes with one number.

Involuntary churn now runs as a separate deterministic pipeline keyed on the decline code returned by the issuer. A do-not-honour, an insufficient-funds and an authentication-required decline call for three different messages sent on three different schedules, and none of the three is an offer.

## Six reason codes, because six families of response

The behavioural score carries a reason code from a deliberately short vocabulary: engagement decay, content fit, technical friction, price and value, seasonal pattern, and billing failure, which is raised by the payments pipeline rather than by the model. A hundred fine-grained reasons would be more faithful to the model and useless to the people acting on it.

Each code is a sentence a human can agree or disagree with, and each routes to a different family of response. That is the constraint that sets the length of the list: six responses, six codes, and no code without an owner.

The signals behind them come from product telemetry and billing, measured against each subscriber's own baseline rather than a global average. Someone who watches one evening a week has not disengaged; someone who watched five evenings and now watches one has. Content seasonality is modelled explicitly for the same reason: a subscriber who follows one returning series is waiting between seasons, not decaying, and a programme that cannot see the difference spends its budget on people who were never leaving.

<img src="motion/churn-early-warning.svg" alt="Animated schematic: pulses travel the flow described above, pausing where a human decides." width="1200" height="630">

*Risk surfaces with a reason code, and the reason decides which save action fires.*

## Risk tells you who is leaving; uplift tells you who stays because you acted

The action selector is trained to estimate uplift rather than risk, because those two questions have different answers. Risk ranks the people most likely to leave. Uplift estimates the people who stay because we did something, and the population that is both at risk and persuadable is much smaller than most retention programmes assume. The gap between the two is where the wasted spend lives.

The catalogue it chooses from holds actions of very different costs: a personalised surface of what to watch next, a heads-up that a followed series is returning, technical outreach with a device fix, a plan-fit suggestion such as annual billing or an ad-supported tier, a card-update prompt, a human callback for high-value subscribers, and, last and most constrained, a discount.

The model never composes an action. It selects from a catalogue that humans wrote and humans own, and adding an action, widening a discount band or opening a new segment to contact is a decision with a name attached to it. Discount depth and eligibility live in a policy layer set by the retention lead and finance, enforced outside the model and readable as plain text by anyone who asks.

## Doing nothing is a first-class action

Doing nothing sits in the catalogue as an option the selector picks frequently and deliberately, not as the absence of a decision. A programme that must always act will always find a reason to act, and the cost of that lands on the people who were happiest.

Some situations are removed from targeting altogether: an open complaint, a bereavement notification, an accessibility case. A save offer is the wrong thing to send into any of those, and the only reliable way to guarantee it is not sent is to make those subscribers invisible to the selector rather than to trust a rule further down the chain.

## The score changes the offer and never the exit

No risk score in this system alters the friction of leaving. It may change what we offer. It may never change what we obstruct, and no experiment is ever run on a slower cancellation path.

Germany makes the floor explicit. Since July 2022, section 312k BGB has obliged providers of continuing-obligation contracts to offer a clearly labelled cancellation button leading directly to a confirmation page, which bounds what a save flow is legally allowed to do. We hold the rule globally as an engineering constraint rather than as a German market configuration, because a rule that exists in one market's settings file will eventually be switched off in another by someone chasing a quarterly number.

## The holdout is permanent, not a launch experiment

A randomised holdout runs continuously inside every reason code, and a share of at-risk subscribers receives nothing at all. Without it, a retention programme takes credit for everyone who was never going to leave, which is the most common way these systems flatter themselves into irrelevance.

Outcomes are measured on retained tenure and value over months rather than on whether someone was still subscribed the following Tuesday. Discount actions carry cannibalisation tracking, so a save granted to someone who was never at risk shows up as the cost it is.

The retention lead reads the weekly outcome review and holds the pen on the catalogue. The selector may reweight among approved actions on its own evidence, and it may not write a new one.

## Common questions

### If failed payments come out of the churn model, where do they go?

Into a deterministic pipeline keyed on the issuer's decline code, with no scoring involved. Expiry and authentication-required declines get a credential-update prompt, insufficient-funds declines get retry scheduling around typical pay dates, and hard declines get a card-change request. Most recovery here is plumbing rather than persuasion, and mixing it into a behavioural model buries a problem a prompt solves outright.

### Isn't the cancel screen the cheapest place to intervene?

It is the latest place, which usually makes it the most expensive. By the time someone opens the cancel flow the decision is typically weeks old and the only remaining lever is price, so you pay full discount to people who had already decided and to people who never needed it. Earlier reasons admit cheaper answers, including answers that cost nothing.

### How do we know the programme works and is not just claiming credit?

The permanent holdout. A share of at-risk subscribers in every reason code receives no action, so retention is measured against a live counterfactual rather than against a pre-period or a hand-picked comparison group. Any programme without a holdout can only report the outcomes of people it chose to contact, which is not evidence of effect.

### Can we still test our cancellation flow?

You can test clarity, layout, wording and the accuracy of what is shown at cancellation, and you should. What is not on the table is testing friction: extra steps, hidden buttons, delays or a mandatory call. That boundary is enforced in the engineering rules rather than in a market configuration file, so it cannot be quietly relaxed later.

## What happens in your product in the three weeks before someone cancels?

If the honest answer is that nobody knows, the discount at the door is doing work that earlier signals could do more cheaply. We build early-warning systems that separate payments failures from decisions, name a reason with an owner, and prove their effect against a permanent holdout. Tell us what your cancel flow looks like today and what it is allowed to do.
