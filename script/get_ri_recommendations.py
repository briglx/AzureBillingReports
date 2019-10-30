#!/usr/bin/python

"""Script to fetch RI recommendations."""

import sys
import json
import csv

import requests

RI_TYPES = ["Shared", "Single"]
HOST_NAME = "https://consumption.azure.com/v2/enrollments/%s"
API_PATH = "/%sReservationRecommendations?lookBackPeriod=%s"


def get_uri(eid, ri_type, look_back_period):
    r"""Return a consumption uri."""
    path_url = HOST_NAME + API_PATH
    uri = path_url % (eid, ri_type, look_back_period)
    return uri


def get_last_week_uri(eid, ri_type):
    r"""Return a consumption uri for last week."""
    look_back_period = "7"
    return get_uri(eid, ri_type, look_back_period)


def get_last_30_days_uri(eid, ri_type):
    r"""Return a consumption uri for last 30 days."""
    look_back_period = "30"
    return get_uri(eid, ri_type, look_back_period)


def get_most_data_uri(eid, ri_type):
    r"""Return a consumption uri for last 60 days."""
    look_back_period = "60"
    return get_uri(eid, ri_type, look_back_period)


def get_recommendations(uri, auth_key, ri_type):
    r"""Download recommendations.."""
    print("Calling uri " + uri)

    headers = {
        "authorization": "bearer " + str(auth_key),
        "Content-Type": "application/json",
    }

    resp = requests.get(uri, headers=headers,)
    print(resp)

    recommendations = json.loads(resp.content)

    header = list(recommendations[0].keys())[1:-1]

    file_name = "ri_" + ri_type.lower() + "_recommendations.csv"
    with open(file_name, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")

        writer.writerows([header])

        for recommend in recommendations:

            row = [recommend.get(key) for key in header]
            writer.writerows([row])


def main(argv):
    r"""Get recommendations from command line."""
    eid = argv[0]
    auth_key = argv[1]

    for ri_type in RI_TYPES:
        uri = get_most_data_uri(eid, ri_type)
        get_recommendations(uri, auth_key, ri_type)


if __name__ == "__main__":
    main(sys.argv[1:])
