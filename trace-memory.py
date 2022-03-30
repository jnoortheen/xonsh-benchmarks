from pathlib import Path
import contextlib
import tracemalloc


def display_top(snapshot, key_type="lineno", limit=10, file=None):
    import linecache

    # todo: display all values greater than 5KiB instead of top 10/50
    snapshot = snapshot.filter_traces(
        (
            tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
            tracemalloc.Filter(False, "<unknown>"),
        )
    )
    top_stats = snapshot.statistics(key_type)

    print(f"Top {limit} lines. {key_type=}", file=file)
    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        print(
            "#%s: %s:%s: %.1f KiB"
            % (index, frame.filename, frame.lineno, stat.size / 1024),
            file=file,
        )
        line = linecache.getline(frame.filename, frame.lineno).strip()
        if line:
            print("    %s" % line, file=file)

    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        print("%s other: %.1f KiB" % (len(other), size / 1024), file=file)
    total = sum(stat.size for stat in top_stats)
    print("Total allocated size: %.1f KiB" % (total / 1024), file=file)


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
def trace_memory(dest: Path, name: str, ts: str):
    tracemalloc.start(25)
    yield
    snap = tracemalloc.take_snapshot()

    dest = dest / name
    dest.mkdir(exist_ok=True)

    out = dest / f"{ts}.md"
    with out.open("w") as fw:
        display_top(snap, file=fw, limit=100, key_type="traceback")
        fw.write("\n\n\n===----=====")
        display_top(snap, file=fw, limit=100)
    print(f"written to {out}")
    tracemalloc.stop()


def bench(fn_name: str, dest: Path, ts: str):
    import bench_helpers

    fn = getattr(bench_helpers, fn_name)

    with trace_memory(dest, fn_name, ts):
        fn()


def _get_funcs():
    import bench_helpers

    for k, val in vars(bench_helpers).items():
        if k.startswith("_"):
            continue
        if callable(val) and val.__module__.endswith("bench_helpers"):
            yield val.__name__


def main():
    import sys, os

    os.environ["XONSH_NO_AMALGAMATE"] = "1"
    args = sys.argv[1:]

    if not args:  # just the file name
        import subprocess as sp

        ts = get_timestamp()
        if branch := get_vcs_mark():
            ts = branch

        dest = Path(__file__).parent / "html" / "tracemalloc"
        dest.mkdir(parents=True, exist_ok=True)

        funcs = list(_get_funcs())
        if not funcs:
            print("No functions found")
        for fn in funcs:
            # run as subprocess so that will not interfere each other functions
            args = [sys.executable, __file__, fn, str(dest), ts]
            print(f"Running {args}")
            sp.run(args, env=os.environ)
    else:
        bench(args[0], Path(args[1]), args[2])


if __name__ == "__main__":
    main()
