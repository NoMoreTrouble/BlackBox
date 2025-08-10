# Install on Raspberry Pi (Raspberry Pi OS)

> Works on Raspberry Pi OS (Bookworm/Bullseye). Supports **PRODUCTION** mode with GPIO/I²C/SPI.

## 1) Prepare the system
- Flash Raspberry Pi OS (Lite is fine).
- Boot, connect to network, `ssh pi@<ip>`.

## 2) Clone
```bash
sudo apt-get update && sudo apt-get install -y git
git clone https://example.com/your/plant-monitor.git
cd plant-monitor
cp .env.example .env
# Edit .env (secret key, admin password, thresholds, pins, ADC driver)
```

## 3) Install
```bash
chmod +x scripts/install.sh scripts/pi-bootstrap.sh
sudo scripts/install.sh
```

This will:
- Install Python virtual env + dependencies
- Enable I²C and SPI (via raspi-config)
- Compile translations (Flask-Babel)
- Create `var/log` and SQLite DB
- Install & start `systemd` service listening on port `8080` (by default)

## 4) First login
- Visit `http://<pi-ip>:8080`
- Default login from `.env`: `ADMIN_USERNAME` / `ADMIN_PASSWORD`

## 5) Switching Modes
- **SIMULATION**: runs mocked sensors/relays (works on any Linux or in Docker)
- **PRODUCTION**: uses real GPIO/I²C/SPI on the Raspberry Pi

Set `MODE` in `.env` and restart service:
```bash
sudo systemctl restart plant-monitor.service
```

## 6) ADC Selection
Set `ADC_DRIVER=ADS1115` (I²C) or `MCP3008` (SPI) in `.env`. Adjust calibration points:
- ADS1115: `SOIL_WET_CAL`, `SOIL_DRY_CAL` (counts)
- MCP3008: `SOIL_WET_CAL`, `SOIL_DRY_CAL` (0..1023)

## 7) Update via Webhook
- Expose `/webhook/update` with header `X-Update-Token` (or `?token=`)
- On success, optional Docker rebuild if `ENABLE_DOCKER_REBUILD=1`

## 8) tmux log monitor
```bash
./scripts/tmux-monitor.sh
```

## 9) Services
- Health endpoint: `/healthz`
- API history: `/api/history?range=24h`
