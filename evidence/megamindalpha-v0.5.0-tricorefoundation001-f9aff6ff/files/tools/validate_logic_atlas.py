#!/usr/bin/env python3
"""Direct-file alias for the supported package validator; resolves the repo root."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from nss_base.logic_atlas import main
if __name__ == '__main__': raise SystemExit(main())
