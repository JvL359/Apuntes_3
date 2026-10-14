"""Regression tests in isolated temporary courses; optional read-only real PDF input."""

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
PDF = None
VALID = "---\nestado: pendiente de revisión\n---\n\n### I. Concepto\n\n#### 1. Desarrollo\n\nExplicación $x$ y `cost = $5` correcta.\n\n### II. Resumen Final\n\nIdea clave.\n"


def run(tool, *arguments, code=0):
    result = subprocess.run([sys.executable, "-X", "utf8", "-B", str(SCRIPTS / tool), *map(str, arguments)],
                            capture_output=True, encoding="utf-8")
    if result.returncode != code:
        raise AssertionError(f"{tool}: expected exit {code}, got {result.returncode}\n"
                             f"{result.stdout}\n{result.stderr}")
    return json.loads(result.stdout) if result.stdout.strip() else result.stderr


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def json_file(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return path


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory(prefix="apuntes-icai-test-")
        self.addCleanup(self.workspace.cleanup)
        self.root = Path(self.workspace.name)
        self.course = self.root / "ASG"
        (self.course / "_materiales").mkdir(parents=True)
        (self.course / "imgs").mkdir()
        self.note = self.course / "Tema 1 - Prueba.md"
        self.note.write_text(VALID, encoding="utf-8")
        self.material = self.course / "_materiales" / "source.txt"
        self.material.write_text("Original", encoding="utf-8")

    def check(self, *extra, code=0):
        return run("audit_notes.py", "check", "--course", self.course, "--note", self.note,
                   *extra, code=code)

    def snapshot(self):
        path = self.root / "before.json"
        run("audit_notes.py", "snapshot", "--course", self.course, "--output", path)
        return path

    def edit(self, text):
        self.note.write_text(text, encoding="utf-8")

    def test_clean_note_and_read_only_audit(self):
        before = (sha(self.note), self.note.stat().st_mtime_ns, sha(self.material))
        result = self.check("--mode", "crear")
        self.assertEqual((result["errors"], result["warnings"]), (0, 0))
        self.assertEqual(before, (sha(self.note), self.note.stat().st_mtime_ns, sha(self.material)))

    def test_noop_preserves_existing_state(self):
        self.edit(VALID.replace("pendiente de revisión", "actualizado"))
        result = self.check("--baseline", self.snapshot(), "--expect-no-change")
        self.assertEqual(result["state"], "actualizado")
        self.assertEqual(result["changes"], [])

    def test_noop_detects_note_changes(self):
        baseline = self.snapshot()
        self.edit(VALID + "Nuevo contenido.\n")
        result = self.check("--baseline", baseline, "--expect-no-change", code=1)
        self.assertIn("idempotence", [f["code"] for f in result["findings"]])

    def test_snapshot_preserves_preexisting_dirty_files(self):
        other = self.course / "Tema 2 - Otro.md"
        other.write_text("Edición previa del usuario", encoding="utf-8")
        baseline = self.snapshot()
        self.edit(VALID + "Añadido permitido.\n")
        result = self.check("--baseline", baseline)
        self.assertEqual([c["path"] for c in result["changes"]], [self.note.name])
        self.assertEqual(other.read_text(encoding="utf-8"), "Edición previa del usuario")

    def test_material_change_is_out_of_scope(self):
        baseline = self.snapshot()
        self.material.write_text("No permitido", encoding="utf-8")
        result = self.check("--baseline", baseline, code=1)
        self.assertIn("unexpected_change", [f["code"] for f in result["findings"]])

    def test_other_note_change_is_out_of_scope(self):
        baseline = self.snapshot()
        (self.course / "Tema 2.md").write_text("No permitido", encoding="utf-8")
        result = self.check("--baseline", baseline, code=1)
        self.assertEqual(result["errors"], 1)

    def test_image_addition_and_explicit_replacement(self):
        baseline = self.snapshot()
        image = self.course / "imgs" / "figure.png"
        image.write_bytes(b"fixture image bytes")
        self.edit(VALID + "\n![[figure.png]]\n")
        self.assertEqual(self.check("--baseline", baseline)["metrics"]["images"], 1)
        baseline = self.snapshot()
        image.write_bytes(b"different fixture bytes")
        self.check("--baseline", baseline, code=1)
        self.check("--baseline", baseline, "--allowed-images", image)

    def test_image_deletion_is_not_authorized_by_replacement_flag(self):
        image = self.course / "imgs" / "figure.png"
        image.write_bytes(b"fixture image bytes")
        baseline = self.snapshot()
        image.unlink()
        self.check("--baseline", baseline, "--allowed-images", image, code=1)

    def test_missing_embed_is_error(self):
        self.edit(VALID + "\n![[missing.png]]\n")
        result = self.check(code=1)
        self.assertIn("missing_embed", [f["code"] for f in result["findings"]])

    def test_embeds_in_code_are_not_real_links(self):
        self.edit(VALID + "\nSintaxis: `![[missing.png]]` y `![x](missing.png)`.\n\n```python\ntext = '![[missing.png]]'\n```\n")
        result = self.check()
        self.assertEqual(result["errors"], 0)
        self.assertEqual(result["metrics"]["images"], 0)

    def test_math_inside_code_is_ignored_and_unclosed_math_warns(self):
        self.edit(VALID + "\n```python\nx = '$$$'\n```\n\n$$x^2\n")
        result = self.check()
        self.assertEqual([f["code"] for f in result["findings"]], ["display_math"])

    def test_unclosed_code_fence_is_error(self):
        self.edit(VALID + "\n```python\nx = 1\n")
        result = self.check(code=1)
        self.assertIn("unclosed_fence", [f["code"] for f in result["findings"]])

    def test_invalid_frontmatter_and_mode(self):
        for frontmatter, expected in [("estado: [", "invalid_yaml"),
                                      ("estado: 2026-10-12", "invalid_state"),
                                      ("estado: actualizado\nestado: actualizado", "duplicate_state")]:
            with self.subTest(frontmatter=frontmatter):
                self.edit("---\n" + frontmatter + "\n---\n\n### I. Resumen Final\n")
                result = self.check(code=1)
                self.assertIn(expected, [f["code"] for f in result["findings"]])
        self.edit(VALID)
        result = self.check("--mode", "revisar", code=1)
        self.assertIn("mode_state", [f["code"] for f in result["findings"]])

    def test_numbering_allows_global_and_per_block(self):
        for number in [1, 2]:
            self.edit(VALID.replace("### II. Resumen Final", f"### II. Otro\n\n#### {number}. Sección\n\nTexto.\n\n### III. Resumen Final"))
            result = self.check()
            self.assertNotIn("section_sequence", [f["code"] for f in result["findings"]])

    def test_coverage_warns_about_pending_visual_and_missing_reasons(self):
        coverage = json_file(self.root / "coverage.json", {"pages": [
            {"source": 1, "page": 1, "status": "pending", "review_reasons": ["little_extracted_text"]},
            {"source": 1, "page": 2, "status": "duplicate"}]})
        result = self.check("--coverage", coverage)
        self.assertEqual({f["code"] for f in result["findings"]},
                         {"coverage_pending", "visual_pending", "coverage_reason"})


@unittest.skipUnless(PDF, "Supply --pdf for real PDF integration tests")
class PdfTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workspace = tempfile.TemporaryDirectory(prefix="apuntes-icai-pdf-test-")
        cls.root = Path(cls.workspace.name)
        cls.course = cls.root / "ASG"
        materials = cls.course / "_materiales" / "Tema 1"
        materials.mkdir(parents=True)
        cls.original_hash = sha(PDF)
        cls.pdf = materials / "source.pdf"
        shutil.copyfile(PDF, cls.pdf)
        cls.preparation = cls.root / "preparation"
        run("prepare_pdf.py", "prepare", "--pdfs", cls.pdf, "--output", cls.preparation)
        cls.manifest_path = cls.preparation / "manifest.json"
        cls.manifest = json.loads(cls.manifest_path.read_text(encoding="utf-8"))

    @classmethod
    def tearDownClass(cls):
        try:
            if sha(PDF) != cls.original_hash:
                raise AssertionError("The original PDF was changed")
        finally:
            cls.workspace.cleanup()

    def setUp(self):
        self.case = Path(tempfile.mkdtemp(prefix="case-", dir=self.root))

    def specification(self, crops):
        return json_file(self.case / "crops.json", {"preparation": str(self.manifest_path), "crops": crops})

    def crop(self, spec, *extra, code=0):
        return run("crop_figures.py", "--spec", spec, "--output", self.case / "previews", *extra, code=code)

    def test_every_page_has_text_and_thumbnail(self):
        source = self.manifest["sources"][0]
        coverage = json.loads(Path(self.manifest["coverage"]).read_text(encoding="utf-8"))
        self.assertEqual([p["page"] for p in source["pages"]], list(range(1, source["page_count"] + 1)))
        self.assertEqual(len(coverage["pages"]), source["page_count"])
        self.assertTrue(all(Path(p).is_file() for p in self.manifest["assets"]))

    def test_prepare_reuses_without_overwriting_coverage(self):
        coverage = Path(self.manifest["coverage"])
        data = json.loads(coverage.read_text(encoding="utf-8"))
        data["pages"][0]["status"] = "covered"
        json_file(coverage, data)
        before = {p: (sha(p), Path(p).stat().st_mtime_ns) for p in self.manifest["assets"]}
        result = run("prepare_pdf.py", "prepare", "--pdfs", self.pdf, "--output", self.preparation)
        self.assertTrue(result["reused"])
        self.assertEqual(before, {p: (sha(p), Path(p).stat().st_mtime_ns) for p in before})

    def test_changed_settings_require_new_preparation(self):
        run("prepare_pdf.py", "prepare", "--pdfs", self.pdf, "--output", self.preparation,
            "--thumbnail-width", "300", code=2)

    def test_render_range_and_reuse(self):
        arguments = ("render", "--manifest", self.manifest_path, "--source", "1", "--pages", "1", "--dpi", "100")
        result = run("prepare_pdf.py", *arguments)
        image = Path(result[0]["path"])
        before = (sha(image), image.stat().st_mtime_ns)
        run("prepare_pdf.py", *arguments)
        self.assertEqual(before, (sha(image), image.stat().st_mtime_ns))
        run("prepare_pdf.py", "render", "--manifest", self.manifest_path,
            "--source", "1", "--pages", "0", code=2)

    def test_crops_preview_publish_and_reuse(self):
        spec = self.specification([{"source": 1, "page": 1, "box": [0.1, 0.2, 0.8, 0.9]}])
        preview = self.crop(spec)
        self.assertIsNone(preview["crops"][0]["published"])
        self.assertTrue(all(Path(p).is_file() for p in preview["previews"]))
        publish = self.course / "imgs"
        result = self.crop(spec, "--publish", publish)
        image = Path(result["crops"][0]["published"])
        before = (sha(image), image.stat().st_mtime_ns)
        result = self.crop(spec, "--publish", publish)
        self.assertTrue(result["crops"][0]["publication_reused"])
        self.assertEqual(before, (sha(image), image.stat().st_mtime_ns))
        # Relative crop covers 70% of width and height at 220 DPI (rounding <= 2 px).
        page = self.manifest["sources"][0]["pages"][0]["size_points"]
        self.assertAlmostEqual(result["crops"][0]["width"], (page[2] - page[0]) * 0.7 * 220 / 72, delta=2)

    def test_collision_prevents_all_publication(self):
        publish = self.course / "imgs"
        publish.mkdir(exist_ok=True)
        existing = publish / "collision.png"
        existing.write_bytes(b"Previous image, must remain intact")
        spec = self.specification([
            {"source": 1, "page": 1, "box": [0.1, 0.1, 0.5, 0.5], "filename": "must-not-publish.png"},
            {"source": 1, "page": 1, "box": [0.5, 0.5, 0.9, 0.9], "filename": "collision.png"}])
        self.crop(spec, "--publish", publish, code=2)
        self.assertEqual(existing.read_bytes(), b"Previous image, must remain intact")
        self.assertFalse((publish / "must-not-publish.png").exists())
        self.assertFalse((self.case / "previews" / "must-not-publish.png").exists())

    def test_invalid_coordinates_and_publication_target(self):
        invalid = self.specification([{"source": 1, "page": 1, "box": [0.9, 0.1, 0.2, 0.8]}])
        self.crop(invalid, code=2)
        valid = self.specification([{"source": 1, "page": 1, "box": [0.1, 0.1, 0.9, 0.9]}])
        self.crop(valid, "--publish", self.course / "_materiales" / "imgs", code=2)
        self.crop(valid, "--publish", self.case / "OtherCourse" / "imgs", code=2)

    def test_changed_source_hash_rejects_render_and_crops(self):
        broken = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        broken["sources"][0]["sha256"] = "0" * 64
        manifest = json_file(self.case / "changed.json", broken)
        run("prepare_pdf.py", "render", "--manifest", manifest, "--source", "1", "--pages", "1", code=2)
        spec = json_file(self.case / "changed-crops.json", {"preparation": str(manifest), "crops": [
            {"source": 1, "page": 1, "box": [0.1, 0.1, 0.9, 0.9]}]})
        self.crop(spec, code=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", type=Path, help="Existing PDF to copy into the temporary test course")
    args, remaining = parser.parse_known_args()
    PDF = args.pdf.resolve(strict=True) if args.pdf else None
    PdfTests.__unittest_skip__ = not bool(PDF)
    unittest.main(argv=[sys.argv[0], *remaining], verbosity=2)
