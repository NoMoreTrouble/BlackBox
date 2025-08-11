# Reads 3 soil probes via ADS1115 (I²C). Convert raw to % using calibration.
try:
    import board, busio
    from adafruit_ads1x15.ads1115 import ADS1115, Mode
    from adafruit_ads1x15.analog_in import AnalogIn
except Exception:  # allow import on non-Pi
    ADS1115 = None

class SoilADS1115:
    def __init__(self, address=0x48, wet_cal=18000, dry_cal=28000):
        self.address = address
        self.wet = float(wet_cal)
        self.dry = float(dry_cal)
        if ADS1115:
            i2c = busio.I2C(board.SCL, board.SDA)
            self.ads = ADS1115(i2c, address=address)
            self.ads.mode = Mode.CONTINUOUS
            self.channels = [AnalogIn(self.ads, i) for i in range(3)]
        else:
            self.ads = None
            self.channels = [None, None, None]

    def _pct(self, raw):
        # Map raw counts (higher when dry) to moisture %
        raw = float(raw)
        pct = (self.dry - raw) / (self.dry - self.wet) * 100.0
        return max(0.0, min(100.0, pct))

    def read_three(self):
        if not self.ads:
            # placeholder values when not on Pi
            return (50.0, 50.0, 50.0)
        raws = [ch.value for ch in self.channels]
        return tuple(round(self._pct(r),2) for r in raws)
