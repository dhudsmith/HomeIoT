import json
from os.path import join, dirname
from threading import Thread
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# load credentials and authenticate
with open('../../creds/stt.json', 'r') as file:
    creds = json.load(file)

authenticator = IAMAuthenticator(creds["apikey"])
speech_to_text = SpeechToTextV1(
    authenticator=authenticator
)

speech_to_text.set_service_url(creds["url"])

class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)

    def on_data(self, data):
        print(json.dumps(data, indent=2))

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))

# speech recognition function
def watson_streaming_stt(buffer_queue, content_type):

    audio_source = AudioSource(buffer_queue, True, True)
    callback = MyRecognizeCallback()
    stt_stream_thread = Thread(
        target=speech_to_text.recognize_using_websocket,
        kwargs=dict(
            audio=audio_source,
            content_type= content_type,
            recognize_callback=callback,
            model='en-US_BroadbandModel',
            interim_results=False,
            max_alternatives=1)
    )
    stt_stream_thread.start()

    # return everything needed by main script
    return {'audio_source': audio_source,
            'stream_thread': stt_stream_thread}
