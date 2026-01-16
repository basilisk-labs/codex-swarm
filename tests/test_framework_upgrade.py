import copy
import importlib.util
import sys
import unittest
from datetime import datetime, timedelta
from pathlib import Path

AGENTCTL_PATH = Path(".codex-swarm/agentctl.py")
SPEC = importlib.util.spec_from_file_location("agentctl_upgrade_test", AGENTCTL_PATH)
assert SPEC is not None
AGENTCTL = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(AGENTCTL)


class FrameworkUpgradeHelpersTest(unittest.TestCase):
    def setUp(self) -> None:
        self.original_config = copy.deepcopy(AGENTCTL._SWARM_CONFIG)

    def tearDown(self) -> None:
        AGENTCTL._SWARM_CONFIG = self.original_config

    def test_parse_iso_datetime_date_only(self) -> None:
        parsed = AGENTCTL.parse_iso_datetime("2025-01-02")
        self.assertEqual(parsed, datetime(2025, 1, 2, tzinfo=AGENTCTL.UTC))

    def test_parse_iso_datetime_invalid(self) -> None:
        self.assertIsNone(AGENTCTL.parse_iso_datetime("not-a-date"))

    def test_framework_upgrade_due_detects_stale(self) -> None:
        now = datetime(2025, 1, 11, tzinfo=AGENTCTL.UTC)
        last = now - timedelta(days=11)
        should_upgrade, reason = AGENTCTL.framework_upgrade_due(last, now=now)
        self.assertTrue(should_upgrade)
        self.assertIn("stale", reason or "")

    def test_framework_upgrade_due_recent(self) -> None:
        now = datetime(2025, 1, 11, tzinfo=AGENTCTL.UTC)
        last = now - timedelta(days=5)
        self.assertFalse(AGENTCTL.framework_upgrade_due(last, now=now)[0])

    def test_framework_last_update_reads_config(self) -> None:
        config = copy.deepcopy(self.original_config)
        config["framework"] = {"last_update": "2025-01-01T00:00:00+00:00"}
        AGENTCTL._SWARM_CONFIG = config
        delta = AGENTCTL.framework_last_update()
        self.assertEqual(delta, datetime(2025, 1, 1, tzinfo=AGENTCTL.UTC))


if __name__ == "__main__":
    unittest.main()
