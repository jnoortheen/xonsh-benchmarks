"""Measure overall memory usage"""
import sys
from pathlib import Path

# so that bench_helpers import will work
sys.path.append(str(Path(__file__).parent.parent))

timeout = 5.0


def peakmem_script():
    from bench_helpers import script_echo

    script_echo()


def peakmem_interactive_rl():
    from bench_helpers import shell_rl

    shell_rl()


def peakmem_interactive_ptk():
    from bench_helpers import shell_ptk

    shell_ptk()


if __name__ == "__main__":
    peakmem_interactive_ptk()
    peakmem_interactive_rl()
