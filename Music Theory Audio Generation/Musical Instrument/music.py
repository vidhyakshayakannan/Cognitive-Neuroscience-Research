import streamlit as st
import numpy as np
import pygame.mixer
from scipy.io.wavfile import write

def get_song_data(music_notes, durations):
    note_freqs = get_piano_notes()
    
    # Split notes and durations into lists
    notes_list = music_notes.split('-')
    durations_list = durations.split('-')
    
    # Pad the shorter list with empty strings
    max_len = max(len(notes_list), len(durations_list))
    notes_list += [''] * (max_len - len(notes_list))
    durations_list += [''] * (max_len - len(durations_list))
    
    # Generate the song data based on the user input
    song = [get_wave(note_freqs[note], duration) for note, duration in zip(notes_list, durations_list)]
    song = np.concatenate(song)

    return song.astype(np.int16)


def get_piano_notes():
    note_freqs = {}
    base_freq = 100.63

    for octave in range(8):  
        for note in ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']:
            note_name = f"{note}{octave}"
            note_freqs[note_name] = base_freq * pow(2, ((octave * 12 + ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'].index(note)) / 12))
    return note_freqs

def get_wave(freq, duration):
    sample_rate = 44100
    amplitude = 4096
    t = np.linspace(0, float(duration), int(sample_rate * float(duration)))
    wave = amplitude * np.sin(2 * np.pi * freq * t)

    return wave

def play_music(music_notes, durations):
    # Generate the song data based on the user input
    data = get_song_data(music_notes, durations)
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

def main():
    st.title("🎹 Music Composer")

    music_notes = st.text_input("Enter the notes separated by dashes (e.g., C4-G4-A5):")
    durations = st.text_input("Enter the durations separated by dashes (e.g., 0.5-0.5-1):")

    if st.button("Play"):
        if music_notes and durations:
            play_music(music_notes, durations)
        else:
            st.warning("Please enter both notes and durations.")

if __name__ == "__main__":
    main()
