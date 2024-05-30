#!/usr/bin/python
"""Script to upload billing data to blob storage."""
import argparse
import logging
import os
from urllib.parse import urlparse

from billing import blob_storage, util

# pylint: disable=C0103
# pylint: disable=W0621


def main(file_name, container_name, connection_string):
    """Upload file to Azure blob."""
    if file_name is None:
        raise TypeError("Parameter file_name can not be empty.")
    if container_name is None:
        raise TypeError("Parameter container_name can not be empty.")
    if connection_string is None:
        raise TypeError("Parameter connection_string can not be empty.")

    # blob_storage.upload_file(file_name, container_name, connection_string)

    # Test when file_name is remote blob url
    url_parts = urlparse(file_name)
    _name = os.path.basename(url_parts.path)

    dest_file_name = _name.replace(".csv", "_block.csv")
    blob_storage.copy_blob(file_name, dest_file_name, container_name, connection_string)


if __name__ == "__main__":
    util.setup_logging()
    _LOGGER = logging.getLogger(__name__)
    _LOGGER.info("Starting script")

    parser = argparse.ArgumentParser(
        description="Upload billing usage to blob.",
        add_help=True,
    )
    parser.add_argument("--file_name", "-f", help="File name to copy")
    parser.add_argument("--container_name", "-c", help="Name of Destination Container")
    parser.add_argument("--connection_string", "-s, help=Connection string")
    args = parser.parse_args()

    # Use environment variables if arguments are not passed
    file_name = args.file_name
    container_name = args.container_name or os.environ.get("STORAGE_CONTAINER_NAME")
    connection_string = args.connection_string or os.environ.get(
        "STORAGE_CONNECTION_STRING"
    )

    main(file_name, container_name, connection_string)
