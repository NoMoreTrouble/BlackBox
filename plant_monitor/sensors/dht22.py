import adafruit_dht

class DHT22:
    def __init__(self, pin):
        self.pin = pin
    def read(self):
        humidity, temperature = adafruit_dht.read_retry(adafruit_dht.DHT22, self.pin)
        if humidity is None or temperature is None:
            return None, None
        return float(temperature), float(humidity)
