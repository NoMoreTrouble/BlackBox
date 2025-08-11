try:
    import RPi.GPIO as GPIO
except Exception:
    GPIO = None
import time

class Relay:
    def __init__(self, pin, active_low=True):
        self.pin = pin
        self.active_low = bool(active_low)
        if GPIO:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin, GPIO.OUT)
            self.off()

    def on(self):
        if not GPIO:
            return
        GPIO.output(self.pin, GPIO.LOW if self.active_low else GPIO.HIGH)

    def off(self):
        if not GPIO:
            return
        GPIO.output(self.pin, GPIO.HIGH if self.active_low else GPIO.LOW)

    def pulse(self, seconds=1):
        self.on()
        time.sleep(seconds)
        self.off()
