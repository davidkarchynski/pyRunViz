def foo():
	bar()

def bar():
	moo(10)
	moo(1)

def moo(sl):
	time.sleep(sl)

def main():
	foo()

def tracefunc(frame, event, arg, indent=[0]):
	if event == "call":
		caller=inspect.stack()[2][3]
		current=inspect.stack()[1][3]
#		print(caller+"->"+current+"\n")
		indent[0] += 2
		print ("-" * indent[0] + "> call function", frame.f_code.co_name, time.time())
	elif event == "return":
		print ("<" + "-" * indent[0], "exit function", frame.f_code.co_name, time.time())
		indent[0] -= 2
	return tracefunc

import sys
import inspect
import time
sys.setprofile(tracefunc)

main()   # or whatever kicks off your script
