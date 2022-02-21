"""individual component's memory usage"""


def mem_parser():
    from xonsh.parser import Parser

    p = Parser()
    # wait for thread to finish
    p.parse("1")

    return p
