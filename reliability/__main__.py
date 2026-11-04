"""Run bounded synthetic scenarios; all databases are temporary and cleaned up."""
import argparse
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory
from .recovery import Objectives, digest, restore


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scenario', choices=['healthy', 'stale', 'corrupt'], default='healthy')
    args = parser.parse_args()
    with TemporaryDirectory(prefix='recovery-lab-') as directory:
        root = Path(directory)
        source, backup, target = (root / n for n in ['primary.db', 'backup.db', 'restored.db'])
        incident = 1000.0  # Synthetic epoch, deliberately independent of wall time.
        acknowledged = 600.0 if args.scenario == 'stale' else 990.0
        with sqlite3.connect(source) as db:
            db.execute('CREATE TABLE messages (id INTEGER PRIMARY KEY, body TEXT NOT NULL, acknowledged_at REAL NOT NULL)')
            db.execute('INSERT INTO messages VALUES (1, ?, ?)', ('synthetic-message', acknowledged))
            db.commit()
            with sqlite3.connect(backup) as snapshot:
                db.backup(snapshot)
        expected = digest(backup)
        # Simulated primary loss is restricted to this generated temporary file.
        source.unlink()
        if args.scenario == 'corrupt':
            backup.write_bytes(b'corrupted synthetic backup')
        result = restore(backup, target, expected, incident_epoch=incident, objectives=Objectives())
        print(result.to_json())
        return 0 if result.eligible_for_promotion else 1


if __name__ == '__main__':
    raise SystemExit(main())
