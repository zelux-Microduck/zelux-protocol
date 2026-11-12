#!/usr/bin/env python3
"""无第三方依赖的协议仓库基础校验。"""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    files = sorted((ROOT / "schemas").glob("*.json")) + sorted((ROOT / "examples").glob("*.json"))
    if not files:
        raise SystemExit("没有协议文件")
    for path in files:
        data = json.loads(path.read_text("utf-8"))
        if not isinstance(data, dict):
            raise ValueError(f"{path.name} 顶层必须是对象")
        print(f"OK {path.relative_to(ROOT)}")
    version = (ROOT / "VERSION").read_text("utf-8").strip()
    print(f"protocol {version}: {len(files)} files")


if __name__ == "__main__":
    main()
