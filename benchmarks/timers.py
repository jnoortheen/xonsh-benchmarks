"""Timing benchmarks"""

timeout = 5.0


def time_script():
    import subprocess as sp

    sp.run(["xonsh", "-c", "echo 1"])


def time_interactive_rl():
    from ptyprocess import PtyProcessUnicode as pty

    proc = pty.spawn(["xonsh", "--interactive", "--no-rc", "--shell=rl"])
    proc.readline()
    proc.write("echo 1\n")
    proc.terminate()


def time_interactive_ptk():
    from ptyprocess import PtyProcessUnicode as pty

    proc = pty.spawn(["xonsh", "--interactive", "--no-rc", "--shell=ptk"])
    proc.readline()
    proc.write("echo 1\n")
    proc.terminate()
