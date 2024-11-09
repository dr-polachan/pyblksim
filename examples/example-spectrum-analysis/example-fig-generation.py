import pandas as pd
import matplotlib.pyplot as plt

plt.close('all')

# Load the data from CSV files
pulse_wave = pd.read_csv('pulse_wave_scope.csv')
square_wave = pd.read_csv('square_wave_scope.csv')

pulse_spectrum = pd.read_csv('pulse_wave_spectrum.csv')
square_spectrum = pd.read_csv('square_wave_spectrum.csv')

# Create a figure with 2x2 subplots
fig, axs = plt.subplots(2, 2, figsize=(15, 10))

# First row: Time-domain signals
axs[0, 0].plot(pulse_wave['Time'], pulse_wave['Magnitude'], color='purple')
axs[0, 0].set_title('Pulse Wave')
axs[0, 0].set_xlabel('Time (s)')
axs[0, 0].set_ylabel('Amplitude (V)')
axs[0, 0].grid(True)

axs[0, 1].plot(square_wave['Time'], square_wave['Magnitude'], color='green')
axs[0, 1].set_title('Square Wave')
axs[0, 1].set_xlabel('Time (s)')
axs[0, 1].set_ylabel('Amplitude (V)')
axs[0, 1].grid(True)

# Second row: Frequency-domain signals (Spectrums)
axs[1, 0].plot(pulse_spectrum['Frequency'], pulse_spectrum['Magnitude'], color='purple')
axs[1, 0].set_title('Pulse Spectrum')
axs[1, 0].set_xlabel('Frequency (Hz)')
axs[1, 0].set_ylabel('Magnitude')
axs[1, 0].grid(True)

axs[1, 1].plot(square_spectrum['Frequency'], square_spectrum['Magnitude'], color='green')
axs[1, 1].set_title('Square Spectrum')
axs[1, 1].set_xlabel('Frequency (Hz)')
axs[1, 1].set_ylabel('Magnitude')
axs[1, 1].grid(True)

# Adjust layout and save the figure
plt.tight_layout()
plt.subplots_adjust(hspace=0.3, wspace=0.3)
plt.savefig('fig_waveforms_and_spectrums.png', dpi=300)
plt.show()
