import sys
import signal
from snowboylib import snowboydecoder
import os
import Levenshtein
from math import inf
import speech_recognition as sr

# from gtts import gTTS

interrupted = False


# configuration to use pyttsx3 as voice engine

# import pyttsx3 as tts
# engine = tts.init()
# voices = engine.getProperty("voices")
# rate = engine.getProperty("rate")
# print(rate)
# engine.setProperty("rate", 210.0)
# engine.setProperty("voice", "com.apple.speech.synthesis.voice.fiona")
# engine.setProperty("voice", "com.apple.speech.synthesis.voice.samantha")


def collect_computer_programs():
    programs = set()
    with os.scandir("/Applications/") as entries:
        for entry in entries:
            programs.add(entry.name)
        return programs

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def say(s):
    # engine.say(s)
    # engine.runAndWait()
    # gTTS(text)
    os.system("say {0} -v fiona -r 210".format(s.replace("\'", "")))


def interrupt_callback():
    global interrupted
    return interrupted


def openApp(name):
    newname = ''.join(' ' + char if char.isupper() else char for char in name).strip() + ".app"

    print("I heard {0}".format(newname))

    best_score = inf
    candidate = None
    for program in programs:
        score = Levenshtein.distance(newname, program)
        if score < best_score:
            best_score = score
            candidate = program

    path = candidate.replace(" ", "\\ ")

    say("launching {0}".format(candidate))

    os.system("open /Applications/"+path)


def listening():
    print("Hi! I am now listening")
    say("what's up man")

    detector.terminate()
    mic = sr.Microphone()
    rec = sr.Recognizer()

    with mic as source:
        audio = rec.listen(source=source)

    try:
        text = rec.recognize_google(audio)

    except sr.UnknownValueError:
        print("Google could not understand audio")

    except sr.RequestError as e:
        print("Could not request results from shpinx service; {0}".format(e))

    if text:
        interpret(text)

    detector.start(detected_callback=listening,
                   interrupt_check=interrupt_callback,
                   sleep_time=0.03)


def interpret(text):

    if "open" in text or "launch" in text:
        words = text.split()
        i = words.index("open") if "open" in text else words.index("launch")
        openApp("".join(words[i+1:]))

    elif "nothing" in text:
        say("ok sorry")

    else:
        answer = "You said {0}, but you know I am not yet programmed to answer to that".format(text.replace("\'", ""))
        # os.system("say {0}".format(answer))
        say(answer)


if len(sys.argv) == 1:
    print("Error: need to specify model name")
    print("Usage: python demo.py your.model")
    sys.exit(-1)

model = sys.argv[1]

programs = collect_computer_programs()

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
print('Listening... Press Ctrl+C to exit')

# main loop
detector.start(detected_callback=listening,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
