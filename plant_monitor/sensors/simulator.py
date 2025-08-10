import random, math, time

class SimDHT22:
    def read(self):
        # Simulate daily cycle
        t = time.time() % 86400
        temp = 20 + 5*math.sin(2*math.pi*t/86400)
        hum = 50 + 10*math.cos(2*math.pi*t/43200) + random.uniform(-2,2)
        return round(temp,2), round(max(25, min(90, hum)),2)

class SimSoil:
    def __init__(self):
        self.base = [60, 55, 50]
    def read_three(self):
        drift = [random.uniform(-1,1) for _ in range(3)]
        vals = [max(10, min(90, b + d)) for b,d in zip(self.base, drift)]
        # slow trend downwards
        self.base = [v - 0.05 for v in vals]
        return tuple(round(v,2) for v in vals)

class SimWater:
    def __init__(self):
        self.level = 80.0
    def read_level_pct(self):
        # slowly decrease level
        self.level -= 0.1
        if self.level < 10: self.level = 90.0
        return round(self.level,2)
