
import pandas as pd
import matplotlib.pyplot as plt

plt.close('all')

# Load the data from CSV files
noise_wave = pd.read_csv('./noise_wave.csv')
ramp_signal = pd.read_csv('./ramp_signal.csv')
sine_wave = pd.read_csv('./sine_wave.csv')
square_wave = pd.read_csv('./square_wave.csv')

# Create a figure with 2x2 subplots for each waveform
fig, axs = plt.subplots(2, 2, figsize=(5, 5))

# Noise waveform
axs[0, 0].plot(noise_wave['time'], noise_wave['data'], color='grey')
axs[0, 0].set_title('Noise Wave')
axs[0, 0].set_xlabel('Time (s)')
axs[0, 0].set_ylabel('Amplitude (V)')
axs[0, 0].grid(True)

# Ramp waveform
axs[0, 1].plot(ramp_signal['time'], ramp_signal['data'], color='red')
axs[0, 1].set_title('Ramp Signal')
axs[0, 1].set_xlabel('Time (s)')
axs[0, 1].set_ylabel('Amplitude (V)')
axs[0, 1].grid(True)

# Sine waveform
axs[1, 0].plot(sine_wave['time'], sine_wave['data'], color='blue')
axs[1, 0].set_title('Sine Wave')
axs[1, 0].set_xlabel('Time (s)')
axs[1, 0].set_ylabel('Amplitude (V)')
axs[1, 0].grid(True)

# Square waveform
axs[1, 1].plot(square_wave['time'], square_wave['data'], color='green')
axs[1, 1].set_title('Square Wave')
axs[1, 1].set_xlabel('Time (s)')
axs[1, 1].set_ylabel('Amplitude (V)')
axs[1, 1].grid(True)

# Adjust layout and save the figure
plt.tight_layout()
plt.subplots_adjust(hspace=0.3, wspace=0.3)
plt.savefig('./fig_basic_waveforms.png', dpi=300)
plt.show()
