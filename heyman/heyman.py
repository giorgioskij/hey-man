import signal
import sys
import os
import speech_recognition as sr
import Levenshtein


from math import inf
from snowboylib import snowboydecoder


class Heyman:

    def __init__(self, model):
        self.model = model
        self.interrupted = False
        self.detector = snowboydecoder.HotwordDetector(self.model, sensitivity = 0.5)

        signal.signal(signal.SIGINT, self.handle_signal)

    def listen(self):
        print("Listening... press Ctrl+C to exit")
        self.detector.start(detected_callback = self.activate,
                            interrupt_check = lambda: self.interrupted,
                            sleep_time = 0.03)

        self.detector.terminate()

    def handle_signal(self, signal, frame):
        self.interrupted = True

    def say(self, s):
        os.system("say {0} -v fiona -r 210".format(s.replace("\'", "")))

    def activate(self):
        print("Hi! I am now listening")
        self.say("what's up man")

        self.detector.terminate()
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
            self.interpret(text)

        self.listen()


    def interpret(self, text):
        if "open" in text or "launch" in text:
            words = text.split()
            i = words.index("open") if "open" in text else words.index("launch")
            self.openApp("".join(words[i+1:]))


        elif "nothing" in text:
            self.say("ok sorry")

        else:
            answer = "You said {0}, but you know I am not yet programmed to answer to that".format(text.replace("\'", ""))
            # os.system("say {0}".format(answer))
            self.say(answer)

    def openApp(self, name):
        global programs

        if programs == None:
            collect_computer_programs

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
        self.say("launching {0}".format(candidate))

        os.system("open /Applications/"+path)





def collect_computer_programs():
    global programs
    programs = set()
    with os.scandir("/Applications/") as entries:
        for entry in entries:
            programs.add(entry.name)
        return programs


if len(sys.argv) > 1:
    model = sys.argv[1]
else:
    model = "heyman.pmdl"

programs = set()
collect_computer_programs()

heyman = Heyman(model)
heyman.listen()
