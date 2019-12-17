#!/usr/bin/python
"""Script to copy last two weeks of billing data."""
import os
from datetime import datetime
import argparse
import logging
from billing import usage_data, util, blob_storage

# pylint: disable=C0103
# pylint: disable=W0621


def main(eid, auth_key, container_name, connection_string):
    """Upload previous two weeks usage to blob storage."""
    try:
        # config_logger()

        # Validate Paramenters
        if not eid:
            raise ValueError("Parameter eid is required.")

        if not auth_key:
            raise ValueError("Parameter auth_key is required.")

        if not container_name:
            raise ValueError("Parameter name is required.")

        if not connection_string:
            raise ValueError("Parameter connection_string is required.")

        job_id = util.get_job_id()
        _LOGGER.info("Starting job %s", job_id)

        # Request Report for last two weeks
        uri = usage_data.get_last_two_weeks_uri(eid)
        report_url = usage_data.get_report_blob_uri(uri, auth_key)

        cur_time = datetime.utcnow()
        cur_time = cur_time.replace(microsecond=0)
        # cur_time = cur_time.replace(tzinfo=timezone.utc, microsecond=0)

        target_filename = "usage-%s-twoweeks.csv" % (cur_time.isoformat())
        target_filename = target_filename.replace(":", "-")

        copied_file_url = blob_storage.copy_blob(
            report_url, target_filename, container_name, connection_string
        )

        # Convert from append to block blob
        blob_storage.convert_blob(copied_file_url)

        # Notify complete
        util.notify_complete(job_id)

    except ValueError as ve:
        _LOGGER.warning(ve)


if __name__ == "__main__":
    util.setup_logging()
    _LOGGER = logging.getLogger(__name__)
    _LOGGER.info("Starting script")

    parser = argparse.ArgumentParser(
        description="Get latest billing usage to block blob.", add_help=True,
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
