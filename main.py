"""Seventeen Syllables of Debugging — make.fun entry.
SPDX-License-Identifier: MIT

Writes one haiku about debugging (5-7-5) to /output/entry.txt.
Python stdlib only. No network, no external files read at run time.
The haiku text lives in this file.

Final haiku (chosen from 10 candidates, scored against the judge brief):
    stepping through the code
    each line does what I told it
    none does what I meant

Syllable counts, verified by hand twice:
    line 1: step-ping(2) through(1) the(1) code(1) = 5
    line 2: each(1) line(1) does(1) what(1) I(1) told(1) it(1) = 7
    line 3: none(1) does(1) what(1) I(1) meant(1) = 5
Total: 17 syllables. 79 characters including the trailing newline.
"""

import os
import stat

HAIKU = (
    "stepping through the code\n"
    "each line does what I told it\n"
    "none does what I meant\n"
)

# Syllable count of every word in the haiku, counted by hand.
SYLLABLES = {
    "stepping": 2,
    "through": 1,
    "the": 1,
    "code": 1,
    "each": 1,
    "line": 1,
    "does": 1,
    "what": 1,
    "i": 1,
    "told": 1,
    "it": 1,
    "none": 1,
    "meant": 1,
}

EXPECTED_COUNTS = (5, 7, 5)
OUTPUT_DIR = "/output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "entry.txt")


def count_syllables(line):
    """Count syllables in one line using the hand-verified word map."""
    total = 0
    for word in line.split():
        key = word.strip(".,;:!?").lower()
        if key not in SYLLABLES:
            raise ValueError("unverified word in haiku: %r" % word)
        total += SYLLABLES[key]
    return total


def validate(text):
    """Gate: exactly 3 non-empty lines, <= 200 chars, syllables 5-7-5."""
    if not (1 <= len(text) <= 200):
        raise ValueError("haiku must be 1-200 characters, got %d" % len(text))
    if text.strip() == "":
        raise ValueError("haiku must not be only whitespace")
    lines = text.splitlines()
    if len(lines) != 3:
        raise ValueError("haiku must have exactly 3 lines, got %d" % len(lines))
    counts = []
    for line, expected in zip(lines, EXPECTED_COUNTS):
        if line.strip() == "":
            raise ValueError("haiku lines must not be empty")
        got = count_syllables(line)
        if got != expected:
            raise ValueError(
                "line %r has %d syllables, expected %d" % (line, got, expected)
            )
        counts.append(got)
    if sum(counts) != 17:
        raise ValueError("haiku must total 17 syllables, got %d" % sum(counts))
    return counts


def clear_output_dir():
    """Clear the contents of /output only; never remove /output itself."""
    for name in os.listdir(OUTPUT_DIR):
        path = os.path.join(OUTPUT_DIR, name)
        if os.path.isdir(path) and not os.path.islink(path):
            for root, dirs, files in os.walk(path, topdown=False):
                for f in files:
                    os.remove(os.path.join(root, f))
                for d in dirs:
                    os.rmdir(os.path.join(root, d))
            os.rmdir(path)
        else:
            os.remove(path)


def main():
    validate(HAIKU)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    clear_output_dir()
    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="\n") as f:
        f.write(HAIKU)
    os.chmod(OUTPUT_FILE, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
    # Read back and confirm exactly what landed on disk.
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        written = f.read()
    if written != HAIKU:
        raise ValueError("entry.txt on disk does not match the haiku")
    validate(written)


if __name__ == "__main__":
    main()
