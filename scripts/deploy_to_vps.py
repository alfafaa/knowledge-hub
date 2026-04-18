#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import tarfile
from pathlib import Path
from typing import Any

import yaml


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def dump_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def extract_package(package_path: Path, destination_root: Path) -> int:
    destination_root.mkdir(parents=True, exist_ok=True)
    with tarfile.open(package_path, "r:gz") as tar:
        tar.extractall(path=destination_root)
    return sum(1 for item in destination_root.rglob("*") if item.is_file())


def rotate_previous(target_dir: Path) -> Path | None:
    if not target_dir.exists():
        return None
    previous_dir = target_dir.parent / f"{target_dir.name}-previous"
    if previous_dir.exists():
        shutil.rmtree(previous_dir)
    target_dir.rename(previous_dir)
    return previous_dir


def main() -> int:
    parser = argparse.ArgumentParser(description="Deploy packaged knowledge hub targets into VPS-style directories.")
    parser.add_argument("--config", default="deploy.vps.yaml", help="VPS deployment config")
    parser.add_argument(
        "--execution-report",
        default="build/deploy/deploy-execution-report.json",
        help="Path to deployment execution report",
    )
    parser.add_argument(
        "--report-out",
        default="build/deploy/vps-deploy-report.json",
        help="Path to write VPS deployment report",
    )
    args = parser.parse_args()

    workspace_root = Path.cwd().resolve()
    config = load_yaml((workspace_root / args.config).resolve())
    execution = load_json((workspace_root / args.execution_report).resolve())

    deploy_root = (workspace_root / config.get("deploy_root", "deploy/runtime")).resolve()
    target_config = config.get("targets", {})

    deployed = []
    skipped = []

    for item in execution.get("packaged", []):
        target_name = item.get("target")
        cfg = target_config.get(target_name, {})
        if not cfg.get("enabled", False):
            skipped.append({"target": target_name, "reason": "target disabled in deploy.vps.yaml"})
            continue

        package_rel = item.get("package")
        if not package_rel:
            skipped.append({"target": target_name, "reason": "missing package path"})
            continue

        package_path = (workspace_root / package_rel).resolve()
        if not package_path.exists():
            skipped.append({"target": target_name, "reason": "package not found"})
            continue

        deploy_to = cfg.get("deploy_to")
        if not isinstance(deploy_to, str) or not deploy_to:
            skipped.append({"target": target_name, "reason": "missing deploy_to path"})
            continue

        final_target = deploy_root / deploy_to
        extracted_root = final_target.parent / f"{final_target.name}-incoming"

        if extracted_root.exists():
            shutil.rmtree(extracted_root)
        extracted_root.mkdir(parents=True, exist_ok=True)

        file_count = extract_package(package_path, extracted_root)
        previous = None
        if cfg.get("preserve_previous", True):
            previous = rotate_previous(final_target)
        elif final_target.exists():
            shutil.rmtree(final_target)

        extracted_root.rename(final_target)

        deployed.append(
            {
                "target": target_name,
                "environment": item.get("environment"),
                "package": package_rel,
                "deployed_to": str(final_target.relative_to(workspace_root)),
                "previous_path": str(previous.relative_to(workspace_root)) if previous else None,
                "files": file_count,
            }
        )

    for skipped_item in execution.get("skipped", []):
        skipped.append(skipped_item)

    report = {
        "displayName": config.get("display_name"),
        "deploy_root": str(deploy_root.relative_to(workspace_root)),
        "deployed": deployed,
        "skipped": skipped,
    }
    dump_json((workspace_root / args.report_out).resolve(), report)
    print(f"vps deploy complete: deployed={len(deployed)} skipped={len(skipped)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
