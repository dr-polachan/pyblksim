import numpy as np

class UnaryMinus:
    def __init__(self, env, sampling_frequency=1000):
        self.env = env
        self.sampling_frequency = sampling_frequency
        self.input = []
        self.output = []
        self.env.process(self.sample())

    def sample(self):
        """Process to sample the input and calculate the absolute value."""
        sample_interval = 1 / self.sampling_frequency
        while True:
            if self.input:
                _, state = self.input[-1]
                self.output.append((self.env.now, -1*state))
            yield self.env.timeout(sample_interval)

class Signum:
    def __init__(self, env, sampling_frequency=1000):
        self.env = env
        self.sampling_frequency = sampling_frequency
        self.input = []
        self.output = []
        self.env.process(self.sample())

    def sample(self):
        """Process to sample the input and calculate the absolute value."""
        sample_interval = 1 / self.sampling_frequency
        while True:
            if self.input:
                _, state = self.input[-1]
                if state > 0:
                    self.output.append((self.env.now, 1))
                elif state < 0:                    
                    self.output.append((self.env.now, -1))
                else:
                    self.output.append((self.env.now, 0))                    
            yield self.env.timeout(sample_interval)

class Abs:
    def __init__(self, env, sampling_frequency=1000):
        self.env = env
        self.sampling_frequency = sampling_frequency
        self.input = []
        self.output = []
        self.env.process(self.sample())

    def sample(self):
        """Process to sample the input and calculate the absolute value."""
        sample_interval = 1 / self.sampling_frequency
        while True:
            if self.input:
                _, state = self.input[-1]
                self.output.append((self.env.now, np.abs(state)))
            yield self.env.timeout(sample_interval)


class Bias:
    def __init__(self, env, value=0, sampling_frequency=1000):
        self.env = env
        self.value = value
        self.sampling_frequency = sampling_frequency
        self.input = []
        self.output = []
        self.env.process(self.sample())

    def sample(self):
        """Process to sample the input and calculate the absolute value."""
        sample_interval = 1 / self.sampling_frequency
        while True:
            if self.input:
                _, state = self.input[-1]
                self.output.append((self.env.now, state+self.value))
            yield self.env.timeout(sample_interval)

class Round:
    def __init__(self, env, sampling_frequency=1000):
        self.env = env
        self.sampling_frequency = sampling_frequency
        self.input = []
        self.output = []
        self.env.process(self.sample())

    def sample(self):
        """Process to sample the input and calculate the absolute value."""
        sample_interval = 1 / self.sampling_frequency
        while True:
            if self.input:
                _, state = self.input[-1]
                self.output.append((self.env.now, np.round(state)))
            yield self.env.timeout(sample_interval)


class Gain:
    def __init__(self, env, sampling_frequency=1000, gain_value=10):
        self.env = env
        self.sampling_frequency = sampling_frequency
        self.gain_value = gain_value
        self.input = []
        self.output = []
        self.env.process(self.sample())
    
    def sample(self):
        """Process to sample the input and apply the gain."""
        sample_interval = 1 / self.sampling_frequency
        while True:
            if self.input:
                _, state = self.input[-1]
                self.output.append((self.env.now, state * self.gain_value))
            yield self.env.timeout(sample_interval)



class Sum:
    def __init__(self, env, sampling_frequency):
        self.env = env
        self.sampling_frequency = sampling_frequency
        self.input1 = [] # This will be a list of lists
        self.input2 = [] # This will be a list of lists
        self.output = []
        self.env.process(self.sample())
    
    def sample(self):
        """Process to sample the inputs and calculate their product."""
        sample_interval = 1 / self.sampling_frequency
        while True:
            # Ensure both inputs have data to sample
            if self.input1 and self.input2:
                # Take the latest value from each input
                _, state1 = self.input1[-1]
                _, state2 = self.input2[-1]
                # Calculate and store the product                
                self.output.append((self.env.now, state1+state2))
            yield self.env.timeout(sample_interval)

