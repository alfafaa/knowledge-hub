#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from typing import Any

from sync_lib import compute_plans, dump_json, extract_asset_references, load_docs_config, load_yaml, parse_frontmatter


def load_existing_catalog(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"items": []}
    data = load_yaml(path)
    return data if isinstance(data, dict) else {"items": []}


def upsert_catalog_item(items: list[dict[str, Any]], item: dict[str, Any]) -> None:
    key = (item.get("repo_name"), item.get("source"))
    for idx, existing in enumerate(items):
        if (existing.get("repo_name"), existing.get("source")) == key:
            items[idx] = item
            return
    items.append(item)


def write_mirrored_file(source_repo_root: Path, workspace_root: Path, plan: dict[str, Any]) -> dict[str, Any]:
    source_path = source_repo_root / plan["source"]
    destination_path = workspace_root / plan["destination"]
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_path, destination_path)
    return {
        "source": plan["source"],
        "destination": plan["destination"],
        "action": "mirrored",
    }


def is_asset_candidate(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() != ".md"


def copy_linked_assets(
    source_repo_root: Path,
    workspace_root: Path,
    repo_name: str,
    plan: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    source_doc = source_repo_root / plan["source"]
    dest_doc = workspace_root / plan["destination"]
    asset_entries: list[dict[str, Any]] = []
    skipped_assets: list[dict[str, Any]] = []

    for ref in extract_asset_references(source_doc):
        source_asset = (source_doc.parent / ref).resolve()

        try:
            source_asset.relative_to(source_repo_root)
        except ValueError:
            skipped_assets.append({"source": plan["source"], "asset": ref, "reason": "asset path escapes repository root"})
            continue

        if not is_asset_candidate(source_asset):
            continue

        dest_asset = (dest_doc.parent / ref).resolve()
        dest_asset.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_asset, dest_asset)

        asset_entries.append(
            {
                "repo_name": repo_name,
                "source": source_asset.relative_to(source_repo_root).as_posix(),
                "destination": dest_asset.relative_to(workspace_root).as_posix(),
                "action": "mirrored-asset",
                "title": source_asset.name,
                "id": None,
                "type": "asset",
                "visibility": plan.get("visibility"),
                "audience": plan.get("audience"),
                "publish": plan.get("publish"),
                "publish_targets": plan.get("publish_targets", []),
                "product": plan.get("product"),
                "project": plan.get("project"),
                "linked_from": plan["source"],
            }
        )

    return asset_entries, skipped_assets


def catalog_entry(repo_name: str, frontmatter: dict[str, Any], plan: dict[str, Any]) -> dict[str, Any]:
    return {
        "repo_name": repo_name,
        "source": plan["source"],
        "destination": plan.get("destination"),
        "action": plan["action"],
        "title": frontmatter.get("title"),
        "id": frontmatter.get("id"),
        "type": frontmatter.get("type"),
        "visibility": plan.get("visibility"),
        "audience": plan.get("audience"),
        "publish": plan.get("publish"),
        "publish_targets": plan.get("publish_targets", []),
        "product": plan.get("product"),
        "project": plan.get("project"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest repository docs into the central hub.")
    parser.add_argument("--docs-root", required=True, help="Path to docs root")
    parser.add_argument("--config", help="Optional explicit docs.config.yaml path")
    parser.add_argument(
        "--catalog-path",
        default="hub/98-meta/publishing/indexed-docs-catalog.json",
        help="Path to indexed-docs catalog file",
    )
    parser.add_argument(
        "--report-path",
        default="hub/98-meta/publishing/last-ingestion-report.json",
        help="Path to write the ingestion report",
    )
    parser.add_argument(
        "--changed",
        nargs="*",
        help="Optional explicit list of changed files relative to repo root",
    )
    args = parser.parse_args()

    workspace_root = Path.cwd().resolve()
    docs_root = Path(args.docs_root).resolve()
    source_repo_root = docs_root.parent
    config_path = Path(args.config).resolve() if args.config else docs_root / "docs.config.yaml"
    config = load_docs_config(config_path, docs_root)
    repo_name = config.get("repo_name", "unknown-repo")

    plans = compute_plans(docs_root, config, args.changed)

    mirrored: list[dict[str, Any]] = []
    indexed: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    mirrored_assets: list[dict[str, Any]] = []
    skipped_assets: list[dict[str, Any]] = []

    catalog_path = (workspace_root / args.catalog_path).resolve()
    existing_catalog = load_existing_catalog(catalog_path)
    items = existing_catalog.get("items", [])
    if not isinstance(items, list):
        items = []

    for plan in plans:
        source_abs = source_repo_root / plan["source"]
        frontmatter = parse_frontmatter(source_abs) if source_abs.exists() else {}

        if plan["action"] == "skip":
            skipped.append(plan)
            continue

        if plan["action"] == "mirrored":
            mirrored.append(write_mirrored_file(source_repo_root, workspace_root, plan))
            if source_abs.suffix.lower() == ".md":
                asset_entries, asset_skips = copy_linked_assets(source_repo_root, workspace_root, repo_name, plan)
                mirrored_assets.extend(asset_entries)
                skipped_assets.extend(asset_skips)
                for asset_entry in asset_entries:
                    upsert_catalog_item(items, asset_entry)
        elif plan["action"] == "indexed-only":
            indexed.append(plan)
        elif plan["action"] == "local-only":
            skipped.append(plan)
            continue

        upsert_catalog_item(items, catalog_entry(repo_name, frontmatter, plan))

    existing_catalog["items"] = sorted(items, key=lambda item: (item.get("repo_name", ""), item.get("source", "")))
    dump_json(existing_catalog, catalog_path)

    report = {
        "repo_name": repo_name,
        "docs_root": str(docs_root),
        "mirrored_count": len(mirrored),
        "mirrored_asset_count": len(mirrored_assets),
        "indexed_count": len(indexed),
        "skipped_count": len(skipped),
        "mirrored": mirrored,
        "mirrored_assets": mirrored_assets,
        "indexed": indexed,
        "skipped": skipped,
        "skipped_assets": skipped_assets,
    }
    dump_json(report, (workspace_root / args.report_path).resolve())

    print(
        f"ingestion complete: mirrored={len(mirrored)} assets={len(mirrored_assets)} indexed={len(indexed)} skipped={len(skipped)} "
        f"catalog={catalog_path.relative_to(workspace_root)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
