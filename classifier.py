import os
from pathlib import Path
from PIL import Image
import io

# Optional zero-shot classification
try:
    from transformers import pipeline
    _zs = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
except Exception:
    _zs = None

DEFAULT_CANDIDATES = [
    "Photos", "Food and Recipes", "Financial", "Meetings and Notes",
    "Personal", "Travel", "Work", "Presentations", "Spreadsheets", "Misc"
]

IMAGE_EXT = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}
TEXT_EXT = {".txt", ".md"}
DOCX_EXT = {".docx"}
PDF_EXT = {".pdf"}
PPT_EXT = {".ppt", ".pptx"}
SHEET_EXT = {".xlsx", ".xls", ".csv"}

def _ext(fname):
    return os.path.splitext(fname)[1].lower()

def _text_from_pdf(path):
    try:
        import fitz
        doc = fitz.open(path)
        text = ""
        for i, page in enumerate(doc):
            text += page.get_text()
            if i >= 1:  # first two pages
                break
        return text
    except Exception:
        return ""

def _text_from_docx(path):
    try:
        import docx
        doc = docx.Document(path)
        return "\n".join(p.text for p in doc.paragraphs[:50])
    except Exception:
        return ""

def _image_color_heuristic(path):
    try:
        im = Image.open(path).convert("RGB").resize((64, 64))
        pixels = list(im.getdata())
        r = sum(p[0] for p in pixels) / len(pixels)
        g = sum(p[1] for p in pixels) / len(pixels)
        b = sum(p[2] for p in pixels) / len(pixels)
        if b > r*1.12 and b > g*1.12: return "Photos"
        if g > r*1.12 and g > b*1.12: return "Photos"
    except Exception:
        pass
    return None

def _keyword_category_from_text(text, fname):
    s = (fname + " " + (text or "")).lower()
    if any(x in s for x in ("budget", "invoice", "salary", "finance", "expense", "spreadsheet", "xlsx", "csv")):
        return "Financial"
    if any(x in s for x in ("recipe", "chocolate", "cook", "bake", "ingredient")):
        return "Food and Recipes"
    if any(x in s for x in ("meeting", "minutes", "notes", "agenda")):
        return "Meetings and Notes"
    if any(x in s for x in ("resume", "cv", "profile")):
        return "Personal"
    if any(x in s for x in ("vacation", "itinerary", "travel", "trip")):
        return "Travel"
    if any(x in s for x in ("project", "presentation", "ppt", "pptx", "proposal", "strategy")):
        return "Work"
    if any(x in s for x in ("log", "digital log", "logging")):
        return "Presentations"
    return None

def zero_shot_label(text, candidates=DEFAULT_CANDIDATES):
    if not _zs: return None
    try:
        out = _zs(text[:1000], candidate_labels=candidates)
        if out and "labels" in out:
            return out["labels"][0]
    except Exception:
        return None
    return None

def classify_file(temp_path: str, filename: str):
    ext = _ext(filename)
    fname = filename.lower()

    if ext in SHEET_EXT:
        return "Financial", ["spreadsheet"]
    if ext in PPT_EXT:
        return "Presentations", ["presentation"]
    if ext in PDF_EXT:
        text = _text_from_pdf(temp_path) or ""
        quick = _keyword_category_from_text(text, filename)
        if quick: return quick, ["pdf"]
        zs = zero_shot_label(text, DEFAULT_CANDIDATES)
        if zs: return zs, ["pdf", "zs:" + zs]
        return "Misc", ["pdf"]
    if ext in DOCX_EXT:
        text = _text_from_docx(temp_path) or ""
        quick = _keyword_category_from_text(text, filename)
        if quick: return quick, ["docx"]
        zs = zero_shot_label(text, DEFAULT_CANDIDATES)
        if zs: return zs, ["docx", "zs:" + zs]
        return "Documents", ["docx"]
    if ext in TEXT_EXT:
        try:
            with open(temp_path, "r", encoding="utf-8", errors="ignore") as f:
                txt = f.read(3000)
        except Exception:
            txt = ""
        quick = _keyword_category_from_text(txt, filename)
        if quick: return quick, ["text"]
        zs = zero_shot_label(txt or filename, DEFAULT_CANDIDATES)
        if zs: return zs, ["text", "zs:" + zs]
        return "Documents", ["text"]
    if ext in IMAGE_EXT:
        if any(k in fname for k in ("cake", "chocolate", "cookie", "dessert")):
            return "Food and Recipes", ["image", "food"]
        if any(k in fname for k in ("vacation", "trip", "travel", "beach")):
            return "Travel", ["image", "travel"]
        if any(k in fname for k in ("meeting", "office", "team", "work")):
            return "Work", ["image", "work"]
        col = _image_color_heuristic(temp_path)
        if col: return col, ["image", "auto_color"]
        quick = _keyword_category_from_text("", filename)
        if quick: return quick, ["fallback"]
        return "Photos", ["image", "photo"]

    # Fallback
    quick = _keyword_category_from_text("", filename)
    if quick: return quick, ["fallback"]
    return "Misc", ["unknown"]
