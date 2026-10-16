# Implement: carry the approved language into code

The approved HTML prototype is a **design specification**, not production architecture.

## Before modifying source

1. Verify explicit approval: selected variant ID and selected token values.
2. Inspect the repo: framework, route structure, components, design system, lockfiles, and tests.
3. Identify integration boundaries and sensitive pages/business logic.
4. Name expected files to change, and preserve the exploratory artifacts.

## Integration priorities

- Keep the strongest visual idea recognizable through layout and hierarchy.
- Extract reusable tokens (colors, type, space, radius, shadow, motion).
- Implement components in the application's existing framework and conventions.
- Use semantic headings, forms, landmarks, alt text, focus indicators.
- Avoid layout shifts, broken asset paths, unnecessary JS, and hydration issues.
- Respect reduced-motion preferences and test responsive navigation.
- Prefer genuine content and suitable assets to empty decorative placeholders.

## Validation

Perform available checks, recording which actually ran:
- lint/build/typecheck/test where configured
- interactive controls and keyboard navigation
- desktop and mobile rendering
- contrast and readable content
- missing links/images, overflow and focus states

When browser automation is available, take before/after screenshots and describe meaningful deviations. When not, flag visual verification as pending.

## Deliver

Summarize:
- implemented direction and chosen tokens
- specific paths changed
- screenshots / preview URL if actually generated
- checks passed, failed, or not run
- known differences from the approved prototype

Do not silently infer approval from "looks good" when ambiguous in context.
