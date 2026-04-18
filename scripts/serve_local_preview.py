#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import mimetypes
import re
import threading
from dataclasses import dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import unquote


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def parse_frontmatter(markdown: str) -> tuple[dict[str, str], str]:
    if not markdown.startswith("---\n"):
        return {}, markdown

    lines = markdown.splitlines()
    metadata: dict[str, str] = {}
    closing_index = None

    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            closing_index = index
            break
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip()

    if closing_index is None:
        return {}, markdown

    body = "\n".join(lines[closing_index + 1 :]).lstrip("\n")
    return metadata, body


def markdown_to_html(markdown: str) -> str:
    lines = markdown.splitlines()
    output: list[str] = []
    in_code = False
    code_lines: list[str] = []
    in_ul = False
    in_ol = False
    paragraph: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            content = " ".join(part.strip() for part in paragraph if part.strip())
            if content:
                output.append(f"<p>{render_inline(content)}</p>")
        paragraph = []

    def flush_lists() -> None:
        nonlocal in_ul, in_ol
        if in_ul:
            output.append("</ul>")
            in_ul = False
        if in_ol:
            output.append("</ol>")
            in_ol = False

    for raw_line in lines:
        line = raw_line.rstrip("\n")
        stripped = line.strip()

        if stripped.startswith("```"):
            flush_paragraph()
            flush_lists()
            if in_code:
                output.append(f"<pre><code>{html.escape('\n'.join(code_lines))}</code></pre>")
                code_lines = []
                in_code = False
            else:
                in_code = True
            continue

        if in_code:
            code_lines.append(line)
            continue

        if not stripped:
            flush_paragraph()
            flush_lists()
            continue

        heading_match = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if heading_match:
            flush_paragraph()
            flush_lists()
            level = len(heading_match.group(1))
            output.append(f"<h{level}>{render_inline(heading_match.group(2))}</h{level}>")
            continue

        unordered_match = re.match(r"^[-*]\s+(.*)$", stripped)
        if unordered_match:
            flush_paragraph()
            if in_ol:
                output.append("</ol>")
                in_ol = False
            if not in_ul:
                output.append("<ul>")
                in_ul = True
            output.append(f"<li>{render_inline(unordered_match.group(1))}</li>")
            continue

        ordered_match = re.match(r"^\d+\.\s+(.*)$", stripped)
        if ordered_match:
            flush_paragraph()
            if in_ul:
                output.append("</ul>")
                in_ul = False
            if not in_ol:
                output.append("<ol>")
                in_ol = True
            output.append(f"<li>{render_inline(ordered_match.group(1))}</li>")
            continue

        if stripped == "---":
            flush_paragraph()
            flush_lists()
            output.append("<hr>")
            continue

        paragraph.append(stripped)

    flush_paragraph()
    flush_lists()
    if in_code:
        output.append(f"<pre><code>{html.escape('\n'.join(code_lines))}</code></pre>")
    return "\n".join(output)


def render_inline(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)
    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', escaped)
    return escaped


@dataclass
class TargetSite:
    name: str
    root: Path
    content_root: Path
    config: dict[str, Any]

    @property
    def display_name(self) -> str:
        return self.config.get("displayName", self.name)


