
def tracefunc(frame, event, arg, timing={}, stack=[]):
    name = frame.f_code.co_name
    if name == "<module>":
        return tracefunc
    caller = frame.f_back.f_code.co_name
    if event == "call":
        stack.append(name)
        timing[name] = time.time()
    elif event == "return":
        timespent = time.time() - timing[name]
        stack_str = "|".join(stack)
        stack.pop()
        # print(caller + "|" + name + "|" + repr(timespent))
        print(stack_str + "~" + repr(timespent))
    return tracefunc


import sys
import inspect
import time

sys.setprofile(tracefunc)

main()