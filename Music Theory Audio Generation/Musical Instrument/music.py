import numpy as np
import pygame.mixer
import scipy.io.wavfile as wav
from scipy.io.wavfile import write

def interpolate_linearly(wave_table, index):
    truncated_index = int(np.floor(index))
    next_index = (truncated_index + 1) % wave_table.shape[0]

    next_index_weight = index - truncated_index
    truncated_index_weight = 1 - next_index_weight

    return truncated_index_weight * wave_table[truncated_index] + next_index_weight * wave_table[next_index]

def sawtooth(x):
    return (x + np.pi) / np.pi % 2 - 1

def get_wave(freq, duration=2):
    sample_rate = 44100
    amplitude = 4096
    t = np.linspace(0, duration, int(sample_rate * duration))
    wave = amplitude * np.sin(2 * np.pi * freq * t)

    return wave

def get_piano_notes():
    octave = ['C', 'c', 'D', 'd', 'E', 'F', 'f', 'G', 'g', 'A', 'a', 'B']
    base_freq = 261.63

    note_freqs = {octave[i]:base_freq*pow(2, (i/12)) for i in range(len(octave))}
    note_freqs[''] = 0.0

    return note_freqs

def get_song_data(music_notes):
    note_freqs = get_piano_notes()
    song = [get_wave(note_freqs[note], duration=0.5) for note in music_notes.split('-')]
    song = np.concatenate(song)

    return song.astype(np.int16)

def get_chord_data(chords):
    chords = chords.split('-')
    note_freqs = get_piano_notes()

    chord_data = []
    for chord in chords:
        data = sum([get_wave(note_freqs[note], duration=0.5) for note in list(chord)])
        chord_data.append(data)

    chord_data = np.concatenate(chord_data, axis=0)

    return chord_data.astype(np.int16)

if __name__ == '__main__':
    # Get user input for the notes
    music_notes = input("Enter the notes separated by dashes (e.g., C-G-A): ")

    # Generate the song data based on the user input
    data = get_song_data(music_notes)
    data = data * (16300 / np.max(data))

    # Write the generated song data to a WAV file
    write('user_song.wav', 44100, data.astype(np.int16))

    # Load and play the generated WAV file
    pygame.mixer.init()
    pygame.mixer.music.load('user_song.wav')
    pygame.mixer.music.play()

    # Wait until the music finishes playing
    while pygame.mixer.music.get_busy():
        continue
