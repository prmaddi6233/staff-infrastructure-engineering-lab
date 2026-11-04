"""Restore synthetic SQLite backups into a new target and gate promotion.

The caller must trust expected_sha256 independently of the backup. A checksum
proves integrity against that value, not authenticity or administrative isolation.
"""
from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path
import json
import math
import sqlite3
import time


@dataclass(frozen=True)
class Objectives:
    rto_seconds: float = 60
    rpo_seconds: float = 300

    def __post_init__(self):
        for value in (self.rto_seconds, self.rpo_seconds):
            if isinstance(value, bool) or not math.isfinite(value) or value < 0:
                raise ValueError("objectives must be finite nonnegative seconds")


@dataclass(frozen=True)
class RecoveryResult:
    eligible_for_promotion: bool
    reasons: tuple[str, ...]
    restore_seconds: float
    recovery_point_age_seconds: float | None
    restored_messages: int

    def to_json(self):
        return json.dumps(asdict(self), sort_keys=True, indent=2)


def digest(path: Path) -> str:
    with path.open('rb') as source:
        return sha256(source.read()).hexdigest()


def restore(backup: Path, target: Path, expected_sha256: str, *,
            incident_epoch: float, objectives: Objectives,
            clock=time.monotonic) -> RecoveryResult:
    """Never overwrite a target. Remove a failed candidate, retain successful one.

    RTO here measures only local copy + integrity + synthetic journey validation.
    RPO proxy is incident time minus latest backed-up acknowledged write time;
    this conservative age is NOT observed data loss for an idle real service.
    """
    if not math.isfinite(incident_epoch) or incident_epoch < 0:
        raise ValueError('incident_epoch must be finite and nonnegative')
    start = clock()
    reasons = []
    age = None
    count = 0
    # Exclusive creation protects an existing database, including repeated runs.
    with target.open('xb'):
        pass
    try:
        if digest(backup) != expected_sha256:
            raise ValueError('checksum mismatch')
        with sqlite3.connect(backup.resolve().as_uri() + '?mode=ro', uri=True) as source:
            with sqlite3.connect(target) as candidate:
                source.backup(candidate)
                if candidate.execute('PRAGMA integrity_check').fetchone() != ('ok',):
                    raise ValueError('database integrity failure')
                rows = candidate.execute(
                    'SELECT id, body, acknowledged_at FROM messages ORDER BY id'
                ).fetchall()
                if not rows:
                    raise ValueError('empty journey data')
                for ident, body, acknowledged_at in rows:
                    if (not isinstance(ident, int) or not isinstance(body, str)
                            or not body.startswith('synthetic-')
                            or not isinstance(acknowledged_at, (int, float))
                            or not math.isfinite(acknowledged_at)
                            or acknowledged_at < 0 or acknowledged_at > incident_epoch):
                        raise ValueError('invalid synthetic journey data')
                count = len(rows)
                age = incident_epoch - max(row[2] for row in rows)
                # Read-after-write journey in a rolled-back transaction.
                candidate.execute('INSERT INTO messages VALUES (?, ?, ?)',
                                  (max(row[0] for row in rows) + 1,
                                   'synthetic-recovery-probe', incident_epoch))
                if candidate.execute('SELECT COUNT(*) FROM messages').fetchone()[0] != count + 1:
                    raise ValueError('journey probe failure')
                candidate.rollback()
        if age > objectives.rpo_seconds:
            reasons.append('recovery point exceeds RPO target')
    except (OSError, sqlite3.Error, ValueError) as exc:
        reasons.append(str(exc))
    duration = clock() - start
    if not math.isfinite(duration) or duration < 0:
        reasons.append('invalid restore clock')
    elif duration > objectives.rto_seconds:
        reasons.append('restore exceeds local RTO target')
    if reasons:
        target.unlink(missing_ok=True)
    return RecoveryResult(not reasons, tuple(reasons), duration, age, count)
