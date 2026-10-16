---
name: taste-loop
description: Explore, compare, refine, and implement distinctive website and UI designs with visual forks, human approval, project-scoped design memory, an HTML comparison gallery, and a live token playground. Use when asked to design or redesign a landing page, homepage, product website, dashboard, or frontend that should feel intentional instead of generic.
---

# Taste Loop

**Premise:** Generate possibilities cheaply; spend judgment carefully. A good outcome is not the first rendered page. It is a coherent, distinctive direction chosen after comparison.

## When to invoke

Use this skill for visual identity exploration, website/UI redesign, design-system direction, or requests such as "make it feel less AI-generated". For a bug fix or small isolated CSS change, do not launch an entire exploration unless requested.

## Modes

- **explore**: generate distinct standalone HTML prototypes and a comparison gallery.
- **refine**: fork the selected direction, review screenshots, add a live design-token playground.
- **implement**: integrate the explicitly approved result into the real application.

If the user did not name a mode, start in **explore**. If an approved design is already recorded, ask only when a genuinely new decision is required.

## Read when needed

- Creative direction and nontrivial alternatives: [references/exploration.md](references/exploration.md)
- Forking, playground, and state transitions: [references/refinement.md](references/refinement.md)
- Visual review and quality checks: [references/critique.md](references/critique.md)
- Framework integration and acceptance: [references/implementation.md](references/implementation.md)
- JSON formats and paths: [references/state-schema.md](references/state-schema.md)

## Non-negotiable rules

1. Inspect the existing project before designing: framework, established branding, target audience, accessibility constraints, and content. Do not overwrite a coherent existing identity to chase novelty.
2. **Diverge structurally**, not just by swapping colors. Vary at least three among composition, type hierarchy, visual metaphor, media treatment, navigation, motion, and content storytelling.
3. Create *real, inspectable HTML pages* in an isolated directory. Screenshots and textual descriptions alone are not a substitute.
4. Preserve originals and previous forks. Use new files, never silently rewrite an approved or previously reviewed variant.
5. Do not touch production UI before the user has explicitly selected and approved the direction for implementation.
6. Use the browser to inspect desktop/mobile renderings when browser tooling is available. Never claim visual validation unless you actually rendered/inspected them.
7. Treat references as inspiration, not a license to copy layouts, artwork, logos, or code verbatim. Avoid licensing and attribution surprises.
8. Aesthetic heuristics are suggestions, not bans: gradients, cards, glass effects, and popular fonts are fine when they serve the concept.
9. Ask for decisions at the two key gates, **selection** and **approval**. If the agent runtime cannot pause, stop and report exact next actions; don't assume consent.
10. Keep a project-local design history. Never elevate one project's preferences into universal taste.

## Directory contract in target project

```text
.taste-loop/
  session.json
  explore/
    manifest.json
    concept-a.html
    concept-b.html
    ...
    gallery.html
  refine/
    concept-b-r1.html
    concept-b-r2.html
    tokens.json
    playground.html
```

Respect existing files. If a session already exists, continue it instead of resetting history. Existing application source code stays untouched until implementation.

## Phase A: Explore

1. Discover constraints: product purpose, target users, content, technical constraints, existing brand, design references. Make minimal assumptions when details are missing and label them.
2. Generate three concept briefs with **different metaphors** and intended emotional effects. Avoid generic names such as "Modern", "Clean", and "Premium" as your only distinction.
3. Produce 4–6 standalone, runnable HTML prototypes, including at least one intentionally unconventional option. Use believable product copy and basic mobile adaptation.
4. Write `.taste-loop/explore/manifest.json` in the [state schema](references/state-schema.md). Generate gallery:

   ```bash
   python3 PATH_TO_SKILL/scripts/create_gallery.py \
     --manifest .taste-loop/explore/manifest.json \
     --out .taste-loop/explore/gallery.html
   ```

5. Render actual prototypes, visually review, and summarize **trade-offs**: what makes each different, what it sacrifices, and fit for the product.

**STOP:** Present gallery location and ask the user to choose a concept (or combine explicitly named elements). Do not declare a winner on the user's behalf.

## Phase B: Refine

1. Read current `session.json`; branch from the selected prototype, not from an unrelated fresh design.
2. Generate 2–4 forks with **hypotheses**, e.g. "stronger editorial typography" or "more expressive navigation." Copy the selected file to new paths before editing.
3. Introduce CSS custom properties for visible design knobs. Define editable tokens in `tokens.json`.
4. Generate a standalone token playground:

   ```bash
   python3 PATH_TO_SKILL/scripts/create_playground.py \
     --html .taste-loop/refine/concept-b-r2.html \
     --tokens .taste-loop/refine/tokens.json \
     --out .taste-loop/refine/playground.html
   ```

5. Record selected/rejected decisions, version lineage, and reasoning in project-scoped `session.json`. Apply saved token values to the chosen prototype before final approval: the playground only previews and exports changes.

**STOP:** Ask for explicit approval of the exact variant and tokens before integration.

## Phase C: Implement

1. Inspect app structure, dependencies, design conventions, routing, responsiveness, and tests.
2. Extract design tokens, components, media needs, motion behaviors, and content model from approved prototype.
3. Integrate into the framework already used (Vue, React, etc.). Protect business logic and app routes. Prefer incremental changes.
4. Validate at desktop and mobile, functional interactions, keyboard navigation, reduced-motion support, and performance risks.
5. Report files modified, checks actually run, and remaining differences from prototype. Do not report success for unrun checks.

## Design memory

Maintain `.taste-loop/session.json` with a schema version, phase, concepts, forks, selection, approval, and `accepted` / `rejected` decision notes. Decisions are **contextual observations**, not rigid filters. Prefer recording why a decision was made.

## Recovery

- If the agent cannot create files or run commands, provide the concept briefs and file contents, clearly flagging that the gallery was not generated.
- If browser tools are unavailable, provide the local gallery and explicitly mark visual checks as **not performed**.
- If a user requests implementation before exploration, honor it, but seek approval of a proposed visual direction before modifying established UI.
