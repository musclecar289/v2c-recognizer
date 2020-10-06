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
import sys
import tkinter as tk
from websocket import create_connection

# Initialize the recognizer
r = sr.Recognizer()

exitFlag = False
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

# Plays ending sound


def playEndSound():
    ps.playsound('end.wav')


# GUI Functions for tk

'''
async def main():
    uri = "ws://127.0.0.1:2585/v1/messages"

    # starts the websocket
    async with websockets.connect(uri) as websocket:
        register = {
            "action": "REGISTER_LISTENER",
            "app": "recognizer",
            "eavesdrop": False,
        }

        deregister = {
            "action": "DEREGISTER_LISTENER",
            "app": "recognizer"
        }

        # Widget
        widget = tk.Tk()
        widget.geometry("400x240")
        widget.lift()
        widget.call('wm', 'attributes', '.', '-topmost', True)

        # Immediately register the listener with the dispatcher
        # await websocket.send(json.dumps(register))

        txtCommand=tk.Text(widget, height=1)
        txtCommand.pack()
        btnSend=tk.Button(widget, height=1, width=10,
                          text="Send", command=getTextCommand)
        btnSend.pack()
        widget.mainloop()

        # Loop infinitely for user to
        # speak

        while(1):
            if sendText:
                print('Send text')

            # Exception handling to handle
            # exceptions at the runtime
            try:



                text = ''

                print(
                    'Say \"blue\" to input command from microphone, say "file" to input from command file')

                text = SpeechToText()

                print("-> "+text)

                # uses mic after activation phrase
                if text == 'blue':
                    print('activation phrase')
                    playStartSoundThread = threading.Thread(
                        target=playStartSound)
                    playStartSoundThread.start()

                    command = SpeechToText()
                    print('Command heard: ' + command)
                    playEndSoundThread = threading.Thread(target=playEndSound)
                    playEndSoundThread.start()
                    command = json.dumps({
                        "action": "DISPATCH_COMMAND",
                        "command": command,
                    })
                    await websocket.send(command)
                # uses file to send command
                elif text == 'file':
                    # askes user for file name input
                    name = input('Input file name: ')
                    command = FileToText(name)
                    print('File command: ' + command)
                    command = json.dumps({
                        "action": "DISPATCH_COMMAND",
                        "command": command,
                    })
                    await websocket.send(command)

                # exit condition
                if text == 'exit':
                    deregister = {
                        "action": "DEREGISTER_LISTENER",
                        "app": "recognizer",
                    }
                    await websocket.send(json.dumps(deregister))
                    # time.sleep(0.5)
                    exit()

            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))

            except KeyboardInterrupt:
                await websocket.send(json.dumps(deregister))
                print("Bye")
                sys.exit()

            except sr.UnknownValueError:
                print("unknown error occured")
'''

#setting up
register = {
    "action": "REGISTER_LISTENER",
    "app": "recognizer",
    "eavesdrop": False,
}
deregister = {
    "action": "DEREGISTER_LISTENER",
    "app": "recognizer"
}
uri = "ws://127.0.0.1:2585/v1/messages"
ws = create_connection(uri)
widget = tk.Tk()
widget.geometry("400x240")
widget.lift()
widget.call('wm', 'attributes', '.', '-topmost', True)

speakImage = tk.PhotoImage(file='speak.png')
noSpeakImage = tk.PhotoImage(file='nospeak.png')
speakLabel = tk.Label(widget, image=noSpeakImage)
speakLabel.pack()



def SendCommand():
    result = txtCommand.get("1.0", "end")
    payload = {
        "action": "DISPATCH_COMMAND",
        "command": result.strip(),
        "recipient": "desktop"
    }
    ws.send(json.dumps(payload))


def VoiceCommand():

    while True:
        if exitFlag == True:
            exit()
        try:
            
            text = ''

            print('Say \"blue\" to input command from microphone, say "file" to input from command file')

            text = SpeechToText()

            print("-> "+text)

            # uses mic after activation phrase
            if text == 'blue':
                speakLabel.configure(image=speakImage)
                speakLabel.image = speakImage
                print('activation phrase')
                playStartSoundThread = threading.Thread(target=playStartSound)
                playStartSoundThread.start()

                command = SpeechToText()
                print('Command heard: ' + command)
                playEndSoundThread = threading.Thread(target=playEndSound)
                playEndSoundThread.start()
                speakLabel.configure(image=noSpeakImage)
                speakLabel.image = noSpeakImage
                txtCommand.delete("1.0", "end")
                txtCommand.insert("1.0", command)
                command = json.dumps({
                    "action": "DISPATCH_COMMAND",
                    "command": command,
                })
                ws.send(command)            

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except KeyboardInterrupt:
            ws.send(json.dumps(deregister))
            sys.exit()

        except sr.UnknownValueError:
            print("unknown error occured")




#starting the program
ws.send(json.dumps(register))

#setting up threads
voiceCommandThread = threading.Thread(target=VoiceCommand)

txtCommand=tk.Text(widget, height=1)
txtCommand.pack()
btnSend=tk.Button(widget, height=1, width=10, text="Send", command=SendCommand)
btnSend.pack()
def on_quit():
    global widget, exitFlag
    exitFlag = True
    widget.destroy()
voiceCommandThread.start()
widget.protocol("WM_DELETE_WINDOW", on_quit)
widget.mainloop()

#exitting

voiceCommandThread.join()
print('exit')
ws.send(json.dumps(deregister))

# runs the main function as an async function
# asyncio.get_event_loop().run_until_complete(main())
