"""Script to fetch latest monthly billing data and price sheet."""
import logging
import time
from datetime import datetime, timedelta

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

_LOGGER = logging.getLogger(__name__)


def get_utc_now():
    """Get current utc time."""
    return datetime.utcnow()


def get_usage_uri(eid, previous_months, rolling=True, dte=None):
    """Build usage uri from eid for the given months."""
    # validate previous_months
    if previous_months < 0:
        raise TypeError("Parameter previous_months must be positive.")

    if rolling:
        start_format = "%Y-%m-%d"
    else:
        start_format = "%Y-%m-01"

    if dte is None:
        dte = get_utc_now()

    dte = dte.replace(microsecond=0)
    # dte = dte.replace(tzinfo=timezone.utc, microsecond=0)

    delta = timedelta(previous_months * 365 / 12)
    start_date = (dte - delta).strftime(start_format)
    end_date = dte.strftime("%Y-%m-%d")

    path_url = HOST_NAME + API_PATH
    uri = path_url % (eid, start_date, end_date)

    return uri


def get_most_data_uri(eid):
    """Build usage uri from eid for the past three years."""
    return get_usage_uri(eid, 36, False)


def get_last_two_weeks_uri(eid):
    """Build usage uri from eid for the last two weeks."""
    return get_usage_uri(eid, 0.5)


def get_current_month_uri(eid):
    """Build usage uri from eid for the current month."""
    return get_usage_uri(eid, 1, False)


def get_previous_30_days_uri(eid):
    """Build usage uri starting with the first of the previous month."""
    return get_usage_uri(eid, 1)


def get_previous_6_months_uri(eid):
    """Build usage uri for the previous 6 months."""
    return get_usage_uri(eid, 6, False)


def get_previous_12_months_uri(eid):
    """Build usage uri for the previous 12 months."""
    return get_usage_uri(eid, 12, False)


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
                joined = bom + "\r\n".join(lines[ignore_header_rows:])

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
    _LOGGER.info("Calling uri %s", uri)

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

    err_string = "Error calling uri. {} {}".format(resp.status_code, resp.text)
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
                _LOGGER.info("Queued.")
                time.sleep(10)

            elif status == STATUS_IN_PROGRESS:

                # Wait a few secs and check again
                _LOGGER.info("In Progress.")
                time.sleep(10)

            elif status == STATUS_COMPLETED:

                _LOGGER.info("Completed.")
                blob_path = resp.json()["blobPath"]
                return blob_path

            elif status == STATUS_FAILED:

                _LOGGER.error("Failed.")
                break

            elif status == STATUS_NO_DATA_FOUND:

                _LOGGER.warning("No Data Found.")
                break

            elif status == STATUS_READY_TO_DOWNLOAD:

                _LOGGER.info("Ready to download.")
                blob_path = resp.json()["blobPath"]
                break

            elif status == STATUS_TIMED_OUT:

                _LOGGER.warning("Timed out.")
                break

            else:

                _LOGGER.warning("Unknown Status.")
                break

            resp = request_report(report_url, auth_key, polling=True)
            status = resp.json()["status"]

    except NotOKError as ex:
        _LOGGER.error(ex)
        raise ex
