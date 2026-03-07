import json
import os
from flask import session

TRANSLATIONS_DIR = os.path.join(os.path.dirname(__file__), "translations")
SUPPORTED_LANGS  = ("en", "ka")
DEFAULT_LANG     = "en"


def load_translations(lang: str) -> dict:
    """Load and return the translation dict for *lang*.
    Falls back to English if the file is missing or the lang is unsupported.
    """
    if lang not in SUPPORTED_LANGS:
        lang = DEFAULT_LANG

    path = os.path.join(TRANSLATIONS_DIR, f"{lang}.json")
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # Fallback: try English
        fallback = os.path.join(TRANSLATIONS_DIR, "en.json")
        with open(fallback, encoding="utf-8") as f:
            return json.load(f)


def get_current_lang() -> str:
    """Return the active language code stored in the session."""
    return session.get("lang", DEFAULT_LANG)
