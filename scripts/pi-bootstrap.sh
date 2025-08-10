#!/usr/bin/env bash
set -euo pipefail
echo "Enabling I2C and SPI via raspi-config"
raspi-config nonint do_i2c 0 || true
raspi-config nonint do_spi 0 || true
