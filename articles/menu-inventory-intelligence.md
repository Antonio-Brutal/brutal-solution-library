# A Costing Engine That Knows Which Dishes Actually Make Money

> How we built recipe costing, waste attribution, and menu engineering for a multi-site restaurant group, and why the same approach matters for any business selling assembled goods at a fixed price.

![Flow diagram: supplier prices and inventory feed recipe costing while waste is attributed per dish; margin and popularity meet at a dish node, with recommendations passing a chef's approval](graphics/menu-inventory-intelligence.svg)

## The problem: the price is printed once, the cost moves every week

Most restaurant groups don't have a pricing problem. They have a *costing* problem.

Our customer runs dozens of sites across several cities under a handful of formats, from fast counters to full-service dining rooms. Hundreds of dishes, hundreds of ingredients, dozens of suppliers, deliveries most days of the week. The menu price is set once or twice a year and printed. Everything underneath it moves — a supplier reprices, a contract lapses, a seasonal item doubles, a distributor swaps a pack size and unit cost changes without anyone noticing.

The theoretical cost of every dish existed, in the way these things usually exist: a spreadsheet a chef built at some point, accurate the day it was written and quietly wrong ever since. Recipes drift. A dish gets a new garnish for a photo shoot and the garnish stays. Portioning varies between the kitchen that trained on the dish and the kitchen that learned it from a photo.

Waste was worse, because waste was a single number. Food cost came in over target, and the same conversation followed every month: it's waste, tighten up. But "waste" is at least five different things — trim and prep loss, spoilage, over-portioning, dishes comped or remade, and till errors that make sales look different from what left the pass. Each has a different cause and a different fix. Collapsed into one percentage, none of them is actionable.

So menu decisions got made on instinct and popularity, which is the trap. The best seller is not automatically the most profitable, and the slowest seller sometimes carries the margin. Cut the wrong dish and you remove the reason a table of four chose you. Keep the wrong one and you sell a loss enthusiastically, hundreds of times a week, across dozens of sites.

## What we built

We built an engine that costs every dish continuously, explains where food actually goes, and maps each dish by what it earns and how it sells — then hands the chef a short list of recommendations with the reasoning attached.

Recipes are modeled properly, down to sub-preparations and yields, so a change in one ingredient price flows through everything containing it within a day of the invoice landing. Inventory movements, deliveries, and till data are reconciled into a variance attributed to a cause, a site, and a shift rather than a group-level number. Every dish carries a live plate cost, a contribution margin, and its real sales pattern by site and daypart.

The output is proposals, never actions. The engine does not change a menu, does not change a price, does not place an order, and does not edit a recipe or its allergen specification. Menus belong to the executive chef, prices need finance approval, and orders are placed by people who know what is happening in their kitchen this week. The engine removes the guessing, not the deciding.

<video src="media/menu-inventory-intelligence.mp4" poster="media/menu-inventory-intelligence-poster.jpg" controls playsinline preload="none" width="1280" height="720"></video>

*Cost, waste and popularity meet at the dish, where a chef can actually act on them.*

## How it works

### Layer 1: Recipes that cost themselves

The foundation is a recipe model that reflects how kitchens actually work. A dish is not a flat list of ingredients; it is a tree. The dish contains a sauce, the sauce is a prep batch made twice a week, the batch contains a stock reduced from bones that arrive with a whole-animal delivery. Each level has a yield, and trim loss is a real cost that flat spreadsheets systematically hide.

Supplier invoices feed the bottom of that tree. Every line is matched to an ingredient and normalized to a costing unit, so a pack-size change or a supplier switch registers as what it is: a change in cost per kilogram, not an unexplained variance at month-end. When a price moves, everything above it recosts automatically, and every dish containing that ingredient shows a new plate cost with the invoice that caused it.

Kitchens can see the tree, and that matters more than it sounds. When a chef can point at the exact line where a dish got more expensive, costing stops being a finance instrument and becomes a kitchen tool.

### Layer 2: Waste attribution, not a waste percentage

This layer answers one question: what did we buy that we did not sell, and why. It computes theoretical usage from what was sold — every ticket exploded back into ingredients through the recipe tree — and compares it against actual usage from deliveries and counts. The gap is the variance.

Then the variance gets split. Prep waste and trim, logged at the bench. Spoilage, from expiry and stock-rotation records. Comps, voids, and remakes, which come from the till and are not kitchen waste at all — they are service recovery, and they belong in a different conversation. Over-portioning, which shows up as a persistent one-directional gap on a specific dish at a specific site. Everything left is unexplained, and the unexplained portion is reported honestly rather than spread across the named causes to make the model look complete.

Attribution runs by site, by shift, and by ingredient, which surfaces what a group-level number buries: one kitchen's portioning drifting on the highest-cost protein, one site's spoilage concentrated in items ordered on a fixed schedule regardless of forecast.

One design rule is explicit here. Variance is a question, not an accusation. The system reports patterns and never judges a person or a shift team — a spike on a Saturday night is a prompt to go and look, and the looking is done by a human who knows the fryer was down.

### Layer 3: Dish-level margin and popularity

With true cost on one axis and real sales on the other, every dish gets placed: what it contributes per plate, how often it sells, and how that varies by site, daypart, and season. This is where assumptions took their worst beating — dishes everyone was proud of contributed little, and unglamorous ones were quietly carrying whole sites.

The map is deliberately not a verdict. A dish that earns little may be the vegetarian option that makes a group of six choose you, or the anchor of a set menu that is profitable as a whole. So the engine shows the dish in context — what it sells alongside, which sites depend on it, what happened when it came off a menu before — and leaves the judgment where it belongs.

### Layer 4: Recommendations a chef accepts or rejects

The engine produces a short list, not a dashboard nobody opens. Each states the observation, the mechanism, and the options: this dish's margin has fallen since a specific ingredient repriced — reformulate, resize the portion, change supplier, adjust the price, or retire it.

Every recommendation goes to the executive chef, who accepts, rejects, or defers it. Price changes need finance sign-off on top of that. Rejections are as valuable as acceptances, because a rejection carries its reason: this dish is why people come; that supplier switch would fail our sourcing standard; that portion is the portion. Those reasons become constraints the engine respects afterwards, so the list gets sharper rather than more repetitive.

The boundary is architectural, not cultural. No menu, price, purchase order, or recipe changes without a named human approving it. The engine is very good at knowing what things cost. It knows nothing about what a restaurant is for.

## Why this generalizes

The shape is any business assembling physical inputs into a fixed-price product while its input costs move underneath it. Hotel and contract catering runs the same problem with tighter contracts and less room to maneuver. Bakery and coffee chains run it with fewer SKUs and far higher volume, where a few cents per unit decides the year. Food manufacturers run it as a bill of materials — different vocabulary, identical mechanics: yields, trim, substitutions, and a price list that never stops moving.

The pattern is the same. Cost the tree, not the plate. Attribute the variance instead of averaging it. Then put a short, explained list in front of the person who owns the decision.

## Do you know which of your dishes lose money?

If your recipe costing lives in a spreadsheet older than your current supplier list, your margin is being decided by invoices nobody has read. We build these engines to explain themselves, with every menu and price decision left to your chefs and your finance team. Tell us what your menu looks like.
