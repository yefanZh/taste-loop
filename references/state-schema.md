# State and manifest formats

All paths are **relative to the target project**, unless invoking a script with an absolute path. Do not store secrets or credentials in state.

## `.taste-loop/session.json`

Suggested structure (the agent maintains this JSON; helper scripts do not change it):

```json
{
  "schema_version": 1,
  "phase": "refine",
  "brief": {
    "product": "Travel memories",
    "audience": "Couples",
    "constraints": ["responsive", "accessible"]
  },
  "concepts": [
    {"id": "a", "path": ".taste-loop/explore/field-notes.html", "idea": "Field notes"},
    {"id": "b", "path": ".taste-loop/explore/cinematic.html", "idea": "Film contact sheet"}
  ],
  "forks": [
    {"id": "b-r1", "parent_id": "b", "path": ".taste-loop/refine/cinematic-r1.html", "hypothesis": "Bolder editorial type"}
  ],
  "selected_id": "b-r1",
  "approval": {
    "approved": false,
    "variant_id": null,
    "tokens_path": null
  },
  "decisions": {
    "accepted": [{"trait": "film captions", "reason": "personal and memorable"}],
    "rejected": [{"trait": "heavy motion", "reason": "distracting on mobile"}]
  }
}
```

Valid phase values: `explore`, `refine`, `implement`, `complete`. A transition to implement requires `approval.approved: true` and an exact `variant_id`.

## Gallery manifest

Saved alongside concept files. The `path` for each variant is relative to the **manifest directory** and must stay inside it.

```json
{
  "title": "Travel journal directions",
  "description": "Choose one direction to refine",
  "variants": [
    {
      "id": "a",
      "name": "Field Notes",
      "path": "field-notes.html",
      "concept": "An editorial travel diary",
      "tradeoff": "Expressive, but denser on mobile",
      "tags": ["editorial", "warm"]
    },
    {
      "id": "b",
      "name": "Cinematic",
      "path": "cinematic.html",
      "concept": "Memories as frames",
      "tradeoff": "Requires strong photography",
      "tags": ["film", "immersive"]
    }
  ]
}
```

Run `create_gallery.py` to generate `gallery.html`. Gallery contains iframe previews and open-in-new-tab links.

## Playground tokens

```json
{
  "title": "Cinematic tokens",
  "tokens": [
    {"name": "Background", "variable": "--page-bg", "type": "color", "value": "#17171d"},
    {"name": "Spacing", "variable": "--section-gap", "type": "range", "value": "64", "min": 16, "max": 128, "step": 4, "unit": "px"},
    {"name": "Headline font", "variable": "--font-display", "type": "select", "value": "Georgia, serif", "options": ["Georgia, serif", "Arial, sans-serif"]}
  ]
}
```

All variables must use `--name` syntax. `color`, `range`, `select`, and `text` are supported. A range value is a *number string without its unit*. The playground uses `value + unit` when setting CSS. Exported JSON reflects current values; CSS export contains ready-to-paste `:root` overrides.

The playground is a **temporary tuning UI**, not an automatic rewrite of source or an asset/design editor.
