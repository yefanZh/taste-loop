#!/usr/bin/env python3
"""Generate a live CSS-variable playground around a standalone HTML prototype."""
import argparse
import html
import json
from pathlib import Path
import re


VARIABLE = re.compile(r"^--[A-Za-z][A-Za-z0-9_-]*$")
VALID_TYPES = {"color", "range", "select", "text"}


def validate_tokens(data):
    if not isinstance(data, dict) or not isinstance(data.get("tokens"), list):
        raise ValueError("Token file must contain a tokens array")
    if not 1 <= len(data["tokens"]) <= 60:
        raise ValueError("Token file must contain 1 to 60 tokens")
    seen = set()
    for token in data["tokens"]:
        if not isinstance(token, dict):
            raise ValueError("Each token must be an object")
        var = token.get("variable")
        kind = token.get("type")
        if not isinstance(var, str) or not VARIABLE.fullmatch(var) or var in seen:
            raise ValueError("Token variable must be unique and start with --")
        if kind not in VALID_TYPES or not isinstance(token.get("value"), (str, int, float)):
            raise ValueError("Invalid type or value for " + var)
        if kind == "color" and not re.fullmatch(r"#[0-9a-fA-F]{6}", str(token["value"])):
            raise ValueError("Color values must be six-digit hex colors: " + var)
        if kind == "range":
            for prop in ("min", "max", "step"):
                if not isinstance(token.get(prop), (int, float)) or isinstance(token.get(prop), bool):
                    raise ValueError("range requires numeric min/max/step: " + var)
            if token["step"] <= 0 or token["min"] > token["max"]:
                raise ValueError("Invalid range bounds: " + var)
            try:
                number = float(token["value"])
            except ValueError as exc:
                raise ValueError("range value must be numeric: " + var) from exc
            if not token["min"] <= number <= token["max"]:
                raise ValueError("range value out of bounds: " + var)
        if kind == "select":
            options = token.get("options")
            if not isinstance(options, list) or not options or not all(isinstance(o, str) for o in options):
                raise ValueError("select must declare string options: " + var)
            if str(token["value"]) not in options:
                raise ValueError("select value missing from options: " + var)
        if not isinstance(token.get("name", var), str):
            raise ValueError("token name must be string: " + var)
        if not isinstance(token.get("unit", ""), str):
            raise ValueError("token unit must be string: " + var)
        seen.add(var)
    return data


BRIDGE = """<script>
window.addEventListener('message', function(event) {
  var data = event.data;
  if (!data || data.tasteLoop !== 'set-token' || typeof data.variable !== 'string') return;
  if (!/^--[A-Za-z][A-Za-z0-9_-]*$/.test(data.variable) || typeof data.value !== 'string') return;
  document.documentElement.style.setProperty(data.variable, data.value);
});
</script>"""

CSS = """
:root{color-scheme:dark;--line:#363d4d;--bg:#10131a;--panel:#1a202b;--ink:#f5f7fc;--muted:#b1bac8;--accent:#a1f2ca}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.5 system-ui,sans-serif}
header{padding:17px 24px;border-bottom:1px solid var(--line);display:flex;align-items:center;gap:16px;flex-wrap:wrap}
h1{font-size:1.25rem;margin:0}small{color:var(--muted)}.layout{display:grid;grid-template-columns:320px minmax(0,1fr);min-height:calc(100vh - 74px)}
aside{background:var(--panel);padding:22px;border-right:1px solid var(--line);max-height:calc(100vh - 74px);overflow:auto}
label{display:block;font-weight:600;margin-top:18px;margin-bottom:6px}.meta{font:11px monospace;color:var(--muted)}
.control{display:flex;gap:10px;align-items:center}input,select{min-width:0;max-width:100%;width:100%;padding:8px;background:#272f3b;border:1px solid var(--line);color:var(--ink);border-radius:8px}
input[type=color]{width:68px;height:40px;padding:2px;flex:none}output{min-width:60px;text-align:right;font-family:monospace}
.actions{display:grid;gap:8px;margin-top:26px}button{background:#2c3845;color:var(--ink);border:1px solid var(--line);padding:10px;border-radius:9px;cursor:pointer}
button.primary{background:var(--accent);color:#132218;font-weight:700}button:focus-visible,input:focus-visible,select:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.preview{padding:16px;min-width:0}.frame{margin:auto;max-width:100%;height:calc(100vh - 124px);background:white;border:1px solid var(--line);border-radius:10px;overflow:hidden}
iframe{border:0;width:100%;height:100%}.size{margin-left:auto;display:flex;gap:6px}.size button[aria-pressed=true]{border-color:var(--accent);color:var(--accent)}
.notice{color:var(--muted);font-size:.83rem;margin-top:14px}
@media(max-width:800px){.layout{grid-template-columns:1fr}aside{max-height:none;border-right:0;border-bottom:1px solid var(--line)}.frame{height:600px}.preview{padding:10px}}
"""

