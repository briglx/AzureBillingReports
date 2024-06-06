#!/usr/bin/python
"""Get the most recent file that should be used for processing or analysis from the daily exported folders."""
import argparse
import logging
import os

from dotenv import load_dotenv

from billing import util
from billing.blob_storage import copy_most_recent_files

load_dotenv()


def main(source, destination):
    """Get the most recent file."""
    _LOGGER.info(f"Copying most recent files from {source} to {destination}")

    _, file_count = copy_most_recent_files(source, destination)

    _LOGGER.info(f"Files copied: {file_count}")


if __name__ == "__main__":
    util.setup_logging()
    _LOGGER = logging.getLogger(__name__)
    _LOGGER.info("Starting Get Latest File script")

    parser = argparse.ArgumentParser(
        description="Get the most recent files.",
        add_help=True,
    )
    parser.add_argument(
        "--source",
        "-s",
        help="Path to source folder",
    )
    parser.add_argument(
        "--destination",
        "-d",
        help="Path to destination folder",
    )
    args = parser.parse_args()

    default_source = os.environ["EXPORT_URL"] + "?" + os.environ["EXPORT_SAS"]
    default_destination = (
        os.environ["EXPORT_LATEST_URL"] + "?" + os.environ["EXPORT_LATEST_SAS"]
    )
    SOURCE_CONTAINER = args.source or default_source
    DESTINATION_CONTAINER = args.destination or default_destination

    if not SOURCE_CONTAINER:
        raise ValueError(
            "source is required. Default values not found. Have you set the EXPORT_URL and EXPORT_URL env variable?"
        )

    if not DESTINATION_CONTAINER:
        raise ValueError(
            "destination is required. Default values not found. Have you set the EXPORT_LATEST_URL and EXPORT_LATEST_SAS env variable?"
        )

    main(SOURCE_CONTAINER, DESTINATION_CONTAINER)
