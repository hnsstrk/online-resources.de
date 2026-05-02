#!/bin/bash
set -euo pipefail

REPO_DIR="/home/hans/Repositories/online-resources.de"
DEPLOY_DIR="/var/www/online-resources.de"

cd "$REPO_DIR"
git pull --ff-only origin main
git submodule update --init --recursive

# Wenn build.sh selbst durch den Pull aktualisiert wurde, läuft der bash-Prozess
# noch mit der alten Skript-Sequenz im Speicher. Re-exec einmal in der neuen
# Version weiter — BUILD_REEXECED schützt vor Endlos-Loops.
if [ -z "${BUILD_REEXECED:-}" ]; then
  export BUILD_REEXECED=1
  exec "$0" "$@"
fi

# PostCSS-Pipeline (theme: rollenspiel) — node_modules aus Lockfile installieren.
# --prefer-offline und --no-audit halten den Schritt schnell, sobald der Cache warm ist.
npm ci --no-audit --prefer-offline

hugo --minify --gc --cleanDestinationDir --destination "$DEPLOY_DIR"

# Prüfe ob Build erfolgreich
[ -f "$DEPLOY_DIR/index.html" ] || { echo "Build fehlgeschlagen: index.html fehlt"; exit 1; }
echo "Deploy erfolgreich: $(date)"
