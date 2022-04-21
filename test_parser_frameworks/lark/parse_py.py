import subprocess
import sys

from lark.lark import Lark
from lark.indenter import PythonIndenter
from pathlib import Path

current = Path(__file__)


def lark_parse():
    GRAMMAR = current.with_name("grammar.lark").read_text()
    parser = Lark(
        GRAMMAR,
        parser="lalr",
        start=["single_input", "file_input", "eval_input"],
        postlex=PythonIndenter(),
        # import lark_cython
        # _plugins=lark_cython.plugins,
    )

    tree = parser.parse(
        current.with_name("sample.py").read_text(),
        start="file_input",
    )

    # Remove the 'python3__' prefix that was added to the implicitly imported rules.
    for t in tree.iter_subtrees():
        t.data = t.data.rsplit("__", 1)[-1]
    # print(tree.pretty())


def lark_standalone():
    if not current.with_name("standalone.py").exists():
        subprocess.call(
            [
                sys.executable,
                "-m",
                "lark.tools.standalone",
                "grammar.lark",
                "--start=file_input",
                "--out=standalone.py",
            ],
            cwd=current.parent,
        )
    from test_parser_frameworks.lark.standalone import Lark_StandAlone

    parser = Lark_StandAlone(
        # start=["single_input", "file_input", "eval_input"],
        postlex=PythonIndenter(),
    )

    tree = parser.parse(
        current.with_name("sample.py").read_text(),
        start="file_input",
    )

    # Remove the 'python3__' prefix that was added to the implicitly imported rules.
    for t in tree.iter_subtrees():
        t.data = t.data.rsplit("__", 1)[-1]


if __name__ == "__main__":
    from bench_utils import trace_memory, get_timestamp

    dest = current.parent.parent.parent.joinpath("html", "tracemalloc")

    for fn in [
        lark_parse,
        lark_standalone,
    ]:
        with trace_memory(dest, fn.__name__, get_timestamp(), limit=20, show_tb=False):
            fn()
