"""Lightweight SysML v2 folder parser used by helper scripts and tests.

The repository keeps the textual SysML architecture split across several
`.sysml` files (package metadata, requirements, part definitions, port payloads,
connections, etc.).  Tools such as the SSD generator or verification scripts
often need a consolidated view of the system without depending on the full
PySysML parser.  This module provides a minimal parser that:

* walks a directory and loads every `.sysml` file,
* validates that they target the same package,
* merges their contents into a single text representation, and
* exposes structured access to part definitions, port payload schemas,
  requirements, and connections.

The implementation intentionally understands only the subset of SysML syntax used
in this repository.  It is not a general-purpose parser but is sufficient for
unit tests and helper tooling.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, is_dataclass
from pathlib import Path
import re
from typing import Dict, Iterable, Iterator, List, Optional, Sequence, Tuple

__all__ = [
    "SysMLAttribute",
    "SysMLPortEndpoint",
    "SysMLPartReference",
    "SysMLPartDefinition",
    "SysMLPortDefinition",
    "SysMLRequirement",
    "SysMLConnection",
    "SysMLArchitecture",
    "SysMLFolderParser",
    "parse_sysml_folder",
]


def _to_jsonable(value):
    if is_dataclass(value):
        return {
            field_name: _to_jsonable(getattr(value, field_name))
            for field_name in value.__dataclass_fields__
        }
    if isinstance(value, dict):
        return {str(key): _to_jsonable(val) for key, val in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_to_jsonable(item) for item in value]
    if isinstance(value, Path):
        return str(value)
    return value


def _json_dumps(value) -> str:
    return json.dumps(_to_jsonable(value), indent=2, sort_keys=True)


@dataclass
class SysMLAttribute:
    name: str
    type: Optional[str] = None
    value: Optional[str] = None
    doc: Optional[str] = None

    def __str__(self) -> str:
        return _json_dumps(self)


@dataclass
class SysMLPartReference:
    name: str
    target: str
    doc: Optional[str] = None

    def __str__(self) -> str:
        return _json_dumps(self)


@dataclass
class SysMLPortDefinition:
    name: str
    doc: Optional[str] = None
    attributes: Dict[str, SysMLAttribute] = field(default_factory=dict)

    def __str__(self) -> str:
        return _json_dumps(self)


@dataclass
class SysMLPortEndpoint:
    name: str
    direction: str  # "in" or "out"
    payload: str
    doc: Optional[str] = None
    payload_def: Optional["SysMLPortDefinition"] = None

    def __str__(self) -> str:
        return _json_dumps(self)


@dataclass
class SysMLPartDefinition:
    name: str
    doc: Optional[str] = None
    attributes: Dict[str, SysMLAttribute] = field(default_factory=dict)
    ports: List[SysMLPortEndpoint] = field(default_factory=list)
    parts: List[SysMLPartReference] = field(default_factory=list)

    def __str__(self) -> str:
        return _json_dumps(self)


@dataclass
class SysMLRequirement:
    identifier: str
    text: str

    def __str__(self) -> str:
        return _json_dumps(self)


@dataclass
class SysMLConnection:
    src_component: str
    src_port: str
    dst_component: str
    dst_port: str

    def __str__(self) -> str:
        return _json_dumps(self)


@dataclass
class SysMLArchitecture:
    package: str
    parts: Dict[str, SysMLPartDefinition]
    port_definitions: Dict[str, SysMLPortDefinition]
    requirements: List[SysMLRequirement]
    connections: List[SysMLConnection]

    def part(self, name: str) -> SysMLPartDefinition:
        return self.parts[name]

    def port(self, name: str) -> SysMLPortDefinition:
        return self.port_definitions[name]

    def __str__(self) -> str:
        return _json_dumps(self)


class SysMLFolderParser:
    """Parse and merge all `.sysml` files within a directory."""

    def __init__(self, folder: Path | str):
        self.folder = Path(folder)
        if not self.folder.is_dir():
            raise FileNotFoundError(f"SysML folder not found: {self.folder}")

    def parse(self) -> SysMLArchitecture:
        files = sorted(self.folder.glob("*.sysml"))
        if not files:
            raise FileNotFoundError(f"No .sysml files found under {self.folder}")

        parts: Dict[str, SysMLPartDefinition] = {}
        port_defs: Dict[str, SysMLPortDefinition] = {}
        requirements: List[SysMLRequirement] = []
        connections: List[SysMLConnection] = []
        package_sections: List[str] = []
        package_name: Optional[str] = None

        for path in files:
            text = path.read_text()
            pkg, body = _extract_package_body(text, path)
            if package_name is None:
                package_name = pkg
            elif pkg != package_name:
                raise ValueError(
                    f"Mismatched package names: {package_name} vs {pkg} in {path}"
                )
            package_sections.append(body.strip())

            for name, block in _extract_named_blocks(body, "part def"):
                if name in parts:
                    raise ValueError(f"Duplicate part definition for {name} in {path}")
                parts[name] = _parse_part_block(name, block)

            for name, block in _extract_named_blocks(body, "port def"):
                if name in port_defs:
                    raise ValueError(f"Duplicate port definition for {name} in {path}")
                port_defs[name] = _parse_port_block(name, block)

            requirements.extend(_parse_requirements(body))
            connections.extend(_parse_connections(body))

        _attach_port_definitions(parts, port_defs)
        return SysMLArchitecture(
            package=package_name or "Package",
            parts=parts,
            port_definitions=port_defs,
            requirements=requirements,
            connections=connections,
        )


def parse_sysml_folder(folder: Path | str) -> SysMLArchitecture:
    """Convenience helper mirroring `SysMLFolderParser(folder).parse()`."""
    return SysMLFolderParser(folder).parse()


# ---------------------------------------------------------------------------
# Parsing helpers


_PACKAGE_RE = re.compile(r"package\s+([A-Za-z0-9_]+)\s*\{", re.MULTILINE)


def _extract_package_body(text: str, path: Path) -> Tuple[str, str]:
    match = _PACKAGE_RE.search(text)
    if not match:
        raise ValueError(f"No package declaration found in {path}")
    pkg_name = match.group(1)
    brace_start = match.end() - 1
    body, _ = _collect_block(text, brace_start)
    return pkg_name, body


def _collect_block(text: str, brace_start: int) -> Tuple[str, int]:
    """Return the substring inside the curly braces starting at brace_start."""
    depth = 0
    body_start = brace_start + 1
    idx = brace_start
    while idx < len(text):
        char = text[idx]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[body_start:idx], idx + 1
        idx += 1
    raise ValueError("Unterminated block while parsing SysML text")


def _extract_named_blocks(body: str, keyword: str) -> List[Tuple[str, str]]:
    pattern = re.compile(rf"{keyword}\s+([A-Za-z0-9_]+)\s*\{{", re.MULTILINE)
    blocks: List[Tuple[str, str]] = []
    idx = 0
    while True:
        match = pattern.search(body, idx)
        if not match:
            break
        name = match.group(1)
        brace_start = match.end() - 1
        block, new_idx = _collect_block(body, brace_start)
        blocks.append((name, block))
        idx = new_idx
    return blocks


def _parse_part_block(name: str, block: str) -> SysMLPartDefinition:
    attributes: Dict[str, SysMLAttribute] = {}
    ports: List[SysMLPortEndpoint] = []
    parts: List[SysMLPartReference] = []
    pending_doc: Optional[str] = None
    part_doc: Optional[str] = None

    for kind, payload in _iter_block_items(block):
        if kind == "doc":
            # First doc before any statements becomes the part-level description.
            if part_doc is None and not attributes and not ports and not parts:
                part_doc = payload
            else:
                pending_doc = payload
            continue

        line = _strip_inline_comment(payload)
        if not line:
            continue

        if line.startswith("attribute "):
            attr = _parse_attribute(line, pending_doc)
            attributes[attr.name] = attr
        elif line.startswith("in port "):
            ports.append(_parse_port_endpoint("in", line, pending_doc))
        elif line.startswith("out port "):
            ports.append(_parse_port_endpoint("out", line, pending_doc))
        elif line.startswith("part "):
            parts.append(_parse_part_reference(line, pending_doc))

        pending_doc = None

    return SysMLPartDefinition(
        name=name, doc=part_doc, attributes=attributes, ports=ports, parts=parts
    )


def _parse_port_block(name: str, block: str) -> SysMLPortDefinition:
    attributes: Dict[str, SysMLAttribute] = {}
    port_doc: Optional[str] = None
    pending_doc: Optional[str] = None

    for kind, payload in _iter_block_items(block):
        if kind == "doc":
            if port_doc is None and not attributes:
                port_doc = payload
            else:
                pending_doc = payload
            continue

        line = _strip_inline_comment(payload)
        if not line:
            continue
        if line.startswith("attribute "):
            attr = _parse_attribute(line, pending_doc)
            attributes[attr.name] = attr
        pending_doc = None

    return SysMLPortDefinition(name=name, doc=port_doc, attributes=attributes)


def _parse_attribute(line: str, doc: Optional[str]) -> SysMLAttribute:
    content = line[len("attribute ") :].strip()
    if content.endswith(";"):
        content = content[:-1].strip()
    attr_type: Optional[str] = None
    value: Optional[str] = None
    if "=" in content:
        name, value = content.split("=", 1)
        name = name.strip()
        value = value.strip()
    elif ":" in content:
        name, attr_type = content.split(":", 1)
        name = name.strip()
        attr_type = attr_type.strip()
    else:
        name = content.strip()
    return SysMLAttribute(name=name, type=attr_type, value=value, doc=doc)


def _normalize_port_name(name: str) -> str:
    name = name.strip()
    if name.startswith("port "):
        return name[len("port ") :].strip()
    return name


def _parse_port_endpoint(
    direction: str, line: str, doc: Optional[str]
) -> SysMLPortEndpoint:
    content = line[len(direction) :].strip()
    if content.endswith(";"):
        content = content[:-1].strip()
    if ":" not in content:
        raise ValueError(f"Malformed port declaration: {line}")
    name, payload = content.split(":", 1)
    return SysMLPortEndpoint(
        direction=direction,
        name=_normalize_port_name(name),
        payload=payload.strip(),
        doc=doc,
    )


def _parse_part_reference(line: str, doc: Optional[str]) -> SysMLPartReference:
    content = line[len("part ") :].strip()
    if content.endswith(";"):
        content = content[:-1].strip()
    if ":" not in content:
        raise ValueError(f"Malformed part reference: {line}")
    name, target = content.split(":", 1)
    return SysMLPartReference(name=name.strip(), target=target.strip(), doc=doc)


def _strip_inline_comment(line: str) -> str:
    result = line
    while "/*" in result and "*/" in result:
        start = result.find("/*")
        end = result.find("*/", start + 2)
        if end == -1:
            break
        result = (result[:start] + result[end + 2 :]).strip()
    return result.strip()


def _attach_port_definitions(
    parts: Dict[str, SysMLPartDefinition], port_defs: Dict[str, SysMLPortDefinition]
) -> None:
    for part in parts.values():
        for port in part.ports:
            port.payload_def = port_defs.get(port.payload)


def _iter_block_items(block: str) -> Iterator[Tuple[str, str]]:
    lines = block.splitlines()
    idx = 0
    while idx < len(lines):
        raw = lines[idx].rstrip()
        stripped = raw.strip()
        idx += 1
        if not stripped:
            continue
        if stripped.startswith("doc"):
            doc_lines = [stripped]
            while "*/" not in stripped:
                if idx >= len(lines):
                    raise ValueError("Unterminated doc comment in SysML block")
                stripped = lines[idx].strip()
                doc_lines.append(stripped)
                idx += 1
            yield ("doc", _normalize_doc(" ".join(doc_lines)))
        else:
            yield ("stmt", stripped)


def _normalize_doc(text: str) -> str:
    start = text.find("/*")
    end = text.rfind("*/")
    slice_ = text[start + 2 : end] if start != -1 and end != -1 else text
    # Collapse repeated whitespace so doc strings remain compact.
    return re.sub(r"\s+", " ", slice_.strip())


def _parse_requirements(body: str) -> List[SysMLRequirement]:
    reqs: List[SysMLRequirement] = []
    pattern = re.compile(r"comment\s+([A-Za-z0-9_]+)\s*/\*\s*(.*?)\s*\*/", re.DOTALL)
    for match in pattern.finditer(body):
        identifier = match.group(1)
        text = re.sub(r"\s+", " ", match.group(2).strip())
        reqs.append(SysMLRequirement(identifier=identifier, text=text))
    return reqs


def _parse_connections(body: str) -> List[SysMLConnection]:
    connections: List[SysMLConnection] = []
    pattern = re.compile(
        r"connect\s+([A-Za-z0-9_]+)\.([A-Za-z0-9_]+)\s+to\s+([A-Za-z0-9_]+)\.([A-Za-z0-9_]+)\s*;",
        re.MULTILINE,
    )
    for match in pattern.finditer(body):
        connections.append(
            SysMLConnection(
                src_component=match.group(1),
                src_port=match.group(2),
                dst_component=match.group(3),
                dst_port=match.group(4),
            )
        )
    return connections
