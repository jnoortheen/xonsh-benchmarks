import subprocess as sp

import requests
from tqdm import tqdm


def get_tags():
    count = 10  # run for latest 10 tags
    resp = requests.get("https://api.github.com/repos/xonsh/xonsh/tags").json()
    for obj in resp:
        count -= 1
        yield obj["name"]
        if count < 0:
            break
    yield "main"


def main():
    tags = list(get_tags())
    for tag in tqdm(tags):
        args = [
            "asv",
            "run",
            "--skip-existing",
            "--show-stderr",
            "--profile",
            f"{tag}^!",
        ]
        print(f"${args}")
        sp.run(args)


if __name__ == "__main__":
    main()
