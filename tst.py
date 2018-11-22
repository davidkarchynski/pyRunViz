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