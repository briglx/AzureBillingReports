#!/usr/bin/python
"""Script to convert blob type."""
import argparse
import logging
import os

from billing import blob_storage, util

# pylint: disable=C0103


if __name__ == "__main__":
    util.setup_logging()
    _LOGGER = logging.getLogger(__name__)
    _LOGGER.info("Starting script")

    parser = argparse.ArgumentParser(
        description="Convert azure blob type.",
        add_help=True,
    )
    parser.add_argument("--blob_url", "-f", help="Url of file to convert")
    parser.add_argument("--sas_key", "-s", help="Sas key")
    args = parser.parse_args()

    # parse arguments
    blob_url = args.blob_url

    # Use environment variables if arguments are not passed
    sas_key = args.sas_key or os.environ.get("BILLING_STORAGE_SAS_KEY")

    if not blob_url:
        raise ValueError("Parameter blob_url is required.")
    if not sas_key:
        raise ValueError("Parameter sas_key is required.")

    dest_url = blob_storage.get_block_name(blob_url + sas_key)

    blob_storage.copy_blob_as_azcopy(blob_url + sas_key, dest_url)
