from .simulator import SimDHT22, SimSoil, SimWater
from .dht22 import DHT22
from .moisture_ads1115 import SoilADS1115
from .moisture_mcp3008 import SoilMCP3008
from .hcsr04 import HCSR04

def build_sensors(cfg):
    mode = cfg.get("MODE", "SIMULATION").upper()
    if mode == "SIMULATION":
        return {
            "th": SimDHT22(),
            "soil": SimSoil(),
            "water": SimWater()
        }
    else:
        if cfg.get("ADC_DRIVER", "ADS1115").upper() == "ADS1115":
            soil = SoilADS1115(cfg["ADS1115_ADDRESS"], cfg["SOIL_WET_CAL"], cfg["SOIL_DRY_CAL"])
        else:
            soil = SoilMCP3008(cfg["MCP3008_CHANNELS"], cfg["MCP3008_SPI_BUS"], cfg["MCP3008_SPI_DEVICE"],
                               cfg["SOIL_WET_CAL"], cfg["SOIL_DRY_CAL"])
        return {
            "th": DHT22(cfg["DHT22_PIN"]),
            "soil": soil,
            "water": HCSR04(cfg["HCSR04_TRIG_PIN"], cfg["HCSR04_ECHO_PIN"], cfg["TANK_HEIGHT_CM"], cfg["TANK_EMPTY_DISTANCE_CM"])
        }
