"""Render reproducible PDF crops; preview first, explicitly publish to course/imgs."""

import argparse
import hashlib
import json
import math
import shutil
import time
from pathlib import Path

import pymupdf as fitz
from prepare_pdf import contact_sheets, digest_file, temporary_directory, write_json


def execute(args):
    started = time.perf_counter()
    spec_path = Path(args.spec).resolve(strict=True)
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    manifest_path = Path(spec["preparation"])
    if not manifest_path.is_absolute():
        manifest_path = spec_path.parent / manifest_path
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    sources = {s["source"]: s for s in manifest["sources"]}
    directory = temporary_directory(args.output, "apuntes-icai-crops-")
    publish = Path(args.publish).resolve() if args.publish else None
    if publish and (publish.name != "imgs" or "_materiales" in publish.parts):
        raise ValueError("Publication is allowed only in a course's imgs directory, outside _materiales.")
    if publish:
        materials = publish.parent / "_materiales"
        if not materials.is_dir() or any(not Path(s["path"]).resolve().is_relative_to(materials)
                                         for s in sources.values()):
            raise ValueError("Publication must belong to the course containing the prepared materials.")
    crops = spec.get("crops", [])
    if not crops:
        raise ValueError("No crops specified.")
    plans, documents, previews, results = [], {}, [], []
    try:
        for crop in crops:
            source = sources.get(crop["source"])
            if source is None:
                raise ValueError("Unknown source index.")
            if source["source"] not in documents:
                if digest_file(source["path"]) != source["sha256"]:
                    raise ValueError("Source changed; prepare again before cropping.")
                documents[source["source"]] = fitz.open(source["path"])
            doc = documents[source["source"]]
            number = crop["page"]
            if not isinstance(number, int) or not 1 <= number <= len(doc):
                raise ValueError("Page numbers must be 1-based integers within the PDF.")
            page = doc[number - 1]
            box = crop["box"]
            if len(box) != 4 or not all(isinstance(v, (float, int)) and math.isfinite(v) for v in box):
                raise ValueError("box must contain four finite coordinates [x0,y0,x1,y1].")
            units = crop.get("units", "relative")
            if units == "relative":
                if not (0 <= box[0] < box[2] <= 1 and 0 <= box[1] < box[3] <= 1):
                    raise ValueError("Relative box must be ordered and entirely within [0,1].")
                clip = fitz.Rect(box[0] * page.rect.width, box[1] * page.rect.height,
                                 box[2] * page.rect.width, box[3] * page.rect.height)
            elif units == "points":
                clip = fitz.Rect(box)
                if clip.is_empty or not page.rect.contains(clip):
                    raise ValueError("Point coordinates must describe a nonempty rectangle inside the displayed page.")
            else:
                raise ValueError("units must be relative or points.")
            key = json.dumps({"pdf": source["sha256"], "page": number, "clip": list(clip),
                              "dpi": args.dpi}, sort_keys=True).encode()
            stable = hashlib.sha256(key).hexdigest()[:12]
            name = crop.get("filename", f"apuntes-{source['sha256'][:12]}-p{number:04d}-{stable}.png")
            if Path(name).name != name or "/" in name or "\\" in name or not name.lower().endswith(".png"):
                raise ValueError("filename must be a plain PNG filename without directories.")
            if any(p["name"] == name for p in plans):
                raise ValueError(f"Duplicate crop filename in specification: {name}")
            plans.append({"page_object": page, "name": name, "clip": clip, "source": source["source"],
                          "page": number})
        # Render to memory and check every collision before writing or publishing any crop.
        for plan in plans:
            pix = plan["page_object"].get_pixmap(dpi=args.dpi, clip=plan["clip"], alpha=False)
            payload = pix.tobytes("png")
            plan.update(payload=payload, sha256=hashlib.sha256(payload).hexdigest(),
                        width=pix.width, height=pix.height)
            targets = [directory / plan["name"]]
            if publish:
                targets.append(publish / plan["name"])
            for target in targets:
                if target.exists() and digest_file(target) != plan["sha256"]:
                    raise ValueError(f"Filename collision with different content: {target}")
        if publish:
            publish.mkdir(parents=True, exist_ok=True)
        for plan in plans:
            output = directory / plan["name"]
            if not output.exists():
                output.write_bytes(plan["payload"])
            reused = False
            if publish:
                target = publish / plan["name"]
                reused = target.exists()
                if not reused:
                    shutil.copyfile(output, target)
            previews.append((output, f"Source {plan['source']} / p{plan['page']} / {plan['width']}x{plan['height']}"))
            results.append({"source": plan["source"], "page": plan["page"], "box_points": list(plan["clip"]),
                            "path": str(output), "filename": plan["name"], "sha256": plan["sha256"],
                            "width": plan["width"], "height": plan["height"],
                            "embed": f"![[{plan['name']}]]", "published": str(publish / plan["name"]) if publish else None,
                            "publication_reused": reused})
        sheets = contact_sheets(previews, directory, stem="crops")
        report = {"preparation": str(manifest_path), "crops": results, "previews": sheets,
                  "seconds": round(time.perf_counter() - started, 3)}
        write_json(directory / "crops.json", report)
        print(json.dumps(report, ensure_ascii=False, indent=2))
    finally:
        for doc in documents.values():
            doc.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", required=True, help="JSON with preparation path and crop list")
    parser.add_argument("--output", help="Working directory inside the system temporary directory")
    parser.add_argument("--dpi", type=int, default=220)
    parser.add_argument("--publish", help="Course imgs directory; omit to generate previews only")
    args = parser.parse_args()
    if args.dpi <= 0:
        parser.error("DPI must be positive.")
    try:
        execute(args)
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as exc:
        parser.exit(2, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
