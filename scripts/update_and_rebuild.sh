#!/usr/bin/env bash
set -euo pipefail
TOKEN="${1:-}"
curl -fsS -X POST "http://localhost:${FLASK_PORT:-8080}/webhook/update?token=${TOKEN}" || true
