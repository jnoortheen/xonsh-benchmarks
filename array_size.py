import array
from pympler import asizeof


def init_array():
    # H -> unsigned short - positive only - 0-65,000 - 2bytes
    ar = array.array("H", range(2000))
    size = asizeof.asizeof(ar)
    print(f"shorts array: {size=}")


def init_list():
    ar = list(range(2000))
    size = asizeof.asizeof(ar)
    print(f"list: {size=}")


if __name__ == "__main__":
    init_array()  # 4.3kB -> 5%
    init_list()  # 80kB
