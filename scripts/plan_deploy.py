#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def decide_target(branch: str, event: str, target: str, generated_files: int) -> dict[str, Any]:
    if generated_files == 0:
        return {
            "environment": "none",
            "allowed": False,
            "requires_approval": False,
            "reason": "no generated files",
        }

    is_pr = event == "pull_request"
    is_main = branch == "main"
    is_release = event in {"workflow_dispatch", "release"} or branch.startswith("release/")

    if is_pr:
        if target == "admin-site":
            return {
                "environment": "preview",
                "allowed": False,
                "requires_approval": True,
                "reason": "admin previews are disabled by default",
            }
        return {
            "environment": "preview",
            "allowed": True,
            "requires_approval": False,
            "reason": "preview deploy allowed for pull requests",
        }

    if is_main:
        if target in {"internal-site", "engineering-site"}:
            return {
                "environment": "internal",
                "allowed": True,
                "requires_approval": False,
                "reason": "internal deploy allowed on main",
            }
        if target == "public-site":
            return {
                "environment": "production",
                "allowed": False,
                "requires_approval": True,
                "reason": "public production deploy requires approval",
            }
        if target == "admin-site":
            return {
                "environment": "internal",
                "allowed": False,
                "requires_approval": True,
                "reason": "admin deploy requires approval",
            }

    if is_release:
        if target == "public-site":
            return {
                "environment": "production",
                "allowed": True,
                "requires_approval": True,
                "reason": "release candidate for public deploy",
            }
        if target in {"internal-site", "engineering-site"}:
            return {
                "environment": "internal",
                "allowed": True,
                "requires_approval": False,
                "reason": "internal release deploy allowed",
            }
        if target == "admin-site":
            return {
                "environment": "internal",
                "allowed": False,
                "requires_approval": True,
                "reason": "admin deploy requires restricted approval",
            }

    return {
        "environment": "none",
        "allowed": False,
        "requires_approval": False,
        "reason": "no deployment rule matched",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Plan deployment decisions from rendered Quartz site outputs.")
    parser.add_argument("--branch", default="local", help="Git branch name")
    parser.add_argument("--event", default="local", help="Trigger event name, e.g. push or pull_request")
    parser.add_argument(
        "--rendered-summary",
        default="build/rendered/summary.json",
        help="Rendered Quartz summary path",
    )
    parser.add_argument("--build-summary", default="build/manifests/summary.json", help="Publish summary path")
    parser.add_argument("--output", default="build/deploy/deploy-plan.json", help="Deployment plan output path")
    args = parser.parse_args()

    workspace_root = Path.cwd().resolve()
    rendered_summary = load_json((workspace_root / args.rendered_summary).resolve())
    build_summary = load_json((workspace_root / args.build_summary).resolve())

    targets = []
    for target, meta in rendered_summary.get("targets", {}).items():
        build_meta = build_summary.get("targets", {}).get(target, {})
        decision = decide_target(args.branch, args.event, target, int(meta.get("generatedFiles", 0)))
        targets.append(
            {
                "target": target,
                "workspace": meta.get("workspace"),
                "site_root": meta.get("site_root"),
                "generated_files": meta.get("generatedFiles", 0),
                "content_summary": build_meta,
                **decision,
            }
        )

    plan = {
        "displayName": rendered_summary.get("displayName"),
        "branch": args.branch,
        "event": args.event,
        "targets": targets,
    }
    dump_json((workspace_root / args.output).resolve(), plan)
    print(f"deployment plan complete: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
