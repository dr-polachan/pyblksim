import pandas as pd
import matplotlib.pyplot as plt

plt.close('all')

# Load the data from CSV files
clock_output = pd.read_csv('clock_output.csv')
uart_output = pd.read_csv('uart_output.csv')
ook_output = pd.read_csv('ook_modulator_output.csv')
bpf_output = pd.read_csv('band_pass_filter_output.csv')
squared_output = pd.read_csv('squared_signal_output.csv')
lpf_output = pd.read_csv('lpf_output.csv')
threshold_output = pd.read_csv('threshold_output.csv')

clock_spectrum = pd.read_csv('clock_spectrum.csv')
uart_spectrum = pd.read_csv('uart_spectrum.csv')
ook_spectrum = pd.read_csv('ook_spectrum.csv')
bpf_spectrum = pd.read_csv('bpf_spectrum.csv')
squared_spectrum = pd.read_csv('squared_signal_spectrum.csv')
lpf_spectrum = pd.read_csv('lpf_spectrum.csv')
threshold_spectrum = pd.read_csv('threshold_spectrum.csv')

# Create a figure with 2x8 subplots
fig, axs = plt.subplots(2, 7, figsize=(40, 10))  # Adjust the figure size as necessary

# Titles for plots
titles = ["Carrier Signal", "UART Signal", "OOK Signal", "BPF Output", "Squarer Output", "LPF Output", "Comparator Output"]
spectr_titles = ["Clock Spectrum", "UART Spectrum", "OOK Spectrum", "BPF Output Spectrum", "Squarer Output Spectrum", "LPF Spectrum", "Comparator Output Spectrum"]
data = [clock_output, uart_output,  ook_output, bpf_output, squared_output, lpf_output, threshold_output]
spectrum_data = [clock_spectrum, uart_spectrum,  ook_spectrum, bpf_spectrum, squared_spectrum, lpf_spectrum, threshold_spectrum]

# Filter and plot data for each scope within the specified time range
time_limit = 0.00012
for i in range(7):
    time_filtered_data = data[i][data[i]['Time'] <= time_limit]
    axs[0, i].plot(time_filtered_data['Time'], time_filtered_data['Magnitude'])
    axs[0, i].set_title(titles[i])
    axs[0, i].set_xlabel('Time (s)')
    axs[0, i].set_ylabel('Magnitude')
    axs[0, i].ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    axs[0, i].grid(True)

    # Plot spectrum data
    axs[1, i].plot(spectrum_data[i]['Frequency'], spectrum_data[i]['Magnitude'])
    axs[1, i].set_title(spectr_titles[i])
    axs[1, i].set_xlabel('Freq (Hz)')
    axs[1, i].set_ylabel('Magnitude')
    axs[1, i].grid(True)

# Adjust layout and save the figure
plt.tight_layout()
plt.subplots_adjust(hspace=0.3, wspace=0.3)
plt.savefig('full_waveforms_and_spectrums.png', dpi=300)
plt.show()
