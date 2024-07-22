#!/usr/bin/env python3
"""Docstring."""

import sys
import my_module as mod

def get_args():
    return sys.argv[1:]

def main():
    """Do the things."""
    infile, outfile = get_args()
    lines = mod.get_file_data(infile)
    newlines = []
    for i in range(len(lines)):
        if i%4 < 2:
            newlines.append(lines[i])
    with open(outfile, "w", encoding = "utf8") as out:
        out.write("\n".join(newlines) + "\n")

if __name__ == "__main__":
    main()
