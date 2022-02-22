from pathlib import Path
import contextlib


def get_dest(typ: str):
    from datetime import datetime

    now = datetime.now()

    results = (
        Path(__file__).parent
        / "html"
        / typ
        / f"{now.date():%Y-%m-%d}"
        / f"{now.time():%H-%M-%S}"
    )
    results.mkdir(parents=True, exist_ok=True)
    return results


@contextlib.contextmanager
def pyinstr_profiler(dest, name):
    from pyinstrument import Profiler

    profiler = Profiler()
    profiler.start()
    yield
    profiler.stop()

    out = dest / f"{name}.html"
    out.write_text(profiler.output_html())


@contextlib.contextmanager
def yappi_profiler(dest: Path, name: str):
    import yappi

    yappi.set_clock_type("cpu")  # Use set_clock_type("wall") for wall time
    yappi.start()
    yield

    func_stats = yappi.get_func_stats()

    # use snakeviz or such packages to view
    func_stats.save(dest / f"{name}-funcs.pstat", "pstat")

    # func_stats.save(dest / f"{name}-funcs.grind", "callgrind")
    with (dest / f"{name}-prints.txt").open("w") as fw:
        func_stats.print_all(fw)
        yappi.get_thread_stats().print_all(fw)


def bench(fn_name: str, dest):
    import bench_helpers

    fn = getattr(bench_helpers, fn_name)

    profiler = pyinstr_profiler
    if "yappi" in str(dest):
        profiler = yappi_profiler
    with profiler(dest, fn_name):
        fn()


def main():
    import sys, os

    os.environ["XONSH_NO_AMALGAMATE"] = "1"
    args = sys.argv[1:]

    if not args:  # just the file name
        import subprocess as sp

        for typ in ["pyinstrument", "yappi"]:
            dest = get_dest(typ)
            for fn in ["script_echo", "shell_rl", "shell_ptk"]:
                # run as subprocess so that will not interfere each other functions
                args = [sys.executable, __file__, fn, str(dest)]
                print(f"Running {args}")
                sp.run(args, env=os.environ)
    else:
        bench(args[0], Path(args[1]))


if __name__ == "__main__":
    main()
