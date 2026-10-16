#!/usr/bin/env python3
"""Generate a standalone comparison gallery from a Taste Loop manifest."""
import argparse
import html
import json
import os
from pathlib import Path
from urllib.parse import quote


def h(value):
    return html.escape(str(value), quote=True)


def load_manifest(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("variants"), list):
        raise ValueError("Manifest must contain a variants array")
    if not 1 <= len(data["variants"]) <= 24:
        raise ValueError("Manifest must contain 1 to 24 variants")
    return data


def safe_variant_path(manifest_dir, value):
    if not isinstance(value, str) or not value or "://" in value:
        raise ValueError("Variant path must be a local relative HTML file")
    raw = Path(value)
    if raw.is_absolute():
        raise ValueError("Absolute variant paths are not allowed")
    resolved = (manifest_dir / raw).resolve()
    try:
        resolved.relative_to(manifest_dir)
    except ValueError as exc:
        raise ValueError("Variant path escapes the manifest directory") from exc
    if resolved.suffix.lower() not in (".html", ".htm") or not resolved.is_file():
        raise ValueError("Missing local HTML variant: " + value)
    return resolved


CSS = """
:root{color-scheme:dark;--bg:#0e1119;--panel:#171c27;--line:#303745;--ink:#f3f6fb;--muted:#abb4c3;--accent:#a4ffca}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,-apple-system,sans-serif}
header{padding:30px max(24px,4vw) 18px;border-bottom:1px solid var(--line)}
.eyebrow{text-transform:uppercase;letter-spacing:.18em;color:var(--accent);font-weight:700;font-size:.72rem}
h1{font-size:clamp(2rem,4vw,3.1rem);letter-spacing:-.04em;line-height:1.1;margin:10px 0}
.sub{color:var(--muted);max-width:66ch;margin:0}.toolbar{display:flex;gap:10px;flex-wrap:wrap;align-items:center;padding:18px max(24px,4vw)}
input,select,button{background:var(--panel);border:1px solid var(--line);color:var(--ink);padding:10px 12px;border-radius:10px;font:inherit}
input{min-width:220px;flex:1}button{cursor:pointer}button[aria-pressed=true]{border-color:var(--accent);color:var(--accent)}
#count{color:var(--muted);margin-left:auto}.gallery{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,480px),1fr));gap:20px;padding:0 max(24px,4vw) 48px}
.candidate{background:var(--panel);border:1px solid var(--line);border-radius:16px;overflow:hidden;min-width:0}
.candidate[hidden]{display:none}.cardhead{padding:17px 18px;display:flex;justify-content:space-between;gap:12px}
.cardhead h2{margin:0;font-size:1.3rem}.id{color:var(--accent);font-size:.7rem;text-transform:uppercase;letter-spacing:.14em}
.open{color:var(--accent);text-decoration:none;font-weight:650;white-space:nowrap}
.framewrap{height:410px;background:#fff;overflow:auto;display:flex;justify-content:center}
iframe{width:100%;min-width:0;height:100%;border:0;background:#fff;transition:width .2s}
body.mobile iframe{width:390px;flex:none}body.mobile .framewrap{background:#333d4d}
.foot{padding:16px 18px;border-top:1px solid var(--line)}
.foot p{margin:0 0 8px}.trade{color:var(--muted);font-size:.92rem}
.tags{display:flex;gap:6px;flex-wrap:wrap;margin-top:10px}.tag{border:1px solid var(--line);border-radius:20px;padding:2px 8px;font-size:.75rem;color:var(--muted)}
@media(max-width:600px){header{padding-top:24px}.gallery{grid-template-columns:minmax(0,1fr)}.framewrap{height:350px}#count{margin-left:0}}
"""

