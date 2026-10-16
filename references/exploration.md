# Explore: visual divergence

## Step 1: extract constraints

Gather only what materially affects design:
- Product promise, audience, user task, tone, content hierarchy.
- Existing colors/brand/assets and what is **not** negotiable.
- Existing app framework if present.
- Inspirations and aversions (links or screenshots supplied by user).

Do not confuse a user's domain with its most common template. A developer tool does not have to look like every other developer SaaS.

## Step 2: derive concepts from metaphors

Form at least three **meaningfully different** concept briefs. Each brief contains:
- Short conceptual name.
- Metaphor sourced from the product story or user behavior.
- Mood and intended user perception.
- Composition and information hierarchy.
- Type system and interaction idea.
- What makes it recognizable.
- Main risk/trade-off.

Example for a travel-memory product:
- Field notes: handwritten marginalia, stamps, asymmetrical archival pages.
- Film contact sheet: frames, captions, dense sequences, dark room palette.
- Itinerary atlas: routes, coordinates, waypoints, cartographic hierarchy.

## Step 3: deliberate range

Produce 4–6 directions spread across an explicit expressiveness spectrum:
- 1–2 controlled, information-first.
- 2–3 expressive but plausible for production.
- 1 experimental / "go wild."

Concepts may share product copy but must differ in **at least three** of:
layout/composition; typographic voice; visual metaphor; graphic/photographic treatment; animation/interaction; hierarchy/navigation.

Do not output six near-identical centered hero sections with different backgrounds.

## Step 4: practical prototype requirements

- Each concept is a complete HTML file, runnable without bundling.
- Include meta viewport and sensible responsive CSS.
- Use real text that communicates a product; avoid lorem ipsum.
- Functional basic navigation/controls when displayed as interactive.
- Prefer self-contained CSS; declare external assets and rights.
- Any animation must respect prefers-reduced-motion.
- The hero and first meaningful content block must both demonstrate the concept.
- No credential, personal data, or production API calls.

## Step 5: compare honestly

Populate a gallery manifest (see state-schema.md), produce gallery with script, then inspect actual rendering.

For each concept explain: visual thesis, distinctiveness, clarity, mobile risk, implementation cost, and main drawback. These are observations, not numerical truth.

## Selection gate

Offer 1–2 questions at most: which candidate to fork, and whether to borrow named attributes from another. Pause if runtime supports human interaction.
