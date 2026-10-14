"""Prepare read-only PDF sources for visual study. All page numbers are 1-based."""

import argparse
import hashlib
import json
import math
import re
import tempfile
import time
from collections import Counter
from pathlib import Path

import pymupdf as fitz
from PIL import Image, ImageDraw

VERSION = 2


def digest_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def temporary_directory(output, prefix):
    if output is None:
        return Path(tempfile.mkdtemp(prefix=prefix))
    path = Path(output).resolve()
    if not path.is_relative_to(Path(tempfile.gettempdir()).resolve()):
        raise ValueError("The working directory must be inside the system temporary directory.")
    path.mkdir(parents=True, exist_ok=True)
    return path


def contact_sheets(items, directory, stem="contact", columns=3, per_sheet=12, width=360):
    """Return paginated, labeled previews. Each item is (image_path, label)."""
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    outputs = []
    height = int(width * 0.75) + 42
    for offset in range(0, len(items), per_sheet):
        batch = items[offset:offset + per_sheet]
        sheet = Image.new("RGB", (columns * width, math.ceil(len(batch) / columns) * height), "white")
        draw = ImageDraw.Draw(sheet)
        for index, (path, label) in enumerate(batch):
            x, y = (index % columns) * width, (index // columns) * height
            with Image.open(path) as original:
                thumb = original.convert("RGB")
                thumb.thumbnail((width - 16, height - 46))
                sheet.paste(thumb, (x + (width - thumb.width) // 2, y + 4))
            draw.text((x + 8, y + height - 34), label[:52], fill="black")
        output = directory / f"{stem}-{offset // per_sheet + 1:03d}.png"
        sheet.save(output)
        outputs.append(str(output))
    return outputs


def parse_pages(value, count):
    pages = set()
    for part in value.split(","):
        match = re.fullmatch(r"\s*(\d+)(?:-(\d+))?\s*", part)
        if not match:
            raise ValueError("Pages must look like 1,3-5 (1-based).")
        start, end = int(match[1]), int(match[2] or match[1])
        if not 1 <= start <= end <= count:
            raise ValueError(f"Invalid page range {part}; source has {count} pages.")
        pages.update(range(start, end + 1))
    return sorted(pages)


def prepare(args):
    start = time.perf_counter()
    paths = [Path(p).resolve(strict=True) for p in args.pdfs]
    if any(p.suffix.lower() != ".pdf" for p in paths):
        raise ValueError("All sources must be PDF files.")
    signatures = [{"path": str(p), "sha256": digest_file(p)} for p in paths]
    settings = {"thumbnail_width": args.thumbnail_width, "low_words": args.low_words,
                "ocr": args.ocr, "ocr_language": args.ocr_language}
    directory = temporary_directory(args.output, "apuntes-icai-pdf-")
    manifest_path = directory / "manifest.json"
    if manifest_path.exists():
        previous = json.loads(manifest_path.read_text(encoding="utf-8"))
        assets = previous.get("assets", [])
        if (previous.get("version") == VERSION and previous.get("inputs") == signatures
                and previous.get("settings") == settings and assets
                and all(Path(p).is_file() for p in assets)):
            print(json.dumps({"manifest": str(manifest_path), "reused": True,
                              "seconds": round(time.perf_counter() - start, 3)}, ensure_ascii=False))
            return
        raise ValueError("Output contains a different or incomplete preparation; use a new temporary directory.")
    if any(directory.iterdir()):
        raise ValueError("Preparation output must be empty, or a matching reusable preparation.")
    sources, assets, coverage, warnings = [], [], [], []
    for source_index, (path, signature) in enumerate(zip(paths, signatures), 1):
        source_dir = directory / f"source-{source_index:02d}-{signature['sha256'][:12]}"
        source_dir.mkdir()
        pages, previews = [], []
        with fitz.open(path) as doc:
            if doc.needs_pass:
                raise ValueError(f"Password-protected PDF: {path.name}")
            # Repeated slide backgrounds/logos should not flag every page as high priority.
            # They are still visible in the overview and never assumed conceptually irrelevant.
            raster_by_page = [p.get_image_info(hashes=True) for p in doc]
            occurrences = Counter(d for infos in raster_by_page for d in {i["digest"] for i in infos})
            repeated = {d for d, count in occurrences.items() if count >= max(3, math.ceil(len(doc) * 0.6))}
            for index, page in enumerate(doc):
                number = index + 1
                text = page.get_text("text", sort=True)
                words = len(text.split())
                image_info = raster_by_page[index]
                area = max(page.rect.get_area(), 1)
                image_ratio = min(1, sum(fitz.Rect(i["bbox"]).get_area() for i in image_info) / area)
                variable_ratio = min(1, sum(fitz.Rect(i["bbox"]).get_area() for i in image_info
                                            if i["digest"] not in repeated) / area)
                drawing_count = len(page.get_drawings())
                reasons = []
                if words < args.low_words:
                    reasons.append("little_extracted_text")
                if variable_ratio >= 0.15:
                    reasons.append("significant_raster_content")
                if drawing_count >= 20:
                    reasons.append("complex_vector_content")
                if "\ufffd" in text:
                    reasons.append("replacement_characters")
                page_path = source_dir / f"page-{number:04d}.txt"
                page_path.write_text(text, encoding="utf-8")
                assets.append(str(page_path))
                thumbnail = source_dir / f"page-{number:04d}.png"
                scale = args.thumbnail_width / page.rect.width
                page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False).save(thumbnail)
                assets.append(str(thumbnail))
                previews.append((thumbnail, f"Source {source_index} / page {number} / words {words}"))
                record = {"page": number, "words": words, "size_points": list(page.rect),
                          "rotation": page.rotation, "image_count": len(image_info),
                          "image_area_ratio": round(image_ratio, 3), "nonrepeated_image_area_ratio": round(variable_ratio, 3),
                          "repeated_image_count": sum(i["digest"] in repeated for i in image_info), "drawing_count": drawing_count,
                          "visual_review_reasons": reasons, "text": str(page_path), "thumbnail": str(thumbnail)}
                if args.ocr == "all" or (args.ocr == "flagged" and reasons):
                    try:
                        tp = page.get_textpage_ocr(language=args.ocr_language, dpi=200, full=True)
                        ocr_path = source_dir / f"page-{number:04d}-ocr.txt"
                        ocr_path.write_text(page.get_text(textpage=tp), encoding="utf-8")
                        record["ocr_text"] = str(ocr_path)
                        assets.append(str(ocr_path))
                    except Exception as exc:
                        record["ocr_error"] = str(exc)
                        warnings.append(f"Source {source_index}, page {number}: OCR unavailable; inspect the render.")
                pages.append(record)
                coverage.append({"source": source_index, "page": number, "status": "pending",
                                 "items": [], "destination_sections": [], "visual_reviewed": False,
                                 "review_reasons": reasons})
        sheets = contact_sheets(previews, source_dir)
        assets.extend(sheets)
        sources.append({"source": source_index, **signature, "page_count": len(pages),
                        "contact_sheets": sheets, "pages": pages})
    coverage_path = directory / "coverage.json"
    write_json(coverage_path, {"version": VERSION, "pages": coverage})
    assets.append(str(coverage_path))
    result = {"version": VERSION, "inputs": signatures, "settings": settings, "sources": sources,
              "coverage": str(coverage_path), "assets": assets, "warnings": warnings,
              "preparation_seconds": round(time.perf_counter() - start, 3)}
    write_json(manifest_path, result)
    print(json.dumps({"manifest": str(manifest_path), "pages": len(coverage),
                      "flagged_pages": sum(bool(p["review_reasons"]) for p in coverage),
                      "warnings": warnings, "seconds": result["preparation_seconds"]}, ensure_ascii=False))


def render(args):
    manifest_path = Path(args.manifest).resolve(strict=True)
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    source = next((s for s in data["sources"] if s["source"] == args.source), None)
    if source is None:
        raise ValueError("Source index not found in manifest.")
    if digest_file(source["path"]) != source["sha256"]:
        raise ValueError("Source PDF changed; prepare again in a fresh working directory.")
    directory = temporary_directory(str(manifest_path.parent / "renders"), "apuntes-icai-render-")
    result = []
    with fitz.open(source["path"]) as doc:
        for number in parse_pages(args.pages, len(doc)):
            page = doc[number - 1]
            output = directory / f"source-{args.source:02d}-page-{number:04d}-{args.dpi}dpi.png"
            if not output.exists():
                page.get_pixmap(dpi=args.dpi, alpha=False).save(output)
            result.append({"page": number, "path": str(output), "size_points": list(page.rect)})
    print(json.dumps(result, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("prepare", help="Extract and render all pages into a temporary working directory")
    p.add_argument("--pdfs", nargs="+", required=True, help="PDFs in the user's priority order")
    p.add_argument("--output", help="Empty directory inside the system temporary directory")
    p.add_argument("--thumbnail-width", type=int, default=540)
    p.add_argument("--low-words", type=int, default=25)
    p.add_argument("--ocr", choices=["none", "flagged", "all"], default="none")
    p.add_argument("--ocr-language", default="eng+spa")
    p.set_defaults(func=prepare)
    r = sub.add_parser("render", help="Render selected pages at readable resolution")
    r.add_argument("--manifest", required=True)
    r.add_argument("--source", type=int, required=True)
    r.add_argument("--pages", required=True, help="1,3-5 (1-based)")
    r.add_argument("--dpi", type=int, default=160)
    r.set_defaults(func=render)
    args = parser.parse_args()
    if getattr(args, "thumbnail_width", 540) <= 0 or getattr(args, "dpi", 160) <= 0:
        parser.error("Image dimensions and DPI must be positive.")
    if getattr(args, "low_words", 25) < 0:
        parser.error("The word threshold must not be negative.")
    try:
        args.func(args)
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as exc:
        parser.exit(2, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