SCRIPT = """
const search = document.getElementById('search');
const tag = document.getElementById('tag');
const cards = [...document.querySelectorAll('.candidate')];
function filterCards() {
  const needle = search.value.toLocaleLowerCase().trim();
  const selected = tag.value;
  let visible = 0;
  cards.forEach(card => {
    const match = card.dataset.search.includes(needle) &&
      (!selected || card.dataset.tags.split('|').includes(selected));
    card.hidden = !match;
    if (match) visible++;
  });
  document.getElementById('count').textContent = visible + ' / ' + cards.length + ' concepts';
}
search.addEventListener('input', filterCards);
tag.addEventListener('change', filterCards);
document.querySelectorAll('[data-viewport]').forEach(button => {
  button.addEventListener('click', () => {
    document.body.classList.toggle('mobile', button.dataset.viewport === 'mobile');
    document.querySelectorAll('[data-viewport]').forEach(other => {
      other.setAttribute('aria-pressed', String(other === button));
    });
  });
});
filterCards();
"""


def render(manifest, manifest_path, output_path):
    manifest_dir = manifest_path.parent.resolve()
    out_dir = output_path.parent.resolve()
    cards = []
    tags = set()
    seen = set()
    for entry in manifest["variants"]:
        if not isinstance(entry, dict):
            raise ValueError("Each variant must be an object")
        vid = entry.get("id")
        name = entry.get("name")
        if not isinstance(vid, str) or not vid or vid in seen:
            raise ValueError("Each variant needs a unique nonempty string id")
        if not isinstance(name, str) or not name:
            raise ValueError("Each variant needs a nonempty name")
        seen.add(vid)
        source = safe_variant_path(manifest_dir, entry.get("path"))
        href = quote(Path(os.path.relpath(source, out_dir)).as_posix(), safe="/.-_")
        raw_tags = entry.get("tags", [])
        if not isinstance(raw_tags, list) or any(not isinstance(t, str) for t in raw_tags):
            raise ValueError("tags must be a string array")
        tags.update(raw_tags)
        concept = str(entry.get("concept", ""))
        tradeoff = str(entry.get("tradeoff", ""))
        search_text = " ".join((name, vid, concept, tradeoff, *raw_tags)).lower()
        chips = "".join('<span class="tag">' + h(t) + '</span>' for t in raw_tags)
        cards.append(
            '<article class="candidate" data-search="' + h(search_text) +
            '" data-tags="' + h("|".join(raw_tags)) + '">' +
            '<div class="cardhead"><div><div class="id">Variant ' + h(vid) +
            '</div><h2>' + h(name) + '</h2></div>' +
            '<a class="open" href="' + h(href) +
            '" target="_blank" rel="noopener noreferrer">Open ↗</a></div>' +
            '<div class="framewrap"><iframe loading="lazy" title="' + h(name) +
            ' preview" src="' + h(href) + '"></iframe></div>' +
            '<div class="foot"><p>' + h(concept) + '</p>' +
            '<div class="trade">' + h(tradeoff) + '</div>' +
            '<div class="tags">' + chips + '</div></div></article>'
        )
    options = ['<option value="">All tags</option>'] + [
        '<option value="' + h(t) + '">' + h(t) + '</option>' for t in sorted(tags)
    ]
    title = h(manifest.get("title", "Taste Loop Gallery"))
    desc = h(manifest.get("description", "Compare real HTML prototypes."))
    page = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title><style>__CSS__</style></head><body>
<header><div class="eyebrow">Taste Loop / Design exploration</div><h1>__TITLE__</h1>
<p class="sub">__DESC__</p></header>
<div class="toolbar"><input id="search" type="search" aria-label="Search concepts" placeholder="Search concepts...">
<select id="tag" aria-label="Filter by tag">__OPTIONS__</select>
<button data-viewport="desktop" aria-pressed="true">Desktop</button>
<button data-viewport="mobile" aria-pressed="false">Mobile (390px)</button>
<span id="count" role="status"></span></div>
<main class="gallery">__CARDS__</main><script>__SCRIPT__</script></body></html>"""
    for key, value in {
        "__TITLE__": title, "__DESC__": desc, "__CSS__": CSS,
        "__OPTIONS__": "".join(options), "__CARDS__": "".join(cards), "__SCRIPT__": SCRIPT
    }.items():
        page = page.replace(key, value)
    return page


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    source = args.manifest.resolve()
    target = args.out.resolve()
    if source == target:
        parser.error("Output must not overwrite the manifest")
    try:
        page = render(load_manifest(source), source, target)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(page, encoding="utf-8")
    print("Gallery:", target)


if __name__ == "__main__":
    main()
