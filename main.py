#!/usr/bin/env python3
"""Ship the pre-drawn entry.png into the output directory (stdlib only)."""
from os import environ as _env
from pathlib import Path
from shutil import copyfile as _copy

HERE = Path(__file__).resolve().parent


def ship():
    target = Path(_env.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target.mkdir(parents=True, exist_ok=True)
    _copy(HERE / "entry.png", target / "entry.png")


ship()
