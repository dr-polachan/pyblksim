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

import numpy as np

class PIController:
    def __init__(self, env, sampling_frequency=1000, Kp=1, Ki=0, output_limit=[-1000, 1000]):
        self.env = env
        self.sampling_frequency = sampling_frequency
        self.Kp = Kp  # Proportional gain
        self.Ki = Ki  # Integral gain
        self.output_limit = output_limit
        self.input = []  # This will be a list of (time, value) pairs
        self.output = []  # This will store the control action output
        self.integral = 0  # Integral accumulator
        self.env.process(self.sample())

    def sample(self):
        """Process to calculate control action based on proportional and integral error."""
        sample_interval = 1 / self.sampling_frequency
        while True:
            if self.input:
                _, state = self.input[-1]
                self.integral += state * sample_interval  # Update integral
                output = np.clip(self.Kp * state + self.Ki * self.integral,
                                 self.output_limit[0], self.output_limit[1])
                self.output.append((self.env.now, output))
            else:
                self.output.append((self.env.now, 0))

            yield self.env.timeout(sample_interval)


class PIDController:
    def __init__(self, env, sampling_frequency=1000, Kp=1, Ki=0, Kd=0, output_limit=[-1000, 1000]):
        self.env = env
        self.sampling_frequency = sampling_frequency
        self.Kp = Kp  # Proportional gain
        self.Ki = Ki  # Integral gain
        self.Kd = Kd  # Derivative gain
        self.output_limit = output_limit
        self.input = []  # This will be a list of (time, value) pairs
        self.output = []  # This will store the control action output
        self.integral = 0  # Integral accumulator
        self.previous_error = 0  # To store the previous error for derivative calculation
        self.env.process(self.sample())

    def sample(self):
        """Process to calculate control action based on proportional, integral, and derivative error."""
        sample_interval = 1 / self.sampling_frequency
        while True:
            if self.input:
                _, state = self.input[-1]
                error = state
                self.integral += error * sample_interval
                derivative = (error - self.previous_error) / sample_interval if sample_interval > 0 else 0
                output = np.clip(self.Kp * error + self.Ki * self.integral + self.Kd * derivative,
                                 self.output_limit[0], self.output_limit[1])
                self.output.append((self.env.now, output))
                self.previous_error = error
            else:
                self.output.append((self.env.now, 0))

            yield self.env.timeout(sample_interval)



       
