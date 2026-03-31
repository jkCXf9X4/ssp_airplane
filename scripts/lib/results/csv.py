"""CSV helpers shared across result analysis commands."""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, List, Sequence


def numeric_series(
    rows: Sequence[Dict[str, str]], key: str, cast=float
) -> List[float]:
    values: List[float] = []
    for row in rows:
        raw = row.get(key, "")
        if raw is None:
            continue
        raw_str = str(raw).strip()
        if not raw_str:
            continue
        try:
            values.append(cast(raw_str))
        except ValueError:
            try:
                values.append(cast(raw_str.replace(",", "")))
            except ValueError:
                continue
    return values


def read_result_rows(result_file: Path) -> List[Dict[str, str]]:
    with result_file.open() as fh:
        reader = csv.DictReader(fh)
        return list(reader)


def series_from_candidates(
    rows: Sequence[Dict[str, str]], keys: Sequence[str], cast=float
) -> List[float]:
    for key in keys:
        series = numeric_series(rows, key, cast=cast)
        if series:
            return series
    return []
