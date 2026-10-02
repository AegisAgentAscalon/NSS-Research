"""Subprocess crash injector; invoked by test_recovery001a.py."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from nss_base.experiment001a import action
from nss_base.ledger import Ledger

Ledger(sys.argv[1]).perform(action(), crash_at=sys.argv[2])
