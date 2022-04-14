import contextlib
from pathlib import Path


@contextlib.contextmanager
def profile(dest: Path, name: str, ts: str):
    from scalene import scalene_profiler
    scalene_profiler.start()
    yield
    scalene_profiler.stop()

    dest = dest / name
    dest.mkdir(exist_ok=True)

    out = dest / f"{ts}.html"
    scalene_profiler.Scalene.output_profile()
    # out.write_text(profiler.output_html())
