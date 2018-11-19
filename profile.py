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
	return tracefunc

import sys
import inspect
import time
sys.setprofile(tracefunc)