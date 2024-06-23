import pyaudio
import numpy as np

fs = 22050
x = np.linspace(0, 3, 22050 * 3)
b = np.sin(2 * np.pi * 440 * x) * 10000
b = np.array(b).astype(np.int16).tobytes()

p = pyaudio.PyAudio()
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNEL = 1
RATE = fs
stream = p.open(
    format=FORMAT,
    channels=CHANNEL,
    rate=RATE,
    output=True,
)

stream.write(b)

stream.stop_stream()
stream.close()
p.terminate()
