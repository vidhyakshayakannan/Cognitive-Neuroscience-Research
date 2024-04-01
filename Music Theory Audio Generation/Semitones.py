import numpy as np
import matplotlib.pyplot as plt
import pyaudio

# Constants
base_freq = 440  # Base frequency (Hz)
num_octaves = 4  # Number of octaves
semitones_per_octave = 12  # Number of semitones per octave
duration = 1.0  # Duration of the audio (seconds)
fs = 44100  # Sampling rate (samples per second)

# Generate time values
t = np.linspace(0, duration, int(fs * duration), endpoint=False)

# Initialize the PyAudio object
p = pyaudio.PyAudio()

# Function to play audio
def play_audio(audio_data):
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=fs, output=True)
    stream.write(audio_data.astype(np.float32).tobytes())
    stream.stop_stream()
    stream.close()

# Calculate the frequencies for each semitone
semitone_ratio = 2 ** (1 / 12)  # Ratio between semitones
for octave in range(num_octaves):
    for semitone in range(semitones_per_octave):
        semitone_index = octave * semitones_per_octave + semitone
        semitone_freq = base_freq * (semitone_ratio ** semitone_index)
        semitone_waveform = np.sin(2 * np.pi * semitone_freq * t)
        play_audio(semitone_waveform)
        plt.plot(t[:300], semitone_waveform[:300])
        plt.title(f'Octave {octave + 1}, Semitone {semitone + 1} (Frequency: {semitone_freq:.2f} Hz)')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.show()

# Terminate PyAudio
p.terminate()
