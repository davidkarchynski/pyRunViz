import os
import subprocess
import sys
from pathlib import Path
from functools import reduce
import json

nodes_list = []
links_list = []

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

    print (result_json)


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

    parse_input(lines)
    return create_json()

def parse_input(lines):
    for line in lines:
        caller, name, timespent = line.split('|')
        log_node(name, timespent)
        log_link(caller, name)

# Helper methods for JSON
def log_link(from_node, to_node):
    links_list.append((from_node, to_node))

def log_node(node, t):
    nodes_list.append((node, t))

def create_nodes_dictionary():
    results = []

    all_nodes = list(map((lambda x: x[0]), nodes_list))
    all_nodes = list(set(all_nodes))

    for n in all_nodes:
        all_element_n = list(filter((lambda x: x[0] == n), nodes_list))
        all_element_sizes = list(map((lambda x: float(x[1])), all_element_n))
        sum_element_n = reduce((lambda a, b: a + b), all_element_sizes)
        avg_element_n = sum_element_n / len(all_element_n)
        results.append({"id": n, "size": avg_element_n})
    return results

def create_links_dictionary():
    results = []
    all_links = set(links_list)

    for l in all_links:
        count_l = links_list.count(l)
        results.append({"source": l[0], "target": l[1], "value": count_l})
    return results

def create_json():
    nodes_dictionary = create_nodes_dictionary()
    links_dictionary = create_links_dictionary()
    results_object = {
        "nodes": nodes_dictionary,
        "links": links_dictionary
    }
    results_json = json.dumps(results_object)
    return results_json

main()