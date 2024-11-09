import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import numpy as np
import csv

class ToCSV:
    def __init__(self, env, sampling_frequency=1000, filename="data.csv", column_label='data'):
        self.env = env
        self.sampling_frequency = sampling_frequency
        self.filename = filename
        self.column_label = column_label
        self.input = []
        self.sampled_data = []
        self.env.process(self.sample())

    def sample(self):
        """Process to sample the input."""
        sample_interval = 1 / self.sampling_frequency
        while True:
            if self.input:
                _, state = self.input[-1]
                self.sampled_data.append((self.env.now, state))
            yield self.env.timeout(sample_interval)

    def save(self):
        """Save the sampled data to a CSV file."""
        with open(self.filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['time', self.column_label])
            writer.writerows(self.sampled_data)
       
class Scope:
    def __init__(self, env, sampling_frequency, name):
        self.env = env
        self.sampling_frequency = sampling_frequency
        self.input = []  # Initialize as an empty list
        self.sampled_output = []
        self.name = name  # Name for the figure window
        self.signal_name = " "

        self.env.process(self.sample())

    def sample(self):
        """Process to sample the assigned clock generator output at the specified frequency."""
        sample_interval = 1 / self.sampling_frequency
        index = 0
        
        while True:
            if index < len(self.input):
                self.sampled_output.append(self.input[index])
                index += int(sample_interval * self.sampling_frequency)
            yield self.env.timeout(sample_interval)

    def plot(self):
        if self.sampled_output:
            plt.figure(num=f'{self.name}')  # Set figure window title
            times, values = zip(*self.sampled_output)
            plt.plot(times, values, drawstyle='steps-post')
            plt.xlabel('Time')
            plt.ylabel('Magnitude')
            plt.title(f'{self.signal_name}')

            # Create scientific notation formatter for the x-axis
            formatter = ScalarFormatter(useMathText=True)
            formatter.set_scientific(True)
            formatter.set_powerlimits((-1,1))  # This limits when scientific notation is used
            plt.gca().xaxis.set_major_formatter(formatter)

            plt.tight_layout()
            plt.show()
        else:
            print("No data to plot.", self.name)

    def to_csv(self, filename):
        """Save the sampled data to a CSV file."""
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Time', 'Magnitude'])  # Column headers
            writer.writerows(self.sampled_output)  # Data points


class Spectrum:
    def __init__(self, env, sampling_frequency, name):
        self.env = env
        self.sampling_frequency = sampling_frequency
        self.input = []  # Initialize as an empty list
        self.fft_output = []
        self.name = name  # Name for the figure window
        self.signal_name = "Frequency Spectrum"

        self.env.process(self.sample())

    def sample(self):
        """Process to sample the input signal at the specified frequency."""
        sample_interval = 1 / self.sampling_frequency
        index = 0
        
        while True:
            if index < len(self.input):
                # Assumes input is a list of (time, value) tuples
                _, value = self.input[index]
                self.fft_output.append(value)
                index += int(sample_interval * self.sampling_frequency)
            yield self.env.timeout(sample_interval)

    def find_spectrum(self):
        """Calculates the frequency spectrum of the sampled signal."""
        # Perform FFT on the sampled signal values
        fft_vals = np.fft.fft(self.fft_output)        
        fft_vals = np.fft.fftshift(fft_vals)

        # Get the power spectrum (magnitude of the FFT values)
        power_spectrum = np.abs(fft_vals)
        return power_spectrum

    def plot(self):
        if self.fft_output:
            # Calculate the frequency spectrum
            spectrum = self.find_spectrum()
            
            # Generate frequency axis
            n = len(spectrum)
            freq = np.fft.fftfreq(n, d=1/self.sampling_frequency)
            freq = np.fft.fftshift(freq)


            plt.figure(num=f'{self.name}')
            plt.plot(freq, spectrum)
            plt.xlabel('Frequency')
            plt.ylabel('Magnitude')
            plt.title(f'{self.signal_name}')
            plt.xlim(0, self.sampling_frequency / 2)  # Only plot up to Nyquist frequency
            plt.tight_layout()
            plt.show()
        else:
            print("No data to analyze.", self.name)

    def to_csv(self, filename):
        """Save the frequency spectrum data to a CSV file."""
        spectrum = self.find_spectrum()  # Get the spectrum data
        n = len(spectrum)
        freq = np.fft.fftfreq(n, d=1/self.sampling_frequency)
        freq = np.fft.fftshift(freq)  # Adjust frequencies for plotting
        positive_mask = freq >= 0  # Mask to filter only positive frequencies
    
        # Filter out negative frequencies
        freq_positive = freq[positive_mask]
        spectrum_positive = spectrum[positive_mask]
    
        # Open a file and write the frequency and magnitude data
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Frequency', 'Magnitude'])  # Column headers
            writer.writerows(zip(freq_positive, spectrum_positive))  # Write data rows
