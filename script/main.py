#!/usr/bin/python
"""Script to copy last two weeks of billing data."""

import sys
import os
import datetime
import get_usage_data
import upload_to_blob


def main(argv):
    """Upload previous two weeks usage to blob storage."""
    eid = argv[0] or os.environ.get("ENROLLMENT_ID")
    auth_key = argv[1] or os.environ.get("BILLING_AUTH_KEY")
    container_name = argv[2] or os.environ.get("STORAGE_CONTAINER_NAME")
    connection_string = argv[3] or os.environ.get("STORAGE_CONNECTION_STRING")

    argv = [eid, auth_key]

    uri = get_usage_data.get_last_two_weeks_uri(eid)
    blob_url = get_usage_data.get_report_blob_uri(uri, auth_key)

    cur_time = datetime.datetime.utcnow()
    local_filename = "usage-%s-twoweeks.csv" % (cur_time.isoformat())
    local_filename = local_filename.replace(":", "-")

    upload_to_blob.copy_blob(
        blob_url, local_filename, container_name, connection_string
    )


if __name__ == "__main__":
    main(sys.argv[1:])
