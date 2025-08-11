# HC-SR04 water level via echo pulse duration -> distance cm -> tank %
import time
try:
    import RPi.GPIO as GPIO
except Exception:
    GPIO = None

class HCSR04:
    def __init__(self, trig_pin, echo_pin, tank_height_cm, empty_distance_cm):
        self.trig = trig_pin
        self.echo = echo_pin
        self.height = float(tank_height_cm)
        self.empty = float(empty_distance_cm)
        if GPIO:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.trig, GPIO.OUT)
            GPIO.setup(self.echo, GPIO.IN)

    def _distance_cm(self):
        if not GPIO:
            return self.empty - (self.height * 0.5)
        GPIO.output(self.trig, True)
        time.sleep(0.00001)
        GPIO.output(self.trig, False)
        start = time.time()
        while GPIO.input(self.echo) == 0:
            start = time.time()
        while GPIO.input(self.echo) == 1:
            stop = time.time()
        elapsed = stop - start
        dist = (elapsed * 34300) / 2  # speed of sound cm/s
        return dist

    def read_level_pct(self):
        d = self._distance_cm()
        # distance decreases when full. Convert to fill height = (empty - d)
        fill_cm = max(0.0, min(self.height, self.empty - d))
        pct = (fill_cm / self.height) * 100.0
        return round(pct, 2)
