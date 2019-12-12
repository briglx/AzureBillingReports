"""Test the get_usage_data methods."""
from datetime import datetime
from unittest.mock import Mock, patch
from script import get_usage_data

HOST_NAME = "https://consumption.azure.com"
API_PATH = "/v3/enrollments/%s/usagedetails/submit?startTime=%s&endTime=%s"


def test_get_usage_uri():
    eid = 123
    previous_months = 1
    rolling = True
    dte = datetime(1900, 1, 2, 3, 4, 5)

    expected_path = HOST_NAME + API_PATH
    expected_uri = expected_path % (eid, "1899-12-02", "1900-01-02")

    uri = get_usage_data.get_usage_uri(eid, previous_months, rolling, dte)

    assert uri == expected_uri


def test_get_last_two_weeks_uri():
    eid = 123

    expected_path = HOST_NAME + API_PATH
    expected_uri = expected_path % (eid, "1899-12-30", "1900-01-15")

    test_date = datetime(1900, 1, 15, 3, 4, 5)
    with patch("script.get_usage_data.datetime") as dte:
        dte.utcnow = Mock(return_value=test_date)
        uri = get_usage_data.get_last_two_weeks_uri(eid)

        assert uri == expected_uri


def test_get_previous_30_days_uri():
    eid = 123

    expected_path = HOST_NAME + API_PATH
    expected_uri = expected_path % (eid, "1899-12-15", "1900-01-15")

    test_date = datetime(1900, 1, 15, 3, 4, 5)
    with patch("script.get_usage_data.datetime") as dte:
        dte.utcnow = Mock(return_value=test_date)
        uri = get_usage_data.get_previous_30_days_uri(eid)

        assert uri == expected_uri
