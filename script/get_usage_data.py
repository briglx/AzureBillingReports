#!/usr/bin/python
"Script to fetch latest monthly billing data and price sheet"
import sys
import requests
import datetime
import time
import csv

HOST_NAME = 'https://consumption.azure.com'
API_PATH = '/v3/enrollments/%s/usagedetails/submit?startTime=%s&endTime=%s'
PRICING_PATH = '/v2/enrollments/%s/pricesheet'


def get_usage_uri(eid, startDate, endDate):
    """Build usage uri from eid and start and end dates."""
    path_url = HOST_NAME + API_PATH
    uri = (path_url % (eid, startDate, endDate))
    return uri


def get_pricing_uri(eid):
    """Build pricing uri for this eid."""
    path_url = HOST_NAME + PRICING_PATH
    uri = (path_url % (eid))
    return uri


def get_most_data_uri(eid):
    """Build usage uri from eid for the past three years."""
    dte = datetime.datetime.now()
    startDate = (dte - datetime.timedelta(36 * 365 / 12)).strftime("%Y-%m-01")
    endDate = dte.strftime("%Y-%m-%d")
    return get_usage_uri(eid, startDate, endDate)


def get_current_month_uri(eid):
    """Build usage uri from eid for the current month."""
    dte = datetime.datetime.now()
    startDate = dte.strftime("%Y-%m-01")
    endDate = dte.strftime("%Y-%m-%d")
    return get_usage_uri(eid, startDate, endDate)


def get_previous_30_days_uri(eid):
    """Build usage uri starting with the first of the previous month."""
    dte = datetime.datetime.now()
    startDate = (dte - datetime.timedelta(1 * 365 / 12)).strftime("%Y-%m-01")
    endDate = dte.strftime("%Y-%m-%d")
    return get_usage_uri(eid, startDate, endDate)


def get_previous_12_months_uri(eid):
    """Build usage uri for the previous 12 months."""
    dte = datetime.datetime.now()
    startDate = (dte - datetime.timedelta(12 * 365 / 12)).strftime("%Y-%m-01")
    endDate = dte.strftime("%Y-%m-%d")
    return get_usage_uri(eid, startDate, endDate)


def download_file(url, dte):
    """Download usage report with shared access key based URL."""
    local_filename = "usage-%s.csv" % (dte.isoformat())
    local_filename = local_filename.replace(":", "-")
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                # f.flush() commented by recommendation from J.F.Sebastian
    return local_filename


def get_status(uri, auth_key, count, isReportUrl=False):
    """Submit request and poll for shared access key based URL."""
    STATUS_QUEUED = 1
    STATUS_IN_PROGRESS = 2
    STATUS_COMPLETED = 3
    STATUS_FAILED = 4
    STATUS_NO_DATA_FOUND = 5
    STATUS_READY_TO_DOWNLOAD = 6
    STATUS_TIMED_OUT = 7

    print("[" + str(count) + "] Calling uri " + uri)

    headers = {
        "authorization": "bearer " + str(auth_key),
        "Content-Type": "application/json"}

    if isReportUrl:
        resp = requests.get(
            uri,
            headers=headers,
        )
    else:
        resp = requests.post(
            uri,
            headers=headers,
        )

    if resp.status_code == 200 or resp.status_code == 202:

        status = resp.json()["status"]
        reportUrl = resp.json()["reportUrl"]

        if status == STATUS_QUEUED:

            print("Queued.")
            print(reportUrl)

            # Wait a few secs and check again
            time.sleep(10)
            get_status(reportUrl, auth_key, count + 1, True)

        elif status == STATUS_IN_PROGRESS:

            print("In Progress.")
            print(reportUrl)

            # Wait a few secs and check again
            time.sleep(10)
            get_status(reportUrl, auth_key, count + 1, True)

        elif status == STATUS_COMPLETED:

            print("Completed.")
            blobPath = resp.json()["blobPath"]
            print(blobPath)

            print("download blob")
            download_file(blobPath, datetime.datetime.now())

        elif status == STATUS_FAILED:

            print("Failed.")

        elif status == STATUS_NO_DATA_FOUND:

            print("No Data Found.")

        elif status == STATUS_READY_TO_DOWNLOAD:

            print("Ready to download.")
            blobPath = resp.json()["blobPath"]
            print(blobPath)

            # Download Blob
            print("download blob")
            download_file(blobPath, datetime.datetime.now())

        elif status == STATUS_TIMED_OUT:

            print("Timed out.")

        else:

            print("Unknown Status.")
    else:
        print("Error calling uri")
        print(resp.status_code)
        print(resp.text)


def get_price_sheet(uri, auth_key):
    """Get latest price sheet."""
    print("Calling uri " + uri)

    headers = {
        "authorization": "bearer " + str(auth_key),
        "Content-Type": "application/json"}

    resp = requests.get(uri, headers=headers,)

    if resp.status_code == 200:

        resp_body = resp.json()

        dte = datetime.datetime.now()
        local_filename = "pricing-%s.csv" % (dte.isoformat())
        local_filename = local_filename.replace(":", "-")

        with open(local_filename, 'w', newline='') as f:
            csvwriter = csv.writer(f)

            count = 0

            for row in resp_body:

                if count == 0:
                    header = row.keys()
                    csvwriter.writerow(header)
                    count += 1
                csvwriter.writerow(row.values())
    else:
        print("Error calling uri")
        print(resp.status_code)
        print(resp.text)


def main(argv):
    """Get previous 30 days usage and latest pricing."""
    eid = argv[0]
    auth_key = argv[1]

    uri = get_most_data_uri(eid)
    get_status(uri, auth_key, 0)

    uri = get_pricing_uri(eid)
    get_price_sheet(uri, auth_key)


if __name__ == "__main__":
    main(sys.argv[1:])
