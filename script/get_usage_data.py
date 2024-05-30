#!/usr/bin/python
"""Script to fetch latest billing usage data."""
import argparse
from datetime import datetime, timezone
import logging
import os

from billing import usage_data, util

# pylint: disable=C0103
# pylint: disable=W0621


def main(eid, auth_key, ignore_rows):
    """Download previous 30 days usage and latest pricing."""
    uri = usage_data.get_previous_6_months_uri(eid)
    blob_path = usage_data.get_report_blob_uri(uri, auth_key)

    cur_time = datetime.utcnow()
    cur_time = cur_time.replace(tzinfo=timezone.utc, microsecond=0)

    file_name, file_size = usage_data.download_file(blob_path, cur_time, ignore_rows)

    return (file_name, file_size)


if __name__ == "__main__":
    util.setup_logging()
    _LOGGER = logging.getLogger(__name__)
    _LOGGER.info("Starting script")

    parser = argparse.ArgumentParser(
        description="Get billing data report.",
        add_help=True,
    )
    parser.add_argument("--eid", "-e", help="Enrollment ID number")
    parser.add_argument("--auth_key", "-a", help="Billing Auth Key")
    parser.add_argument("--ignore_rows", "-i", help="Number of rows to skip")
    args = parser.parse_args()

    # Use environment variables if arguments are not passed
    eid = args.eid or os.environ.get("ENROLLMENT_ID")
    auth_key = args.auth_key or os.environ.get("BILLING_AUTH_KEY")
    ignore_rows = args.ignore_rows or os.environ.get("BILLING_IGNORE_ROWS", 2)

    file_name, total_size = main(eid, auth_key, ignore_rows)
    _LOGGER.info("Downloaded: %s; total size: %s.", file_name, total_size)
