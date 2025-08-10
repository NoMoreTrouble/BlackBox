import os

class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///var/plant_monitor.sqlite3")
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = bool(int(os.getenv("FLASK_DEBUG", "0")))
    HOST = os.getenv("FLASK_HOST", "0.0.0.0")
    PORT = int(os.getenv("FLASK_PORT", "8080"))
    MODE = os.getenv("MODE", "SIMULATION").upper()
    ADS1115_ADDRESS = int(os.getenv("ADS1115_ADDRESS", "0x48"), 16)
    ADC_DRIVER = os.getenv("ADC_DRIVER", "ADS1115").upper()
    MCP3008_SPI_BUS = int(os.getenv("MCP3008_SPI_BUS", "0"))
    MCP3008_SPI_DEVICE = int(os.getenv("MCP3008_SPI_DEVICE", "0"))
    MCP3008_CHANNELS = [int(x) for x in os.getenv("MCP3008_CHANNELS", "0,1,2").split(",")]
    DHT22_PIN = int(os.getenv("DHT22_PIN", "4"))
    HCSR04_TRIG_PIN = int(os.getenv("HCSR04_TRIG_PIN", "23"))
    HCSR04_ECHO_PIN = int(os.getenv("HCSR04_ECHO_PIN", "24"))
    TANK_HEIGHT_CM = float(os.getenv("TANK_HEIGHT_CM", "30"))
    TANK_EMPTY_DISTANCE_CM = float(os.getenv("TANK_EMPTY_DISTANCE_CM", "32"))
    RELAY_LIGHT_PIN = int(os.getenv("RELAY_LIGHT_PIN", "17"))
    RELAY_IRRIGATION_PIN = int(os.getenv("RELAY_IRRIGATION_PIN", "27"))
    RELAY_ACTIVE_LOW = bool(int(os.getenv("RELAY_ACTIVE_LOW", "1")))
    SOIL_WET_CAL = float(os.getenv("SOIL_WET_CAL", "18000"))
    SOIL_DRY_CAL = float(os.getenv("SOIL_DRY_CAL", "28000"))
    AUTO_WATER_THRESHOLD = float(os.getenv("AUTO_WATER_THRESHOLD", "35"))
    IRRIGATION_PULSE_SECONDS = int(os.getenv("IRRIGATION_PULSE_SECONDS", "10"))
    SAMPLE_INTERVAL_SECONDS = int(os.getenv("SAMPLE_INTERVAL_SECONDS", "20"))
    EWMA_ALPHA = float(os.getenv("EWMA_ALPHA", "0.3"))
    UPDATE_WEBHOOK_TOKEN = os.getenv("UPDATE_WEBHOOK_TOKEN", "token")
    ENABLE_DOCKER_REBUILD = bool(int(os.getenv("ENABLE_DOCKER_REBUILD", "0")))
    DOCKER_COMPOSE_FILE_PATH = os.getenv("DOCKER_COMPOSE_FILE_PATH", "./docker-compose.yml")
    IN_DOCKER = bool(int(os.getenv("IN_DOCKER", "0")))
    # Auth
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "changeme")
    # i18n
    BABEL_DEFAULT_LOCALE = os.getenv("BABEL_DEFAULT_LOCALE", "en")
    BABEL_SUPPORTED_LOCALES = [x.strip() for x in os.getenv("BABEL_SUPPORTED_LOCALES", "en,it").split(",")]
    BABEL_DEFAULT_TIMEZONE = os.getenv("BABEL_DEFAULT_TIMEZONE", "Europe/Rome")
    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
