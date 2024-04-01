# Generate and play a sine wave audio signal

import time  # Import time module to measure the duration of sound playback
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pyaudio

p = pyaudio.PyAudio()

volume = 1  # range [0.0, 1.0]
fs = 1000  #  sampling rate of the audio signal in Hz
duration = 2  # in seconds, may be float
f = 400.0  # sine frequency, Hz, may be float

samples = (np.sin(2 * np.pi * np.arange(fs * duration) * f / fs)).astype(np.float32)

''' Generates a sine wave signal using NumPy. 
Creates an array of samples by computing the sine function at equally spaced time intervals over the duration specified. 
'''

output_bytes = (volume * samples).tobytes()

stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)


# play
start_time = time.time()
stream.write(output_bytes)
print("Played sound for {:.2f} seconds".format(time.time() - start_time))

stream.stop_stream()
stream.close()
p.terminate()
t = np.linspace(0, duration, 150, endpoint=False)

# generate samples
samples = np.sin(2 * np.pi * f * t)

# plot the sine wave
plt.figure(figsize=(10, 4))
plt.plot(t, samples)
plt.title('Sine Wave')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.show()