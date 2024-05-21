import numpy as np
from scipy.io import wavfile

def generate_tone(frequency, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    tone = np.sin(2 * np.pi * frequency * t)
    return tone

def combine_beats_with_tones(beat_file, tone_frequency, tone_duration, num_times, output_file):
    # Load the beat sound
    sample_rate, beat_data = wavfile.read(beat_file)
    
    # Initialize the combined audio
    combined_audio = np.array([], dtype=np.int16)
    
    # Position to introduce the tone
    position_to_introduce_tone = np.random.randint(1, num_times)
    
    # Concatenate beat sound with tone
    for i in range(num_times):
        # Add the beat sound
        combined_audio = np.concatenate((combined_audio, beat_data))
        
        # Introduce a random tone if at the desired position
        if i == position_to_introduce_tone:
            tone = generate_tone(tone_frequency, tone_duration, sample_rate)
            combined_audio = np.concatenate((combined_audio, tone))
    
    # Write the combined audio to a WAV file
    wavfile.write(output_file, sample_rate, combined_audio)

# Example usage
beat_file = 'kick-classic.wav'
tone_frequency = 1000  # Frequency of the tone to introduce (in Hz)
tone_duration = 1  # Duration of the tone (in seconds)
num_times = 5  # Number of times to play the beat sound
output_file = 'combined_audio.wav'

combine_beats_with_tones(beat_file, tone_frequency, tone_duration, num_times, output_file)
