#!/usr/bin/python

import sys
import requests
import datetime
import time

HOST_NAME = 'https://consumption.azure.com'
API_PATH = '/v3/enrollments/%s/usagedetails/submit?startTime=%s&endTime=%s'


def getUri(eid, startDate, endDate):
    path_url = HOST_NAME + API_PATH
    uri = (path_url % (eid, startDate, endDate))
    return uri


def getMostDataUri(eid):
    dte = datetime.datetime.now()
    startDate = (dte - datetime.timedelta(36 * 365 / 12)).strftime("%Y-%m-01")
    endDate = dte.strftime("%Y-%m-%d")
    return getUri(eid, startDate, endDate)


def getCurrentMonthUri(eid):
    dte = datetime.datetime.now()
    startDate = dte.strftime("%Y-%m-01")
    endDate = dte.strftime("%Y-%m-%d")
    return getUri(eid, startDate, endDate)


def getLast30DaysUri(eid):
    dte = datetime.datetime.now()
    startDate = (dte - datetime.timedelta(1 * 365 / 12)).strftime("%Y-%m-01")
    endDate = dte.strftime("%Y-%m-%d")
    return getUri(eid, startDate, endDate)


def getLast12MonthsUri(eid):
    dte = datetime.datetime.now()
    startDate = (dte - datetime.timedelta(12 * 365 / 12)).strftime("%Y-%m-01")
    endDate = dte.strftime("%Y-%m-%d")
    return getUri(eid, startDate, endDate)


def getStatus(uri, auth_key, count, isReportUrl=False):

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
            getStatus(reportUrl, auth_key, count + 1, True)

        elif status == STATUS_IN_PROGRESS:

            print("In Progress.")
            print(reportUrl)

            # Wait a few secs and check again
            time.sleep(10)
            getStatus(reportUrl, auth_key, count + 1, True)

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


def download_file(url, dte):
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


def main(argv):

    eid = argv[0]
    auth_key = argv[1]

    uri = getLast30DaysUri(eid)
    getStatus(uri, auth_key, 0)


if __name__ == "__main__":
    main(sys.argv[1:])
