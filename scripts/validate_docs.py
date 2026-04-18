#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from sync_lib import extract_asset_references


FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


@dataclass
class Finding:
    severity: str
    path: str
    message: str


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def parse_frontmatter(path: Path) -> tuple[dict[str, Any] | None, str]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None, text
    data = yaml.safe_load(match.group(1)) or {}
    if not isinstance(data, dict):
        return {}, text
    return data, text


def is_markdown(path: Path) -> bool:
    return path.suffix.lower() == ".md"


def validate_date(value: Any) -> bool:
    if isinstance(value, dt.date):
        return True
    if not isinstance(value, str):
        return False
    try:
        dt.date.fromisoformat(value)
        return True
    except ValueError:
        return False


def validate_type(value: Any, expected: str) -> bool:
    if expected == "str":
        return isinstance(value, str)
    if expected == "bool":
        return isinstance(value, bool)
    if expected == "int":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "list":
        return isinstance(value, list)
    if expected == "date":
        return validate_date(value)
    return True


def add(finding_list: list[Finding], severity: str, path: Path, message: str) -> None:
    finding_list.append(Finding(severity=severity, path=str(path), message=message))


def is_asset_reference(ref: str) -> bool:
    suffix = Path(ref).suffix.lower()
    return bool(suffix) and suffix != ".md"


