#!/usr/bin/env python3
"""Lightweight publication-figure export audit.

This script uses only the Python standard library. It catches common file-level
issues, but it cannot replace visual inspection in the final paper template.
"""

from __future__ import annotations

import argparse
import html
import re
import struct
import sys
from pathlib import Path


VECTOR_EXTS = {".pdf", ".svg", ".eps", ".ps"}
RASTER_EXTS = {".png", ".tif", ".tiff", ".jpg", ".jpeg"}
ACCEPTED_EXTS = VECTOR_EXTS | RASTER_EXTS | {".emf"}
TEXT_OVERLAP_LIMIT = 12


def _fmt_bytes(size: int) -> str:
    units = ["B", "KB", "MB", "GB"]
    value = float(size)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} B"
        value /= 1024
    return f"{size} B"


def _png_size(data: bytes) -> tuple[int, int] | None:
    if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 24:
        return struct.unpack(">II", data[16:24])
    return None


def _jpeg_size(data: bytes) -> tuple[int, int] | None:
    if not data.startswith(b"\xff\xd8"):
        return None
    i = 2
    while i + 9 < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        i += 2
        if marker in {0xD8, 0xD9}:
            continue
        if i + 2 > len(data):
            return None
        length = struct.unpack(">H", data[i : i + 2])[0]
        if marker in range(0xC0, 0xC4) or marker in range(0xC5, 0xC8) or marker in range(0xC9, 0xCC) or marker in range(0xCD, 0xD0):
            if i + 7 < len(data):
                height, width = struct.unpack(">HH", data[i + 3 : i + 7])
                return width, height
        i += max(length, 2)
    return None


def _attr_value(tag: str, name: str) -> str | None:
    match = re.search(rf"\b{name}\s*=\s*['\"]([^'\"]+)['\"]", tag, flags=re.IGNORECASE)
    return match.group(1) if match else None


def _first_number(value: str | None) -> float | None:
    if not value:
        return None
    match = re.search(r"-?\d+(?:\.\d+)?", value)
    return float(match.group(0)) if match else None


def _svg_font_size(tag: str) -> float:
    style = _attr_value(tag, "style") or ""
    match = re.search(r"font-size\s*:\s*(-?\d+(?:\.\d+)?)", style, flags=re.IGNORECASE)
    if match:
        return max(float(match.group(1)), 1.0)
    return max(_first_number(_attr_value(tag, "font-size")) or 10.0, 1.0)


def _svg_text_anchor(tag: str) -> tuple[float | None, float | None]:
    x = _first_number(_attr_value(tag, "x"))
    y = _first_number(_attr_value(tag, "y"))
    transform = _attr_value(tag, "transform") or ""
    translate = re.search(
        r"translate\(\s*(-?\d+(?:\.\d+)?)(?:[,\s]+(-?\d+(?:\.\d+)?))?",
        transform,
        flags=re.IGNORECASE,
    )
    if translate:
        tx = float(translate.group(1))
        ty = float(translate.group(2) or 0.0)
        x = tx if x is None else x + tx
        y = ty if y is None else y + ty
    return x, y


def _svg_text_boxes(text: str) -> list[tuple[str, float, float, float, float]]:
    boxes: list[tuple[str, float, float, float, float]] = []
    for match in re.finditer(r"(<text\b[^>]*>)(.*?)</text>", text, flags=re.IGNORECASE | re.DOTALL):
        tag = match.group(1)
        raw_label = re.sub(r"<[^>]+>", "", match.group(2))
        label = html.unescape(raw_label).strip()
        if not label:
            continue
        x, y = _svg_text_anchor(tag)
        if x is None or y is None:
            continue
        font_size = _svg_font_size(tag)
        # Conservative text extent heuristic: enough to catch obvious collisions while avoiding
        # pretending this replaces rendered inspection.
        width = max(len(label), 1) * font_size * 0.58
        height = font_size * 1.25
        if "text-anchor: middle" in tag or 'text-anchor="middle"' in tag:
            x0 = x - width / 2
        elif "text-anchor: end" in tag or 'text-anchor="end"' in tag:
            x0 = x - width
        else:
            x0 = x
        boxes.append((label, x0, y - height, x0 + width, y + height * 0.25))
    return boxes


def _boxes_overlap(a: tuple[str, float, float, float, float], b: tuple[str, float, float, float, float]) -> bool:
    _, ax0, ay0, ax1, ay1 = a
    _, bx0, by0, bx1, by1 = b
    x_overlap = min(ax1, bx1) - max(ax0, bx0)
    y_overlap = min(ay1, by1) - max(ay0, by0)
    if x_overlap <= 0 or y_overlap <= 0:
        return False
    min_area = min((ax1 - ax0) * (ay1 - ay0), (bx1 - bx0) * (by1 - by0))
    return (x_overlap * y_overlap) / max(min_area, 1.0) > 0.18


