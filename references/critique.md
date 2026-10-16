# Critique: review what the browser actually renders

Run this after explore, after each refine round, and after implementation. If no browser exists, explicitly label findings as static inspection.

## Review rubric

1. **Distinctiveness**: does the first screen have a coherent identifiable idea, not a default SaaS assemblage?
2. **Clarity**: can a new visitor understand what the product is, the primary action, and where to go?
3. **Coherence**: do iconography, imagery, sections, copy, interaction, and type all belong to the same visual world?
4. **Craft**: are spacing, alignment, contrast, scale, empty states, and responsive transitions intentional?
5. **Usability**: legible text, keyboard access, visible focus, navigable controls, appropriate touch targets, reduced motion.

## Visual review procedure

- Open every prototype in a real browser if available.
- Inspect at least desktop (around 1440px) and mobile (around 390px), plus tablet when meaningful.
- Capture comparable screenshots and compare variants with the same viewport and content.
- Identify the **most consequential** 3 improvements per candidate.
- Fix obvious clipping, contrast, overflow, missing assets, and broken interaction before user review.

## Common AI-pattern warning signs

These are possible symptoms, **not forbidden features**:
- A centered gradient hero plus three indistinguishable cards with no story.
- Repetitive rounded panels and interchangeable icon-label layouts.
- Uniform visual rhythm with no focal surprises or editorial decisions.
- Decorative motion that communicates nothing.
- All concepts using the same layout under different palettes.
- Ornamental complexity that weakens readability.

Ask "why is this here?" for each strong visual decision. If the answer is only "it looks modern", reconsider.

## Honest output

Report observable trade-offs, not fabricated scores. For example:
- "Concept A is clearest at narrow viewports but has the weakest visual signature."
- "Concept C's type-led hierarchy is distinctive; lower contrast on photo overlays needs work."

Do not claim "pixel-perfect", "WCAG compliant", or "tested" without performing the corresponding verification.