def validate_docs_config(path: Path, schema: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    try:
        data = load_yaml(path) or {}
    except Exception as exc:  # noqa: BLE001
        add(findings, "error", path, f"could not parse YAML: {exc}")
        return findings

    for field in schema["required_root_fields"]:
        if field not in data:
            add(findings, "error", path, f"missing required root field `{field}`")

    if findings:
        return findings

    repo_type = data.get("repo_type")
    if repo_type not in schema["allowed_repo_types"]:
        add(findings, "error", path, f"unsupported repo_type `{repo_type}`")

    docs_version = data.get("docs_version")
    if not isinstance(docs_version, int) or docs_version < 1:
        add(findings, "error", path, "docs_version must be an integer >= 1")

    defaults = data.get("defaults", {})
    for field in schema["required_defaults_fields"]:
        if field not in defaults:
            add(findings, "error", path, f"defaults missing `{field}`")

    if defaults:
        if defaults.get("sync_mode") not in schema["allowed_sync_modes"]:
            add(findings, "error", path, "defaults.sync_mode is invalid")
        if defaults.get("visibility") not in schema["allowed_visibility"]:
            add(findings, "error", path, "defaults.visibility is invalid")
        if defaults.get("audience") not in schema["allowed_audience"]:
            add(findings, "error", path, "defaults.audience is invalid")
        publish_targets = defaults.get("publish_targets", [])
        if not isinstance(publish_targets, list):
            add(findings, "error", path, "defaults.publish_targets must be a list")
        else:
            for target in publish_targets:
                if target not in schema["allowed_publish_targets"]:
                    add(findings, "error", path, f"unsupported publish target `{target}`")

    sync = data.get("sync", {})
    for field in schema["required_sync_fields"]:
        if field not in sync:
            add(findings, "error", path, f"sync missing `{field}`")

    for field in ("include", "exclude"):
        values = sync.get(field, [])
        if not isinstance(values, list):
            add(findings, "error", path, f"sync.{field} must be a list")

    overrides = sync.get("overrides", {})
    if not isinstance(overrides, dict):
        add(findings, "error", path, "sync.overrides must be a mapping")

    destinations = sync.get("destinations", {})
    if destinations is not None and not isinstance(destinations, dict):
        add(findings, "error", path, "sync.destinations must be a mapping")
    elif isinstance(destinations, dict):
        for pattern, dest in destinations.items():
            if not isinstance(dest, dict):
                add(findings, "error", path, f"sync.destinations[{pattern!r}] must be a mapping")
                continue
            hub_path = dest.get("hub_path")
            if not isinstance(hub_path, str) or not hub_path.startswith("hub/"):
                add(findings, "error", path, f"sync.destinations[{pattern!r}].hub_path must start with `hub/`")

    approval = data.get("approval", {}).get("required_for", {})
    for field in schema["required_approval_flags"]:
        if field not in approval:
            add(findings, "error", path, f"approval.required_for missing `{field}`")

    ownership = data.get("ownership", {})
    for field in schema["required_ownership_fields"]:
        if field not in ownership:
            add(findings, "error", path, f"ownership missing `{field}`")

    return findings


def validate_asset_links(path: Path, repo_root: Path, is_publishable: bool) -> list[Finding]:
    findings: list[Finding] = []
    severity = "error" if is_publishable else "warning"

    for ref in extract_asset_references(path):
        if not is_asset_reference(ref):
            continue

        resolved = (path.parent / ref).resolve()
        try:
            resolved.relative_to(repo_root)
        except ValueError:
            add(findings, severity, path, f"asset reference escapes repository root: `{ref}`")
            continue

        if not resolved.exists():
            add(findings, severity, path, f"linked asset not found: `{ref}`")
            continue

        if not resolved.is_file():
            add(findings, severity, path, f"linked asset is not a file: `{ref}`")

    return findings


def validate_frontmatter(path: Path, schema: dict[str, Any], repo_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    fm, _ = parse_frontmatter(path)
    if fm is None:
        add(findings, "error", path, "missing YAML frontmatter")
        return findings

    for field in schema["required_fields"]:
        if field not in fm:
            add(findings, "error", path, f"missing required field `{field}`")

    publish_value = fm.get("publish")
    is_publishable = publish_value is True
    visibility = fm.get("visibility")
    is_governed = is_publishable and visibility in {"public", "restricted"}

    if is_publishable:
        for field in schema.get("publish_required_fields", []):
            if field not in fm:
                add(findings, "error", path, f"missing required publish field `{field}`")

    if is_governed:
        for field in schema.get("governed_required_fields", []):
            if field not in fm:
                add(findings, "error", path, f"missing required governed field `{field}`")

    for field, expected in schema.get("field_types", {}).items():
        if field in fm and not validate_type(fm[field], expected):
            add(findings, "error", path, f"field `{field}` has invalid type, expected `{expected}`")

    for field, allowed in schema.get("enums", {}).items():
        if field in fm and fm[field] not in allowed:
            add(findings, "error", path, f"field `{field}` has invalid value `{fm[field]}`")

    publish_targets = fm.get("publish_targets", [])
    if publish_targets is not None:
        if not isinstance(publish_targets, list):
            add(findings, "error", path, "`publish_targets` must be a list")
        else:
            for target in publish_targets:
                if target not in schema["publish_targets"]:
                    add(findings, "error", path, f"unsupported publish target `{target}`")

    findings.extend(validate_asset_links(path, repo_root, is_publishable))

    return findings


def iter_markdown_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*.md") if path.is_file())


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate docs config and markdown frontmatter.")
    parser.add_argument("--docs-root", required=True, help="Path to a repo docs root, e.g. examples/sample-project-repo/docs")
    parser.add_argument(
        "--config",
        help="Optional explicit docs.config.yaml path. Defaults to <docs-root>/docs.config.yaml.",
    )
    parser.add_argument(
        "--schema-dir",
        default="schemas",
        help="Directory containing frontmatter and docs-config schemas.",
    )
    args = parser.parse_args()

    docs_root = Path(args.docs_root).resolve()
    repo_root = docs_root.parent
    config_path = Path(args.config).resolve() if args.config else docs_root / "docs.config.yaml"
    schema_dir = Path(args.schema_dir).resolve()

    config_schema = load_yaml(schema_dir / "docs-config-schema.yaml")
    frontmatter_schema = load_yaml(schema_dir / "frontmatter-schema.yaml")

    findings: list[Finding] = []

    if not docs_root.exists():
        print(f"error: docs root not found: {docs_root}", file=sys.stderr)
        return 2

    if not config_path.exists():
        add(findings, "error", config_path, "docs config file not found")
    else:
        findings.extend(validate_docs_config(config_path, config_schema))

    for md_file in iter_markdown_files(docs_root):
        findings.extend(validate_frontmatter(md_file, frontmatter_schema, repo_root))

    error_count = sum(1 for item in findings if item.severity == "error")
    warning_count = sum(1 for item in findings if item.severity == "warning")

    for item in findings:
        print(f"{item.severity}: {item.path}: {item.message}")

    print(f"summary: {error_count} error(s), {warning_count} warning(s)")
    return 1 if error_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
