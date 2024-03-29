import numpy as np
import matplotlib.pyplot as plt
import pyaudio

# Constants
base_freq = 440  # Base frequency (Hz)
num_harmonics = 10  # Number of harmonics
duration = 1.0  # Duration of the audio (seconds)
fs = 44100  # Sampling rate (samples per second)

# Generate time values
t = np.linspace(0, duration, int(fs * duration), endpoint=False)

# numpy.linspace returns fs*duration evenly spaced values

# Initialize the waveform as zeros
waveform = np.zeros_like(t)

''' Initializes a NumPy array waveform with the same shape 
and data type as the array t, but filled with zeros. 
Waveform will be used to store the values of the audio waveform 
generated by combining the individual harmonic sine waves. '''

# Initialize the PyAudio object
p = pyaudio.PyAudio()

# Function to play audio
def play_audio(audio_data):
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=fs, output=True)
    # Channels: number of independent audio signals or paths that can be used to convey audio data
    stream.write(audio_data.astype(np.float32).tobytes())
    stream.stop_stream()
    stream.close()

# Calculate and play each individual harmonic
for i in range(num_harmonics):
    harmonic_freq = base_freq * (i + 1)
    harmonic_waveform = np.sin(2 * np.pi * harmonic_freq * t)
    play_audio(harmonic_waveform)
    plt.plot(t[:300], harmonic_waveform[:300])
    plt.title(f'Harmonic {i+1} (Frequency: {harmonic_freq} Hz)')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.show()

# Constants
base_freq = 440  # Base frequency (Hz)
num_harmonics = 10  # Number of harmonics
duration = 1.0  # Duration of the audio (seconds)
fs = 44100  # Sampling rate (samples per second)

# Generate time values
t = np.linspace(0, duration, int(fs * duration), endpoint=False)

# Initialize the waveform as zeros
waveform = np.zeros_like(t)

# Calculate the harmonic sequence ratios
harmonic_ratios = np.array([1 / (i + 1) for i in range(num_harmonics)])

# Generate sine waves for each harmonic and sum them
for i, ratio in enumerate(harmonic_ratios):
    harmonic_freq = base_freq * (i + 1)
    waveform += np.sin(2 * np.pi * harmonic_freq * t) * ratio

# Normalize the waveform to [-1, 1]
waveform /= np.max(np.abs(waveform))

# Plot the first 300 samples of the waveform
plt.figure(figsize=(10, 4))
plt.plot(t[:300], waveform[:300])
plt.title('Waveform')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.show()

# Play the audio
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=fs, output=True)
stream.write(waveform.astype(np.float32).tobytes())
stream.stop_stream()
stream.close()
p.terminate()


# Terminate PyAudio
p.terminate()

