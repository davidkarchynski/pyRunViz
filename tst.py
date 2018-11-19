def foo():
    bar()
    moo(0.1)
    bar()


def bar():
    moo(0.3)
    moo(0.5)


def moo(sl):
    time.sleep(sl)


def main():
    foo()


# TODO: add these to another utils class
nodes_list = []
links_list = []


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


def create_lists_dictionary():
    results = []
    all_links = set(links_list)

    for l in all_links:
        count_l = links_list.count(l)
        results.append({"source": l[0], "target": l[1], "value": count_l})
    return results


def tracefunc(frame, event, arg, timing={}):
    name = frame.f_code.co_name
    if name == "<module>":
        return tracefunc
    caller = frame.f_back.f_code.co_name
    if event == "call":
        timing[name] = time.time()
    elif event == "return":
        timespent = time.time() - timing[name]
        print(caller + "->" + name + "->" + repr(timespent))
        log_node(name, repr(timespent))
        log_link(caller, name)
    return tracefunc


import sys
import inspect
import time
from functools import reduce

sys.setprofile(tracefunc)

main()
print(create_nodes_dictionary())
print(create_lists_dictionary())
