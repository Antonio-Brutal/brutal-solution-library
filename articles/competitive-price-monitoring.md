# A Price Monitoring Engine That Prices the Move Against the Next Thirty Days

> Why a tactical price match costs a European electronics retailer two things rather than one, and how we made the second cost visible before anyone approves the move.

![Flow diagram: competitor listings are clamped into matched pairs, unmatched ones held aside; matched lines pass a margin-aware recommendation stage bounded by a floor no line crosses, then a pricing-committee gate](graphics/competitive-price-monitoring.svg)

## Thirty days, not one afternoon: what a price cut actually costs

A price match you hold for three days governs what you may advertise for the next thirty. That is the number that reframes competitive pricing, and it is not a margin number.

Under the Omnibus Directive (EU) 2019/2161, which amends the Price Indication Directive 98/6/EC, any announced price reduction must state the prior price, and the prior price is defined as the lowest price the trader applied during at least the previous 30 days. Match a rival on Tuesday, restore the shelf price on Friday, and the discount you can lawfully announce three weeks later is measured from Tuesday's number rather than from the price the line sat at for most of the month.

Our customer sells consumer electronics across several European markets, with a catalogue in the tens of thousands of active SKUs: televisions, laptops, headphones, and the long tail of cables, mounts and chargers nobody writes a strategy for. Competitors reprice continuously and algorithmically; the retailer's own prices were revisited when a category manager had an afternoon free.

They were not flying blind. They had bought a monitoring tool and it produced alerts in quantity. An alert asserts that somebody is cheaper. It does not establish that the two listings are the same product, and it does not know that the line is earmarked for a headline offer in five weeks.

So the category managers did the work by hand: a spreadsheet export, a dozen browser tabs, hours confirming that the cheap listing really was the same box, and more hours discovering it was not. Moves got made where somebody had time to check, not where the money was.

## The same television is frequently not the same television

Matching absorbed more engineering than pricing did, because a comparison between two products that are not the same product is worse than no comparison at all. Manufacturers ship near-identical variants under names that differ by a single character. Retailers rename products for their own site search. A bundle hides a free soundbar inside a headline price. A marketplace seller with two units and no warranty is not the market.

The matcher runs several signals together: global trade item numbers where they exist and can be trusted, manufacturer part numbers including the regional suffixes that separate a model sold in one market from the identical-looking model sold in another, titles normalised against retailer decoration, specifications recovered from listing text and structured attributes and product images, and a distribution check, because a price far outside the observed range is usually a bad match rather than a bargain.

Every candidate match carries a confidence score and the evidence behind it. Confident matches enter the live map; ambiguous ones land in a category manager's queue as a side-by-side comparison showing which attributes agree and which do not. Those judgments train the matcher, so the queue shrinks as the catalogue grows. Variants and bundles are modelled as related listings with a stated difference rather than forced into a binary.

## What a price is, once you strip the page around it

The number printed on a product page is not the price, so the engine records the mechanics wrapped around it: delivery cost, whether the retailer or a third-party seller is behind the listing, stock status, and whether the number depends on a bundle, a cashback claim, a trade-in, a multibuy or a membership. A cheaper price on an out-of-stock line is not competition.

Everything is stored as history, which is what turns a feed into a picture: who moves first, who follows, which prices hold for months and which oscillate hourly. History is also what makes the thirty-day question answerable, because a rolling minimum cannot be reconstructed from a snapshot.

<img src="motion/competitive-price-monitoring.svg" alt="Animated schematic: pulses travel the flow described above, pausing where a human decides." width="1200" height="630">

*Matching the same product across retailers is the hard part. The price move is the easy part.*

*Listings converge into verified pairs, margin context joins the flow, and every move passes a human gate before it reaches the shelf edge.*

## The reference-price ledger we had to add after we lost a campaign

Same-day margin was the whole of the first recommender's arithmetic, unit margin before set against unit margin after, with a volume assumption attached. Every move it scored was judged as though the cost of a price cut ended the day it was made. It was correct, and it was blind.

