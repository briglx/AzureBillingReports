#!/usr/bin/python
"""Script to convert blob type."""
import os
import argparse
from script import main

# pylint: disable=C0103


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert azure blob type.", add_help=True,
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

    new_name = main.get_block_name(blob_url + sas_key)
    main.convert_blob(blob_url + sas_key, new_name)
