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

def add_link(from_node, to_node):
	links_list.append([from_node, to_node])

def add_node(node, t):
	nodes_list.append([node, t])


def tracefunc(frame, event, arg, timing={}):
	name = frame.f_code.co_name
	if name == "<module>":
		return tracefunc
	caller = frame.f_back.f_code.co_name
	if event == "call":
		timing[name] = time.time()
	elif event == "return":
		timespent = time.time() - timing[name]
		print (caller + "->" + name + "->" + repr(timespent))
		add_node(name, repr(timespent))
		add_link(caller, name)
	return tracefunc

import sys
import inspect
import time
sys.setprofile(tracefunc)

main()
print (nodes_list)
print (links_list)