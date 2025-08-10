import time, logging
log = logging.getLogger("actuators")

class SimRelay:
    def __init__(self, name):
        self.name = name
        self.state = False
    def on(self):
        self.state = True
        log.info("%s ON", self.name)
    def off(self):
        self.state = False
        log.info("%s OFF", self.name)
    def pulse(self, seconds=1):
        log.info("%s PULSE %ss", self.name, seconds)
        self.on()
        time.sleep(seconds)
        self.off()
