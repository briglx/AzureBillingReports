#!/usr/bin/python
"""Script to copy last two weeks of billing data."""

import os
from datetime import datetime, timezone
import argparse
import requests
import random
import string
from urllib.parse import urlparse, urlunparse
import subprocess
from script import get_usage_data
from script import upload_to_blob

# pylint: disable=C0103
# pylint: disable=W0621


def get_block_name(source):
    """Get block name version from source."""
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


def convert_blob(source):
    """Use azcopy to copy as block blob."""
    destination = get_block_name(source)

    # Escape characters
    if os.name == "nt":
        source = source.replace("&", "^&")
        destination = destination.replace("&", "^&")

    # Check if azcopy is installed
    args = ["azcopy", "--version"]
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, shell=False)
    (out, err) = proc.communicate()
    if "azcopy" not in out.decode("utf-8") or err:
        raise Exception("AZ copy not found on the system.")

    # copy as block
    args = ["azcopy", "copy", source, destination, "--blob-type", "BlockBlob"]
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, shell=False)
    (out, err) = proc.communicate()

    print(out.decode("utf-8"))
    if err:
        print(err.decode("utf-8"))


def notify_complete(job_id):
    """Notify trigger that job is complete."""
    print("Calling trigger to stop container")

    uri = "https://myfunctionbilling.azurewebsites.net/api/DockerHTTPTrigger" \
          "?code=sdYZl5NvaT/N1Lo3HRlLsBD5iig2CJE6IR2csvYi5A3PgjzCTpNNLw=="

    resp = requests.get(uri + "&job_id=" + job_id)

    print(resp.text)


def get_job_id():
    """Create random job id."""
    return ''.join(random.choice(string.hexdigits) for x in range(8))


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

    job_id = get_job_id()
    print(f"Starting job {job_id}")

    # Request Report for last two weeks
    uri = get_usage_data.get_last_two_weeks_uri(eid)
    report_url = get_usage_data.get_report_blob_uri(uri, auth_key)

    cur_time = datetime.utcnow()
    cur_time = cur_time.replace(tzinfo=timezone.utc, microsecond=0)

    target_filename = "usage-%s-twoweeks.csv" % (cur_time.isoformat())
    target_filename = target_filename.replace(":", "-")

    copied_file_url = upload_to_blob.copy_blob(
        report_url, target_filename, container_name, connection_string
    )

    # Convert from append to block blob
    convert_blob(copied_file_url)

    # Notify complete
    notify_complete(job_id)


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