class PreviewHandler(BaseHTTPRequestHandler):
    server_version = "AlfafaaLocalPreview/1.0"

    def do_GET(self) -> None:  # noqa: N802
        app: LocalPreviewServer = self.server  # type: ignore[assignment]
        path = unquote(self.path.split("?", 1)[0])
        if path == "/":
            self._send_html("Local Preview", app.render_root())
            return

        path = path.strip("/")
        parts = [part for part in path.split("/") if part]
        if not parts:
            self._send_html("Local Preview", app.render_root())
            return

        target_name = parts[0]
        target = app.targets.get(target_name)
        if target is None:
            self.send_error(HTTPStatus.NOT_FOUND, "Unknown target")
            return

        relative_parts = parts[1:]
        if not relative_parts:
            self._send_html(target.display_name, app.render_target_home(target))
            return

        if relative_parts[0] == "_raw":
            file_path = target.content_root.joinpath(*relative_parts[1:])
            self._send_file(file_path)
            return

        app_path = Path(*relative_parts)
        fs_target = target.content_root / app_path

        if fs_target.is_dir():
            self._send_html(target.display_name, app.render_directory(target, app_path))
            return

        if fs_target.exists() and fs_target.suffix != ".md":
            self._send_file(fs_target)
            return

        markdown_target = fs_target
        if markdown_target.suffix != ".md":
            markdown_target = markdown_target.with_suffix(".md")

        if markdown_target.exists():
            self._send_html(target.display_name, app.render_markdown(target, markdown_target))
            return

        self.send_error(HTTPStatus.NOT_FOUND, "Document not found")

    def log_message(self, format: str, *args: object) -> None:
        return

    def _send_html(self, title: str, body: str) -> None:
        page = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f4efe7;
      --card: #fffaf2;
      --line: #d9ccb9;
      --text: #3d2b1f;
      --muted: #7a6452;
      --accent: #8a3d20;
      --code: #f0e3d1;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: linear-gradient(180deg, #f7f1e8 0%, var(--bg) 100%);
      color: var(--text);
      font-family: "Iowan Old Style", "Palatino Linotype", "Book Antiqua", serif;
      line-height: 1.6;
    }}
    main {{
      max-width: 960px;
      margin: 0 auto;
      padding: 32px 20px 64px;
    }}
    a {{ color: var(--accent); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .card {{
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 18px;
      padding: 20px 24px;
      margin: 18px 0;
      box-shadow: 0 10px 30px rgba(79, 53, 34, 0.06);
    }}
    .muted {{ color: var(--muted); }}
    .chips {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 12px; }}
    .chip {{
      display: inline-block;
      padding: 6px 10px;
      border-radius: 999px;
      background: #efe0cf;
      color: var(--text);
      font-size: 14px;
    }}
    .breadcrumbs {{
      font-size: 14px;
      color: var(--muted);
      margin-bottom: 14px;
    }}
    h1, h2, h3, h4, h5, h6 {{
      line-height: 1.2;
      margin-top: 1.3em;
      margin-bottom: 0.5em;
    }}
    h1 {{ font-size: 2.3rem; margin-top: 0; }}
    h2 {{ font-size: 1.7rem; }}
    pre {{
      overflow-x: auto;
      padding: 14px;
      border-radius: 12px;
      background: var(--code);
      border: 1px solid var(--line);
    }}
    code {{
      background: var(--code);
      padding: 0.1em 0.35em;
      border-radius: 6px;
    }}
    ul, ol {{ padding-left: 24px; }}
    hr {{
      border: 0;
      border-top: 1px solid var(--line);
      margin: 24px 0;
    }}
    .listing li {{ margin: 8px 0; }}
  </style>
</head>
<body>
  <main>{body}</main>
</body>
</html>
"""
        encoded = page.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def _send_file(self, path: Path) -> None:
        if not path.exists() or not path.is_file():
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return
        mime_type, _ = mimetypes.guess_type(str(path))
        payload = path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", mime_type or "application/octet-stream")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


class LocalPreviewServer(ThreadingHTTPServer):
    def __init__(
        self,
        server_address: tuple[str, int],
        targets: dict[str, TargetSite],
        display_name: str,
        workspace_root: Path,
    ):
        super().__init__(server_address, PreviewHandler)
        self.targets = targets
        self.display_name = display_name
        self.workspace_root = workspace_root

    def render_root(self) -> str:
        items = []
        for name, target in sorted(self.targets.items()):
            items.append(
                "<div class='card'>"
                f"<h2><a href='/{name}/'>{html.escape(name)}</a></h2>"
                f"<p class='muted'>{html.escape(target.display_name)}</p>"
                "<div class='chips'>"
                f"<span class='chip'>content root: {html.escape(str(target.content_root.relative_to(self.workspace_root)))}</span>"
                f"<span class='chip'>generated files: {html.escape(str(target.config.get('generatedFiles', 0)))}</span>"
                "</div>"
                "</div>"
            )
        targets_html = "".join(items) or "<div class='card'><p>No deployed targets found.</p></div>"
        return (
            f"<h1>{html.escape(self.display_name)} Local Preview</h1>"
            "<p class='muted'>This preview renders the locally deployed runtime before VPS release.</p>"
            f"{targets_html}"
        )

    def render_target_home(self, target: TargetSite) -> str:
        index_md = target.content_root / "_index.md"
        if index_md.exists():
            return self.render_markdown(target, index_md)
        return self.render_directory(target, Path("."))

    def render_directory(self, target: TargetSite, app_path: Path) -> str:
        directory = target.content_root / app_path
        if not directory.exists() or not directory.is_dir():
            return "<div class='card'><p>Directory not found.</p></div>"

        index_md = directory / "_index.md"
        intro = ""
        if index_md.exists():
            intro = self.render_markdown(target, index_md, embed_only=True)

        entries = []
        for child in sorted(directory.iterdir(), key=lambda item: (item.is_file(), item.name.lower())):
            if child.name.startswith(".") or child.name == "_index.md":
                continue
            rel = child.relative_to(target.content_root)
            href = f"/{target.name}/{rel.as_posix()}"
            if child.is_file() and child.suffix == ".md":
                href = f"/{target.name}/{rel.with_suffix('').as_posix()}"
            label = child.stem if child.suffix == ".md" else child.name
            kind = "folder" if child.is_dir() else "file"
            entries.append(f"<li><a href='{href}'>{html.escape(label)}</a> <span class='muted'>[{kind}]</span></li>")

        listing = "".join(entries) or "<li class='muted'>No child entries.</li>"
        breadcrumbs = self._breadcrumbs(target, app_path)
        return (
            f"{breadcrumbs}"
            f"{intro}"
            "<div class='card'>"
            "<h2>Contents</h2>"
            f"<ul class='listing'>{listing}</ul>"
            "</div>"
        )

    def render_markdown(self, target: TargetSite, markdown_path: Path, embed_only: bool = False) -> str:
        content = markdown_path.read_text(encoding="utf-8")
        metadata, body = parse_frontmatter(content)
        title = metadata.get("title") or markdown_path.stem.replace("-", " ").replace("_", " ").title()
        rel = markdown_path.relative_to(target.content_root)
        breadcrumbs = "" if embed_only else self._breadcrumbs(target, rel)
        raw_href = f"/{target.name}/_raw/{rel.as_posix()}"
        chips = [
            f"<span class='chip'>source: {html.escape(rel.as_posix())}</span>",
            f"<span class='chip'><a href='{raw_href}'>raw markdown</a></span>",
        ]
        body_html = markdown_to_html(body)
        return (
            f"{breadcrumbs}"
            "<div class='card'>"
            f"<h1>{html.escape(title)}</h1>"
            f"<div class='chips'>{''.join(chips)}</div>"
            f"{body_html}"
            "</div>"
        )

    def _breadcrumbs(self, target: TargetSite, app_path: Path) -> str:
        parts = [part for part in app_path.parts if part not in (".", "")]
        crumbs = [f"<a href='/'>preview</a>", f"<a href='/{target.name}/'>{html.escape(target.name)}</a>"]
        current = Path()
        for part in parts:
            current /= part
            href = f"/{target.name}/{current.as_posix()}"
            if current.suffix == ".md":
                href = f"/{target.name}/{current.with_suffix('').as_posix()}"
            crumbs.append(f"<a href='{href}'>{html.escape(part)}</a>")
        return f"<div class='breadcrumbs'>{' / '.join(crumbs)}</div>"


def discover_targets(runtime_root: Path) -> dict[str, TargetSite]:
    targets: dict[str, TargetSite] = {}
    if not runtime_root.exists():
        return targets

    for site_dir in sorted(runtime_root.iterdir()):
        current_root = site_dir / "current"
        config_path = current_root / "site.config.json"
        if not config_path.exists():
            continue
        config = load_json(config_path)
        content_root = current_root / config.get("contentRoot", "content")
        targets[site_dir.name] = TargetSite(
            name=site_dir.name,
            root=current_root,
            content_root=content_root,
            config=config,
        )
    return targets


def main() -> int:
    parser = argparse.ArgumentParser(description="Serve locally deployed knowledge hub targets on localhost.")
    parser.add_argument("--runtime-root", default="deploy/runtime", help="Directory containing deployed site targets")
    parser.add_argument("--host", default="127.0.0.1", help="Bind host")
    parser.add_argument("--port", type=int, default=8010, help="Bind port")
    parser.add_argument(
        "--report-out",
        default="build/local-preview-report.json",
        help="Path to write the local preview report",
    )
    parser.add_argument(
        "--shutdown-after",
        type=int,
        help="Optional number of seconds after which the server stops automatically",
    )
    args = parser.parse_args()

    workspace_root = Path.cwd().resolve()
    runtime_root = (workspace_root / args.runtime_root).resolve()
    targets = discover_targets(runtime_root)
    if not targets:
        print("no deployed targets found under deploy/runtime; run the pipeline first")
        return 1

    display_name = next(iter(targets.values())).display_name
    server = LocalPreviewServer((args.host, args.port), targets, display_name, workspace_root)

    report = {
        "displayName": display_name,
        "host": args.host,
        "port": args.port,
        "rootUrl": f"http://{args.host}:{args.port}/",
        "targets": {
            name: {
                "url": f"http://{args.host}:{args.port}/{name}/",
                "contentRoot": str(target.content_root.relative_to(workspace_root)),
                "generatedFiles": target.config.get("generatedFiles", 0),
            }
            for name, target in sorted(targets.items())
        },
    }
    dump_json((workspace_root / args.report_out).resolve(), report)

    timer = None
    if args.shutdown_after:
        timer = threading.Timer(args.shutdown_after, server.shutdown)
        timer.start()

    print(f"local preview: {report['rootUrl']}")
    for name, target_report in report["targets"].items():
        print(f"  - {name}: {target_report['url']}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        if timer is not None:
            timer.cancel()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
