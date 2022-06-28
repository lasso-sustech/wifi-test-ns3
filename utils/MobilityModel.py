#!/usr/bin/env python3
from abc import ABC, abstractclassmethod
from ns.mobility import MobilityHelper

class MobilityModel(ABC):
    def __init__(self, node):
        self.mobility = MobilityHelper()
        self.mobility.install(node)
        node.mobility = self.mobility
        pass

    @abstractclassmethod
    def advance(self):
        pass

    pass

class StayStill(MobilityModel):
    def __init__(self, node):
        super().__init__(node)
        self.mobility.SetMobilityModel('ns3::ConstantPositionMobilityModel')
        pass
    
    def setMobility(self):
        pass

    def advance(self):
        pass

    pass

class RandomWalk(MobilityModel):
    pass

