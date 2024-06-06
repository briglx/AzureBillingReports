#!/usr/bin/python
"""Split csv files into parts of 100MB-1GB. Running the split will also get `stats` for each file. This includes the total number of rows and the total cost for the file. This is helpful for validating data."""
import argparse
import asyncio
import logging
import os

from dotenv import load_dotenv

from billing import util
from billing.blob_storage import get_blob_service_client_from_url, split_file_and_upload

load_dotenv()
# DEFAULT_CHUNK_SIZE = 500000


def skip_file(file_name, skip_paths):
    """Check if file should be skipped."""
    for skip_path in skip_paths:
        if skip_path in file_name:
            return True
    return False


async def main(source: str, destination: str, skip_paths: list[str] = []):
    """Split csv file."""
    _LOGGER.info("Splitting csv files for %s, to %s", source, destination)

    source_blob_service_client, source_container, source_prefix = (
        get_blob_service_client_from_url(source)
    )
    destination_blob_service_client, destination_container, destination_prefix = (
        get_blob_service_client_from_url(destination)
    )
    destination_container_client = destination_blob_service_client.get_container_client(
        destination_container
    )

    container_client = source_blob_service_client.get_container_client(source_container)
    blobs = container_client.list_blobs(name_starts_with=source_prefix)

    # tasks = []
    blob_count = 0
    try:
        async for blob in blobs:
            blob_client = source_blob_service_client.get_blob_client(
                source_container, blob
            )
            if skip_file(blob.name, skip_paths):
                _LOGGER.info("Skipping %s", blob.name)
                continue

            await split_file_and_upload(blob_client, blob, destination_container_client)
            blob_count += 1

        _LOGGER.info("Split %s blobs", blob_count)
        # await asyncio.gather(*tasks)

    except Exception as e:
        _LOGGER.error("Error splitting files: %s", e)


if __name__ == "__main__":
    util.setup_logging()
    _LOGGER = logging.getLogger(__name__)
    _LOGGER.info("Starting Split CSV Files script")

    parser = argparse.ArgumentParser(
        description="Split csv files.",
        add_help=True,
    )
    parser.add_argument(
        "--source",
        "-s",
        help="Path to source folder",
    )
    parser.add_argument(
        "--destination",
        "-d",
        help="Path to destination folder",
    )
    parser.add_argument(
        "--skip_paths",
        "-sp",
        help="Paths to skip",
    )
    args = parser.parse_args()

    default_source = (
        os.environ["EXPORT_LATEST_URL"] + "?" + os.environ["EXPORT_LATEST_SAS"]
    )
    default_destination = (
        os.environ["EXPORT_LATEST_PARTS_URL"]
        + "?"
        + os.environ["EXPORT_LATEST_PARTS_SAS"]
    )
    SOURCE_CONTAINER = args.source or default_source
    DESTINATION_CONTAINER = args.destination or default_destination
    SKIP_PATHS = args.skip_paths or os.environ["SKIP_PATHS"]

    if not SOURCE_CONTAINER:
        raise ValueError(
            "source is required. Default values not found. Have you set the EXPORT_LATEST_URL and EXPORT_LATEST_SAS env variable?"
        )

    if not DESTINATION_CONTAINER:
        raise ValueError(
            "destination is required. Default values not found. Have you set the EXPORT_LATEST_PARTS_URL and EXPORT_LATEST_SAS env variable?"
        )

    if SKIP_PATHS and len(SKIP_PATHS) > 0:
        SKIP_PATHS = SKIP_PATHS.split(",")

    asyncio.run(main(SOURCE_CONTAINER, DESTINATION_CONTAINER, SKIP_PATHS))
