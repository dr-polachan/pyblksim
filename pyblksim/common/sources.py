import numpy as np
import csv
import simpy

class PRBSGenerator:
    def __init__(self, env, clock_frequency, sampling_frequency, amplitude=1, seed=None, length=7, taps=[6, 7]):
        self.env = env
        self.clock_frequency = clock_frequency  # Frequency at which new bits are generated
        self.sampling_frequency = sampling_frequency  # Frequency at which the output is sampled
        self.amplitude = amplitude  # Amplitude to scale the output
        self.seed = seed  # Optional seed for repeatability
        self.length = length  # Length of the LFSR register
        self.taps = taps  # Positions to apply the XOR feedback
        self.state = self.initialize_lfsr()  # Initialize the LFSR
        self.output = []
        self.env.process(self.generate_prbs())
        self.env.process(self.sampling_process())

    def initialize_lfsr(self):
        """Initialize the LFSR with either a seed or random state."""
        if self.seed is not None:
            np.random.seed(self.seed)
            return np.random.randint(1, 2**self.length - 1)
        else:
            return np.random.randint(1, 2**self.length - 1)

    def generate_prbs(self):
        """Generate a pseudo-random binary sequence at the clock frequency."""
        while True:
            xor = 0
            for tap in self.taps:
                xor ^= (self.state >> (tap - 1)) & 1  # Apply XOR feedback
            self.state = ((self.state << 1) | xor) & (2**self.length - 1)  # Shift left and apply feedback
            # Output the LSB as the PRBS immediately after state update
            # Center the output around 0 and scale by amplitude: Map 0 to -amplitude and 1 to +amplitude
            bit_value = (self.state & 1) * 2 - 1
            bit_value *= self.amplitude
            self.output.append((self.env.now, bit_value))
            yield self.env.timeout(1 / self.clock_frequency)

    def sampling_process(self):
        """Process to sample the state at the sampling frequency."""
        sample_interval = 1 / self.sampling_frequency
        last_sample_time = 0
        while True:
            if self.env.now >= last_sample_time + sample_interval:
                last_sample_time = self.env.now
                # Sample and center the bit value around 0, scaled by amplitude
                bit_value = (self.state & 1) * 2 - 1
                bit_value *= self.amplitude
                self.output.append((self.env.now, bit_value))
            yield self.env.timeout(sample_interval)



class PulseGenerator:
    def __init__(self, env, pulse_duration=1, sampling_frequency=100, start=0):
        self.env = env
        self.pulse_duration = pulse_duration
        self.sampling_frequency = sampling_frequency
        self.start = start  # Time delay before the pulse starts
        self.state = 0  # Start with the pulse low
        self.output = []  # Output will be recorded here
        self.env.process(self.pulse_generation_process())
        self.env.process(self.sampling_process())

    def pulse_generation_process(self):
        """Process to generate a single pulse after an initial delay."""
        # Wait for the start delay
        yield self.env.timeout(self.start)
        # Set the state high to begin the pulse
        self.state = 1
        yield self.env.timeout(self.pulse_duration)
        # Set the state low after the pulse duration
        self.state = 0
        # Hold the low state indefinitely after the pulse
        yield self.env.timeout(float('inf'))  # Alternatively, could stop the process if no further activity is needed

    def sampling_process(self):
        """Process to sample the state at the sampling frequency."""
        sample_interval = 1 / self.sampling_frequency
        while True:
            self.output.append((self.env.now, self.state))
            yield self.env.timeout(sample_interval)

class FromCSV:
    def __init__(self, env, filename, column_label='data',sampling_frequency=None):
        self.env = env
        self.filename = filename
        self.column_label = column_label
        self.sampling_frequency = sampling_frequency
        self.output = []
        self.env.process(self.read_file())

    def read_file(self):
        """Read and emit data from the CSV file."""
        with open(self.filename, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)  # Read header row
            
            # Find the index of the column with the specified label
            if self.column_label in header:
                data_column_index = header.index(self.column_label)
            else:
                raise ValueError(f"Column label '{self.column_label}' not found in the file header.")
                
            # Process each row based on the identified column index
            for row in reader:
                if len(row) > data_column_index:  # Check if the row has enough columns
                    time, data = float(row[0]), float(row[data_column_index]) 
                    self.output.append((self.env.now, data))
                    # Wait until the specified time
                    if(self.sampling_frequency != None):
                        yield self.env.timeout(1.0/self.sampling_frequency)
                    else:
                        yield self.env.timeout(time - self.env.now)
                else:
                    # Handle cases where the row does not have the expected number of columns
                    print(f"Warning: Row {reader.line_num} does not have a column '{self.column_label}'. Skipping...")

class UartTx:
    def __init__(self, env, data_byte=0xAA, baud_rate=100e3, sampling_frequency=1e6):
        self.env = env
        self.data_byte = data_byte
        self.baud_rate = baud_rate
        self.sampling_frequency = sampling_frequency
        self.current_state = 1  # UART line idle state
        self.output = []  # Output waveform (time, state)
        env.process(self.transmit_process())
        env.process(self.sampling_process())

    def transmit_process(self):
        bit_time = 1 / self.baud_rate
        while True:  # Transmitting the byte repeatedly
            # Start bit
            self.current_state = 0
            yield self.env.timeout(bit_time)
            # Data bits (LSB first)
            for bit in range(8):
                self.current_state = (self.data_byte >> bit) & 1
                yield self.env.timeout(bit_time)
            # Stop bit
            self.current_state = 1
            yield self.env.timeout(bit_time*5)

    def sampling_process(self):
        sample_interval = 1 / self.sampling_frequency
        while True:
            self.output.append((self.env.now, self.current_state))
            yield self.env.timeout(sample_interval)                            
            
