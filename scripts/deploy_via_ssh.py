#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
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


def run(cmd: list[str], dry_run: bool) -> dict[str, Any]:
    if dry_run:
        return {
            "command": cmd,
            "returncode": 0,
            "stdout": "",
            "stderr": "",
            "ok": True,
            "dry_run": True,
        }
    completed = subprocess.run(cmd, capture_output=True, text=True, check=False)
    return {
        "command": cmd,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "ok": completed.returncode == 0,
        "dry_run": False,
    }


def ssh_base(host: str, user: str, port: int) -> list[str]:
    return ["ssh", "-p", str(port), f"{user}@{host}"]


def rsync_base(port: int) -> list[str]:
    return ["rsync", "-az", "-e", f"ssh -p {port}"]


def remote_script(remote_packages_dir: str, remote_root: str, targets: list[dict[str, Any]]) -> str:
    lines = [
        "set -euo pipefail",
        f"mkdir -p {shlex.quote(remote_packages_dir)}",
        f"mkdir -p {shlex.quote(remote_root)}",
    ]

    for item in targets:
        package_name = Path(item["package"]).name
        incoming = f"{remote_root.rstrip('/')}/{item['target']}/incoming"
        final = f"{remote_root.rstrip('/')}/{item['deploy_to']}"
        previous = f"{Path(final).parent}/{Path(final).name}-previous"
        package_path = f"{remote_packages_dir.rstrip('/')}/{package_name}"

        lines.extend(
            [
                f"rm -rf {shlex.quote(incoming)}",
                f"mkdir -p {shlex.quote(incoming)}",
                f"tar -xzf {shlex.quote(package_path)} -C {shlex.quote(incoming)}",
            ]
        )

        if item.get("preserve_previous", True):
            lines.extend(
                [
                    f"if [ -d {shlex.quote(final)} ]; then rm -rf {shlex.quote(previous)}; mv {shlex.quote(final)} {shlex.quote(previous)}; fi",
                ]
            )
        else:
            lines.extend(
                [
                    f"rm -rf {shlex.quote(final)}",
                ]
            )

        lines.extend(
            [
                f"mkdir -p {shlex.quote(str(Path(final).parent))}",
                f"mv {shlex.quote(incoming)} {shlex.quote(final)}",
            ]
        )

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Upload deploy packages to a VPS over SSH and extract them remotely.")
    parser.add_argument("--config", default="deploy.ssh.yaml", help="SSH deployment config")
    parser.add_argument(
        "--execution-report",
        default="build/deploy/deploy-execution-report.json",
        help="Deployment execution report path",
    )
    parser.add_argument(
        "--report-out",
        default="build/deploy/ssh-deploy-report.json",
        help="Path to write the SSH deployment report",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print intended actions without executing them")
    args = parser.parse_args()

    workspace_root = Path.cwd().resolve()
    cfg = load_yaml((workspace_root / args.config).resolve())
    execution = load_json((workspace_root / args.execution_report).resolve())

    host = cfg.get("host")
    user = cfg.get("user")
    port = int(cfg.get("port", 22))
    remote_root = cfg.get("remote_root")
    remote_packages_dir = cfg.get("remote_packages_dir")
    target_cfg = cfg.get("targets", {})

    if not all(isinstance(value, str) and value for value in (host, user, remote_root, remote_packages_dir)):
        print("error: deploy.ssh.yaml is missing required connection settings", file=sys.stderr)
        return 2

    remote_targets = []
    skipped = []
    for item in execution.get("packaged", []):
        target_name = item.get("target")
        cfg_target = target_cfg.get(target_name, {})
        if not cfg_target.get("enabled", False):
            skipped.append({"target": target_name, "reason": "target disabled in deploy.ssh.yaml"})
            continue
        remote_targets.append(
            {
                "target": target_name,
                "package": item["package"],
                "deploy_to": cfg_target.get("deploy_to"),
                "preserve_previous": cfg_target.get("preserve_previous", True),
            }
        )

    uploaded = []
    commands = []

    mkdir_cmd = ssh_base(host, user, port) + [f"mkdir -p {shlex.quote(remote_packages_dir)} {shlex.quote(remote_root)}"]
    result = run(mkdir_cmd, args.dry_run)
    commands.append(result)
    if not result["ok"]:
        dump_json((workspace_root / args.report_out).resolve(), {"ok": False, "commands": commands, "uploaded": uploaded, "skipped": skipped})
        return 1

    for item in remote_targets:
        package_path = (workspace_root / item["package"]).resolve()
        if not package_path.exists():
            skipped.append({"target": item["target"], "reason": "local package not found"})
            continue
        cmd = rsync_base(port) + [str(package_path), f"{user}@{host}:{remote_packages_dir.rstrip('/')}/"]
        result = run(cmd, args.dry_run)
        commands.append(result)
        if not result["ok"]:
            dump_json((workspace_root / args.report_out).resolve(), {"ok": False, "commands": commands, "uploaded": uploaded, "skipped": skipped})
            return 1
        uploaded.append({"target": item["target"], "package": item["package"]})

    script = remote_script(remote_packages_dir, remote_root, remote_targets)
    remote_cmd = ssh_base(host, user, port) + [script]
    result = run(remote_cmd, args.dry_run)
    commands.append(result)

    report = {
        "displayName": cfg.get("display_name"),
        "host": host,
        "user": user,
        "port": port,
        "dry_run": args.dry_run,
        "ok": result["ok"],
        "uploaded": uploaded,
        "skipped": skipped,
        "commands": commands,
    }
    dump_json((workspace_root / args.report_out).resolve(), report)
    print(f"ssh deploy {'dry-run ' if args.dry_run else ''}complete: uploaded={len(uploaded)} skipped={len(skipped)}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
