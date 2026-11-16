#!/usr/bin/env python3
"""无第三方依赖的协议仓库基础校验。"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--schemas", action="store_true", help="also validate JSON Schemas and matching examples (requires jsonschema)")
    args = parser.parse_args()
    files = sorted((ROOT / "schemas").glob("*.json")) + sorted((ROOT / "examples").glob("*.json"))
    if not files:
        raise SystemExit("没有协议文件")
    for path in files:
        data = json.loads(path.read_text("utf-8"))
        if not isinstance(data, dict):
            raise ValueError(f"{path.name} 顶层必须是对象")
        print(f"OK {path.relative_to(ROOT)}")
    if args.schemas:
        from jsonschema import Draft202012Validator
        schemas = {}
        for path in sorted((ROOT / "schemas").glob("*.json")):
            schema = json.loads(path.read_text("utf-8"))
            Draft202012Validator.check_schema(schema)
            identifier = schema.get("properties", {}).get("schema", {}).get("const")
            if identifier:
                schemas[identifier] = Draft202012Validator(schema)
        for path in sorted((ROOT / "examples").glob("*.json")):
            value = json.loads(path.read_text("utf-8"))
            if value.get("schema") in schemas:
                schemas[value["schema"]].validate(value)
                print(f"SCHEMA OK {path.name}")
    version = (ROOT / "VERSION").read_text("utf-8").strip()
    print(f"protocol {version}: {len(files)} files")


if __name__ == "__main__":
    main()
