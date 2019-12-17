#!/usr/bin/python
"""Script to fetch pricing."""
import sys
from datetime import datetime, timezone
import json
import csv
import logging
import requests
from billing import util

HOST_NAME = "https://consumption.azure.com/v3/enrollments/%s"
API_PATH = "/pricesheet"


def get_uri(eid):
    r"""Return a consumption uri."""
    path_url = HOST_NAME + API_PATH
    uri = path_url % (eid)
    return uri


def get_pricelist(uri, auth_key):
    r"""Download pricelist."""
    _LOGGER.info("Calling uri %s", uri)

    headers = {
        "authorization": "bearer " + str(auth_key),
        "Content-Type": "application/json",
    }

    resp = requests.get(uri, headers=headers,)
    _LOGGER.info(resp)

    if resp.status_code == 200:

        price_list = json.loads(resp.content)

        dte = datetime.utcnow()
        dte = dte.replace(tzinfo=timezone.utc, microsecond=0)

        local_filename = "pricing-%s.csv" % (dte.isoformat())
        local_filename = local_filename.replace(":", "-")

        header = list(price_list[0].keys())

        with open(local_filename, "w", newline="") as price_sheet:
            writer = csv.writer(price_sheet, delimiter=",")

            writer.writerows([header])

            for meter_rate in price_list:

                row = [meter_rate.get(key) for key in header]
                writer.writerows([row])

    else:
        _LOGGER.error("Error calling uri")
        _LOGGER.error(resp.status_code)
        _LOGGER.error(resp.text)


def main(argv):
    r"""Get pricelist from command line."""
    eid = argv[0]
    auth_key = argv[1]

    uri = get_uri(eid)
    get_pricelist(uri, auth_key)


if __name__ == "__main__":
    util.setup_logging()
    _LOGGER = logging.getLogger(__name__)
    _LOGGER.info("Starting script")

    main(sys.argv[1:])
