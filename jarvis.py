import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def record_audio():
    duration = 5
    fs = 44100

    print("Listening...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()

    recording = (recording * 32767).astype(np.int16)

    wav.write("voice.wav", fs, recording)

def take_command():

    record_audio()

    r = sr.Recognizer()

    with sr.AudioFile("voice.wav") as source:
        audio = r.record(source)

    try:
        command = r.recognize_google(audio)
        print("You said:", command)
        return command.lower()

    except:
        print("Could not understand")
        return "none"

def wish():

    hour = int(datetime.datetime.now().hour)

    if hour < 12:
        speak("Good morning Rohan")

    elif hour < 18:
        speak("Good afternoon Rohan")

    else:
        speak("Good evening Rohan")

    speak("I am Jarvis. How can I help you")

def run_jarvis():

    wish()

    while True:

        command = take_command()

        if "open youtube" in command:
            speak("Opening YouTube")
            webbrowser.open("https://youtube.com")

        elif "open google" in command:
            speak("Opening Google")
            webbrowser.open("https://google.com")

        elif "time" in command:
            time = datetime.datetime.now().strftime("%H:%M")
            speak("The time is " + time)

        elif "open github" in command:
            webbrowser.open("https://github.com")

        elif "exit" in command:
            speak("Goodbye")
            break

run_jarvis()