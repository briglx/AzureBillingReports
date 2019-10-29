#!/usr/bin/python
"""Create a smaller file of data by sampling."""
import sys
import csv
import random


def get_sample(src, sample_rate):
    """Get sample records from source file for given sample rate."""
    with open(
        src + "-sample-" + str(sample_rate) + ".csv", "w", newline=""
    ) as sample_file:
        writer = csv.writer(sample_file)

        with open(src, newline="") as csv_file:
            reader = csv.reader(csv_file, delimiter=",")

            for _ in range(3):
                row = next(reader)
                writer.writerow(row)

            for row in reader:
                val = random.random()
                if val < sample_rate:
                    writer.writerow(row)


def main(argv):
    """Get sample records from command line."""
    path = argv[0]
    rate = float(argv[1])

    get_sample(path, rate)


if __name__ == "__main__":
    main(sys.argv[1:])