JS = """
const schema = __TOKENS__;
const source = __SOURCE__;
const tokens = schema.tokens.map(t => ({...t}));
const frame = document.getElementById('prototype');
const form = document.getElementById('controls');
const valueString = token => String(token.value) + (token.type === 'range' ? (token.unit || '') : '');
function sendToken(token) {
  if (frame.contentWindow) frame.contentWindow.postMessage({
    tasteLoop: 'set-token', variable: token.variable, value: valueString(token)
  }, '*');
}
function applyTokens() { tokens.forEach(sendToken); }
frame.addEventListener('load', applyTokens);
frame.srcdoc = source;
tokens.forEach(token => {
  const label = document.createElement('label');
  label.textContent = token.name || token.variable;
  const meta = document.createElement('div');
  meta.className = 'meta';
  meta.textContent = token.variable;
  const row = document.createElement('div');
  row.className = 'control';
  let control;
  if (token.type === 'select') {
    control = document.createElement('select');
    for (const item of token.options) {
      const option = document.createElement('option');
      option.value = item; option.textContent = item;
      control.appendChild(option);
    }
  } else {
    control = document.createElement('input');
    control.type = token.type === 'color' ? 'color' : token.type === 'range' ? 'range' : 'text';
    if (token.type === 'range') {
      control.min = token.min; control.max = token.max; control.step = token.step;
    }
  }
  control.value = token.value;
  control.setAttribute('aria-label', token.name || token.variable);
  const out = document.createElement('output');
  function update() {
    token.value = control.value;
    out.textContent = token.type === 'range' || token.type === 'color' ? valueString(token) : '';
    sendToken(token);
  }
  control.addEventListener('input', update);
  control.addEventListener('change', update);
  update();
  row.append(control, out);
  form.append(label, meta, row);
});
function download(filename, content, mime) {
  const blob = new Blob([content], {type:mime});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = filename; document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
document.getElementById('export-json').addEventListener('click', () => {
  download('tokens.json', JSON.stringify({...schema, tokens}, null, 2) + '\\n', 'application/json');
});
document.getElementById('export-css').addEventListener('click', () => {
  const css = ':root {\\n' + tokens.map(t => '  ' + t.variable + ': ' + valueString(t) + ';').join('\\n') + '\\n}\\n';
  download('taste-loop-overrides.css', css, 'text/css');
});
document.getElementById('reset').addEventListener('click', () => {
  frame.srcdoc = source;
  location.reload();
});
document.querySelectorAll('[data-width]').forEach(button => {
  button.addEventListener('click', () => {
    document.getElementById('frame').style.width = button.dataset.width;
    document.querySelectorAll('[data-width]').forEach(other => other.setAttribute('aria-pressed', String(other === button)));
  });
});
"""


def safe_json(value):
    # "</script" must not close the outer inline script inside serialized HTML.
    return json.dumps(value, ensure_ascii=True).replace("</", "<\\/")


def render(source, schema):
    # Message bridge runs inside the preview; parent never reaches into its DOM.
    if re.search(r"</body\s*>", source, flags=re.I):
        source = re.sub(r"</body\s*>", lambda m: BRIDGE + m.group(0), source, count=1, flags=re.I)
    else:
        source += BRIDGE
    template = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>__TITLE__ / Taste Loop</title>
<style>__CSS__</style></head><body>
<header><h1>Taste Loop / __TITLE__</h1><small>Live design-token playground</small>
<div class="size"><button data-width="100%" aria-pressed="true">Desktop</button>
<button data-width="390px" aria-pressed="false">Mobile (390px)</button></div></header>
<div class="layout"><aside><div id="controls"></div>
<div class="actions"><button class="primary" id="export-json">Export tokens.json</button>
<button id="export-css">Export CSS overrides</button>
<button id="reset">Reset preview</button></div>
<p class="notice">Changes affect this preview only. Export and apply the values to your selected prototype before implementation.</p></aside>
<main class="preview"><div class="frame" id="frame"><iframe id="prototype"
title="Live prototype preview" sandbox="allow-scripts"></iframe></div></main></div>
<script>__JS__</script></body></html>"""
    return template.replace("__TITLE__", html.escape(str(schema.get("title", "Design tokens")), quote=True)).replace(
        "__CSS__", CSS
    ).replace("__JS__", JS.replace("__TOKENS__", safe_json(schema)).replace("__SOURCE__", safe_json(source)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--html", type=Path, required=True)
    parser.add_argument("--tokens", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    src, token_file, target = args.html.resolve(), args.tokens.resolve(), args.out.resolve()
    if target in (src, token_file):
        parser.error("Output must not overwrite an input")
    try:
        schema = validate_tokens(json.loads(token_file.read_text(encoding="utf-8")))
        source = src.read_text(encoding="utf-8")
        page = render(source, schema)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(page, encoding="utf-8")
    print("Playground:", target)


if __name__ == "__main__":
    main()
