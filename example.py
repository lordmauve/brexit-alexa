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
    "Brexit means Brexit",
    "Strong and stable",
    "I'm bringing my deal back to parliament for a meaningful vote",
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
        with microphone as source:
            audio = recognizer.record (source, duration = 3) 
        try:
            text = recognizer.recognize_google (audio)
        except sr.UnknownValueError:
            continue

        print(text)
        if 'brexit' in text:
            say(random.choice(PHRASES))

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

    # set the list of words, maxnumber of guesses, and prompt limit
    WORDS = ["apple", "banana", "grape", "orange", "mango", "lemon"]
    NUM_GUESSES = 3
    PROMPT_LIMIT = 5

    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()


    for i in range(NUM_GUESSES):
        # get the guess from the user
        # if a transcription is returned, break out of the loop and
        #     continue
        # if no transcription returned and API request failed, break
        #     loop and continue
        # if API request succeeded but no transcription was returned,
        #     re-prompt the user to say their guess again. Do this up
        #     to PROMPT_LIMIT times
        for j in range(PROMPT_LIMIT):
            say('Guess {}. Speak!'.format(i+1))
            guess = recognize_speech_from_mic(recognizer, microphone)
            if guess["transcription"]:
                break
            if not guess["success"]:
                break
            say("I didn't catch that. What did you say?\n")

        # if there was an error, stop the game
        if guess["error"]:
            print("ERROR: {}".format(guess["error"]))
            break

        # show the user the transcription
        say("You said: {}".format(guess["transcription"]))

        # determine if guess is correct and if any attempts remain
        guess_is_correct = guess["transcription"].lower() == word.lower()
        user_has_more_attempts = i < NUM_GUESSES - 1

        # determine if the user has won the game
        # if not, repeat the loop if user has more attempts
        # if no attempts left, the user loses the game
        if guess_is_correct:
            say("Correct! You win!".format(word))
            break
        elif user_has_more_attempts:
            say("Incorrect. Try again.\n")
        else:
            say("Sorry, you lose!\nI was thinking of '{}'.".format(word))
            break
