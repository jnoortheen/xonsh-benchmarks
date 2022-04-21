from pathlib import Path
import contextlib


def get_timestamp():
    from datetime import datetime

    now = datetime.now()

    return f"{now:%Y-%m-%d-%H-%M-%S}"


def display_top(snapshot, key_type="lineno", limit=10, file=None):
    import linecache
    import tracemalloc

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


@contextlib.contextmanager
def trace_memory(dest: Path, name: str, ts: str = None, limit=100, show_tb=True):
    import tracemalloc

    tracemalloc.start(25)
    yield
    snap = tracemalloc.take_snapshot()

    dest = dest / name
    dest.mkdir(exist_ok=True)

    current, peak = [size / 1024 for size in tracemalloc.get_traced_memory()]
    print(f"{name}: {current=:.1f}KiB,  {peak=:.1f}KiB")

    out = dest / f"{ts}.md"
    with out.open("w") as fw:
        if show_tb:
            display_top(snap, file=fw, limit=limit, key_type="traceback")
            fw.write("\n\n\n===----=====")
        display_top(snap, file=fw, limit=limit)
    print(f"written to {out}")
    tracemalloc.reset_peak()
    tracemalloc.stop()
