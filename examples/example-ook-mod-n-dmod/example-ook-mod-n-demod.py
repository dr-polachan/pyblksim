from pyblksim.common.sources import Clock, DC, UartTx
from pyblksim.common.sinks import Scope, Spectrum
from pyblksim.common.math import Squaring, GEQ, Product
from pyblksim.common.filters import LPF_FIR, BPF_FIR
from pyblksim.sims.basics import Environment

def run_analysis():
    # User settings
    TSIM = 2e-3  # Simulation time in seconds
    FS = 10e6   # Sampling frequency in Hz
    
    # Initialize the simulation environment
    env = Environment.init()
    
    # Carrier and baseband signal generation
    clock_signal = Clock(env, frequency=1e6, sampling_frequency=FS)
    uart_transmitter = UartTx(env, sampling_frequency=FS, data_byte=0xAA, baud_rate=100e3)
    
    # DC value for threshold comparator
    dc_offset = DC(env, amplitude=0.1, sampling_frequency=FS)
    
    # OOK Modulation
    ook_modulator = Product(env, sampling_frequency=FS)
    ook_modulator.input1 = clock_signal.output
    ook_modulator.input2 = uart_transmitter.output
    
    # Bandpass filtering to receive signal of interest around the carrier
    band_pass_filter = BPF_FIR(env, sampling_frequency=FS, filter_specs={'Fpass1': 0.8e6, 'Fpass2': 1.2e6, 'N': 100})
    band_pass_filter.input = ook_modulator.output
    
    # Applying non-linear filter to create signal presence in the low-frequency region
    squarer_block = Squaring(env, sampling_frequency=FS)
    squarer_block.input = band_pass_filter.output
    
    # Applying low pass filter to extract the signal in the low-frequency region
    low_pass_filter = LPF_FIR(env, sampling_frequency=FS, filter_specs={'Fpass': 200e3, 'N': 100})
    low_pass_filter.input = squarer_block.output
    
    # Threshold comparator to digitize the recovered signal
    threshold_comparator = GEQ(env, sampling_frequency=FS)
    threshold_comparator.input1 = low_pass_filter.output
    threshold_comparator.input2 = dc_offset.output
    
    # Initialize scopes and spectrums for each component
    clock_scope = Scope(env, sampling_frequency=FS, name="Clock Output")
    clock_spectrum = Spectrum(env, sampling_frequency=FS, name="Clock Spectrum")
    uart_scope = Scope(env, sampling_frequency=FS, name="UART Output")
    uart_spectrum = Spectrum(env, sampling_frequency=FS, name="UART Spectrum")
    dc_scope = Scope(env, sampling_frequency=FS, name="DC Output")
    dc_spectrum = Spectrum(env, sampling_frequency=FS, name="DC Spectrum")
    ook_scope = Scope(env, sampling_frequency=FS, name="OOK Modulator Output")
    ook_spectrum = Spectrum(env, sampling_frequency=FS, name="OOK Spectrum")
    band_pass_scope = Scope(env, FS, name="Band-Pass Filter Output")
    band_pass_spectrum = Spectrum(env, FS, name="BPF Spectrum")
    squarer_scope = Scope(env, FS, name="Squared Signal Output")
    squarer_spectrum = Spectrum(env, FS, name="Squared Signal Spectrum")
    low_pass_scope = Scope(env, FS, name="Low-Pass Filter Output")
    low_pass_spectrum = Spectrum(env, FS, name="LPF Spectrum")
    threshold_scope = Scope(env, FS, name="Threshold Output")
    threshold_spectrum = Spectrum(env, FS, name="Threshold Spectrum")
    
    # Connecting scopes and spectrums
    clock_scope.input = clock_signal.output
    clock_spectrum.input = clock_signal.output
    uart_scope.input = uart_transmitter.output
    uart_spectrum.input = uart_transmitter.output
    dc_scope.input = dc_offset.output
    dc_spectrum.input = dc_offset.output
    ook_scope.input = ook_modulator.output
    ook_spectrum.input = ook_modulator.output
    band_pass_scope.input = band_pass_filter.output
    band_pass_spectrum.input = band_pass_filter.output
    squarer_scope.input = squarer_block.output
    squarer_spectrum.input = squarer_block.output
    low_pass_scope.input = low_pass_filter.output
    low_pass_spectrum.input = low_pass_filter.output
    threshold_scope.input = threshold_comparator.output
    threshold_spectrum.input = threshold_comparator.output
    
    # Run the simulation
    env.run(until=TSIM)
    
    # Plot and save results
    clock_scope.plot()
    clock_scope.to_csv("clock_output.csv")
    clock_spectrum.plot()
    clock_spectrum.to_csv("clock_spectrum.csv")
    
    uart_scope.plot()
    uart_scope.to_csv("uart_output.csv")
    uart_spectrum.plot()
    uart_spectrum.to_csv("uart_spectrum.csv")
    
    dc_scope.plot()
    dc_scope.to_csv("dc_output.csv")
    dc_spectrum.plot()
    dc_spectrum.to_csv("dc_spectrum.csv")
    
    ook_scope.plot()
    ook_scope.to_csv("ook_modulator_output.csv")
    ook_spectrum.plot()
    ook_spectrum.to_csv("ook_spectrum.csv")
    
    band_pass_scope.plot()
    band_pass_scope.to_csv("band_pass_filter_output.csv")
    band_pass_spectrum.plot()
    band_pass_spectrum.to_csv("bpf_spectrum.csv")
    
    squarer_scope.plot()
    squarer_scope.to_csv("squared_signal_output.csv")
    squarer_spectrum.plot()
    squarer_spectrum.to_csv("squared_signal_spectrum.csv")
    
    low_pass_scope.plot()
    low_pass_scope.to_csv("lpf_output.csv")
    low_pass_spectrum.plot()
    low_pass_spectrum.to_csv("lpf_spectrum.csv")
    
    threshold_scope.plot()
    threshold_scope.to_csv("threshold_output.csv")
    threshold_spectrum.plot()
    threshold_spectrum.to_csv("threshold_spectrum.csv")
    
if __name__ == "__main__":
    run_analysis()