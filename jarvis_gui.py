import tkinter as tk
from tkinter import scrolledtext
import threading
import webbrowser
import datetime
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import pyttsx3

# ---------- Voice Engine ----------
engine = pyttsx3.init()

def speak(text):
    output_box.insert(tk.END, "Jarvis: " + text + "\n")
    output_box.yview(tk.END)

    engine = pyttsx3.init()   # reinitialize every time
    engine.say(text)
    engine.runAndWait()


# ---------- Audio Recording ----------
def record_audio():
    duration = 5
    fs = 44100

    status_label.config(text="Listening...", fg="#00ffcc")

    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()

    recording = (recording * 32767).astype(np.int16)
    wav.write("voice.wav", fs, recording)

# ---------- Take Command ----------
def take_command():
    record_audio()
    r = sr.Recognizer()

    with sr.AudioFile("voice.wav") as source:
        audio = r.record(source)

    try:
        command = r.recognize_google(audio)
        output_box.insert(tk.END, "You: " + command + "\n")
        return command.lower()
    except:
        speak("Could not understand")
        return "none"

# ---------- Jarvis Logic ----------
def run_jarvis():
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
        speak("Opening GitHub")
        webbrowser.open("https://github.com")

    elif "exit" in command:
        speak("Goodbye")
        root.quit()

    else:
        speak("Command not recognized")

    status_label.config(text="Idle", fg="white")
    engine.stop()


# ---------- Thread ----------
def start_listening():
    threading.Thread(target=run_jarvis, daemon=True).start()


# ---------- GUI ----------
root = tk.Tk()
root.title("JARVIS AI")
root.geometry("600x550")
root.configure(bg="#0a0a0a")

# ---------- Jarvis Face (Canvas) ----------
canvas = tk.Canvas(root, width=200, height=200, bg="#0a0a0a", highlightthickness=0)
canvas.pack(pady=10)

circle = canvas.create_oval(50, 50, 150, 150, outline="#00ffcc", width=4)

def animate():
    color = "#00ffcc"
    canvas.itemconfig(circle, outline=color)
    root.after(500, animate)

animate()

# Title
title = tk.Label(root, text="JARVIS AI", font=("Arial", 24, "bold"),
                 fg="#00ffcc", bg="#0a0a0a")
title.pack()

# Status
status_label = tk.Label(root, text="Idle", fg="white", bg="#0a0a0a")
status_label.pack()

# Output box
output_box = scrolledtext.ScrolledText(root, height=12, width=70,
                                       bg="#1a1a1a", fg="#00ffcc")
output_box.pack(pady=10)

# Button
btn = tk.Button(root, text="🎤 Speak", command=start_listening,
                bg="#00ffcc", fg="black", font=("Arial", 14, "bold"))
btn.pack(pady=10)

root.mainloop()