import simpy
import matplotlib.pyplot as plt

class Environment:
    @staticmethod
    def init():
        plt.close('all')
        return simpy.Environment()