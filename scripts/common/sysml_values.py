"""Shared helpers for interpreting SysML attribute literal values."""
from __future__ import annotations

import ast
from typing import Any, Optional


def parse_literal(value: Optional[str]) -> Optional[Any]:
    """Decode a SysML attribute string literal into a Python primitive/list."""
    if value is None:
        return None
    text = value.strip()
    if not text:
        return None
    try:
        return ast.literal_eval(text)
    except (ValueError, SyntaxError):
        pass
    if text.startswith('"') and text.endswith('"'):
        return text[1:-1]
    lowered = text.lower()
    if lowered in {"true", "false"}:
        return lowered == "true"
    try:
        if any(ch in text for ch in (".", "e", "E")):
            return float(text)
        return int(text)
    except ValueError:
        return text
