# Python program to translate
# speech to text
# Sound files such as end.wav and start.wav are from windows system sounds

import speech_recognition as sr
import playsound as ps
import time
import asyncio
import websockets
import threading
from _thread import start_new_thread
import json
import signal
import sys

# Sends string to websocket
async def send(command):
    uri = "ws://127.0.0.1:2585/v1/messages"
    async with websockets.connect(uri) as websocket:
        await websocket.send(command)

# Initialize the recognizer
r = sr.Recognizer()

# This function uses the microphone to turn speech to text


def SpeechToText():
    # use the microphone as source for input.
    with sr.Microphone() as source2:

        # wait for a second to let the recognizer
        # adjust the energy threshold based on
        # the surrounding noise level
        r.adjust_for_ambient_noise(source2, duration=0.2)

        # listens for the user's input
        audio = r.listen(source2)
        # Using google to recognize audio
        text = r.recognize_google(audio)
        # converts all text to lower case
        text = text.lower()
        return text

# This funtion uses a .wav file to turn speech to text


def FileToText(file):
    # use the microphone as source for input.
    with sr.AudioFile(file) as source2:

        # wait for a second to let the recognizer
        # adjust the energy threshold based on
        # the surrounding noise level
        r.adjust_for_ambient_noise(source2, duration=0.2)

        # listens for the user's input
        audio = r.record(source2)
        # Using google to recognize audio
        text = r.recognize_google(audio)
        # converts all text to lower case
        text = text.lower()
        return text

# Plays starting sound
def playStartSound():
    ps.playsound('start.wav')

# Plays end sound
def playEndSound():
    ps.playsound('end.wav')


# Initializing program
# Registering recognizer with dispatcher
register = {
    "action": "REGISTER_LISTENER",
    "app": "recognizer",
    "eavesdrop": False,
}

deregister = {
    "action": "DEREGISTER_LISTENER",
    "app": "recognizer"
}

def sigint_handler(sig, frame):
    print('Exiting gracefully...')
    asyncio.get_event_loop().run_until_complete(send(json.dumps(deregister)))
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

asyncio.get_event_loop().run_until_complete(send(json.dumps(register)))

# Loop infinitely for user to
# speak

while(1):

    # Exception handling to handle
    # exceptions at the runtime
    try:

        text = ''

        print('Say \"blue\" to input command from microphone, say "file" to input from file')

        text = SpeechToText()

        print("-> "+text)

        # uses mic after activation phrase
        if text == 'blue':
            print('activation phrase')
            playStartSoundThread = threading.Thread(target=playStartSound)
            playStartSoundThread.start()

            command = SpeechToText()
            print('Sphnix heard: ' + command)
            playEndSoundThread = threading.Thread(target=playEndSound)
            playEndSoundThread.start()
            command = json.dumps({
                "action": "DISPATCH_COMMAND",
                "command": command,
            })
            asyncio.get_event_loop().run_until_complete(send(command))
        # uses file to send command
        elif text == 'file':
            # askes user for file name input
            name = input('Input file name: ')
            command = FileToText(name)
            asyncio.get_event_loop().run_until_complete(send(command))

        # exit condition
        if text == 'exit':
            deregister = {
                "action": "DEREGISTER_LISTENER",
                "app": "recognizer",
            }
            asyncio.get_event_loop().run_until_complete(send(json.dumps(deregister)))
            time.sleep(0.5)
            exit()

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    except sr.UnknownValueError:
        print("unknown error occured")
