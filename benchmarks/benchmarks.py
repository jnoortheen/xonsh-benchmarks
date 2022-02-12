# Write the benchmarking functions here.
# See "Writing benchmarks" in the asv docs for more information.


class TimeSuite:
    """
    An example benchmark that times the performance of various kinds
    of iterating over dictionaries in Python.
    """

    # def setup(self):

    def time_xonsh_script(self):
        import subprocess as sp

        sp.run(["xonsh", "-c", "echo 1"])

    def time_xonsh_interactive(self):
        from ptyprocess import PtyProcessUnicode as pty

        proc = pty.spawn(["xonsh", "--interactive", "--no-rc"])
        proc.readline()
        proc.write("echo 1\n")
        proc.terminate()


# class MemSuite:
#     def mem_xonsh_script(self):
#         from xonsh.main import main
#         main(["-c", "echo 1"])
