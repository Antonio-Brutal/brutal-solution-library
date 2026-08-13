# An Ad Creative Engine That Learns From the Ads It Already Shipped

> How we built a closed-loop creative engine for a DTC consumer brand, and why the same approach matters for any business buying attention at scale.

![Flow diagram: a brand-constraint plate feeds a matrix of creative variants, performance returns are collected on the right, and a feedback rail carries what worked back to shape the next generation](graphics/ad-creative-iteration.svg)

## The problem: the bottleneck moved to creative, and nobody moved with it

Most performance teams don't have a media-buying problem. They have a *production* problem.

Our customer is a direct-to-consumer brand selling physical products into several European markets, buying across paid social, search, and a couple of marketplaces. Targeting and bidding, the two levers performance marketers used to spend their careers on, have largely been taken away by the platforms and handed to their own optimisation systems. What remains is creative. The ad itself — the hook, the format, the first two seconds — is now the main input the advertiser still controls, and the platforms consume it at a rate no small creative team can match.

The status quo was the obvious one. A concept gets written into a brief. A designer turns it around over a week or so. Three variants go live. Everyone watches the dashboard for a fortnight, then argues in a meeting about what won. Somebody writes a slide called "creative learnings Q3." That slide is read once.

The costs of that rhythm are structural, not cosmetic. Volume never matches demand: platforms reward fresh assets weekly, and the team shipped monthly. Fatigue is unreadable, because when an ad stops working the next version changes the hook and the format and the offer at once, so nobody can say which change mattered. And the learnings evaporate — they live in the head of whoever ran the account, and when that person moves on, the brand cheerfully re-briefs a hook it already proved doesn't work.

Underneath all of it sits one broken circuit. Performance data flows into dashboards that are used to allocate budget, and it never flows back into the brief. The loop is open. Everything downstream of that is a symptom.

## What we built

We built an engine that closes the loop. It generates ad variants inside the brand's own constraints, ships them as a deliberate matrix rather than a scatter of one-offs, reads platform performance back at the level of creative attributes rather than individual assets, and turns what it learns into the brief for the next generation.

We have written before about content engines that optimise themselves. This is the same thesis pointed at paid media, where the feedback arrives faster, lands harder, and comes with a price tag attached to every wrong answer.

The boundary was fixed on day one. The engine proposes; a performance marketer decides what ships. Claims belong to the people who own claims. And the machine never touches budget — it can tell you a hook is outperforming, but it cannot move a euro toward it.

<video src="media/ad-creative-iteration.mp4" poster="media/ad-creative-iteration-poster.jpg" controls playsinline preload="none" width="1280" height="720"></video>

*Variants go out, performance comes back, and the next round is shaped by what returned.*

*Concepts fan out into a matrix, results return along the lower rail, and the next batch is briefed by what came back.*

## How it works

### Layer 1: Brand and claim constraints, compiled

The brand's rules are encoded as a machine-readable constraint set rather than a PDF nobody opens: what the product is called and never called, the tone per market, the words that are off-limits, the disclosures each market requires, and the visual rules that make an ad recognisably this brand's.

The sharpest part of this layer is the claim library. Generation may only draw on claims the brand has already substantiated, either verbatim or within a paraphrase range legal has signed off. The model is not permitted to invent a benefit, quantify a result, or improve a claim by making it stronger — which is exactly what an unconstrained model will do, because stronger claims read better. Constraining at the input is cheaper and safer than policing the output, and it means the compliance conversation happens once, over a library, instead of ad by ad forever.

### Layer 2: The variant matrix

Variants are not produced by asking for ten more ads. They are produced against a matrix with explicit axes: the hook (problem-first, social proof, offer-led, curiosity, founder story), the format (static, short vertical video, carousel, creator-style), the market and language, and the offer being carried.

The matrix exists so the results mean something. A batch that changes hook, format, and offer at once can only teach you which whole ad won — never which decision won. Coverage is deliberate: the engine fills the cells that are thin, holds the other axes still, and produces enough of each cell to be readable. Every asset is stamped with its coordinates at the moment it is created, so the tagging that makes learning possible is structural rather than something retro-fitted into a spreadsheet six weeks later.

### Layer 3: Performance ingestion at attribute level

Spend, impressions, engagement, click-through, and conversions flow back from each platform onto the variant record they belong to. The trick is the join. Platforms report per asset; learning happens per attribute. Because every asset carries its coordinates, performance rolls up by hook, by format, by market, by offer — the dimensions a creative decision is actually made on.

Time matters as much as totals. The system keeps each asset's curve in flight rather than a lifetime average, because fatigue is a shape, not a number, and knowing that one format holds up for weeks while another decays within days changes how you plan a quarter. We are also blunt about attribution: platform-reported conversions are a directional signal, reconciled against the brand's own order data where the join is honest and clearly marked as platform-reported where it isn't. A learning loop fed by numbers the team privately distrusts is worse than no loop at all.

### Layer 4: Pattern extraction that writes the next brief

The roll-ups get turned into explicit, readable statements: this hook family carries in one market and not in another, this format decays quickly on cold audiences, offer-led openings win first impressions and lose on retargeting. Those statements become the generation brief for the next cycle, alongside a register of what has already been tried and retired — losing branches are archived, not deleted, so the brand stops rediscovering its own dead ends every time the team changes.

Restraint is designed into this layer. The system reports how much evidence sits behind each pattern and refuses to promote one on thin data. An ad with a handful of conversions is a rumour, and treating rumours as findings is how a closed loop confidently optimises itself into a corner.

### Layer 5: The approval gate, and what the machine never decides

Every batch arrives in front of a performance marketer with its reasoning attached: which pattern it came from, which cells it fills, what it is testing. Approve, edit, or kill. Nothing reaches a platform unapproved. Anything drawing on a regulated claim routes to whoever owns claims before it can ship, and that route has no bypass.

Three decisions stay permanently outside the machine. It does not allocate budget; it recommends, and a human moves the money. It does not choose positioning — the loop optimises within a strategy and has no business selecting one, because who the brand wants to be to its customers is not a metric. And every pattern it surfaces is a hypothesis until a human agrees it is a rule. The human role moves from producing creative to directing it: less time in the asset, more time deciding what is worth testing next.

## Why this generalizes

The shape is any business where creative volume, not media strategy, is the constraint, and where performance data comes back fast enough to teach you something.

Mobile app publishers live this most acutely — user-acquisition teams burn through creative faster than anyone, and their loop is already instrumented end to end. Online travel brands run it across seasons and routes, where the same offer needs a different hook in every market. B2B demand-gen teams run a slower version with longer feedback cycles and higher-value conversions, which makes the discipline about evidence thresholds matter more, not less.

In all of them the winning move is the same: stop treating creative as a series of campaigns and start treating it as a system that remembers.

## When did your ad creative last tell you something you didn't already believe?

If your creative learnings live in a quarterly slide and your best-performing hook is whatever your last agency happened to suggest, the loop isn't closed — you're producing, not learning. We build creative engines constraint-first, with approval before anything ships and budget decisions left where they belong. Tell us what you're running.
