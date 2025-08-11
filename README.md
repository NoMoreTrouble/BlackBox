# Raspberry Pi Plant Monitor — SIMULATION + PRODUCTION

A production-ready plant monitoring & control system for Raspberry Pi with a dark, minimalist web dashboard, historical charts, multilingual UI (English/Italian), and both **SIMULATION** and **PRODUCTION** modes. Includes Docker support, native Raspberry Pi installers, webhooks for Git updates with rollback, Telegram notifications, tests, and documentation.

## Highlights
- DHT22, 3× soil probes via ADS1115 or MCP3008, HC-SR04 water level
- Relays for **light** and **irrigation**
- Auto & Manual control modes
- SQLite + SQLAlchemy ORM
- Flask dashboard (dark monochrome + Chart.js)
- Flask-Login auth, Flask-Babel (EN/IT) with language switcher
- Webhook Git pull + rollback; optional Docker rebuild; Telegram notifications
- Dockerfile + docker-compose (multi-arch)
- Native Raspberry Pi install scripts (enable I²C/SPI, systemd, tmux log monitor)
- Pytest with mocked sensors for simulation mode

## Quickstart (Docker)
```bash
cp .env.example .env
# Edit .env as needed (admin password, tokens, pins)
docker compose up -d --build
# Visit http://localhost:8080  (default credentials created on first run)
```

## Quickstart (Native on Raspberry Pi)
```bash
cp .env.example .env
chmod +x scripts/install.sh scripts/pi-bootstrap.sh
sudo scripts/install.sh
# When done: http://<pi-ip>:8080
```

See **docs/INSTALL_PI.md** for a step-by-step guide.
