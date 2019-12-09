#!/usr/bin/python
"""Script to copy last two weeks of billing data."""

import os
import datetime
import argparse
import get_usage_data
import upload_to_blob

# pylint: disable=C0103
# pylint: disable=W0621


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

    cur_time = datetime.datetime.utcnow()
    local_filename = "usage-%s-twoweeks.csv" % (cur_time.isoformat())
    local_filename = local_filename.replace(":", "-")

    upload_to_blob.copy_blob(
        blob_url, local_filename, container_name, connection_string
    )


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
