import json
from pathlib import Path
import sqlite3
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from reliability.recovery import Objectives, digest, restore


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.backup = Path(self.tmp.name) / 'backup.db'
        self.target = Path(self.tmp.name) / 'target.db'
        with sqlite3.connect(self.backup) as db:
            db.execute('CREATE TABLE messages(id INTEGER PRIMARY KEY, body TEXT, acknowledged_at REAL)')
            db.execute("INSERT INTO messages VALUES (1, 'synthetic-message', 990)")

    def run_restore(self, **kwargs):
        return restore(self.backup, self.target, digest(self.backup),
                       incident_epoch=1000, objectives=kwargs.pop('objectives', Objectives()), **kwargs)

    def test_success_preserves_data_and_rolls_back_probe(self):
        result = self.run_restore()
        self.assertTrue(result.eligible_for_promotion)
        self.assertEqual(result.recovery_point_age_seconds, 10)
        with sqlite3.connect(self.target) as db:
            self.assertEqual(db.execute('SELECT * FROM messages').fetchall(), [(1, 'synthetic-message', 990.0)])

    def test_checksum_rejects_corruption(self):
        expected = digest(self.backup)
        self.backup.write_bytes(b'bad')
        result = restore(self.backup, self.target, expected, incident_epoch=1000, objectives=Objectives())
        self.assertIn('checksum mismatch', result.reasons)
        self.assertFalse(self.target.exists())

    def test_matching_hash_cannot_bypass_schema_validation(self):
        self.backup.write_bytes(b'not sqlite')
        self.assertFalse(self.run_restore().eligible_for_promotion)
        self.assertFalse(self.target.exists())

    def test_stale_point(self):
        result = self.run_restore(objectives=Objectives(rpo_seconds=9))
        self.assertFalse(result.eligible_for_promotion)
        self.assertFalse(self.target.exists())

    def test_rpo_boundary_inclusive(self):
        self.assertTrue(self.run_restore(objectives=Objectives(rpo_seconds=10)).eligible_for_promotion)

    def test_rto_breach_includes_validation(self):
        ticks = iter([0, 61])
        result = self.run_restore(clock=lambda: next(ticks))
        self.assertIn('restore exceeds local RTO target', result.reasons)
        self.assertFalse(self.target.exists())

    def test_rto_boundary_inclusive(self):
        ticks = iter([0, 60])
        self.assertTrue(self.run_restore(clock=lambda: next(ticks)).eligible_for_promotion)

    def test_invalid_clock_fails_closed(self):
        ticks = iter([1, 0])
        self.assertFalse(self.run_restore(clock=lambda: next(ticks)).eligible_for_promotion)

    def test_target_never_overwritten(self):
        self.target.write_text('keep')
        with self.assertRaises(FileExistsError):
            self.run_restore()
        self.assertEqual(self.target.read_text(), 'keep')

    def test_missing_backup(self):
        self.backup.unlink()
        result = restore(self.backup, self.target, 'unused', incident_epoch=1000, objectives=Objectives())
        self.assertFalse(result.eligible_for_promotion)
        self.assertFalse(self.target.exists())

    def test_empty_data(self):
        with sqlite3.connect(self.backup) as db:
            db.execute('DELETE FROM messages')
        self.assertIn('empty journey data', self.run_restore().reasons)

    def test_future_and_invalid_timestamp(self):
        for value in [1001, -1, 'unknown']:
            with self.subTest(value=value):
                with sqlite3.connect(self.backup) as db:
                    db.execute('UPDATE messages SET acknowledged_at=?', (value,))
                self.assertFalse(self.run_restore().eligible_for_promotion)

    def test_invalid_objectives(self):
        for value in [-1, float('inf'), float('nan'), True]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                Objectives(rto_seconds=value)

    def test_invalid_incident_time(self):
        for value in [-1, float('nan'), float('inf')]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                restore(self.backup, self.target, digest(self.backup), incident_epoch=value, objectives=Objectives())
        self.assertFalse(self.target.exists())

    def test_cli_scenarios_and_exit_codes(self):
        for scenario, status, eligible in [('healthy', 0, True), ('stale', 1, False), ('corrupt', 1, False)]:
            with self.subTest(scenario=scenario):
                run = subprocess.run([sys.executable, '-m', 'reliability', '--scenario', scenario], capture_output=True, text=True)
                self.assertEqual(run.returncode, status, run.stderr)
                self.assertIs(json.loads(run.stdout)['eligible_for_promotion'], eligible)
