"""Test the filter_data methods."""

from datetime import datetime
import os
import pathlib

from billing import util


def test_predicate_previous_date():
    """Test predicate with a previous date."""
    target_date = datetime(2021, 10, 1, 0, 0, 0)

    test_accept_row = [0, 1, 2, 3, 4, 5, 6, 7, 8, "2021-10-16"]
    test_same_row = [0, 1, 2, 3, 4, 5, 6, 7, 8, "2021-10-01"]
    test_drop_row = [0, 1, 2, 3, 4, 5, 6, 7, 8, "2021-09-01"]

    predicate = util.filter_greater_than_equal_date(target_date)

    assert predicate
    assert predicate(test_accept_row)
    assert predicate(test_same_row)
    assert not predicate(test_drop_row)


def test_filter_data():
    """Test filter data."""
    sample_file = "test_sample.csv"
    sample_path = pathlib.Path(__file__).parent.joinpath(sample_file)

    target_date = datetime(2021, 10, 17, 0, 0, 0)

    predicate = util.filter_greater_than_equal_date(target_date)

    util.filter_data(sample_path, predicate)

    # Generated file
    generated_file_name = pathlib.Path(str(sample_path) + "-filtered.csv")
    row_len = len(list(open(generated_file_name)))

    assert row_len == 3

    os.remove(generated_file_name)
