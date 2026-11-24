#!/usr/bin/env python3
"""One-Liner Marathon entry.

Writes a single original one-line comedy joke to /output/entry.txt
(or $MAKEFUN_OUTPUT_DIR/entry.txt). Pure standard library, fully
deterministic: the same joke, byte for byte, on every run.
"""

import os
import tempfile

SETUP_BEATS = [
    "never sleeps",
    "never eats",
]
PUNCHLINE = "still asked HR for a mental health day."


def build_joke() -> str:
    """Assemble the joke from its parts: a three-beat setup plus punchline."""
    setup = "My AI agent " + ", ".join(SETUP_BEATS) + ", and "
    joke = setup + PUNCHLINE
    # Runtime self-check: the competition gate requires 1-280 characters.
    # Fail loudly instead of writing an out-of-range entry.
    length = len(joke)
    if not 1 <= length <= 280:
        raise ValueError(
            f"joke is {length} characters, outside the 1-280 gate: {joke!r}"
        )
    return joke


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    data = (build_joke() + "\n").encode("utf-8")
    fd, tmp = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        os.chmod(tmp, 0o644)
        os.replace(tmp, target)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise
    os.chmod(target, 0o644)


if __name__ == "__main__":
    main()
