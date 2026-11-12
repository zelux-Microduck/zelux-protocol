#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = (ROOT / "VERSION").read_text("utf-8").strip()
DIST = ROOT / "dist"
DIST.mkdir(exist_ok=True)
OUT = DIST / f"zelux-protocol-{VERSION}.zip"
FILES = [ROOT / "VERSION", ROOT / "README.md", *sorted((ROOT / "schemas").glob("*.json")),
         *sorted((ROOT / "examples").glob("*.json"))]
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as archive:
    for path in FILES:
        archive.write(path, path.relative_to(ROOT).as_posix())
digest = hashlib.sha256(OUT.read_bytes()).hexdigest()
OUT.with_suffix(OUT.suffix + ".sha256").write_text(f"{digest}  {OUT.name}\n", "ascii")
print(OUT)
