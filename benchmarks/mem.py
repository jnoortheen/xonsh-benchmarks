"""individual component's memory usage"""


def _get_parser():
    from xonsh.parser import Parser

    p = Parser()
    # wait for thread to finish
    p.parse("1")
    return p


def _in_detail(more_info=False):
    from pympler import asizeof

    p = _get_parser()

    if more_info:
        print(asizeof.asized(p, detail=2).format())
        # print detailed memory usage of the ply yacc
        print(asizeof.asized(p.parser, detail=2).format())

    # size of the combined object in bytes
    return asizeof.asizeof(p)


def track_parser_size():
    """use pympler to the size of the parser including all of its attributes"""
    return _in_detail()


if __name__ == "__main__":
    print(_in_detail(True))
