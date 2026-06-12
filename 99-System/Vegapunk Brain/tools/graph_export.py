#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def load_records(path: Path) -> dict:
    data = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            item = json.loads(line)
            data[item["id"]] = item
    return data


def safe_id(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]", "_", value)


def write_mermaid(records: dict, path: Path) -> None:
    rows = ["graph TD"]
    for rid, item in sorted(records.items()):
        rows.append("  " + safe_id(rid) + "[\"" + item["name"].replace("\"", "'") + "\"]")
    for rid, item in sorted(records.items()):
        for link in item.get("links", []):
            target = link.get("target")
            if target in records:
                rows.append("  " + safe_id(rid) + " --> " + safe_id(target))
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")


def write_text_tree(records: dict, path: Path, root_id: str) -> None:
    root = records.get(root_id)
    rows = []
    if root:
        rows.append(root["name"])
        for link in root.get("links", []):
            target = records.get(link.get("target"))
            if target:
                rows.append("- " + target["name"] + " (" + link.get("type", "related") + ")")
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--root", default="concept:knowledge-vault")
    args = parser.parse_args()
    records = load_records(Path(args.graph))
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    write_mermaid(records, out_dir / "graph.mmd")
    write_text_tree(records, out_dir / "knowledge-vault-tree.txt", args.root)
    (out_dir / "graph.json").write_text(json.dumps(records, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("Exported graph artifacts into " + str(out_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
