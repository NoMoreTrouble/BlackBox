import Adafruit_DHT

class DHT22:
    def __init__(self, pin):
        self.pin = pin
    def read(self):
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, self.pin)
        if humidity is None or temperature is None:
            return None, None
        return float(temperature), float(humidity)
