import time
import matplotlib.pyplot as plt
import numpy as np
import pyaudio
import wave

p = pyaudio.PyAudio()

volume = 1  # range [0.0, 1.0]
fs = 44000  # sampling rate of the audio signal in Hz
duration = 5  # in seconds, may be float
f = 500.0  # sine frequency, Hz, may be float

samples = (np.sin(2 * np.pi * np.arange(fs * duration) * f / fs)).astype(np.float32)

output_bytes = (volume * samples).tobytes()

stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)

# Play audio
start_time = time.time()
stream.write(output_bytes)
print("Played sound for {:.2f} seconds".format(time.time() - start_time))

stream.stop_stream()
stream.close()
p.terminate()

# Save as WAV file
wav_file = wave.open("sine_wave.wav", 'wb')
wav_file.setnchannels(1)
wav_file.setsampwidth(pyaudio.get_sample_size(pyaudio.paFloat32))
wav_file.setframerate(fs)
wav_file.writeframes(output_bytes)
wav_file.close()

# Plot the sine wave
t = np.linspace(0, duration, len(samples), endpoint=False)
plt.figure()
plt.plot(t, samples)
plt.title('Sine Wave')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.show()
