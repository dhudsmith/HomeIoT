import pyaudio # Soundcard audio I/O access library
import stt
from queue import Queue
import time

# Setup channel info
FORMAT = pyaudio.paInt16 # data type formate
CHANNELS = 1 # Adjust to your number of channels
RATE = 16000 # Sample Rate
DEV_INDEX = 0 # Device index
CHUNK = 2**14 # Block Size
RECORD_SECONDS = 15 # Record time
BUFFER_MAX_ELEMENT = 20

# Startup pyaudio instance
audio = pyaudio.PyAudio()
 
# start Recording
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                       rate=RATE,
                       input_device_index=DEV_INDEX,
                       frames_per_buffer=CHUNK,
                       input=True,
                       output=True
)  

# initialize the queue to hold audio chunks
buffer_queue = Queue(maxsize=BUFFER_MAX_ELEMENT)

# set speech transcription websocket listening on the outstream
stt_dict = stt.watson_streaming_stt(buffer_queue, content_type="audio/l16;rate=%i"%RATE)

print( "recording...")
# Record for RECORD_SECONDS
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        # read chunk
        chunk = stream.read(CHUNK)

        buffer_queue.put(chunk)

        # play it back
        #tream.write(chunk)

print("finished recording")

# Stop Audio
stream.stop_stream()
stream.close()
audio.terminate()

# Stop stt
stt_dict["audio_source"].completed_recording()
stt_dict["stream_thread"].join()
