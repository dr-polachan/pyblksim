import numpy as np

class PController:
    def __init__(self, env, sampling_frequency=1000, Kp=1, output_limit=[-1000, 1000]):
        """
        Initialize the Proportional (P) Controller.

        Parameters:
            env: The simulation environment.
            sampling_frequency: Frequency at which the controller samples input (Hz).
            Kp: Proportional gain.
            output_limit: List specifying the lower and upper bounds for the output.
        """
        self.env = env
        self.sampling_frequency = sampling_frequency
        self.Kp = Kp  # Proportional gain
        self.output_limit = output_limit
        self.input = []  # List of (time, value) pairs for input signal
        self.output = []  # List of (time, value) pairs for control action output
        self.env.process(self.sample())  # Start sampling process in the simulation environment

    def sample(self):
        """Process to compute and apply control action based on the latest error."""
        sample_interval = 1 / self.sampling_frequency  # Interval between samples (seconds)
        while True:
            if self.input:  # If input data is available
                _, state = self.input[-1]  # Get the latest input state
                output = np.clip(self.Kp * state, self.output_limit[0], self.output_limit[1])
                # Apply proportional control and limit output to specified range
                self.output.append((self.env.now, output))
            else:
                # Default output to 0 if no input data is available
                self.output.append((self.env.now, 0))

            yield self.env.timeout(sample_interval)  # Wait for the next sample interval


class PIController:
    def __init__(self, env, sampling_frequency=1000, Kp=1, Ki=0, output_limit=[-1000, 1000]):
        """
        Initialize the Proportional-Integral (PI) Controller.

        Parameters:
            env: The simulation environment.
            sampling_frequency: Frequency at which the controller samples input (Hz).
            Kp: Proportional gain.
            Ki: Integral gain.
            output_limit: List specifying the lower and upper bounds for the output.
        """
        self.env = env
        self.sampling_frequency = sampling_frequency
        self.Kp = Kp  # Proportional gain
        self.Ki = Ki  # Integral gain
        self.output_limit = output_limit
        self.input = []  # List of (time, value) pairs for input signal
        self.output = []  # List of (time, value) pairs for control action output
        self.integral = 0  # Integral accumulator to hold accumulated error
        self.env.process(self.sample())  # Start sampling process in the simulation environment

    def sample(self):
        """Process to compute control action using proportional and integral error."""
        sample_interval = 1 / self.sampling_frequency  # Interval between samples (seconds)
        while True:
            if self.input:
                _, state = self.input[-1]  # Get the latest input state
                self.integral += state * sample_interval  # Update integral with current error
                output = np.clip(self.Kp * state + self.Ki * self.integral,
                                 self.output_limit[0], self.output_limit[1])
                # Apply proportional and integral control, limit output to specified range
                self.output.append((self.env.now, output))
            else:
                # Default output to 0 if no input data is available
                self.output.append((self.env.now, 0))

            yield self.env.timeout(sample_interval)  # Wait for the next sample interval


class PIDController:
    def __init__(self, env, sampling_frequency=1000, Kp=1, Ki=0, Kd=0, output_limit=[-1000, 1000]):
        """
        Initialize the Proportional-Integral-Derivative (PID) Controller.

        Parameters:
            env: The simulation environment.
            sampling_frequency: Frequency at which the controller samples input (Hz).
            Kp: Proportional gain.
            Ki: Integral gain.
            Kd: Derivative gain.
            output_limit: List specifying the lower and upper bounds for the output.
        """
        self.env = env
        self.sampling_frequency = sampling_frequency
        self.Kp = Kp  # Proportional gain
        self.Ki = Ki  # Integral gain
        self.Kd = Kd  # Derivative gain
        self.output_limit = output_limit
        self.input = []  # List of (time, value) pairs for input signal
        self.output = []  # List of (time, value) pairs for control action output
        self.integral = 0  # Integral accumulator to hold accumulated error
        self.previous_error = 0  # Stores previous error for derivative calculation
        self.env.process(self.sample())  # Start sampling process in the simulation environment

    def sample(self):
        """Process to compute control action using proportional, integral, and derivative error."""
        sample_interval = 1 / self.sampling_frequency  # Interval between samples (seconds)
        while True:
            if self.input:
                _, state = self.input[-1]  # Get the latest input state
                error = state  # Current error value
                self.integral += error * sample_interval  # Update integral with current error
                derivative = (error - self.previous_error) / sample_interval if sample_interval > 0 else 0
                # Calculate derivative based on change in error
                output = np.clip(self.Kp * error + self.Ki * self.integral + self.Kd * derivative,
                                 self.output_limit[0], self.output_limit[1])
                # Apply PID control and limit output to specified range
                self.output.append((self.env.now, output))
                self.previous_error = error  # Update previous error for the next derivative calculation
            else:
                # Default output to 0 if no input data is available
                self.output.append((self.env.now, 0))

            yield self.env.timeout(sample_interval)  # Wait for the next sample interval
