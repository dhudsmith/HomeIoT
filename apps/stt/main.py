import pyaudio # Soundcard audio I/O access library
import stt
import wave # Python 3 module for reading / writing simple .wav files

# Setup channel info
FORMAT = pyaudio.paInt16 # data type formate
CHANNELS = 1 # Adjust to your number of channels
RATE = 16000 # Sample Rate
DEV_INDEX = 0 # Device index
CHUNK = 1024 # Block Size
RECORD_SECONDS = 5 # Record time
WAVE_OUTPUT_FILENAME = "file.wav"

# Startup pyaudio instance
audio = pyaudio.PyAudio()

# start Recording
in_stream = audio.open(format=FORMAT,
                       channels=CHANNELS,
                       rate=RATE,
                       input_device_index=DEV_INDEX,
                       frames_per_buffer=CHUNK,
                       input=True)

out_stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input_device_index=DEV_INDEX,
                        frames_per_buffer=CHUNK,
                        output=True)

# set speech transcription websocket listening on the outstream
#stt.recognize(content_type="audio/l16;rate=%i"%RATE, audio_stream=out_stream)

print( "recording...")
frames = []

# Record for RECORD_SECONDS
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        # read chunk
        data = in_stream.read(CHUNK)

        # write chunk
        out_stream.write(data)

        # do additional work with data
        frames.append(data)

print("finished recording")

# Stop Recording
in_stream.stop_stream()
in_stream.close()
out_stream.stop_stream()
out_stream.close()
audio.terminate()

# Write your new .wav file with built in Python 3 Wave module
waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()
