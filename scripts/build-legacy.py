#!/usr/bin/env python3
"""Build the other session's dashboard (site/build.py, unchanged) into docs/legacy/.

site/build.py writes to ROOT/docs by default. This wrapper imports it and redirects
its output folder to docs/legacy/, so the planner in docs/ root is not overwritten.
"""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("legacy_build", ROOT / "site" / "build.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
mod.OUT = ROOT / "docs" / "legacy"
sys.exit(mod.main())
