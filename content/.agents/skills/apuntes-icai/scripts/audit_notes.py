"""Read-only Markdown audit and course snapshots. Warnings require editorial judgment."""

import argparse
import hashlib
import json
import re
import tempfile
import time
from collections import Counter
from pathlib import Path
from urllib.parse import unquote

import yaml

STATES = {"crear": "pendiente de revisión", "actualizar": "actualizado", "revisar": "completado"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def inventory(course):
    # Ignore tool metadata; never compare Git internals or editor state.
    return {p.relative_to(course).as_posix(): digest(p) for p in sorted(course.rglob("*"))
            if p.is_file() and not any(x in {".git", ".agents", ".codex", ".obsidian"} for x in p.relative_to(course).parts)}


def save_temporary(path, payload):
    path = Path(path).resolve()
    if not path.is_relative_to(Path(tempfile.gettempdir()).resolve()):
        raise ValueError("Reports and snapshots must be inside the system temporary directory.")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def plain_line(line):
    return re.sub(r"^(?:\s*>\s?)+", "", line)


def roman_value(text):
    values = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    nums = [values[c] for c in text]
    return sum(-v if i + 1 < len(nums) and v < nums[i + 1] else v for i, v in enumerate(nums))


def audit(args):
    started = time.perf_counter()
    course = Path(args.course).resolve(strict=True)
    note = Path(args.note).resolve(strict=True)
    if note.parent != course or note.suffix.lower() != ".md":
        raise ValueError("The note must be a Markdown file in the course root.")
    vault = Path(args.vault).resolve(strict=True) if args.vault else course
    if not course.is_relative_to(vault):
        raise ValueError("The course must be inside the supplied vault.")
    text = note.read_text(encoding="utf-8-sig")
    findings = []

    def add(level, code, message, line=None):
        findings.append({"severity": level, "code": code, "message": message, "line": line})

    lines = text.splitlines()
    body_start, state = 0, None
    if lines and lines[0].strip() == "---":
        end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
        if end is None:
            add("error", "frontmatter_unclosed", "Frontmatter has no closing delimiter.", 1)
        else:
            body_start = end + 1
            fm = "\n".join(lines[1:end])
            try:
                parsed = yaml.safe_load(fm)
                if not isinstance(parsed, dict):
                    add("error", "frontmatter_mapping", "Frontmatter must be a YAML mapping.", 1)
                else:
                    state = parsed.get("estado")
                    if state not in STATES.values():
                        add("error", "invalid_state", f"Unknown or missing estado: {state!r}.", 1)
                    if args.mode and state != STATES[args.mode]:
                        add("error", "mode_state", f"Mode {args.mode} expects {STATES[args.mode]!r}.", 1)
                if len(re.findall(r"(?m)^estado\s*:", fm)) > 1:
                    add("error", "duplicate_state", "Duplicate estado key.", 1)
            except yaml.YAMLError as exc:
                add("error", "invalid_yaml", str(exc), 1)
    else:
        add("error", "missing_frontmatter", "Missing YAML frontmatter.", 1)

    fence = None
    visible, headings = [], []
    for i in range(body_start, len(lines)):
        line = plain_line(lines[i])
        marker = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
        if marker:
            if fence is None:
                fence = (marker[1][0], len(marker[1]), i + 1)
            elif marker[1][0] == fence[0] and len(marker[1]) >= fence[1] and not marker[2].strip():
                fence = None
            continue
        if fence:
            continue
        visible.append((i + 1, line))
        h = re.match(r"^(#{1,6})\s+(.+?)\s*#*\s*$", line)
        if h:
            headings.append((i + 1, len(h[1]), h[2]))
            if len(h[1]) < 3:
                add("warning", "heading_level", "Expected headings to start at ###.", i + 1)
    if fence:
        add("error", "unclosed_fence", "Unclosed code fence.", fence[2])

    if not headings or not re.fullmatch(r"(?:[IVXLCDM]+\.\s*)?(?:Resumen Final|Final Summary)",
                                       headings[-1][2], re.IGNORECASE) or headings[-1][1] != 3:
        add("warning", "final_summary", "Last heading should be ### with Resumen Final or Final Summary.")
    romans, sections, current_sections, section_groups = [], [], [], []
    previous_level = None
    for line, level, title in headings:
        if previous_level is not None and level > previous_level + 1:
            add("warning", "heading_jump", "Skipped a heading level.", line)
        previous_level = level
        if level == 3:
            if current_sections:
                section_groups.append(current_sections)
                current_sections = []
            m = re.match(r"^([IVXLCDM]+)\.\s+", title)
            if m:
                romans.append(roman_value(m[1]))
            else:
                add("warning", "block_number", "Block heading lacks Roman numbering.", line)
        elif level == 4:
            m = re.match(r"^(\d+)\.\s+", title)
            if m:
                sections.append(int(m[1]))
                current_sections.append(int(m[1]))
            else:
                add("warning", "section_number", "Section heading lacks Arabic numbering.", line)
        elif level >= 5 and not re.match(r"^\d+(?:\.\d+){1,2}\.?\s+", title):
            add("warning", "subsection_number", "Check hierarchical subsection numbering.", line)
    if current_sections:
        section_groups.append(current_sections)
    if romans and romans != list(range(1, len(romans) + 1)):
        add("warning", "roman_sequence", "Roman block numbering is not consecutive from I.")
    global_ok = sections == list(range(1, len(sections) + 1))
    local_ok = all(g == list(range(1, len(g) + 1)) for g in section_groups)
    if sections and not (global_ok or local_ok):
        add("warning", "section_sequence", "Check section numbering; neither global nor per-block sequence is consecutive.")

    # Heuristic only: dollars may denote currency or valid uncommon LaTeX syntax.
    math_mode, math_line = None, None
    for lineno, line in visible:
        clean = re.sub(r"(`+).*?\1", "", line)
        for token in re.finditer(r"(?<!\\)(\$\$|\$)", clean):
            value = token[1]
            if math_mode is None:
                math_mode, math_line = value, lineno
            elif value == math_mode:
                math_mode = None
            elif math_mode == "$":
                add("warning", "math_delimiter", "Mixed inline/display math delimiters; inspect manually.", lineno)
        if math_mode == "$":
            add("warning", "inline_math", "Potential unmatched inline dollar on this line.", math_line)
            math_mode = None
    if math_mode:
        add("warning", "display_math", "Potential unclosed display math delimiter.", math_line)

    visible_text = "\n".join(line for _, line in visible)
    todo_lines = [n for n, line in visible if re.search(r"\bTODO\b", line)]
    for n in todo_lines:
        add("warning", "todo", "Unresolved TODO.", n)
    link_text = re.sub(r"(`+).*?\1", "", visible_text)
    wiki = list(re.finditer(r"(!?)\[\[([^\]]+)\]\]", link_text))
    all_files = [p for p in vault.rglob("*") if p.is_file() and not any(x in {".git", ".agents", ".codex"} for x in p.parts)]
    images = []
    for match in wiki:
        target = match[2].split("|", 1)[0].split("#", 1)[0].strip()
        if not target:
            continue
        path = Path(unquote(target).replace("\\", "/"))
        direct = [note.parent / path, vault / path]
        if not path.suffix:
            direct += [p.with_suffix(".md") for p in list(direct)]
        candidates = [p.resolve() for p in direct if p.is_file() and p.resolve().is_relative_to(vault)]
        if not candidates:
            candidates = [p for p in all_files if (p.name == path.name or
                          (not path.suffix and p.suffix == ".md" and p.stem == path.name))
                          and (len(path.parts) == 1 or p.as_posix().endswith(path.as_posix()))]
        candidates = sorted(set(candidates))
        if not candidates:
            add("error" if match[1] else "warning", "missing_embed" if match[1] else "missing_wikilink", f"Target does not exist: {target}")
        elif len(candidates) > 1:
            add("warning", "ambiguous_link", f"Multiple files match: {target}")
        elif match[1] and candidates[0].suffix.lower() in IMAGE_EXTENSIONS:
            images.append(candidates[0])
            if candidates[0].parent != course / "imgs":
                add("warning", "image_location", f"Image is outside course/imgs: {target}")
    # Ordinary Markdown images are checked as well; remote images require manual inspection.
    for match in re.finditer(r"!\[[^\]]*\]\((<[^>]+>|[^\s)]+)(?:\s+[^)]*)?\)", link_text):
        target = unquote(match[1].strip("<>"))
        if re.match(r"https?://", target):
            add("warning", "remote_image", f"Remote image cannot be audited locally: {target}")
            continue
        path = (note.parent / target).resolve()
        if not path.is_relative_to(vault) or not path.is_file():
            add("error", "missing_embed", f"Markdown image does not exist inside vault: {target}")
        else:
            images.append(path)
    duplicate_names = [name for name, count in Counter(str(p) for p in images).items() if count > 1]
    for name in duplicate_names:
        add("warning", "repeated_image", f"Image embedded multiple times: {name}")
    image_hashes = Counter(digest(p) for p in set(images))
    if any(count > 1 for count in image_hashes.values()):
        add("warning", "duplicate_image_content", "Different filenames contain identical image bytes.")
    word_count = len(re.findall(r"\b\w+\b", re.sub(r"!\[\[[^\]]+\]\]", "", visible_text)))
    if len(images) > 2 and word_count / len(images) < 100:
        add("warning", "image_density", "Less than 100 text words per image: inspect visual load. This is not a hard limit.")

    changed = []
    if args.baseline:
        baseline = json.loads(Path(args.baseline).read_text(encoding="utf-8"))
        if Path(baseline["course"]).resolve() != course:
            raise ValueError("Baseline belongs to another course.")
        now, before = inventory(course), baseline["files"]
        allowed_images = {Path(p).resolve() for p in args.allowed_images}
        for rel in sorted(set(now) | set(before)):
            if now.get(rel) == before.get(rel):
                continue
            kind = "added" if rel not in before else "deleted" if rel not in now else "modified"
            changed.append({"path": rel, "change": kind})
            full = course / rel
            allowed = full == note or (kind == "added" and full.parent == course / "imgs"
                                      and full.suffix.lower() in IMAGE_EXTENSIONS)
            allowed = allowed or (kind == "modified" and full in allowed_images and full.parent == course / "imgs")
            if not allowed:
                add("error", "unexpected_change", f"Out-of-scope {kind}: {rel}")
        if args.expect_no_change and changed:
            add("error", "idempotence", "Changes were found although zero changes were expected.")

    if args.coverage:
        coverage = json.loads(Path(args.coverage).read_text(encoding="utf-8"))
        for page in coverage["pages"]:
            label = f"Source {page['source']} / page {page['page']}"
            if page.get("status") not in {"covered", "duplicate", "irrelevant", "todo"}:
                add("warning", "coverage_pending", f"{label}: coverage not finalized.")
            if page.get("status") == "covered" and not page.get("destination_sections"):
                add("warning", "coverage_destination", f"{label}: no destination section recorded.")
            if page.get("status") in {"duplicate", "irrelevant"} and not page.get("reason"):
                add("warning", "coverage_reason", f"{label}: explain why it is duplicate or irrelevant.")
            if page.get("review_reasons") and not page.get("visual_reviewed"):
                add("warning", "visual_pending", f"{label}: flagged visual content was not inspected.")

    result = {"note": str(note), "state": state if isinstance(state, (str, type(None))) else repr(state),
              "errors": sum(f["severity"] == "error" for f in findings),
              "warnings": sum(f["severity"] == "warning" for f in findings), "findings": findings,
              "metrics": {"headings": len(headings), "words_outside_code": word_count,
                          "images": len(images), "todos": len(todo_lines)}, "changes": changed,
              "seconds": round(time.perf_counter() - started, 3)}
    if args.report:
        save_temporary(args.report, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result["errors"] else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    s = sub.add_parser("snapshot", help="Save a read-only baseline of course files")
    s.add_argument("--course", required=True)
    s.add_argument("--output", required=True, help="JSON inside the system temporary directory")
    a = sub.add_parser("check", help="Inspect a note without editing it")
    a.add_argument("--course", required=True)
    a.add_argument("--note", required=True)
    a.add_argument("--vault", help="Vault root for resolving cross-course wikilinks")
    a.add_argument("--mode", choices=STATES, help="Omit for a no-op update preserving the earlier state")
    a.add_argument("--baseline")
    a.add_argument("--allowed-images", nargs="*", default=[], help="Explicitly authorized existing image replacements")
    a.add_argument("--expect-no-change", action="store_true")
    a.add_argument("--coverage")
    a.add_argument("--report", help="Optional temporary JSON report")
    args = parser.parse_args()
    try:
        if args.command == "snapshot":
            course = Path(args.course).resolve(strict=True)
            save_temporary(args.output, {"course": str(course), "files": inventory(course)})
            print(json.dumps({"snapshot": str(Path(args.output).resolve())}))
            return 0
        if args.expect_no_change and not args.baseline:
            raise ValueError("--expect-no-change requires --baseline.")
        return audit(args)
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as exc:
        parser.exit(2, f"Error: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
