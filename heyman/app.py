import sys
import os

from heyman.core.assistant import Assistant

from heyman.config import assistant as cfg

def collect_computer_programs():
    global programs
    programs = set()
    with os.scandir("/Applications/") as entries:
        for entry in entries:
            programs.add(entry.name)
        return programs



# if len(sys.argv) > 1:
#     model = sys.argv[1]
# else:
#     model = "models/heyman.pmdl"

programs = set()
collect_computer_programs()

heyman = Assistant(cfg["model"])
heyman.listen()
