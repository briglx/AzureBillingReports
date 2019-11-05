#!/usr/bin/python
"""Script to remove metadata header information from  monthly billing data."""
import os
import sys
import shutil


def remove_first_lines(file_name, count):
    """Remove first count of lines from file_name."""
    with open(file_name, "r") as source_file, open(
        file_name + ".tmp", "w"   # pylint: disable=C0330
    ) as target_file:

        for _ in range(count):
            source_file.readline()

        shutil.copyfileobj(source_file, target_file)

        os.remove(source_file)
        os.rename(target_file, source_file)


def main(argv):
    """Remove header fro filename passed in from command line."""
    file_name = argv[0]
    remove_first_lines(file_name, 2)


if __name__ == "__main__":
    main(sys.argv[1:])
