from scipy.signal import iirfilter, lfilter, lfilter_zi
import numpy as np


from scipy.signal import firwin

class LPF_FIR:
    def __init__(self, env, sampling_frequency, filter_specs):
        self.env = env
        self.sampling_frequency = sampling_frequency
        self.filter_specs = filter_specs
        self.input = []
        self.output = []
        # Design an FIR filter instead of IIR
        self.filter_coefficients, self.zi = self.design_lowpass_filter()
        
        self.env.process(self.sample())

    def design_lowpass_filter(self):
        order = self.filter_specs.get('N', 20)  # Default filter order (number of taps) is 20 if not specified
        numtaps = order+1
        
        filt_window = self.filter_specs.get('Window', 'hamming')  # Default filter order (number of taps) is 20 if not specified

        Fpass = self.filter_specs['Fpass']  # Passband cutoff frequency
        # Normalize the cutoff frequency with respect to the Nyquist frequency
        Wn = Fpass / (0.5 * self.sampling_frequency)
        b = firwin(numtaps, Wn, window=filt_window)  # Design FIR filter with Hamming window
        a = [1.0]  # FIR filters have an all-zero polynomial 'a' equal to 1.0
        zi = lfilter_zi(b, a) * 0  # Initial conditions for the FIR filter are typically set to zero
        return (b, a), zi

    def apply_filter(self, sample):
        # Process a single sample through the filter, updating zi
        y, zf = lfilter(self.filter_coefficients[0], self.filter_coefficients[1], [sample], zi=self.zi)
        self.zi = zf  # Update filter state
        return y[0]  # Return the filtered sample
    
    def sample(self):
        sample_interval = 1 / self.sampling_frequency
        while True:
            if not self.input:
                yield self.env.timeout(sample_interval)  # Wait for next sample if input is empty
                continue
            _, state = self.input[-1]
            filtered_sample = self.apply_filter(state)
            self.output.append((self.env.now, filtered_sample))
            yield self.env.timeout(sample_interval)



class BPF_FIR:
    def __init__(self, env, sampling_frequency, filter_specs):
        self.env = env
        self.sampling_frequency = sampling_frequency
        self.filter_specs = filter_specs
        self.input = []
        self.output = []
        # Design an FIR band-pass filter
        self.filter_coefficients, self.zi = self.design_bandpass_filter()
        
        self.env.process(self.sample())

    def design_bandpass_filter(self):
        order = self.filter_specs.get('N', 20)  # Default filter order (number of taps) is 20 if not specified
        filt_window = self.filter_specs.get('Window', 'hamming')  # Default filter order (number of taps) is 20 if not specified

        numtaps = order+1
        Fpass1 = self.filter_specs['Fpass1']  # Lower cutoff frequency of the passband
        Fpass2 = self.filter_specs['Fpass2']  # Upper cutoff frequency of the passband
        # Normalize the cutoff frequencies with respect to the Nyquist frequency
        Wn = [Fpass1 / (0.5 * self.sampling_frequency), Fpass2 / (0.5 * self.sampling_frequency)]
        b = firwin(numtaps, Wn, pass_zero=False, window=filt_window)  # Design FIR band-pass filter
        a = [1.0]  # FIR filters have an all-zero polynomial 'a' equal to 1.0
        zi = lfilter_zi(b, a) * 0  # Initial conditions for the FIR filter are typically set to zero
        return (b, a), zi

    def apply_filter(self, sample):
        # Process a single sample through the filter, updating zi
        y, zf = lfilter(self.filter_coefficients[0], self.filter_coefficients[1], [sample], zi=self.zi)
        self.zi = zf  # Update filter state
        return y[0]  # Return the filtered sample
    
    def sample(self):
        sample_interval = 1 / self.sampling_frequency
        while True:
            if not self.input:
                yield self.env.timeout(sample_interval)  # Wait for next sample if input is empty
                continue
            _, state = self.input[-1]
            filtered_sample = self.apply_filter(state)
            self.output.append((self.env.now, filtered_sample))
            yield self.env.timeout(sample_interval)

