#!/usr/bin/python
"""Create a smaller file of data by sampling."""
import sys
import logging
from billing import util


def main(argv):
    """Get sample records from command line."""
    path = argv[0]
    rate = float(argv[1])

    util.get_sample(path, rate)


if __name__ == "__main__":
    util.setup_logging()
    _LOGGER = logging.getLogger(__name__)
    _LOGGER.info("Starting script")

    main(sys.argv[1:])
