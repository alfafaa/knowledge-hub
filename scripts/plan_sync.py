#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from sync_lib import compute_plans, load_yaml


def main() -> int:
    parser = argparse.ArgumentParser(description="Plan sync actions for docs in a repository.")
    parser.add_argument("--docs-root", required=True, help="Path to docs root")
    parser.add_argument("--config", help="Optional explicit docs.config.yaml path")
    parser.add_argument(
        "--changed",
        nargs="*",
        help="Optional explicit list of changed files relative to the repo root. Defaults to all markdown files under docs root.",
    )
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    docs_root = Path(args.docs_root).resolve()
    config_path = Path(args.config).resolve() if args.config else docs_root / "docs.config.yaml"
    config = load_yaml(config_path)
    plans = compute_plans(docs_root, config, args.changed)

    if args.json:
        print(json.dumps(plans, indent=2))
    else:
        for plan in plans:
            print(json.dumps(plan, sort_keys=True))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
