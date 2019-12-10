#!/usr/bin/python
"""Script to copy last two weeks of billing data."""

import os
from datetime import datetime, timezone
import argparse
from urllib.parse import urlparse, urlunparse
import subprocess
from script import get_usage_data
from script import upload_to_blob

# pylint: disable=C0103
# pylint: disable=W0621


def get_block_name(source):
    """Get block name version of source."""
    url_parts = urlparse(source)

    file_name = url_parts.path
    extension = file_name.split(".")[-1]

    new_path = file_name.replace("." + extension, "_block." + extension)

    new_file_name = urlunparse(
        (
            url_parts.scheme,
            url_parts.netloc,
            new_path,
            url_parts.params,
            url_parts.query,
            url_parts.fragment,
        )
    )

    return new_file_name


def copy_as_block(source, destination):
    """Use azcopy to copy as block blob."""
    # Escape characters
    source = source.replace("&", "^&")
    destination = destination.replace("&", "^&")

    # Check if azcopy is installed
    args = ["azcopy", "--version"]
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    if "azcopy" not in out.decode("utf-8") or err:
        raise Exception("AZ copy not found on the system.")

    # copy as block
    args = ["azcopy", "copy", source, destination, "--blob-type", "BlockBlob"]
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()

    print(out, err)


def main(eid, auth_key, container_name, connection_string):
    """Upload previous two weeks usage to blob storage."""
    # Validate Paramenters
    if not eid:
        raise ValueError("Parameter eid is required.")

    if not auth_key:
        raise ValueError("Parameter auth_key is required.")

    if not container_name:
        raise ValueError("Parameter name is required.")

    if not connection_string:
        raise ValueError("Parameter connection_string is required.")

    uri = get_usage_data.get_last_two_weeks_uri(eid)
    blob_url = get_usage_data.get_report_blob_uri(uri, auth_key)

    print("Fetching: " + blob_url)

    cur_time = datetime.utcnow()
    cur_time = cur_time.replace(tzinfo=timezone.utc, microsecond=0)

    local_filename = "usage-%s-twoweeks.csv" % (cur_time.isoformat())
    local_filename = local_filename.replace(":", "-")

    copied_blob = upload_to_blob.copy_blob(
        blob_url, local_filename, container_name, connection_string
    )

    # Change to block blob
    dest_file_name = get_block_name(copied_blob)
    copy_as_block(copied_blob, dest_file_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Upload billing usage to blob.", add_help=True,
    )
    parser.add_argument("--eid", "-e", help="Enrollment ID number")
    parser.add_argument("--auth_key", "-a", help="Billing Auth Key")
    parser.add_argument("--name", "-n", help="Destination Container Name")
    parser.add_argument(
        "--connection_string",
        "-s",
        help="Destination Storage Account Connection String",
    )

    args = parser.parse_args()

    # Use environment variables if arguments are not passed
    eid = args.eid or os.environ.get("ENROLLMENT_ID")
    auth_key = args.auth_key or os.environ.get("BILLING_AUTH_KEY")
    container_name = args.name or os.environ.get("STORAGE_CONTAINER_NAME")
    connection_string = args.connection_string or os.environ.get(
        "STORAGE_CONNECTION_STRING"
    )

    main(eid, auth_key, container_name, connection_string)
