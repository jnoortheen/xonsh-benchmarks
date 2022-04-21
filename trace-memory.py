from pathlib import Path
from bench_utils import trace_memory, get_timestamp


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
