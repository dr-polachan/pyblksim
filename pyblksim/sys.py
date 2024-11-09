import simpy

class sys:
    @staticmethod
    def init():
        return simpy.Environment()