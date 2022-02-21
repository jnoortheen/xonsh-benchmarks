"""Measure overall memory usage"""

from contextlib import contextmanager


@contextmanager
def _inp_exit():
    from tempfile import NamedTemporaryFile
    from unittest import mock

    with NamedTemporaryFile(mode="w+") as inp, NamedTemporaryFile(
        mode="w+"
    ) as out, NamedTemporaryFile(mode="w+") as err:
        with (
            mock.patch("sys.stdin", inp),
            # mock.patch("sys.stdout", out),
            mock.patch("sys.stderr", err),
        ):
            inp.write("exit\n")
            inp.seek(0)
            yield inp, out, err

        def read(file):
            file.seek(0)
            return file.read()

        assert "exit" in read(inp)
        # print(f"{read(inp)=}, {read(out)=}, {read(err)=}")


@contextmanager
def _mock_rl():
    from unittest import mock

    with _inp_exit() as inp, mock.patch(
        "xonsh.readline_shell.ReadlineShell._load_remaining_input_into_queue"
    ):
        yield inp


class PeakmemSuit:
    timeout = 5.0

    def peakmem_script(self):
        from xonsh.main import main, setup

        try:
            setup()
            main(["-c", "echo 1"])
        except SystemExit:
            return

    def peakmem_interactive_rl(self):
        with _mock_rl():
            from xonsh.main import main

            try:
                main(["-i", "--shell=rl", "--no-rc"])
            except SystemExit:
                return

    def peakmem_interactive_ptk(self):
        with _inp_exit():
            from xonsh.main import main

            try:
                main(["-i", "--shell=ptk", "--no-rc"])
            except SystemExit:
                return


if __name__ == "__main__":
    p = PeakmemSuit()
    p.peakmem_interactive_ptk()
    p.peakmem_interactive_rl()