class Difference:
    def __init__(self, env, sampling_frequency):
        self.env = env
        self.sampling_frequency = sampling_frequency
        self.input1 = [] # This will be a list of lists
        self.input2 = [] # This will be a list of lists
        self.output = []
        self.env.process(self.sample())
    
    def sample(self):
        """Process to sample the inputs and calculate their product."""
        sample_interval = 1 / self.sampling_frequency
        while True:
            # Ensure both inputs have data to sample
            if self.input1 and self.input2:
                # Take the latest value from each input
                _, state1 = self.input1[-1]
                _, state2 = self.input2[-1]
                # Calculate and store the product                
                self.output.append((self.env.now, state1-state2))
            yield self.env.timeout(sample_interval)

class Integrator:
    def __init__(self, env, sampling_frequency=1000, initial_value=0):
        self.env = env
        self.sampling_frequency = sampling_frequency
        self.initial_value = initial_value
        self.input = []
        self.output = []
        self.env.process(self.sample())
    
    def sample(self):
        """Process to sample the input and integrate over time."""
        sample_interval = 1 / self.sampling_frequency
        integral = self.initial_value
        while True:
            if self.input:
                _, state = self.input[-1]
                integral += state * sample_interval
                self.output.append((self.env.now, integral))
            yield self.env.timeout(sample_interval)

class Differentiator:
    def __init__(self, env, sampling_frequency=1000):
        self.env = env
        self.sampling_frequency = sampling_frequency
        self.input = []
        self.output = []
        self.last_state = None
        self.env.process(self.sample())
    
    def sample(self):
        """Process to sample the input and differentiate it."""
        sample_interval = 1 / self.sampling_frequency
        while True:
            if self.input:
                if self.last_state is None:
                    self.last_state = self.input[-1]
                else:
                    _, current_state = self.input[-1]
                    _, last_state = self.last_state
                    derivative = (current_state - last_state) / sample_interval
                    self.output.append((self.env.now, derivative))
                    self.last_state = self.input[-1]
            yield self.env.timeout(sample_interval)

class GEQ: 
    def __init__(self, env, sampling_frequency):
        self.env = env
        self.sampling_frequency = sampling_frequency
        self.input1 = []
        self.input2 = []
        self.output = []
        self.env.process(self.sample())

    def sample(self):
        """Process to sample the inputs and calculate their product."""
        sample_interval = 1 / self.sampling_frequency
        while True:
            # Ensure both inputs have data to sample
            if self.input1 and self.input2:
                # Take the latest value from each input
                _, state1 = self.input1[-1]
                _, state2 = self.input2[-1]
                # Calculate and store the product
                if(state1 >= state2):
                    out = 1
                else:
                    out = 0
                self.output.append((self.env.now, out))
            yield self.env.timeout(sample_interval)
            
class Product:
    def __init__(self, env, sampling_frequency):
        self.env = env
        self.sampling_frequency = sampling_frequency
        self.input1 = []
        self.input2 = []
        self.output = []
        self.env.process(self.sample())

    def sample(self):
        """Process to sample the inputs and calculate their product."""
        sample_interval = 1 / self.sampling_frequency
        while True:
            # Ensure both inputs have data to sample
            if self.input1 and self.input2:
                # Take the latest value from each input
                _, state1 = self.input1[-1]
                _, state2 = self.input2[-1]
                # Calculate and store the product
                self.output.append((self.env.now, state1 * state2))
            yield self.env.timeout(sample_interval)

class Squaring:
    def __init__(self, env, sampling_frequency):
        self.env = env
        self.sampling_frequency = sampling_frequency
        self.input = []
        self.output = []
        self.env.process(self.sample())

    def sample(self):
        """Process to sample the inputs and calculate their product."""
        sample_interval = 1 / self.sampling_frequency
        while True:
            # Ensure both inputs have data to sample
            if self.input:
                # Take the latest value from each input
                _, state = self.input[-1]
                # Calculate and store the product
                self.output.append((self.env.now, np.square(state)))
            yield self.env.timeout(sample_interval)
