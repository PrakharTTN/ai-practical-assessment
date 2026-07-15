#!/bin/sh
set -e

echo "[entrypoint] Waiting for PostgreSQL..."
until python -c "
import os, sys
import psycopg2
url = os.environ.get('DATABASE_URL', '')
# psycopg2 needs libpq URL without +driver suffix
url = url.replace('postgresql+psycopg2://', 'postgresql://')
try:
    conn = psycopg2.connect(url)
    conn.close()
    sys.exit(0)
except Exception:
    sys.exit(1)
" 2>/dev/null; do
  echo "[entrypoint] Postgres not ready — retrying in 2s..."
  sleep 2
done
echo "[entrypoint] PostgreSQL is ready."

/scripts/migrate.sh
/scripts/seed.sh

echo "[entrypoint] Starting backend..."
exec "$@"
