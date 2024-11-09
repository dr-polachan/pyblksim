from pyblksim.common.sources import SquareWave, SineWave, BandLimitedWhiteNoise, Ramp
from pyblksim.common.sinks import Scope, ToCSV
from pyblksim.sims.basics import Environment

# User settings
TSIM = 5  # Simulation time in seconds
FS = 1000   # Sampling frequency in Hz

# Create simulation environment
env = Environment.init()

# Create a square wave source
square_wave = SquareWave(env, offset=0, amplitude=5, frequency=1, sampling_frequency=FS, duty_cycle=0.5)

# Create a sine wave source
sine_wave = SineWave(env, amplitude=5, frequency=1, sampling_frequency=FS)

# Create a BandLimitedWhiteNoise source
band_limited_white_noise = BandLimitedWhiteNoise(env, amplitude=5, sampling_frequency=FS)

# Create a Ramp source
ramp_signal = Ramp(env, start=0, slope=1, sampling_frequency=FS)


# Create scopes to observe the waves
square_scope = Scope(env, sampling_frequency=FS, name="Square Wave Scope")
sine_scope = Scope(env, sampling_frequency=FS, name="Sine Wave Scope")
noise_scope = Scope(env, sampling_frequency=FS, name="Noise Scope")
ramp_scope = Scope(env, sampling_frequency=FS, name="Ramp Scope")

# Create CSV sinks to save the signals
square_csv = ToCSV(env, filename="square_wave.csv", sampling_frequency=FS)
sine_csv = ToCSV(env, filename="sine_wave.csv", sampling_frequency=FS)
noise_csv = ToCSV(env, filename="noise_wave.csv", sampling_frequency=FS)
ramp_csv = ToCSV(env, filename="ramp_signal.csv", sampling_frequency=FS)

# Connect sources to scopes and CSV sinks
square_scope.input = square_wave.output
square_csv.input = square_wave.output

sine_scope.input = sine_wave.output
sine_csv.input = sine_wave.output

noise_scope.input = band_limited_white_noise.output
noise_csv.input = band_limited_white_noise.output

ramp_scope.input = ramp_signal.output
ramp_csv.input = ramp_signal.output

# Run the simulation
env.run(until=TSIM)

# Plot the results
square_scope.plot()
sine_scope.plot()
noise_scope.plot()
ramp_scope.plot()

# Save CSV files
square_csv.save()
sine_csv.save()
noise_csv.save()
ramp_csv.save()
