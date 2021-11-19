#!/usr/bin/python
"""Filter out data from file."""
import argparse
import logging
import sys
from datetime import datetime

from billing import util


def main(argv):
    """Filter records from command line."""
    path = argv[0]
    target_date = datetime.strptime(argv[1], "%Y-%m-%d")

    predicate = util.filter_greater_than_equal_date(target_date)

    util.filter_data(path, predicate)


if __name__ == "__main__":
    util.setup_logging()
    _LOGGER = logging.getLogger(__name__)
    _LOGGER.info("Starting script")

    parser = argparse.ArgumentParser(
        description="Filter data.",
        add_help=True,
    )
    parser.add_argument(
        "--path",
        "-p",
        help="Path to file",
    )
    parser.add_argument(
        "--min_date",
        "-m",
        help="Minimum date. Earlier dates are removed. Format 2021-05-30",
    )

    main(sys.argv[1:])
