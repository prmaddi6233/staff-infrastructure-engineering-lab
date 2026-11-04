#!/usr/bin/env bash
# Run as an unprivileged user with PostgreSQL server and client tools on PATH.
set -euo pipefail
scenario=${1:-healthy}
case "$scenario" in healthy|missing|stale|corrupt|schema) ;; *) exit 2 ;; esac
[[ $(id -u) != 0 ]] || { echo 'initdb requires a non-root user' >&2; exit 2; }
for tool in initdb pg_ctl psql pg_dump pg_restore createdb; do command -v "$tool" >/dev/null || exit 2; done
root=$(mktemp -d)
export PGHOST="$root" PGPORT=5432 PGUSER=drill PGDATABASE=postgres
unset PGSERVICE PGOPTIONS PGSERVICEFILE
cleanup() {
  if [[ -f "$root/data/postmaster.pid" ]]; then
    pg_ctl -D "$root/data" -m immediate -w stop >/dev/null || return 1
  fi
  rm -rf -- "$root"
}
trap cleanup EXIT
initdb -U drill -A trust -D "$root/data" > /dev/null
pg_ctl -D "$root/data" -l "$root/server.log" -o "-c listen_addresses='' -c unix_socket_directories='$root'" -w start >/dev/null
sql() { psql -XAtq -v ON_ERROR_STOP=1 -d "$1" -c "$2"; }
createdb source
sql source 'CREATE TABLE messages(id integer PRIMARY KEY, body text NOT NULL, ack_epoch integer NOT NULL)'
ack=990
if [[ $scenario == stale ]]; then ack=600; fi
# psql exits successfully only after the statement commits. Keep the returned ID
# outside both databases, so restoring the backup cannot rewind the witness.
sql source "INSERT INTO messages VALUES(1,'synthetic-one',$ack) RETURNING id" > "$root/ledger"
if [[ $scenario == schema ]]; then sql source 'ALTER TABLE messages RENAME body TO obsolete'; fi
pg_dump -Fc source > "$root/backup"
sha256sum "$root/backup" > "$root/expected"
if [[ $scenario == missing ]]; then
  sql source "INSERT INTO messages VALUES(2,'synthetic-two',999) RETURNING id" >> "$root/ledger"
fi
if [[ $scenario == corrupt ]]; then truncate -s 10 "$root/backup"; fi
createdb candidate
start=$(date +%s)
sha256sum --status -c "$root/expected" || { echo 'REFUSED checksum'; exit 1; }
pg_restore --exit-on-error --single-transaction -d candidate "$root/backup"
sql candidate 'SELECT id FROM messages ORDER BY id' > "$root/actual"
diff -u "$root/ledger" "$root/actual" || { echo 'REFUSED acknowledgement mismatch'; exit 1; }
shape=$(sql candidate "SELECT string_agg(column_name || ':' || data_type, ',' ORDER BY ordinal_position) FROM information_schema.columns WHERE table_schema='public' AND table_name='messages'")
[[ $shape == 'id:integer,body:text,ack_epoch:integer' ]] || { echo 'REFUSED schema'; exit 1; }
age=$(sql candidate 'SELECT 1000-max(ack_epoch) FROM messages')
[[ $age =~ ^[0-9]+$ && $age -le 300 ]] || { echo 'REFUSED stale'; exit 1; }
sql candidate "INSERT INTO messages VALUES(1,'synthetic-one',$ack) ON CONFLICT(id) DO NOTHING"
[[ $(sql candidate "SELECT count(*) FROM messages WHERE id=1 AND body='synthetic-one'") == 1 ]]
echo "ELIGIBLE reconciled=1 recovery_point_age_seconds=$age local_restore_validation_seconds=$(( $(date +%s) - start ))"
