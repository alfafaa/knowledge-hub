#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import tarfile
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def make_tarball(source_dir: Path, output_path: Path) -> int:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(output_path, "w:gz") as tar:
        for item in sorted(source_dir.rglob("*")):
            if not item.is_file():
                continue
            tar.add(item, arcname=str(item.relative_to(source_dir)))
    return sum(1 for _ in source_dir.rglob("*") if _.is_file())


def main() -> int:
    parser = argparse.ArgumentParser(description="Package allowed deployment targets from the deploy plan.")
    parser.add_argument("--plan", default="build/deploy/deploy-plan.json", help="Deploy plan path")
    parser.add_argument("--output-dir", default="build/deploy/packages", help="Package output directory")
    parser.add_argument(
        "--report",
        default="build/deploy/deploy-execution-report.json",
        help="Deployment execution report path",
    )
    args = parser.parse_args()

    workspace_root = Path.cwd().resolve()
    plan = load_json((workspace_root / args.plan).resolve())
    output_dir = (workspace_root / args.output_dir).resolve()

    packaged = []
    skipped = []

    for target in plan.get("targets", []):
        deploy_source = target.get("site_root") or target.get("workspace")
        target_name = target.get("target")
        if not target.get("allowed"):
            skipped.append(
                {
                    "target": target_name,
                    "reason": target.get("reason"),
                }
            )
            continue

        if not deploy_source:
            skipped.append(
                {
                    "target": target_name,
                    "reason": "missing deploy source path",
                }
            )
            continue

        source_dir = (workspace_root / deploy_source).resolve()
        if not source_dir.exists():
            skipped.append(
                {
                    "target": target_name,
                    "reason": "deploy source directory not found",
                }
            )
            continue

        package_path = output_dir / f"{target_name}.tar.gz"
        file_count = make_tarball(source_dir, package_path)
        packaged.append(
            {
                "target": target_name,
                "environment": target.get("environment"),
                "package": str(package_path.relative_to(workspace_root)),
                "files": file_count,
                "workspace": target.get("workspace"),
                "site_root": target.get("site_root"),
                "deploy_source": deploy_source,
            }
        )

    report = {
        "displayName": plan.get("displayName"),
        "branch": plan.get("branch"),
        "event": plan.get("event"),
        "packaged": packaged,
        "skipped": skipped,
    }
    dump_json((workspace_root / args.report).resolve(), report)
    print(f"deployment execution complete: packaged={len(packaged)} skipped={len(skipped)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
