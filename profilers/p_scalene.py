import contextlib
from pathlib import Path


@contextlib.contextmanager
def profile(dest: Path, name: str, ts: str):

    profiler = Profiler()
    profiler.start()
    yield
    profiler.stop()

    dest = dest / name
    dest.mkdir(exist_ok=True)

    out = dest / f"{ts}.html"
    out.write_text(profiler.output_html())
