"""Unit and integration smoke tests for the Taste Loop local helpers."""
import json
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
GALLERY = runpy.run_path(str(ROOT / "scripts" / "create_gallery.py"))
PLAYGROUND = runpy.run_path(str(ROOT / "scripts" / "create_playground.py"))
EXAMPLE = ROOT / "examples" / "travel-journal"


class GalleryTests(unittest.TestCase):
    def test_example_gallery_renders_four_previews(self):
        manifest = EXAMPLE / "manifest.json"
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "gallery.html"
            data = GALLERY["load_manifest"](manifest)
            page = GALLERY["render"](data, manifest, dest)
            self.assertEqual(page.count("<iframe "), 4)
            self.assertIn('id="search"', page)
            self.assertIn('data-viewport="mobile"', page)
            self.assertIn("Field Notes", page)
            self.assertIn("Postcard Party", page)

    def test_escape_user_controlled_manifest_fields(self):
        manifest = EXAMPLE / "manifest.json"
        data = {
            "title": "<script>alert(1)</script>",
            "variants": [{
                "id": "a",
                "name": '<img src=x onerror="alert(1)">',
                "path": "cinematic.html",
                "tags": ["safe"]
            }]
        }
        page = GALLERY["render"](data, manifest, EXAMPLE / "gallery.html")
        self.assertNotIn("<script>alert(1)</script>", page)
        self.assertNotIn('<img src=x onerror=', page)
        self.assertIn("&lt;script&gt;", page)

    def test_path_traversal_is_rejected(self):
        with self.assertRaises(ValueError):
            GALLERY["safe_variant_path"](EXAMPLE.resolve(), "../outside.html")
        with self.assertRaises(ValueError):
            GALLERY["safe_variant_path"](EXAMPLE.resolve(), "/tmp/outside.html")

    def test_duplicate_ids_are_rejected(self):
        data = {"variants": [
            {"id": "duplicate", "name": "A", "path": "cinematic.html"},
            {"id": "duplicate", "name": "B", "path": "atlas.html"}
        ]}
        with self.assertRaises(ValueError):
            GALLERY["render"](data, EXAMPLE / "manifest.json", EXAMPLE / "gallery.html")


class PlaygroundTests(unittest.TestCase):
    def test_example_tokens_and_preview(self):
        tokens = json.loads((EXAMPLE / "tokens.json").read_text(encoding="utf-8"))
        PLAYGROUND["validate_tokens"](tokens)
        html_source = (EXAMPLE / "cinematic.html").read_text(encoding="utf-8")
        page = PLAYGROUND["render"](html_source, tokens)
        self.assertIn("Export CSS overrides", page)
        self.assertIn("sandbox=\"allow-scripts\"", page)
        self.assertIn("--hero-size", page)
        self.assertIn("tasteLoop: 'set-token'", page)

    def test_script_end_is_escaped_inside_json(self):
        data = {"title": "test", "tokens": [{"variable": "--ink", "type": "text", "value": "red"}]}
        src = '<html><body><script>console.log("a")</script></body></html>'
        page = PLAYGROUND["render"](src, data)
        self.assertIn(r"<\/script>", page)
        self.assertEqual(page.count("</script>"), 1)

    def test_invalid_tokens_are_rejected(self):
        with self.assertRaises(ValueError):
            PLAYGROUND["validate_tokens"]({"tokens": [
                {"variable": "background", "type": "color", "value": "#abcdef"}
            ]})
        with self.assertRaises(ValueError):
            PLAYGROUND["validate_tokens"]({"tokens": [
                {"variable": "--bg", "type": "color", "value": "red"}
            ]})

    def test_commands_generate_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            gallery = Path(tmp) / "gallery.html"
            playground = Path(tmp) / "playground.html"
            subprocess.run([
                sys.executable, str(ROOT / "scripts" / "create_gallery.py"),
                "--manifest", str(EXAMPLE / "manifest.json"), "--out", str(gallery)
            ], check=True, capture_output=True, text=True)
            subprocess.run([
                sys.executable, str(ROOT / "scripts" / "create_playground.py"),
                "--html", str(EXAMPLE / "cinematic.html"),
                "--tokens", str(EXAMPLE / "tokens.json"), "--out", str(playground)
            ], check=True, capture_output=True, text=True)
            self.assertIn("Postcard Party", gallery.read_text(encoding="utf-8"))
            self.assertIn("Export tokens.json", playground.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
