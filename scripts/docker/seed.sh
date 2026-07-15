#!/bin/sh
set -e

cd /app

if [ ! -f app/seed.py ]; then
  echo "[seed] app/seed.py not found — skipping seed (scaffold not ready)"
  exit 0
fi

echo "[seed] Running seed script..."
python -m app.seed
echo "[seed] Done."
