#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

from sync_lib import dump_json, load_yaml


def relative_to_hub(destination: str) -> str:
    prefix = "hub/"
    if destination.startswith(prefix):
        return destination[len(prefix) :]
    return destination


def should_include(item: dict[str, Any], target: str) -> bool:
    if not item.get("publish"):
        return False
    return target in item.get("publish_targets", [])


def stage_mirrored_content(workspace_root: Path, target_root: Path, item: dict[str, Any]) -> str | None:
    destination = item.get("destination")
    if not destination:
        return None
    source_path = workspace_root / destination
    if not source_path.exists():
        return None
    rel = relative_to_hub(destination)
    staged_path = target_root / rel
    staged_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_path, staged_path)
    return str(staged_path.relative_to(workspace_root))


def generate_catalog_page(workspace_root: Path, target_root: Path, item: dict[str, Any]) -> str | None:
    destination = item.get("destination")
    if not destination:
        return None

    rel = relative_to_hub(destination)
    staged_path = target_root / rel
    staged_path.parent.mkdir(parents=True, exist_ok=True)

    frontmatter_lines = [
        "---",
        f"id: {item.get('id') or 'catalog-entry'}",
        f"title: {item.get('title') or 'Catalog Entry'}",
        "type: reference",
        f"audience: {item.get('audience') or 'internal'}",
        f"visibility: {item.get('visibility') or 'internal'}",
        "status: active",
        f"owner: {item.get('repo_name') or 'unknown-repo'}",
        "publish: true",
        f"summary: Generated catalog page for {item.get('source')}.",
        "---",
        "",
        f"# {item.get('title') or 'Catalog Entry'}",
        "",
        "## Catalog Entry",
        "",
        "This page was generated from an `indexed-only` document.",
        "",
        f"- Source repo: `{item.get('repo_name') or 'unknown-repo'}`",
        f"- Source path: `{item.get('source') or ''}`",
        f"- Intended hub destination: `{item.get('destination') or ''}`",
        f"- Type: `{item.get('type') or 'unknown'}`",
        f"- Audience: `{item.get('audience') or 'unknown'}`",
        f"- Visibility: `{item.get('visibility') or 'unknown'}`",
    ]

    if item.get("product"):
        frontmatter_lines.append(f"- Product: `{item['product']}`")
    if item.get("project"):
        frontmatter_lines.append(f"- Project: `{item['project']}`")

    frontmatter_lines.extend(
        [
            "",
            "## Note",
            "",
            "The full content has not been mirrored into this site yet. This entry exists so the document remains discoverable in audience-specific builds.",
            "",
        ]
    )

    staged_path.write_text("\n".join(frontmatter_lines), encoding="utf-8")
    return str(staged_path.relative_to(workspace_root))


def load_catalog(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    data = load_yaml(path)
    if not isinstance(data, dict):
        return []
    items = data.get("items", [])
    return items if isinstance(items, list) else []


def main() -> int:
    parser = argparse.ArgumentParser(description="Create audience-specific publish manifests and staged content.")
    parser.add_argument("--hub-config", default="hub.config.yaml", help="Path to hub runtime config")
    parser.add_argument(
        "--catalog-path",
        default="hub/98-meta/publishing/indexed-docs-catalog.json",
        help="Path to indexed docs catalog",
    )
    parser.add_argument("--build-root", default="build", help="Build output root")
    args = parser.parse_args()

    workspace_root = Path.cwd().resolve()
    hub_config = load_yaml((workspace_root / args.hub_config).resolve())
    catalog_items = load_catalog((workspace_root / args.catalog_path).resolve())
    build_root = (workspace_root / args.build_root).resolve()
    manifests_root = build_root / "manifests"
    sites_root = build_root / "sites"

    manifests_root.mkdir(parents=True, exist_ok=True)
    sites_root.mkdir(parents=True, exist_ok=True)

    summary: dict[str, Any] = {
        "display_name": hub_config.get("display_name"),
        "targets": {},
    }

    for target in hub_config.get("publish_targets", []):
        target_site_root = sites_root / target / "content"
        if target_site_root.exists():
            shutil.rmtree(target_site_root)
        target_site_root.mkdir(parents=True, exist_ok=True)

        items_for_target = []
        mirrored_count = 0
        generated_count = 0
        catalog_only_count = 0

        for item in catalog_items:
            if not should_include(item, target):
                continue

            entry = {
                "id": item.get("id"),
                "title": item.get("title"),
                "type": item.get("type"),
                "repo_name": item.get("repo_name"),
                "source": item.get("source"),
                "destination": item.get("destination"),
                "action": item.get("action"),
                "audience": item.get("audience"),
                "visibility": item.get("visibility"),
                "product": item.get("product"),
                "project": item.get("project"),
                "publish_targets": item.get("publish_targets", []),
                "staged_content": None,
                "stage_status": "catalog-only",
            }

            if item.get("action") in {"mirrored", "mirrored-asset"}:
                staged = stage_mirrored_content(workspace_root, target_site_root, item)
                if staged:
                    entry["staged_content"] = staged
                    entry["stage_status"] = "staged"
                    mirrored_count += 1
                else:
                    entry["stage_status"] = "missing-mirrored-source"
            else:
                staged = generate_catalog_page(workspace_root, target_site_root, item)
                if staged:
                    entry["staged_content"] = staged
                    entry["stage_status"] = "generated-catalog-page"
                    generated_count += 1
                else:
                    catalog_only_count += 1

            items_for_target.append(entry)

        manifest = {
            "display_name": hub_config.get("display_name"),
            "publish_target": target,
            "site_content_root": str((sites_root / target / "content").relative_to(workspace_root)),
            "items": items_for_target,
            "counts": {
                "total": len(items_for_target),
                "staged": mirrored_count,
                "generated_catalog_pages": generated_count,
                "catalog_only": catalog_only_count,
            },
        }
        dump_json(manifest, manifests_root / f"{target}.json")
        summary["targets"][target] = manifest["counts"]

    dump_json(summary, manifests_root / "summary.json")
    print(f"publish planning complete: manifests={manifests_root.relative_to(workspace_root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
