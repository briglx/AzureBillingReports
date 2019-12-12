"""Test the main helper methods."""
from script import main
from datetime import datetime, timezone
from tqdm import tqdm as progress


def test_get_new_name():
    """Test test_get_new_name."""

    BLOCK_NAME = "usage-2019-11-23T00-00-00.156611-twoweeks_block.csv"

    # testing
    t_host = "https://blxbillingstorage.blob.core.windows.net/billingfiles/"
    t_sas_key = "".join(
        (
            "?st=2019-12-09T17%3A25%3A10Z",
            "&se=2020-12-10T17%3A25%3A00Z",
            "&sp=racwdl&sv=2018-03-28",
            "&sr=c&sig=WBmZjsBVKmabcdedfDBX4wTN51Q3BzHWms%3D",
        )
    )
    t_file_name = "usage-2019-11-23T00-00-00.156611-twoweeks.csv"

    copied_blob = t_host + t_file_name + t_sas_key
    target_name = t_host + BLOCK_NAME + t_sas_key

    new_name = main.get_block_name(copied_blob)

    assert len(new_name) == len(copied_blob) + len("-block")
    assert new_name == target_name


def test_datetime_fix():
    """Test test_datetime_fix."""
    cur_time = datetime.utcnow()
    cur_time = cur_time.replace(tzinfo=timezone.utc, microsecond=0)
    cur_time.isoformat()

    assert cur_time


def test_progress():
    total_size = 100
    prog = progress(total=total_size, unit="iB", unit_scale=True)

    for i in range(100):
        prog.update(i)
