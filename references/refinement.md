# Refine: preserve options, sharpen intent

## Branch rather than overwrite

Give forks unique, stable IDs. Keep parent source unchanged.
- A fork should test a **single design hypothesis** or tightly related set.
- Generate 2–4 forks per round, not endless variants.
- Keep a concise change log and parent ID per fork.
- Do not quietly replace earlier screenshots or filenames.

Example: chosen `cinematic.html` →
`cinematic-r1-editorial.html`,
`cinematic-r2-motion.html`,
`cinematic-r3-map-hybrid.html`.

## Design tokens are an interface, not an afterthought

Expose meaningful parameters as CSS custom properties:
`--page-bg`, `--ink`, `--accent`, `--font-display`,
`--radius`, `--section-gap`.

Use `tokens.json` with token types:
- color: HTML color picker
- range: numeric slider with min/max/step and CSS unit
- select: list of CSS-ready values, e.g. font stacks
- text: editable string for safe user-set CSS variables

Call:

```bash
python3 PATH_TO_SKILL/scripts/create_playground.py --html variant.html --tokens tokens.json --out playground.html
```

The script generates a self-contained playground that renders the prototype in an iframe and lets the user update CSS properties live, export `tokens.json`, or export CSS overrides.

**Limitations:** Playground adjustments affect the preview only until exported and applied. CSS variables must already be referenced by the prototype. JavaScript-controlled rendering or external assets may need custom integration.

## Prefer rendered comparison over vague taste feedback

Compare candidates at target breakpoints using real browser tooling when available. Inspect:
- hierarchy, visual rhythm, typography density
- expressive concept coherence
- legibility and accessibility
- mobile composition and controls
- motion purpose vs distraction

Do not blindly maximize novelty: an internal operations dashboard needs faster scanning than a brand-forward marketing page.

## Record the user's choices

In `session.json`, record:
- chosen variant and parent
- accepted traits with *reasons*
- rejected traits with *reasons*
- any combination or direction change
- approval explicitly granted (boolean, exact variant ID, tokens path)

No global design preference database is required. Keep memory in the target project only.

## Approval gate

Ask: "Approve variant X and these token values for implementation?" Proceed only on explicit yes. If the user wants another iteration, continue with a new fork rather than changing the accepted source.
