#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export the project starter template as a standalone repository tree."
    )
    parser.add_argument(
        "--source",
        default="starter-templates/project-starter-template-repo",
        help="source starter template directory inside the knowledge hub repo",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="directory where the standalone starter repo should be written",
    )
    parser.add_argument(
        "--zip-path",
        help="optional output path for a release zip built from the exported tree",
    )
    return parser.parse_args()


def copy_tree(source: Path, output_dir: Path) -> None:
    if not source.exists():
        raise FileNotFoundError(f"starter template source not found: {source}")
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, output_dir)


def build_zip(export_root: Path, zip_path: Path) -> None:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(zip_path, "w", ZIP_DEFLATED) as archive:
        for file_path in sorted(export_root.rglob("*")):
            if file_path.is_dir():
                continue
            archive.write(file_path, file_path.relative_to(export_root))


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parent.parent
    source = (repo_root / args.source).resolve()
    output_dir = Path(args.output_dir).resolve()

    copy_tree(source, output_dir)

    if args.zip_path:
        build_zip(output_dir, Path(args.zip_path).resolve())

    print(f"Exported starter template to {output_dir}")
    if args.zip_path:
        print(f"Built starter template zip at {Path(args.zip_path).resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
