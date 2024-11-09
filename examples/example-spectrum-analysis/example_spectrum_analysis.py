from pyblksim.common.sources import PulseGenerator, SquareWave
from pyblksim.common.sinks import Scope, Spectrum
from pyblksim.sims.basics import Environment

# User settings
TSIM = 5  # Simulation time in seconds
FS = 1000   # Sampling frequency in Hz

# Create simulation environment
env = Environment.init()

# Create sources
pulse_wave = PulseGenerator(env, pulse_duration=0.01, sampling_frequency=FS, start=2.5)
square_wave = SquareWave(env, amplitude=1, frequency=50, sampling_frequency=FS, duty_cycle=0.5)

# Create scopes for visual observation
pulse_scope = Scope(env, sampling_frequency=FS, name="Pulse Wave Scope")
square_scope = Scope(env, sampling_frequency=FS, name="Square Wave Scope")

# Create spectrums for frequency analysis
pulse_spectrum = Spectrum(env, sampling_frequency=FS, name="Pulse Wave Spectrum")
square_spectrum = Spectrum(env, sampling_frequency=FS, name="Square Wave Spectrum")

# Connect sources to scopes, spectrums, and CSV sinks
pulse_scope.input = pulse_wave.output
pulse_spectrum.input = pulse_wave.output

square_scope.input = square_wave.output
square_spectrum.input = square_wave.output

# Run the simulation
env.run(until=TSIM)

# Plot the results from scopes
pulse_scope.plot()
square_scope.plot()

# Save the data from scopes
pulse_scope.to_csv("pulse_wave_scope.csv")
square_scope.to_csv("square_wave_scope.csv")

# Plot the results from spectrums
pulse_spectrum.plot()
square_spectrum.plot()

# Save the data from scopes
pulse_spectrum.to_csv("pulse_wave_spectrum.csv")
square_spectrum.to_csv("square_wave_spectrum.csv")
