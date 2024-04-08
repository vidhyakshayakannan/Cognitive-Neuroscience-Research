import numpy as np
import matplotlib.pyplot as plt
import pyaudio
import time

# Constants
base_freq = 440  # Base frequency (Hz)
num_octaves = 4  # Number of octaves
semitones_per_octave = 12  # Number of semitones per octave
duration = 0.3  # Duration of the audio (seconds)
fs = 44100  # Sampling rate (samples per second)

# Function to map Carnatic notes to frequencies based on a chosen base frequency and octave
def carnatic_notes_to_frequencies(base_frequency, num_octaves=1):
    ratios = {
        'S': 16/15,
        'R': 9/8,
        'G': 5/4,
        'M': 4/3,
        'P': 3/2,
        'D': 5/3,
        'N': 15/16
    }
    note_frequencies = {}
    for note, ratio in ratios.items():
        note_frequencies[note] = [base_frequency * (ratio ** (octave + 1)) for octave in range(num_octaves)]
    return note_frequencies

# Generate time values
t = np.linspace(0, duration, int(fs * duration), endpoint=False)

# Initialize the PyAudio object
p = pyaudio.PyAudio()


# Function to play audio with attack and delay
def play_audio(audio_data, attack_time=0.05, delay_time=0.05):
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=fs, output=True)
    
    # Ensure attack time doesn't exceed duration
    attack_samples = min(int(attack_time * fs), len(audio_data))
    
    # Add attack time
    attack_data = np.linspace(0, 1, attack_samples)
    audio_data_with_attack = np.concatenate((audio_data[:attack_samples] * attack_data, audio_data[attack_samples:]))
    
    # Write audio data to stream
    stream.write(audio_data_with_attack.astype(np.float32).tobytes())
    
    # Add delay time
    time.sleep(delay_time)
    
    stream.stop_stream()
    stream.close()

# Function to generate waveform for a given frequency
def generate_waveform(frequency):
    waveform = np.sin(2 * np.pi * frequency * t)
    return waveform

# Function to parse user input and return the corresponding frequencies
def parse_user_input(user_input):
    frequencies = []
    for note_octave in user_input:
        note, octave = note_octave[:-1], int(note_octave[-1])
        if note in carnatic_frequencies and 1 <= octave <= num_octaves:
            freq = carnatic_frequencies[note][octave - 1]  # Octave is 1-indexed
            frequencies.append(freq)
    return frequencies

# Calculate Carnatic note frequencies based on the base frequency and number of octaves
carnatic_frequencies = carnatic_notes_to_frequencies(base_freq, num_octaves)

# User input for Carnatic notes
user_input = input("Enter Carnatic notes with octave (e.g., S1, R2, etc.): ").upper().split()

# Parse user input and get frequencies
user_notes = parse_user_input(user_input)

# Play the notes
for freq in user_notes:
    waveform = generate_waveform(freq)
    play_audio(waveform)

# Terminate PyAudio
p.terminate()
