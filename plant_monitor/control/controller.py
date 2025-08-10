import time, logging, traceback
from datetime import datetime
from ..sensors.factory import build_sensors
from ..actuators.relay import Relay
from ..actuators.simulator import SimRelay
from ..control.forecast import ewma
from ..models import db, Reading, ActuationLog

log = logging.getLogger("control")

class ControlLoop:
    def __init__(self, cfg):
        self.cfg = cfg
        self.mode = cfg["MODE"]
        self.sensors = build_sensors(cfg)
        if self.mode == "SIMULATION":
            self.light = SimRelay("light")
            self.irrigation = SimRelay("irrigation")
        else:
            self.light = Relay(cfg["RELAY_LIGHT_PIN"], cfg["RELAY_ACTIVE_LOW"])
            self.irrigation = Relay(cfg["RELAY_IRRIGATION_PIN"], cfg["RELAY_ACTIVE_LOW"])
        self.soil_avg_ewma = None

    def run(self):
        interval = int(self.cfg["SAMPLE_INTERVAL_SECONDS"])
        alpha = float(self.cfg["EWMA_ALPHA"])
        threshold = float(self.cfg["AUTO_WATER_THRESHOLD"])
        pulse_seconds = int(self.cfg["IRRIGATION_PULSE_SECONDS"])
        while True:
            try:
                t, h = self.sensors["th"].read()
                s1, s2, s3 = self.sensors["soil"].read_three()
                avg = round((s1 + s2 + s3)/3.0, 2)
                self.soil_avg_ewma = round(ewma(self.soil_avg_ewma, avg, alpha), 2) if avg is not None else self.soil_avg_ewma
                water = self.sensors["water"].read_level_pct()
                r = Reading(temperature=t, humidity=h, soil1=s1, soil2=s2, soil3=s3,
                            soil_avg=avg, soil_avg_ewma=self.soil_avg_ewma, water_level_pct=water)
                db.session.add(r)
                db.session.commit()

                # Auto irrigation
                if avg is not None and avg < threshold:
                    self.irrigation.pulse(pulse_seconds)
                    db.session.add(ActuationLog(device="irrigation", action="pulse", duration=pulse_seconds))
                    db.session.commit()

            except Exception as e:
                log.error("Control loop error: %s\n%s", e, traceback.format_exc())

            time.sleep(interval)

    # Manual controls exposed to routes
    def pulse_irrigation(self, seconds):
        self.irrigation.pulse(seconds)
        db.session.add(ActuationLog(device="irrigation", action="pulse", duration=seconds))
        db.session.commit()

    def light_on(self):
        self.light.on()
        db.session.add(ActuationLog(device="light", action="on", duration=0))
        db.session.commit()

    def light_off(self):
        self.light.off()
        db.session.add(ActuationLog(device="light", action="off", duration=0))
        db.session.commit()
