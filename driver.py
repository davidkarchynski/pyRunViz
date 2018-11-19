import os
import subprocess
import sys
from pathlib import Path

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 driver.py [input filename]")
        return

    filename = sys.argv[1]
    path = Path(filename)

    if path.is_file() and filename.endswith(".py") is False:
        print("File", filename, "does not exists or has an invalid extension.")
        return

    result = subprocess.run(['py', filename], stdout=subprocess.PIPE, shell=True)
    lines = result.stdout.decode('utf-8').split("\n")

    if len(lines) < 2:
        # todo: make sure there is output, otherwise tell user to call something from their script
        print("blablabla")
        return

    lines.reverse()
    lines.pop(0)

    parse_input(lines)
    

def inject_profiling_code(filename):
    # todo read in filename and inject the profiling code from profile.py into it
    # then save it as filename_profile.py
    return

def parse_input(lines):
    # todo generate the json here
    # Nodes = id, size
    # links {"source": "Napoleon", "target": "Myriel", "value": 1},

    for x in lines:
        print(x)



main()