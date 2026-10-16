# Taste Loop

**Explore before you implement.** A design-exploration skill for coding agents such as Claude Code and Codex.

Taste Loop turns "make my website look less AI-generated" into a repeatable workflow:

**Explore → Compare → Refine → Approve → Implement**

Instead of producing one generic page and polishing it endlessly, the agent generates meaningfully different HTML prototypes, lets you compare them in a gallery, forks your favorite, and only touches the production app after explicit approval.

## What is included

- `SKILL.md`: agent instructions, phase boundaries, and safety rules.
- `references/`: creative exploration, critique, refinement, implementation, and state conventions.
- `scripts/create_gallery.py`: generates a multi-variant HTML comparison gallery from a JSON manifest.
- `scripts/create_playground.py`: generates an interactive design-token editor for a standalone HTML prototype.
- `examples/travel-journal/`: working sample prototypes, manifest, and tokens.
- `tests/`: standard-library smoke tests.

**No Node packages or Python dependencies are required** for the helper scripts (Python 3.9+). A browser is required to view the generated pages.

## Quick start

```bash
git clone https://github.com/yefanZh/taste-loop.git
cd taste-loop

python3 scripts/create_gallery.py \
  --manifest examples/travel-journal/manifest.json \
  --out examples/travel-journal/gallery.html

python3 scripts/create_playground.py \
  --html examples/travel-journal/cinematic.html \
  --tokens examples/travel-journal/tokens.json \
  --out examples/travel-journal/playground.html

python3 -m unittest discover -s tests -v
```

Open `examples/travel-journal/gallery.html` and `playground.html` in your browser. If file-URL restrictions affect an asset, serve the directory with `python3 -m http.server 8000`.

## Install as an agent skill

**Claude Code:** Copy the skill directory into `~/.claude/skills/taste-loop/` (or `.claude/skills/taste-loop/` for one project).

**Codex:** Copy the directory into `~/.agents/skills/taste-loop/` (or use your Codex installation's configured skills directory).

Keep `SKILL.md`, `references/`, and `scripts/` together. Alternatively, point your agent at this repo's `SKILL.md` when invoking it.

Prompt example:

> Use taste-loop to explore a distinctive homepage for my travel journal. Generate four visually different prototypes and a comparison gallery. Do not touch the production app until I choose a design.

For an existing application:

> Use taste-loop in refine mode on the selected prototype. Fork three variations; preserve the original. Add a playground for colors, typography, and spacing.

## Expected workflow

1. **Explore:** inspect constraints, pick visual metaphors, make 4–6 standalone prototypes.
2. **Compare:** create a gallery and show actual rendered pages, not just descriptions.
3. **Refine:** preserve forks, record design decisions, create a live token playground.
4. **Approve:** explicitly obtain the user's final design choice.
5. **Implement:** translate the approved direction into the existing framework; validate responsive behavior.

Generated exploratory files should live under `.taste-loop/` in the target project, not in production source directories. This repository's `examples/` is only a demonstration.

## Design memory

The agent records project-scoped preferences in `.taste-loop/session.json`. Accepted and rejected choices are evidence for future branches, **not** global rules like "never use gradients."

## Scope and limitations

This is a workflow skill plus local tooling, not an autonomous aesthetic judge. Browser screenshot inspection is recommended when the agent has browser tooling; the scripts do not run a browser, generate visual designs using AI, or automatically modify Vue/React projects. The human approves visual decisions.

Inspired by the design-exploration process described in [How I vibe-coded a website that doesn't look AI-generated](https://railcode.dev/blog/vibe-coded-website). Taste Loop is an independent project.

