#!/usr/bin/env bash
set -euo pipefail

if [[ ${EUID} -ne 0 ]]; then
  echo "Please run as root: sudo scripts/install.sh"
  exit 1
fi

# Install OS deps
apt-get update
apt-get install -y --no-install-recommends python3-venv python3-pip git tmux gettext

# Enable interfaces on Pi
if command -v raspi-config >/dev/null 2>&1; then
  ./scripts/pi-bootstrap.sh || true
fi

# Python venv
if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

# Compile translations
pybabel compile -d plant_monitor/web/translations || true

# Create database folders
mkdir -p var/log

# Create systemd service
install -m 0644 scripts/systemd/plant-monitor.service /etc/systemd/system/plant-monitor.service
systemctl daemon-reload
systemctl enable plant-monitor.service
systemctl restart plant-monitor.service

# Setup tmux helper (optional)
chmod +x scripts/tmux-monitor.sh

echo "Installation complete. Visit http://<pi-ip>:${FLASK_PORT:-8080}"
