#!/usr/bin/env bash
set -euo pipefail

echo "---- Starting installation ----"

# Install OS dependencies
echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y --no-install-recommends python3-venv python3-pip git tmux gettext

# Create a virtual environment if it doesn't exist
if [[ ! -d .venv ]]; then
  echo "Creating virtual environment in .venv"
  python3 -m venv .venv
  echo "Virtual environment created in .venv"
else
  echo "Virtual environment already exists in .venv"
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Check if we're inside the virtual environment
echo "---- Checking the virtual environment ----"
which python
which pip
echo "Python version: $(python --version)"
echo "Pip version: $(pip --version)"

# Upgrade pip in the virtual environment
echo "Upgrading pip..."
pip install --upgrade pip

# Install the required Python packages inside the virtual environment
echo "Installing Python dependencies from requirements.txt..."
pip install -r requirements.txt

# Compile translations (if any)
echo "Compiling translations (if any)..."
pybabel compile -d plant_monitor/web/translations || true

# Create log folders (if they don't exist)
echo "Creating log directories..."
mkdir -p var/log

# Install systemd service for background running of the app
echo "Installing systemd service for the app..."
sudo install -m 0644 scripts/systemd/blackbox-monitor.service /etc/systemd/system/blackbox-monitor.service
sudo systemctl daemon-reload
sudo systemctl enable plant-monitor.service
sudo systemctl restart plant-monitor.service

# Setup tmux helper for log monitoring (optional)
echo "Setting up tmux for log monitoring..."
chmod +x scripts/tmux-monitor.sh

echo "Installation complete. Visit http://<pi-ip>:${FLASK_PORT:-8080}"

