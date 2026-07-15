#!/bin/sh
set -e

cd /app

if [ ! -f alembic.ini ]; then
  echo "[migrate] alembic.ini not found — skipping migrations (scaffold not ready)"
  exit 0
fi

echo "[migrate] Running alembic upgrade head..."
alembic upgrade head
echo "[migrate] Done."
