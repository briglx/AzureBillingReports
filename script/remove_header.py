#!/usr/bin/python
"""Script to remove metadata header information from  monthly billing data."""
import sys
import shutil


def remove_first_lines(src_file_name, dest_file_name, count):
    """Remove first count of lines from file_name."""
    with open(src_file_name, "r") as src_stream, open(
        dest_file_name, "w"  # pylint: disable=C0330
    ) as dest_stream:

        # Skip lines
        for _ in range(count):
            src_stream.readline()

        # Copy contents
        shutil.copyfileobj(src_stream, dest_stream)


def main(argv):
    """Remove header fro filename passed in from command line."""
    full_file_name = argv[0]

    file_parts = full_file_name.split('.')
    file_name = file_parts[:-1]
    extension_part = file_parts[-1]
    dest_file_name = file_name + "-noheader" + extension_part
    remove_first_lines(full_file_name, dest_file_name, 2)


if __name__ == "__main__":
    main(sys.argv[1:])
