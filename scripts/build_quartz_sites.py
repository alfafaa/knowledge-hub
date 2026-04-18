#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from sync_lib import rewrite_asset_links_for_quartz


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


def target_title(display_name: str, target: str) -> str:
    suffix_map = {
        "public-site": "Public",
        "internal-site": "Internal",
        "engineering-site": "Engineering",
        "admin-site": "Admin",
    }
    suffix = suffix_map.get(target, target.replace("-", " ").title())
    return f"{display_name} {suffix}"


def write_root_index(content_root: Path, display_name: str, target: str) -> None:
    index_path = content_root / "index.md"
    if index_path.exists():
        return

    entries = []
    for child in sorted(content_root.iterdir(), key=lambda item: (item.is_file(), item.name.lower())):
        if child.name.startswith(".") or child.name == "index.md":
            continue
        if child.is_dir():
            entries.append(f"- [{child.name}]({child.name}/)")
        elif child.suffix == ".md":
            entries.append(f"- [{child.stem}]({child.stem})")

    title = target_title(display_name, target)
    body = [
        "---",
        f"title: {title}",
        "publish: true",
        f"summary: Generated landing page for {target}.",
        "---",
        "",
        f"# {title}",
        "",
        "This landing page was generated automatically from the staged knowledge-hub content.",
        "",
        "## Sections",
        "",
    ]
    body.extend(entries or ["- No sections available yet."])
    body.append("")
    index_path.write_text("\n".join(body), encoding="utf-8")


def count_files(path: Path) -> int:
    return sum(1 for item in path.rglob("*") if item.is_file())


def rewrite_markdown_asset_links(content_root: Path) -> int:
    changed = 0
    for markdown_path in sorted(path for path in content_root.rglob("*.md") if path.is_file()):
        if rewrite_asset_links_for_quartz(markdown_path, content_root):
            changed += 1
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Quartz static sites from prepared workspaces.")
    parser.add_argument("--workspace-summary", default="quartz/workspace-summary.json", help="Quartz workspace summary")
    parser.add_argument("--quartz-app", default="quartz/app", help="Path to the Quartz app checkout")
    parser.add_argument("--source-root", default="build/quartz-sources", help="Generated Quartz build source root")
    parser.add_argument("--output-root", default="build/rendered", help="Rendered site output root")
    parser.add_argument("--report-out", default="build/rendered/summary.json", help="Rendered site summary path")
    parser.add_argument("--base-url-root", default="localhost", help="Base hostname used for Quartz metadata")
    args = parser.parse_args()

    workspace_root = Path.cwd().resolve()
    workspace_summary = load_json((workspace_root / args.workspace_summary).resolve())
    quartz_app = (workspace_root / args.quartz_app).resolve()
    source_root = (workspace_root / args.source_root).resolve()
    output_root = (workspace_root / args.output_root).resolve()
    display_name = workspace_summary.get("displayName", "Alfafaa Knowledge Hub")

    source_root.mkdir(parents=True, exist_ok=True)
    output_root.mkdir(parents=True, exist_ok=True)

    summary: dict[str, Any] = {
        "displayName": display_name,
        "targets": {},
    }

    overall_ok = True

    for target, meta in workspace_summary.get("targets", {}).items():
        workspace_rel = meta.get("workspace")
        if not workspace_rel:
            continue

        source_workspace = (workspace_root / workspace_rel).resolve()
        source_content = source_workspace / "content"
        build_content_root = source_root / target / "content"
        build_output_root = output_root / target

        ensure_clean_dir(build_content_root)
        copied_files = copy_tree_contents(source_content, build_content_root)
        write_root_index(build_content_root, display_name, target)
        rewritten_files = rewrite_markdown_asset_links(build_content_root)

        env = os.environ.copy()
        env["QUARTZ_PAGE_TITLE"] = target_title(display_name, target)
        env["QUARTZ_BASE_URL"] = f"{target}.{args.base_url_root}"

        cmd = [
            "node",
            "./quartz/bootstrap-cli.mjs",
            "build",
            "-d",
            str(build_content_root),
            "-o",
            str(build_output_root),
        ]
        completed = subprocess.run(
            cmd,
            cwd=quartz_app,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )

        generated_files = count_files(build_output_root) if build_output_root.exists() else 0
        ok = completed.returncode == 0
        overall_ok = overall_ok and ok

        summary["targets"][target] = {
            "workspace": str(source_workspace.relative_to(workspace_root)),
            "source_content_root": str(source_content.relative_to(workspace_root)),
            "build_content_root": str(build_content_root.relative_to(workspace_root)),
            "site_root": str(build_output_root.relative_to(workspace_root)),
            "copiedFiles": copied_files,
            "rewrittenMarkdownFiles": rewritten_files,
            "generatedFiles": generated_files,
            "ok": ok,
            "command": cmd,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }

        if completed.stdout:
            print(completed.stdout, end="")
        if completed.stderr:
            print(completed.stderr, end="", file=sys.stderr)

        if not ok:
            break

    dump_json((workspace_root / args.report_out).resolve(), summary)
    print(f"quartz static render complete: {Path(args.report_out)}")
    return 0 if overall_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
