# Reads 3 soil probes via MCP3008 (SPI). Convert raw (0..1023) to % using calibration.
try:
    import spidev
except Exception:
    spidev = None

class SoilMCP3008:
    def __init__(self, channels=(0,1,2), spi_bus=0, spi_dev=0, wet_cal=250, dry_cal=800):
        self.channels = tuple(channels)
        self.wet = float(wet_cal)
        self.dry = float(dry_cal)
        if spidev:
            self.spi = spidev.SpiDev()
            self.spi.open(spi_bus, spi_dev)
            self.spi.max_speed_hz = 1350000
        else:
            self.spi = None

    def _read_channel(self, ch):
        # MCP3008 SPI protocol
        cmd = 0b11 << 6 | (ch & 0x7) << 3
        resp = self.spi.xfer2([1, cmd, 0])
        val = ((resp[1] & 0x0F) << 8) | resp[2]
        return val

    def _pct(self, raw):
        raw = float(raw)
        pct = (self.dry - raw) / (self.dry - self.wet) * 100.0
        return max(0.0, min(100.0, pct))

    def read_three(self):
        if not self.spi:
            return (50.0, 50.0, 50.0)
        vals = [self._read_channel(ch) for ch in self.channels]
        return tuple(round(self._pct(v),2) for v in vals)
