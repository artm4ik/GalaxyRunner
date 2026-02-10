import os
from constants import HIGHSCORE_FILE


def load_highscore() -> int:
    if not os.path.exists(HIGHSCORE_FILE):
        return 0
    with open(HIGHSCORE_FILE, "r") as f:
        try:
            return int(f.read().strip())
        except ValueError:
            return 0


def save_highscore(score: int):
    old = load_highscore()
    if score > old:
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(score))