Coming into a peak trading period, the promotions team found that the announceable discount on a block of accessory lines had collapsed. Dozens of small matches the engine had recommended over the preceding weeks had each reset that line's thirty-day low, and the campaign built on those lines no longer had a legal headline. The engine had recommended its way out of a campaign, one defensible move at a time.

We added a reference-price ledger, one per SKU per market, carrying the rolling thirty-day minimum applied price. It is a constraint inside the recommender rather than a report somebody reads afterwards, and the promotions calendar can declare blackout windows in which no competitive match may be recommended on a line earmarked for a headline offer. Every recommendation now carries two costs: margin per unit, and reference-price headroom consumed.

Reference-price debt is the advertised-discount headroom that a tactical price cut consumes. Because a promotional reduction must be announced against the lowest price applied in the preceding 30 days, a match made today reduces the discount that can lawfully be announced on that line for the next month, whether or not the margin recovers.

## Why we will not aim the engine at a named competitor

We refuse to build an automatic follower rule that targets a named competitor's price. Commercially, a rule like that makes you the reactive party in a spiral you have no mechanism to stop. Legally, automated alignment on an identified rival's price is the pattern competition authorities have already acted against in online retail, and we will not ship an architecture whose defence rests on nobody at the two companies ever having spoken to each other.

The engine recommends and the pricing committee decides. The committee can delegate a band of routine moves, defines that band in writing, and can revoke it in an afternoon. The delegated band is deliberately narrow and boring: small moves on accessory lines, inside the margin floor, on human-confirmed matches, outside any blackout window.

What the system may not decide is fixed in the architecture rather than in a policy document. It cannot set a price. It cannot cross a margin floor or touch a protected line. It cannot recommend a move on a match no human has confirmed, and it cannot recommend a move on a line the promotions calendar has closed.

## Do nothing, with a written reason, is a first-class output

"Do nothing" is a recommendation the engine produces deliberately, with its reasoning attached, and it is frequently the right one. A competitor undercutting you on a line where you hold the range, the stock and the service has told you something about their inventory position, not about your price.

The daily list is ordered by what the moves are worth rather than by how loud the alert was. Each entry shows the current price, the recommended price, what the relevant competitors have been doing and for how long, margin per unit before and after, reference-price headroom consumed, and a rationale written to be argued with. The committee approves, adjusts, or rejects with a reason, and the decision is recorded against the evidence that was on screen at the time.

That record is the most durable output of the system. When gross margin moves at the end of a quarter, the story is reconstructable move by move with a reason attached to each one, and pricing stops being folklore living in three people's memories.

## Common questions

### Can this reprice our catalogue automatically overnight?

Only inside a band your pricing committee writes and can withdraw the same day. The default is a recommendation a person approves. A competitor-triggered follower rule is something we decline to build: it makes you the reactive party in a price spiral, and automated alignment on a named rival's price attracts competition-law scrutiny.

### How is this different from the price monitoring tool we already pay for?

Monitoring tools tell you a competitor is cheaper. This tells you whether it is the same product, what the move does to unit margin, and how much advertised-discount headroom the move consumes under the thirty-day prior-price rule. The output is a short ranked list of decisions with reasoning, not a feed of alerts.

### What happens outside the EU, where the prior-price rule is different?

The ledger stays and the constraint changes shape. Jurisdictions outside the EU regulate reference pricing through advertising and consumer protection rules with different lookback periods and evidence standards. The engine holds a rolling minimum per market and applies each market's rule to it, so the same move can be free in one country and expensive in another.

### How long before the recommendations are worth acting on?

Matching quality decides that, not model tuning. Confident matches on well-identified categories are usable early; the long tail of accessories takes a few weeks of category managers confirming or rejecting queued comparisons. Reference-price ledgers need a month of collected history before the thirty-day floor is real rather than inferred.

## What did your last quarter of price moves actually cost you?

If you cannot answer that in margin and in advertised-discount headroom, you are running a pricing function on half its arithmetic. We build these engines matching-first and approval-first, with the promotional consequence of every move priced alongside the commercial one. Tell us what your catalogue and your promotional calendar look like.
