#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def final_remote_root(remote_root: str, deploy_to: str) -> str:
    return f"{remote_root.rstrip('/')}/{deploy_to.lstrip('/')}"


def server_block(server_name: str, port: int, root_path: str, target: str) -> str:
    return f"""server {{
    listen {port};
    listen [::]:{port};
    server_name {server_name};

    root {root_path};
    index index.html;

    access_log /var/log/nginx/{target}.access.log;
    error_log /var/log/nginx/{target}.error.log;

    location / {{
        try_files $uri $uri/ /index.html;
    }}

    location ~* \\.(css|js|png|jpg|jpeg|gif|svg|ico|webp|xml|json)$ {{
        expires 1h;
        add_header Cache-Control "public";
        try_files $uri =404;
    }}
}}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate nginx config for staged knowledge hub targets.")
    parser.add_argument("--deploy-plan", default="build/deploy/deploy-plan.json", help="Deploy plan path")
    parser.add_argument("--ssh-config", default="deploy.ssh.yaml", help="SSH deployment config")
    parser.add_argument("--nginx-config", default="deploy.nginx.yaml", help="nginx deployment config")
    parser.add_argument(
        "--output",
        default="build/deploy/nginx/alfafaa-knowledge-hub-staging.conf",
        help="Generated nginx config path",
    )
    args = parser.parse_args()

    workspace_root = Path.cwd().resolve()
    deploy_plan = load_json((workspace_root / args.deploy_plan).resolve())
    ssh_cfg = load_yaml((workspace_root / args.ssh_config).resolve())
    nginx_cfg = load_yaml((workspace_root / args.nginx_config).resolve())

    remote_root = ssh_cfg.get("remote_root", "/srv/alfafaa-knowledge-hub")
    ssh_targets = ssh_cfg.get("targets", {})
    nginx_targets = nginx_cfg.get("targets", {})
    server_name = nginx_cfg.get("server_name", "_")

    blocks: list[str] = [
        f"# Generated for {deploy_plan.get('displayName', 'Alfafaa Knowledge Hub')}",
        "# This file is generated. Do not edit manually.",
        "",
    ]

    generated_targets = []

    for target in deploy_plan.get("targets", []):
        target_name = target.get("target")
        if not isinstance(target_name, str):
            continue

        nginx_target = nginx_targets.get(target_name, {})
        ssh_target = ssh_targets.get(target_name, {})
        if not nginx_target.get("enabled", False):
            continue
        if not ssh_target.get("enabled", False):
            continue

        deploy_to = ssh_target.get("deploy_to")
        listen_port = nginx_target.get("listen_port")
        if not isinstance(deploy_to, str) or not isinstance(listen_port, int):
            continue

        root_path = final_remote_root(remote_root, deploy_to)
        blocks.append(server_block(server_name, listen_port, root_path, target_name))
        generated_targets.append(
            {
                "target": target_name,
                "listen_port": listen_port,
                "root": root_path,
            }
        )

    output_path = (workspace_root / args.output).resolve()
    write_text(output_path, "\n".join(blocks).rstrip() + "\n")
    report = {
        "displayName": deploy_plan.get("displayName"),
        "server_name": server_name,
        "generated_config": str(output_path.relative_to(workspace_root)),
        "targets": generated_targets,
    }
    write_text(output_path.with_suffix(".json"), json.dumps(report, indent=2) + "\n")
    print(f"nginx config generated: {output_path.relative_to(workspace_root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
