"""Measure overall memory usage"""

from contextlib import contextmanager


@contextmanager
def _inp_exit():
    from tempfile import NamedTemporaryFile
    from unittest import mock

    with NamedTemporaryFile(mode="w+") as inp_file:
        with mock.patch("sys.stdin", inp_file):
            inp_file.write("exit\n")
            inp_file.seek(0)
            yield inp_file


@contextmanager
def _mock_rl():
    from unittest import mock

    with _inp_exit(), mock.patch(
        "xonsh.readline_shell.ReadlineShell._load_remaining_input_into_queue"
    ):
        yield


def peakmem_script():
    from xonsh.main import main

    try:
        main(["-c", "echo 1"])
    except SystemExit:
        return


def peakmem_interactive_rl():
    from xonsh.main import main

    with _mock_rl():
        try:
            main(["-i", "--shell=rl"])
        except SystemExit:
            return


def peakmem_interactive_ptk():
    from xonsh.main import main

    with _inp_exit():
        try:
            main(["-i", "--shell=ptk"])
        except SystemExit:
            return


if __name__ == "__main__":
    peakmem_interactive_ptk()
    peakmem_interactive_rl()