def _svg_text_overlap_audit(text: str, warnings: list[str], notes: list[str]) -> None:
    boxes = _svg_text_boxes(text)
    if len(boxes) < 2:
        return
    overlaps: list[tuple[str, str]] = []
    for i, box_a in enumerate(boxes):
        for box_b in boxes[i + 1 :]:
            if _boxes_overlap(box_a, box_b):
                overlaps.append((box_a[0], box_b[0]))
                if len(overlaps) >= TEXT_OVERLAP_LIMIT:
                    break
        if len(overlaps) >= TEXT_OVERLAP_LIMIT:
            break
    if overlaps:
        sample = "; ".join(f"{a!r} vs {b!r}" for a, b in overlaps[:3])
        warnings.append(
            "Possible overlapping SVG text labels detected; inspect final-size output "
            f"and fix before calling the figure ready. Examples: {sample}."
        )
    else:
        notes.append("No obvious SVG text-label overlap detected by heuristic scan.")


def _svg_audit(text: str, warnings: list[str], notes: list[str]) -> None:
    lower = text.lower()
    if "<svg" not in lower:
        warnings.append("SVG header not found.")
    if "viewbox" not in lower:
        warnings.append("SVG has no viewBox; scaling/cropping may be brittle.")
    if re.search(r"<image\b", lower):
        notes.append("SVG contains raster <image> elements; verify embedded image DPI.")
    if re.search(r"(href|xlink:href)=[\"']https?://", lower):
        warnings.append("SVG references external network images; embed or localize them.")
    if "font-size" not in lower and "<text" in lower:
        notes.append("SVG has text but no explicit font-size; inspect final-size readability.")
    if re.search(r"font-size\s*:\s*([0-5](?:\.\d+)?)(?!\d)", lower):
        warnings.append("SVG may contain text below 6 pt/px; inspect readability.")
    if "#ff0000" in lower and ("#00ff00" in lower or "#008000" in lower):
        warnings.append("Red/green pair detected; add redundant encoding and test grayscale.")
    _svg_text_overlap_audit(text, warnings, notes)


def _pdf_audit(data: bytes, warnings: list[str], notes: list[str]) -> None:
    if not data.startswith(b"%PDF"):
        warnings.append("PDF header not found.")
    if b"/Font" in data:
        if not any(token in data for token in [b"/FontFile", b"/FontFile2", b"/FontFile3"]):
            notes.append("PDF uses fonts; embedded font files were not obvious in a quick scan.")
    if b"/Image" in data:
        notes.append("PDF contains raster images; verify their effective DPI at final size.")
    pages = len(re.findall(rb"/Type\s*/Page\b", data))
    if pages > 1:
        warnings.append(f"PDF appears to contain {pages} pages; a figure export is usually one page.")
    notes.append("PDF text overlap cannot be reliably detected by this lightweight audit; inspect rendered output.")


def audit_file(path: Path) -> int:
    warnings: list[str] = []
    notes: list[str] = []

    if not path.exists():
        print(f"[FAIL] {path}: file does not exist")
        return 1
    if not path.is_file():
        print(f"[FAIL] {path}: not a file")
        return 1

    ext = path.suffix.lower()
    size = path.stat().st_size
    data = path.read_bytes()

    if ext not in ACCEPTED_EXTS:
        warnings.append(f"Extension {ext or '<none>'} is not a common ACM/IEEE figure format.")
    if size < 1024:
        warnings.append("File is smaller than 1 KB; export may be empty or incomplete.")
    if size > 50 * 1024 * 1024:
        warnings.append("File is larger than 50 MB; submission systems may reject it.")

    if ext in {".jpg", ".jpeg"}:
        warnings.append("JPEG is usually unsuitable for plots/line art; prefer PDF/SVG/PNG/TIFF.")
    if ext in VECTOR_EXTS:
        notes.append("Vector-capable format detected.")
    if ext == ".svg":
        _svg_audit(data.decode("utf-8", errors="ignore"), warnings, notes)
    elif ext == ".pdf":
        _pdf_audit(data, warnings, notes)
    elif ext == ".png":
        dims = _png_size(data)
        if dims:
            notes.append(f"PNG dimensions: {dims[0]} x {dims[1]} px.")
            if dims[0] < 1050:
                notes.append("PNG width is below 1050 px; may be low for IEEE one-column raster output.")
        else:
            warnings.append("Could not read PNG dimensions.")
    elif ext in {".jpg", ".jpeg"}:
        dims = _jpeg_size(data)
        if dims:
            notes.append(f"JPEG dimensions: {dims[0]} x {dims[1]} px.")

    status = "PASS" if not warnings else "WARN"
    print(f"[{status}] {path} ({_fmt_bytes(size)})")
    for item in warnings:
        print(f"  warning: {item}")
    for item in notes:
        print(f"  note: {item}")
    return 0 if not warnings else 2


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Audit exported paper figure files.")
    parser.add_argument("figures", nargs="+", help="Figure export files to inspect")
    args = parser.parse_args(argv)

    exit_code = 0
    for name in args.figures:
        code = audit_file(Path(name))
        exit_code = max(exit_code, code)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
