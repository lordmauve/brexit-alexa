"""Example voice game.

Copied from https://realpython.com/python-speech-recognition/.
"""

import random
import time


from gtts import gTTS
import os
from io import BytesIO
from pygame import mixer
from tempfile import NamedTemporaryFile

import speech_recognition as sr


PHRASES = [
    "We demand a permanent customs union.",
    "No border in the Irish sea.",
    "Blue passports.",
    "Strong and stable",
    "I'm bringing my deal back to parliament for a meaningful vote",
    "After all the division this country must come together.",
    "We will leave the EU on the twenty-ninth of March.",
]

GREETINGS = [
    'Hey!', 'Wait a second!', 'Did you know?', 'Speaking about Brexit...',
]


def recognize_speech_from_mic(recognizer, microphone):
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
      
        # that sends to Google
        while True: 
            audio = recognizer.record (source, duration = 3) 
            try:
                text = recognizer.recognize_google (audio)
            except sr.UnknownValueError:
                continue


            print(text)
            if 'brexit' in text:
                greeting = random.choice(GREETINGS)
                phrase = random.choice(PHRASES)
                say(f'{greeting} {phrase}')

    return response


def say(words):
    with NamedTemporaryFile(suffix='.mp3') as mp3_fp:
        tts = gTTS(text=words, lang='en')
        tts.write_to_fp(mp3_fp)
        mp3_fp.flush()
        mixer.music.load(mp3_fp.name)
        mixer.music.play()
        while mixer.music.get_pos() > -1:
            time.sleep(0.2)


if __name__ == "__main__":

    mixer.pre_init(25000, 16, 2)
    mixer.init()

    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    say("Hi, I'm Brexa. What would you like to know?")
    guess = recognize_speech_from_mic(recognizer, microphone)
   
