#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def run_step(name: str, cmd: list[str], workdir: Path) -> dict[str, Any]:
    completed = subprocess.run(
        cmd,
        cwd=workdir,
        capture_output=True,
        text=True,
        check=False,
    )
    return {
        "name": name,
        "command": cmd,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "ok": completed.returncode == 0,
    }


def write_report(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the Alfafaa Knowledge Hub MVP pipeline end-to-end.")
    parser.add_argument("--docs-root", required=True, help="Path to a repository docs root")
    parser.add_argument("--config", help="Optional explicit docs.config.yaml path")
    parser.add_argument(
        "--report-path",
        default="build/pipeline-report.json",
        help="Path to write the aggregated pipeline report",
    )
    parser.add_argument(
        "--skip-quartz",
        action="store_true",
        help="Skip Quartz workspace preparation",
    )
    parser.add_argument("--branch", default="local", help="Git branch name for deployment planning")
    parser.add_argument("--event", default="local", help="Trigger event name for deployment planning")
    args = parser.parse_args()

    workspace_root = Path.cwd().resolve()
    docs_root = Path(args.docs_root).resolve()
    config_args = ["--config", str(Path(args.config).resolve())] if args.config else []

    steps = [
        {
            "name": "validate",
            "cmd": ["python3", "scripts/validate_docs.py", "--docs-root", str(docs_root), *config_args],
        },
        {
            "name": "ingest",
            "cmd": ["python3", "scripts/ingest_sync.py", "--docs-root", str(docs_root), *config_args],
        },
        {
            "name": "publish-plan",
            "cmd": ["python3", "scripts/plan_publish.py"],
        },
    ]

    if not args.skip_quartz:
        steps.append(
            {
                "name": "prepare-quartz-workspace",
                "cmd": ["python3", "scripts/prepare_quartz_workspace.py"],
            }
        )
        steps.append(
            {
                "name": "build-quartz-sites",
                "cmd": ["python3", "scripts/build_quartz_sites.py"],
            }
        )
        steps.append(
            {
                "name": "plan-deploy",
                "cmd": ["python3", "scripts/plan_deploy.py", "--branch", args.branch, "--event", args.event],
            }
        )
        steps.append(
            {
                "name": "generate-nginx-config",
                "cmd": ["python3", "scripts/generate_nginx_config.py"],
            }
        )
        steps.append(
            {
                "name": "execute-deploy",
                "cmd": ["python3", "scripts/execute_deploy.py"],
            }
        )
        steps.append(
            {
                "name": "deploy-to-vps",
                "cmd": ["python3", "scripts/deploy_to_vps.py"],
            }
        )

    results = []
    overall_ok = True
    for step in steps:
        result = run_step(step["name"], step["cmd"], workspace_root)
        results.append(result)
        if result["stdout"]:
            print(result["stdout"], end="")
        if result["stderr"]:
            print(result["stderr"], end="", file=sys.stderr)
        if not result["ok"]:
            overall_ok = False
            break

    report = {
        "displayName": "Alfafaa Knowledge Hub",
        "docsRoot": str(docs_root),
        "branch": args.branch,
        "event": args.event,
        "success": overall_ok,
        "steps": results,
    }
    report_path = (workspace_root / args.report_path).resolve()
    write_report(report_path, report)

    print(f"pipeline report: {report_path.relative_to(workspace_root)}")
    return 0 if overall_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
