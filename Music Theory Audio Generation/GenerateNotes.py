import numpy as np
import matplotlib.pyplot as plt
import pyaudio
import time

# Constants
base_frequency = 440  # Base frequency (Hz)
duration = 1.0  # Duration of the audio (seconds)
fs = 44100  # Sampling rate (samples per second)
attack_time = 0.05  # Attack time (seconds)
delay_time = 0.05  # Delay time (seconds)

# Function to map Carnatic notes to frequencies based on a chosen base frequency and octave
def carnatic_notes_to_frequencies(base_frequency, num_octaves=1):
    ratios = {
        'S': 1,
        'R': 9/8,
        'G': 5/4,
        'M': 4/3,
        'P': 3/2,
        'D': 5/3,
        'N': 15/8
    }
    # Initialize a dictionary to store frequencies for each note
    note_frequencies = {}
    for note, ratio in ratios.items():
        # Generate frequencies for each note in the specified number of octaves
        note_frequencies[note] = [base_frequency * (ratio ** i) for i in range(num_octaves)]
    return note_frequencies

# Function to parse Carnatic note with octave notation
def parse_carnatic_note_with_octave(note_with_octave):
    note = note_with_octave[:-1]  # Extract the note name
    octave = int(note_with_octave[-1])  # Extract the octave number
    return note, octave

# Function to play audio with attack and delay
def play_audio_with_attack_delay(audio_data):
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=fs, output=True)
    
    # Add attack time
    attack_samples = int(attack_time * fs)
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
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    waveform = np.sin(2 * np.pi * frequency * t)
    return waveform

# Function to play notes from a list of frequencies
def play_notes(notes):
    for freq in notes:
        waveform = generate_waveform(freq)
        play_audio_with_attack_delay(waveform)

# Get the base frequency (e.g., A4)
base_frequency = 440

# Initialize the PyAudio object
p = pyaudio.PyAudio()

# Calculate Carnatic note frequencies based on the base frequency and number of octaves
num_octaves = 2  # Number of octaves
carnatic_frequencies = carnatic_notes_to_frequencies(base_frequency, num_octaves)

# User input for Carnatic notes with octave information
user_input = input("Enter Carnatic notes with octave (e.g., S1, R2, etc.): ").upper().split()

# Convert user input to list of frequencies
user_notes = []
for note_with_octave in user_input:
    note, octave = parse_carnatic_note_with_octave(note_with_octave)
    if note in carnatic_frequencies and 1 <= octave <= num_octaves:
        freq = carnatic_frequencies[note][octave - 1]  # Octave is 1-indexed
        user_notes.append(freq)

# Play the notes
play_notes(user_notes)
