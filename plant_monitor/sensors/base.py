from abc import ABC, abstractmethod

class TempHumiditySensor(ABC):
    @abstractmethod
    def read(self):
        '''Return (temperature_c, humidity_percent) or (None, None) on failure'''
        ...

class SoilSensor(ABC):
    @abstractmethod
    def read_three(self):
        '''Return tuple of three moisture percentages [0-100]'''
        ...

class WaterLevelSensor(ABC):
    @abstractmethod
    def read_level_pct(self):
        '''Return water level percent 0-100'''
        ...
