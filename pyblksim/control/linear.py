import numpy as np

class PController:
    def __init__(self, env, sampling_frequency=1000, Kp=1, output_limit=[-1000,1000]):
        self.env = env
        self.sampling_frequency = sampling_frequency
        self.Kp = Kp  # Proportional gain
        self.output_limit = output_limit
        self.input = []  # This will be a list of (time, value) pairs
        self.output = []  # This will store the control action output
        self.env.process(self.sample())

    def sample(self):
        """Process to calculate control action based on the proportional error."""
        sample_interval = 1 / self.sampling_frequency
        while True:
            if self.input:
                _, state = self.input[-1]
                output = np.clip(self.Kp*state,self.output_limit[0],\
                                 self.output_limit[1])
                self.output.append((self.env.now, output))
            else:
                self.output.append((self.env.now, 0))

            yield self.env.timeout(sample_interval)



       
