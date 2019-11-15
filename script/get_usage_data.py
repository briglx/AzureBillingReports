#!/usr/bin/python
"""Script to fetch latest monthly billing data and price sheet."""
import sys
import datetime
import time
import requests
from tqdm import tqdm as progress


STATUS_QUEUED = 1
STATUS_IN_PROGRESS = 2
STATUS_COMPLETED = 3
STATUS_FAILED = 4
STATUS_NO_DATA_FOUND = 5
STATUS_READY_TO_DOWNLOAD = 6
STATUS_TIMED_OUT = 7

HOST_NAME = "https://consumption.azure.com"
API_PATH = "/v3/enrollments/%s/usagedetails/submit?startTime=%s&endTime=%s"


def get_usage_uri(eid, start_date, end_date):
    """Build usage uri from eid and start and end dates."""
    path_url = HOST_NAME + API_PATH
    uri = path_url % (eid, start_date, end_date)
    return uri


def get_most_data_uri(eid):
    """Build usage uri from eid for the past three years."""
    dte = datetime.datetime.utcnow()
    start_date = (dte - datetime.timedelta(36 * 365 / 12)).strftime("%Y-%m-01")
    end_date = dte.strftime("%Y-%m-%d")
    return get_usage_uri(eid, start_date, end_date)


def get_last_two_weeks_uri(eid):
    """Build usage uri from eid for the last two weeks."""
    dte = datetime.datetime.utcnow()
    fdte = dte - datetime.timedelta(0.5 * 365 / 12)
    start_date = fdte.strftime("%Y-%m-%d")
    end_date = dte.strftime("%Y-%m-%d")
    return get_usage_uri(eid, start_date, end_date)


def get_current_month_uri(eid):
    """Build usage uri from eid for the current month."""
    dte = datetime.datetime.utcnow()
    start_date = dte.strftime("%Y-%m-01")
    end_date = dte.strftime("%Y-%m-%d")
    return get_usage_uri(eid, start_date, end_date)


def get_previous_30_days_uri(eid):
    """Build usage uri starting with the first of the previous month."""
    dte = datetime.datetime.utcnow()
    start_date = (dte - datetime.timedelta(1 * 365 / 12)).strftime("%Y-%m-01")
    end_date = dte.strftime("%Y-%m-%d")
    return get_usage_uri(eid, start_date, end_date)


def get_previous_6_months_uri(eid):
    """Build usage uri for the previous 6 months."""
    dte = datetime.datetime.utcnow()
    start_date = (dte - datetime.timedelta(6 * 365 / 12)).strftime("%Y-%m-01")
    end_date = dte.strftime("%Y-%m-%d")
    return get_usage_uri(eid, start_date, end_date)


def get_previous_12_months_uri(eid):
    """Build usage uri for the previous 12 months."""
    dte = datetime.datetime.utcnow()
    start_date = (dte - datetime.timedelta(12 * 365 / 12)).strftime("%Y-%m-01")
    end_date = dte.strftime("%Y-%m-%d")
    return get_usage_uri(eid, start_date, end_date)


def download_file(url, dte, ignore_header_rows=0):
    """Download usage report with shared access key based URL."""
    skipped_header = False
    size = 1024  # 1 Kibibyte

    local_filename = "usage-%s.csv" % (dte.isoformat())
    local_filename = local_filename.replace(":", "-")
    # NOTE the stream=True parameter
    resp = requests.get(url, stream=True)
    resp.encoding = "utf-8"
    total_size = int(resp.headers.get("content-length", 0))

    prog = progress(total=total_size, unit="iB", unit_scale=True)
    with open(local_filename, "wb") as csvfile:
        for chunk in resp.iter_content(chunk_size=size, decode_unicode=True):

            if ignore_header_rows and not skipped_header:
                bom = chunk[0]
                lines = chunk.split("\r\n")
                joined = bom + "".join(lines[ignore_header_rows:])

                encoded_chunk = joined.encode()

                skipped_header = True
            else:
                encoded_chunk = chunk.encode()

            if encoded_chunk:  # filter out keep-alive new chunks
                prog.update(len(encoded_chunk))
                csvfile.write(encoded_chunk)
                # f.flush() commented by recommendation from J.F.Sebastian
    prog.close()
    return (local_filename, total_size)


class NotOKError(requests.exceptions.BaseHTTPError):
    """Custom error for No OK http request status."""


def request_report(uri, auth_key, polling=False):
    """Initiate request for billing usage report."""
    print("Calling uri " + uri)

    headers = {
        "authorization": "bearer " + str(auth_key),
        "Content-Type": "application/json",
    }

    if polling:
        resp = requests.get(uri, headers=headers,)
    else:
        resp = requests.post(uri, headers=headers,)

    if resp.status_code == 200 or resp.status_code == 202:
        return resp

    err_string = "Error calling uri. " + resp.status_code + ": " + resp.text
    print(err_string)
    raise NotOKError(err_string)


def get_report_blob_uri(uri, auth_key):
    """Get the Report File location by polling for a request."""
    try:

        # Request billing report
        resp = request_report(uri, auth_key, polling=False)
        status = resp.json()["status"]
        report_url = resp.json()["reportUrl"]

        while True:

            # Start polling
            if status == STATUS_QUEUED:

                # Wait a few secs and check again
                print("Queued.")
                time.sleep(10)

            elif status == STATUS_IN_PROGRESS:

                # Wait a few secs and check again
                print("In Progress.")
                time.sleep(10)

            elif status == STATUS_COMPLETED:

                print("Completed.")
                blob_path = resp.json()["blobPath"]
                return blob_path

            elif status == STATUS_FAILED:

                print("Failed.")
                break

            elif status == STATUS_NO_DATA_FOUND:

                print("No Data Found.")
                break

            elif status == STATUS_READY_TO_DOWNLOAD:

                print("Ready to download.")
                blob_path = resp.json()["blobPath"]
                break

            elif status == STATUS_TIMED_OUT:

                print("Timed out.")
                break

            else:

                print("Unknown Status.")
                break

            resp = request_report(report_url, auth_key, polling=True)
            status = resp.json()["status"]

    except NotOKError as ex:
        print(ex)


def main(argv):
    """Get previous 30 days usage and latest pricing."""
    eid = argv[0]
    auth_key = argv[1]
    ignore_rows = 2

    uri = get_previous_30_days_uri(eid)
    blob_path = get_report_blob_uri(uri, auth_key)

    cur_time = datetime.datetime.utcnow()
    file_name, total_size = download_file(blob_path, cur_time, ignore_rows)

    return (file_name, total_size)


if __name__ == "__main__":
    main(sys.argv[1:])
