import contextlib
from pathlib import Path
import yappi


@contextlib.contextmanager
def profile(dest: Path, name: str, ts: str):
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
