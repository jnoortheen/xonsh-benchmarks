import importlib
import pkgutil
from pathlib import Path


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


def bench(fn_name: str, dest: Path, ts: str):
    import bench_helpers

    fn = getattr(bench_helpers, fn_name)

    module = importlib.import_module(f'profilers.{dest.name}')
    profile = getattr(module, "profile")
    with profile(dest, fn_name, ts):
        fn()


def get_profilers():
    import profilers
    import os
    for module in pkgutil.iter_modules([os.path.dirname(profilers.__file__)]):
        if module.name != "init":
            yield module.name


def main():
    import sys, os

    os.environ["XONSH_NO_AMALGAMATE"] = "1"
    args = sys.argv[1:]

    if not args:  # just the file name
        import subprocess as sp

        for typ in get_profilers():
            ts = get_timestamp()
            if branch := get_vcs_mark():
                ts = branch

            dest = Path(__file__).parent.parent / "results" / typ
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
