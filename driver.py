import os
import subprocess
import sys
from pathlib import Path
from functools import reduce
import json
import inspect

nodes_list = []
links_list = []

class Node:
    total_time = 0
    average_time = 0
    def __init__(self, name, children, timespent):
        self.name = name
        self.children = children
        self.timespent = timespent

    def __repr__(self):
        return " Children:" + str(len(self.children)) + " total_time: " + repr(self.total_time) + " average: " + repr(self.average_time) + "\n"

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 driver.py [input filename]")
        return

    filename = sys.argv[1]
    path = Path(filename)

    if path.is_file() and filename.endswith(".py") is False:
        print("File", filename, "does not exists or has an invalid extension.")
        return

    profile_fname = inject_profiling_code(filename)

    # use this for Windows:
    # result = subprocess.run(['py', filename], stdout=subprocess.PIPE, shell=True)
    result = subprocess.run(['python3', profile_fname], stdout=subprocess.PIPE)

    result_json = parse_result(result)

    try:
        os.remove(profile_fname)
    except OSError:
        pass

    # print (result_json)


def inject_profiling_code(filename):
    fout_name = "profile_" + filename

    prof_file = open("profile.py", "r")
    source_file = open(filename, "r")
    output_file = open(fout_name, "w")

    source_code = source_file.read()
    prof_code = prof_file.read()
    source_file.close()
    prof_file.close()

    output_file.write("\n")
    output_file.write(source_code)
    output_file.write(prof_code)

    output_file.close()
    return fout_name

def parse_result(result):
    lines = result.stdout.decode('utf-8').split("\n")

    if len(lines) < 2:
        # todo: make sure there is output, otherwise tell user to call something from their script
        error_object = {"Error": "blablabla"}
        return json.dumps(error_object)

    lines.reverse()
    lines.pop(0)

    json_output = parse_input(lines)
    write_json(json_output)

def parse_input(lines):
    nodes = {}

    for line in lines:
        node_name, timespent = line.split('~')
        call_stack = node_name.split('|')

        if node_name in nodes:
            node = nodes[node_name]
            node.timespent.append(timespent)
            continue

        node = Node(node_name, [], [timespent])
        nodes[node_name] = node

        if len(call_stack) <= 1:
            # no parent
            continue
        
        call_stack.pop()
        parentName = "|".join(call_stack)

        parent = nodes[parentName]
        parent.children.append(node)

    output_start = 0
    output_end = 50
    input_start = 0
    input_end = 0

    for key, n in nodes.items():
        node = nodes[key]
        times = list(map((lambda x: float(x)), node.timespent))
        node.total_time = reduce((lambda a, b: a + b), times)
        node.average_time = node.total_time / len(times)
        del node.timespent

        node_name = node.name.split('|').pop()
        node.name = node_name

        input_end = max(input_end, node.total_time)

    for key, node in nodes.items():
        node.size = map_range(input_start, input_end, output_start, output_end, node.total_time)
        node.size2 = map_range(input_start, input_end, output_start, output_end, node.average_time)

    return json.dumps(nodes["main"], default=lambda x: x.__dict__)

def write_json(data):
    output_file = open("output.json", "w")
    output_file.write(data)
    output_file.close

def map_range(input_start, input_end, output_start, output_end, value):
    slope = 1.0 * (output_end - output_start) / (input_end - input_start)
    output = output_start + slope * (value - input_start)
    return output

main()