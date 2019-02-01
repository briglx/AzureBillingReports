#!/usr/bin/python

import sys
import csv
import random


def getSample(src, sample_rate):

    with open(src + '-sample-' + str(sample_rate) + '.csv', 'w', newline='') as f:
        writer = csv.writer(f)

        with open(src, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')

            for i in range(3):
                row = next(reader)
                writer.writerow(row)

            for row in reader:
                val = random.random()
                if val < sample_rate:
                    writer.writerow(row)


def main(argv):

    path = argv[0]
    rate = float(argv[1])

    getSample(path, rate)


if __name__ == "__main__":
    main(sys.argv[1:])
