#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

import yaml


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def ensure_clean_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def copy_tree_contents(source: Path, target: Path) -> int:
    if not source.exists():
        return 0
    count = 0
    for item in source.rglob("*"):
        if not item.is_file():
            continue
        rel = item.relative_to(source)
        dest = target / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, dest)
        count += 1
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare Quartz-ready workspaces from staged site content.")
    parser.add_argument("--hub-config", default="hub.config.yaml", help="Path to hub runtime config")
    parser.add_argument("--build-root", default="build", help="Build output root")
    parser.add_argument("--quartz-root", default="quartz", help="Quartz workspace root")
    args = parser.parse_args()

    workspace_root = Path.cwd().resolve()
    hub_config = yaml.safe_load((workspace_root / args.hub_config).read_text(encoding="utf-8"))
    build_root = workspace_root / args.build_root
    quartz_root = workspace_root / args.quartz_root
    workspaces_root = quartz_root / "workspaces"

    summary: dict[str, Any] = {
        "displayName": hub_config.get("display_name"),
        "targets": {},
    }

    for target in hub_config.get("publish_targets", []):
        manifest_path = build_root / "manifests" / f"{target}.json"
        if not manifest_path.exists():
            continue

        manifest = load_json(manifest_path)
        source_content_root = workspace_root / manifest["site_content_root"]
        target_workspace = workspaces_root / target
        target_content_root = target_workspace / "content"

        ensure_clean_dir(target_workspace)
        file_count = copy_tree_contents(source_content_root, target_content_root)

        site_config = {
            "displayName": hub_config.get("display_name"),
            "target": target,
            "contentRoot": "content",
            "sourceManifest": str(manifest_path.relative_to(workspace_root)),
            "sourceContentRoot": str(source_content_root.relative_to(workspace_root)),
            "generatedFiles": file_count,
        }
        dump_json(target_workspace / "site.config.json", site_config)

        summary["targets"][target] = {
          "workspace": str(target_workspace.relative_to(workspace_root)),
          "generatedFiles": file_count,
        }

    dump_json(quartz_root / "workspace-summary.json", summary)
    print(f"quartz workspace prepared: {workspaces_root.relative_to(workspace_root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