class Clock:
    def __init__(self, env, frequency, sampling_frequency):
        self.env = env
        self.frequency = frequency
        self.sampling_frequency = sampling_frequency
        self.state = 0
        self.output = []  # Output will be set by the Scope class
        self.env.process(self.state_changing_process())
        self.env.process(self.sampling_process())


    def state_changing_process(self):
        """Process to toggle the state at the clock frequency."""
        half_period = 1 / (2 * self.frequency)
        while True:
            self.state = 1 - self.state
            yield self.env.timeout(half_period)

    def sampling_process(self):
        """Process to sample the state at the sampling frequency."""
        sample_interval = 1 / self.sampling_frequency
        while True:
            self.output.append((self.env.now, self.state))
            yield self.env.timeout(sample_interval)

class DC:
    def __init__(self, env, amplitude, sampling_frequency):
        self.env = env
        self.sampling_frequency = sampling_frequency
        self.state = amplitude
        self.output = []  # Output will be set by the Scope class
        self.env.process(self.sampling_process())


    def sampling_process(self):
        """Process to sample the state at the sampling frequency."""
        sample_interval = 1 / self.sampling_frequency
        while True:
            self.output.append((self.env.now, self.state))
            yield self.env.timeout(sample_interval)

class Ramp:
    def __init__(self, env, slope=1, start=5, initial_output=0, sampling_frequency=1000):
        self.env = env
        self.slope = slope
        self.start_time = start
        self.initial_output = initial_output
        self.sampling_frequency = sampling_frequency
        self.output = []
        self.env.process(self.generate_ramp())

    def generate_ramp(self):
        while True:
            if self.env.now >= self.start_time:
                current_time = self.env.now - self.start_time
                current_value = self.initial_output + self.slope * current_time
                self.output.append((self.env.now, current_value))
            else:
                self.output.append((self.env.now, self.initial_output))

            yield self.env.timeout(1 / self.sampling_frequency)

class RandomNumber:
    def __init__(self, env, mean=5, variance=2, sampling_frequency=1000):
        self.env = env
        self.mean = mean
        self.variance = variance
        self.sampling_frequency = sampling_frequency
        self.output = []
        self.env.process(self.generate_random_number())

    def generate_random_number(self):
        while True:
            random_value = np.random.normal(self.mean, np.sqrt(self.variance))
            self.output.append((self.env.now, random_value))
            yield self.env.timeout(1 / self.sampling_frequency)

class SineWave:
    def __init__(self, env, amplitude=1, frequency=1, offset = 0, phase=0, sampling_frequency=1000):
        self.env = env
        self.amplitude = amplitude
        self.frequency = frequency
        self.offset = offset
        self.phase = phase
        self.sampling_frequency = sampling_frequency
        self.output = []
        self.env.process(self.generate_sine_wave())

    def generate_sine_wave(self):
        while True:
            current_time = self.env.now
            sine_value = self.offset + self.amplitude * np.sin(2 * np.pi * self.frequency * current_time + self.phase)
            self.output.append((self.env.now, sine_value))
            yield self.env.timeout(1 / self.sampling_frequency)

class SquareWave:
    def __init__(self, env, amplitude=1, frequency=1, offset=0, phase=0, sampling_frequency=1000, duty_cycle=0.5):
        self.env = env
        self.amplitude = amplitude
        self.frequency = frequency
        self.offset = offset
        self.phase = phase
        self.sampling_frequency = sampling_frequency
        self.duty_cycle = duty_cycle
        self.output = []
        self.env.process(self.generate_square_wave())

    def generate_square_wave(self):
        while True:
            current_time = self.env.now
            # Calculate the position in the wave cycle [0, 1)
            cycle_position = (self.frequency * current_time + self.phase / (2 * np.pi)) % 1
            # Adjust square wave generation to respect the duty cycle
            if cycle_position < self.duty_cycle:
                # High for the duty cycle's proportion of the period
                square_value = self.amplitude
            else:
                # Low for the rest of the period
                square_value = -self.amplitude
            # Apply offset to move the waveform up or down
            square_value += self.offset
            self.output.append((self.env.now, square_value))
            yield self.env.timeout(1 / self.sampling_frequency)

           
class Step:
    def __init__(self, env, step_time=5, initial_value=0, final_value=1, sampling_frequency=1000):
        self.env = env
        self.step_time = step_time
        self.initial_value = initial_value
        self.final_value = final_value
        self.sampling_frequency = sampling_frequency
        self.output = []
        self.env.process(self.generate_step())

    def generate_step(self):
        while True:
            if self.env.now >= self.step_time:
                self.output.append((self.env.now, self.final_value))
            else:
                self.output.append((self.env.now, self.initial_value))
            yield self.env.timeout(1 / self.sampling_frequency)

class BandLimitedWhiteNoise:
    def __init__(self, env, min_freq=1, max_freq=100, amplitude=1, sampling_frequency=1000):
        self.env = env
        self.min_freq = min_freq
        self.max_freq = max_freq
        self.amplitude = amplitude
        self.sampling_frequency = sampling_frequency
        self.output = []
        self.env.process(self.generate_noise())

    def generate_noise(self):
        while True:
            noise = self.amplitude * np.random.uniform(-1, 1)
            self.output.append((self.env.now, noise))
            yield self.env.timeout(1 / self.sampling_frequency)
