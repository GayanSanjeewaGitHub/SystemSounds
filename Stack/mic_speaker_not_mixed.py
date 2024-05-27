import pyaudio
import wave
import numpy as np

CHUNK = 1024
FORMAT = pyaudio.paInt16
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "tmp.wav"

p = pyaudio.PyAudio()

for i in range(0, p.get_device_count()):
    print(i, p.get_device_info_by_index(i)['name'])

# Stream using as_loopback to get sound from OS
stream = p.open(
    format=FORMAT,
    channels=1,  # change to 2 channels for stereo input
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK,
    input_device_index=2
)

# Stream using my Microphone's input device
stream2 = p.open(
    format=FORMAT,
    channels=1,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK,
    input_device_index=2
)

frames = []
frames2 = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    data2 = stream2.read(CHUNK)
    frames.append(data)
    frames2.append(data2)

# Convert frames to bytes
frames = b''.join(frames)
frames2 = b''.join(frames2)

# Decode the speaker data
Sdecoded = np.frombuffer(frames, 'int16')

# Decode the microphone data
Mdecoded = np.frombuffer(frames2, 'int16')

# Convert speaker data into a Numpy array
Sdecoded = np.array(Sdecoded, dtype='int16')

# Split the channels
direito = Sdecoded[1::2]  # Right channel
esquerdo = Sdecoded[::2]  # Left channel

# Ensure all arrays are the same length
min_len = min(len(direito), len(esquerdo), len(Mdecoded))
direito = direito[:min_len]
esquerdo = esquerdo[:min_len]
Mdecoded = Mdecoded[:min_len]

# Mix everything to mono by adding right side, left side, and microphone decoded data
mix = direito + esquerdo + Mdecoded

# Ensure no value goes beyond the limits of short int
signal = np.clip(mix, -32767, 32766)

# Encode the data again
encoded = wave.struct.pack("%dh" % len(signal), *list(signal))

# Stop all streams and terminate pyaudio
stream.stop_stream()
stream.close()
stream2.stop_stream()
stream2.close()
p.terminate()

# Record mixed audio in mono
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(1)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(encoded)
wf.close()
