#!/usr/bin/python
"""Generate sample blob inventory data."""
import csv
import random
import uuid
from datetime import datetime, timezone


def generate_guid():
    """Generate a UUID string."""
    return str(uuid.uuid4())


def get_random_date(start_date, end_date, prop):
    """Get a time at a proportion of a range of two dates."""
    return start_date + prop * (end_date - start_date)


def get_date_isoformat(date):
    """Format Iso Formatted Date."""
    cur_time = date.replace(tzinfo=timezone.utc, microsecond=0)
    return cur_time.isoformat().replace("+00:00", "Z")


def get_date_now_isoformat():
    """Generate Iso Formatted Date based on Now."""
    cur_time = datetime.utcnow()
    return get_date_isoformat(cur_time)


def generate_filename(storage_account="test_storage", container_name="sample_container"):
    """Generate a random filename."""
    extentions = ["csv", "csv", "csv", "csv", "csv", "csv", "csv", "txt", "log"]

    file_id = generate_guid()

    extension = random.choice(extentions)

    return f"{storage_account}/{container_name}/file{file_id}.{extension}"


def create_sample_row():
    """Generate sample row of data."""

    storage_accounts = [
        "dev_storage",
        "dev_project1",
        "dev_project2",
        "dev_project3",
        "prod_project1",
        "prod_project2",
        "prod_project3",
    ]
    blob_types = [
        "BlockBlob",
        "BlockBlob",
        "BlockBlob",
        "BlockBlob",
        "BlockBlob",
        "BlockBlob",
        "BlockBlob",
        "BlockBlob",
        "BlockBlob",
        "BlockBlob",
        "BlockBlob",
        "BlockBlob",
        "BlockBlob",
        "BlockBlob",
        "BlockBlob",
        "BlockBlob",
        "PageBlob",
        "AppendBlob",
    ]
    storage_tiers = ["Hot", "Cool", "Archive"]

    utc_now = datetime.utcnow()

    min_date = datetime.fromisoformat("2017-09-20T13:56:36")

    storage_account = random.choice(storage_accounts)
    create_date = get_random_date(min_date, utc_now, random.random())

    file_bucket_size = 2 ** int(random.uniform(0, 32))

    sample_data = (
        generate_filename(storage_account),
        get_date_isoformat(create_date),
        random.choice(blob_types),
        int(random.uniform(0, file_bucket_size)),
        get_date_isoformat(get_random_date(create_date, utc_now, random.random())),
        get_date_isoformat(get_random_date(create_date, utc_now, random.random())),
        random.choice(storage_tiers),
    )

    return sample_data


def main():
    """Generate the sample file."""
    file_name = "blob-inventory.csv"
    with open(file_name, "w", newline="") as sample_file:
        writer = csv.writer(sample_file)

        header = (
            "Name",
            "Creation-Time",
            "BlobType",
            "Content-Length",
            "LastAccessTime",
            "Last-Modified",
            "AccessTier",
        )

        writer.writerow(header)
        for _ in range(10000):
            sample_row = create_sample_row()

            writer.writerow(sample_row)


if __name__ == "__main__":
    main()
