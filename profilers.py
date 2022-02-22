from pathlib import Path
import contextlib


def get_timestamp():
    from datetime import datetime

    now = datetime.now()

    return f"{now:%Y-%m-%d-%H-%M-%S}"


def get_vcs_mark():
    import xonsh, os, subprocess as sp

    path = os.path.dirname(xonsh.__file__)
    branch = sp.run(
        ["git", "branch", "--show-current"], capture_output=True, cwd=path, text=True
    )
    if branch.stdout:
        commit = sp.run(
            "git rev-parse --short HEAD".split(),
            capture_output=True,
            cwd=path,
            text=True,
        )
        return branch.stdout.strip() + "-" + commit.stdout.strip()


@contextlib.contextmanager
def pyinstr_profiler(dest: Path, name: str, ts: str):
    from pyinstrument import Profiler

    profiler = Profiler()
    profiler.start()
    yield
    profiler.stop()

    dest = dest / name
    dest.mkdir(exist_ok=True)

    out = dest / f"{ts}.html"
    out.write_text(profiler.output_html())


@contextlib.contextmanager
def yappi_profiler(dest: Path, name: str, ts: str):
    import yappi

    yappi.set_clock_type("cpu")  # Use set_clock_type("wall") for wall time
    yappi.start()
    yield

    func_stats = yappi.get_func_stats()

    dest = dest / name
    dest.mkdir(exist_ok=True)

    # use snakeviz or such packages to view
    func_stats.save(dest / f"{ts}.pstat", "pstat")

    # func_stats.save(dest / f"{name}-funcs.grind", "callgrind")
    with (dest / f"{ts}.txt").open("w") as fw:
        func_stats.print_all(fw)
        yappi.get_thread_stats().print_all(fw)


def bench(fn_name: str, dest: Path, ts: str):
    import bench_helpers

    fn = getattr(bench_helpers, fn_name)

    profiler = pyinstr_profiler
    if "yappi" in str(dest):
        profiler = yappi_profiler
    with profiler(dest, fn_name, ts):
        fn()


def main():
    import sys, os

    os.environ["XONSH_NO_AMALGAMATE"] = "1"
    args = sys.argv[1:]

    if not args:  # just the file name
        import subprocess as sp

        for typ in ["pyinstrument", "yappi"]:
            ts = get_timestamp()
            if branch := get_vcs_mark():
                ts = branch

            dest = Path(__file__).parent / "html" / typ
            dest.mkdir(parents=True, exist_ok=True)

            for fn in ["script_echo", "shell_rl", "shell_ptk"]:
                # run as subprocess so that will not interfere each other functions
                args = [sys.executable, __file__, fn, str(dest), ts]
                print(f"Running {args}")
                sp.run(args, env=os.environ)
    else:
        bench(args[0], Path(args[1]), args[2])


if __name__ == "__main__":
    main()
