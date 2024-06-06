"""Module to manage billing data with blob storage."""

import asyncio
import csv
from datetime import datetime, timedelta
from decimal import Decimal
from io import StringIO
import logging
import os
import subprocess
import time
from urllib.parse import urlparse, urlunparse

from azure.storage.blob import (
    AccountSasPermissions,
    BlobBlock,
    ResourceTypes,
    generate_account_sas,
)
from azure.storage.blob.aio import BlobClient, BlobServiceClient, ContainerClient
import requests
from tqdm import tqdm as progress

_LOGGER = logging.getLogger(__name__)


DEFAULT_CHUNK_SIZE = (1024**2) * 250  # 250MB


def get_blob_service_client_from_url(url_with_sas):
    """Get a blob client from a URL with a SAS token."""
    prefix = ""
    url_parts = urlparse(url_with_sas)
    sas_token = url_parts.query
    account_url = f"https://{url_parts.hostname}"
    parts = url_parts.path.split("/")
    container_name = parts[1]
    if len(parts) > 2:
        prefix = "/".join(parts[2:])

    # return (account_url, sas_token, container_name, prefix)
    return (
        BlobServiceClient(account_url=account_url, credential=sas_token),
        container_name,
        prefix,
    )


def get_most_recent_files(blob_service_client: BlobServiceClient, prefix):
    """Get the most recent file for each subfolder for a given prefix pattern in a container."""
    _LOGGER.info("Getting most recent files for %s", prefix)
    subfolder_details = {}
    file_details = []

    # List all blobs in the container with the given prefix
    blobs = blob_service_client.list_blobs(name_starts_with=prefix)

    for blob in blobs:
        blob_name = blob.name
        subfolders = blob_name.split("/")

        # Ignore the last element (the actual file name)
        subfolder_path = "/".join(subfolders[:-1])

        blob_client = blob_service_client.get_blob_client(blob=blob)
        blob_properties = blob_client.get_blob_properties()
        blob_size = blob_properties.size
        last_modified = blob_properties.last_modified

        if (
            subfolder_path not in subfolder_details
            or last_modified > subfolder_details[subfolder_path][-1]
        ):
            subfolder_details[subfolder_path] = (
                blob_client.url,
                blob_name,
                blob_size,
                last_modified,
            )

    for _, details in subfolder_details.items():
        _LOGGER.info(
            "url: %s, name: %s, size: %d, last_modified: %s",
            details[0],
            details[1],
            details[2],
            details[3],
        )
        file_details.append((details[0], details[1], details[2]))

    return file_details


def get_most_recent_files_by_connection_string(
    connection_string, container_name, prefix
):
    """Get the most recent file for a given prefix."""
    subfolder_details = {}
    file_details = []

    # Get blobs that match prefix
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blobs = blob_service_client.get_container_client(container_name).list_blobs(
        name_starts_with=prefix
    )

    for blob in blobs:
        # Get the blob name (including subfolder structure)
        blob_name = blob.name

        if "csv" in blob_name:

            # Split the blob name by slashes to get subfolder names
            subfolders = blob_name.split("/")

            # Ignore the last element (the actual file name)
            subfolder_path = "/".join(subfolders[:-1])

            # Get the blob size
            blob_client = blob_service_client.get_blob_client(
                container=container_name, blob=blob
            )
            properties = blob_client.get_blob_properties()
            blob_size = properties.size
            last_modified = properties.last_modified

            if (
                subfolder_path not in subfolder_details
                or last_modified > subfolder_details[subfolder_path][0]
            ):
                subfolder_details[subfolder_path] = (
                    last_modified,
                    blob_name,
                    blob_size,
                    blob_client.url,
                )

    for _, details in subfolder_details.items():
        file_details.append((details[1], details[2], details[3]))

    return file_details


def copy_most_recent_files(source, destination):
    """Get the most recent files for a given source and copy to the destination."""
    file_count = 0
    source_blob_service_client, source_container, source_prefix = (
        get_blob_service_client_from_url(source)
    )
    destination_blob_service_client, destination_container, destination_prefix = (
        get_blob_service_client_from_url(destination)
    )

    latest_files = get_most_recent_files(
        source_blob_service_client.get_container_client(source_container), source_prefix
    )

    for blob_url, blob_name, blob_size in latest_files:
        destination_blob_client = destination_blob_service_client.get_blob_client(
            container=destination_container, blob=blob_name
        )
        # Copy the blob to the destination
        copy_status = destination_blob_client.start_copy_from_url(blob_url)
        _LOGGER.info(
            "Copying %s, %s, %d to %s, %s",
            blob_name,
            blob_url,
            blob_size,
            destination,
            copy_status,
        )
        file_count = file_count + 1

    return latest_files, file_count


def get_account_info(connection_string):
    """Get Account info from a connection string."""
    account_name = connection_string.split(";")[1].split("=")[-1]
    account_key = connection_string.split(";")[2].replace("AccountKey=", "")

    return (account_name, account_key)


def generate_sas_key(connection_string):
    """Generate SAS key from connection string info."""
    account_name, account_key = get_account_info(connection_string)
    sas_token = generate_account_sas(
        account_name=account_name,
        account_key=account_key,
        resource_types=ResourceTypes(container=True, object=True),
        permission=AccountSasPermissions(read=True, write=True),
        expiry=datetime.utcnow() + timedelta(hours=1),
    )

    return sas_token


def copy_blob(blob_url, dest_file_name, container_name, connection_string):
    """Copy remote blob file to destination container."""
    # Validate Parameters
    if not blob_url:
        raise ValueError("Parameter blob_url is required.")

    if not dest_file_name:
        raise ValueError("Parameter dest_file_name is required.")

    if not container_name:
        raise ValueError("Parameter container_name is required.")

    if not connection_string:
        raise ValueError("Parameter connection_string is required.")

    _LOGGER.info("Copying Report %s", blob_url)

    try:

        # Create Destination Blob
        client = BlobServiceClient.from_connection_string(connection_string)
        copied_blob = client.get_blob_client(container_name, dest_file_name)

        # Generate Sas Key for writing
        sas_token = generate_sas_key(connection_string)
        dest_url = copied_blob.url + "?" + sas_token

        # Choose from different copy implementations
        # copy_blob_as_remote(blob_url, copied_blob)
        # copy_blob_as_github_suggested(blob_url, copied_blob)
        # copy_blob_as_blocks(blob_url, copied_blob)
        copy_blob_as_azcopy(blob_url, dest_url)

        return dest_url

    except Exception as ex:
        _LOGGER.error("Failed to copy Report.", exc_info=True)
        raise ex


def copy_blob_as_remote(blob_url, copied_blob):
    """Copy blob as append file."""
    # Copies as Append file
    count = 0

    # Get file size
    resp = requests.get(blob_url, stream=True)
    total_size = int(resp.headers.get("content-length", 0))
    prog = progress(total=total_size, unit="iB", unit_scale=True)

    # Start copy process
    copied_blob.start_copy_from_url(blob_url)
    props = copied_blob.get_blob_properties()

    while props.copy.status == "pending":

        _LOGGER.info(props.copy.status + " " + props.copy.progress)

        count = count + 1
        if count > 100:
            raise TimeoutError("Timed out waiting for async copy to complete.")
        time.sleep(5)

        length = int(props.copy.progress.split("/")[0])
        diff = length - prog.n
        prog.update(diff)

        props = copied_blob.get_blob_properties()

    prog.close()


def copy_blob_as_blocks(blob_url, copied_blob):
    """Copy blob as blocks."""
    # Get target size
    resp = requests.get(blob_url, stream=True)
    total_size = int(resp.headers.get("content-length", 0))
    chunk_size = 10 * 10 * 10 * 10 * 1024

    # Upload empty file
    copied_blob.upload_blob(b"")

    i = 0
    running = 0
    prog = progress(total=total_size, unit="iB", unit_scale=True)
    for step in range(total_size, 0, -chunk_size):

        offset = total_size - step
        length = chunk_size
        if step < chunk_size:
            length = step

        # this will only stage your block
        copied_blob.stage_block_from_url(
            block_id=i + 1,
            source_url=blob_url,
            source_offset=offset,
            source_length=length,
        )

        # now it is committed
        running += length
        i += 1
        prog.update(length)

    copied_blob.commit_block_list([j + 1 for j in range(i)])

    prog.close()
    committed, _ = copied_blob.get_block_list("all")
    assert total_size == running
    assert total_size == len(committed)


def copy_blob_as_github_suggested(blob_url, copied_blob):
    """Copy append as block via github suggession."""
    i = 0
    running = 0
    chunk_size = 10 * 10 * 10 * 10 * 10 * 1024

    # Upload empty file
    copied_blob.upload_blob(b"")

    # Get File size
    resp = requests.get(blob_url, stream=True)
    total_size = int(resp.headers.get("content-length", 0))

    prog = progress(total=total_size, unit="iB", unit_scale=True)

    # Add step
    for step in range(total_size, 0, -chunk_size):
        offset = total_size - step
        length = chunk_size
        if step < chunk_size:
            length = step

        copied_blob.stage_block_from_url(
            block_id=i + 1,
            source_url=blob_url,
            source_offset=offset,
            source_length=length,
        )

        running += length
        i += 1
        prog.update(length)

    block_list = [BlobBlock(block_id=1)]
    copied_blob.commit_block_list(block_list)

    # committed, _ = copied_blob.get_block_list("all")

    prog.close()

    # Throws error
    #   azure.core.exceptions.ResourceNotFoundError:
    #     The source request body for copy source is too
    #     large and exceeds the maximum
    #   permissible limit (100MB).
    #   RequestId:a0ddef58-801e-00a3-45b9-ae8f52000000
    #   Time:2019-12-09T17:54:51.8263383Z
    #   ErrorCode:CannotVerifyCopySource
    #   Error:None

    # Throws error
    #   ErrorCode:InvalidBlobOrBlock
    #
    # When trying smaller chunks


# def copy_blob_as_stream(blob_url, container_client):
# headers
# Authorization
# x-ms-version = 2019-02-02
# x-ms-copy-source:name
# https://myaccount.blob.core.windows.net/mycontainer/myblob

# resp = requests.get(blob_url, stream=True)
# resp.encoding = "utf-8"
# total_size = int(resp.headers.get("content-length", 0))
# # prog = progress(total=total_size, unit="iB", unit_scale=True)
# # for chunk in resp.iter_content(chunk_size=size, decode_unicode=True):

# with open(src, "rb") as data:
#     blob = container_client.upload_blob(name=src, data=data)
#     properties = blob.get_blob_properties()
#     logging.info(properties)


def copy_blob_as_azcopy(src_url, dest_url, output_type=None, recursive=False):
    """Use azcopy to copy as block blob."""
    _LOGGER.info("Copying using azcopy")
    # Escape characters
    # if os.name == "nt":
    #     source = source.replace("&", "^&")
    #     destination = destination.replace("&", "^&")

    # Check if azcopy is installed
    args = ["azcopy", "--version"]
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, shell=False)
    (out, err) = proc.communicate()
    if "azcopy" not in out.decode("utf-8") or err:
        raise Exception("AZ copy not found on the system.")

    # copy as block
    args = ["azcopy", "copy", src_url, dest_url, "--blob-type", "BlockBlob"]
    if output_type == "json":
        args.append("--output-type", "json")
    if recursive:
        args.append("--recursive")

    _LOGGER.info("Call process: %s", " ".join(args))
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, shell=False)
    (out, err) = proc.communicate()

    if err:
        _LOGGER.error(out)
    else:
        _LOGGER.info(out)


def upload_file(src, container_name, connection_string):
    """Upload file to azure."""
    _LOGGER.info("Uploading %s", src)

    client = BlobServiceClient.from_connection_string(connection_string)
    container_client = client.get_container_client(container_name)

    with open(src, "rb") as data:
        blob = container_client.upload_blob(name=src, data=data)
        properties = blob.get_blob_properties()
        _LOGGER.info(properties)


def get_block_name(source):
    """Get block name version from source."""
    url_parts = urlparse(source)

    file_name = url_parts.path
    extension = file_name.split(".")[-1]

    new_path = file_name.replace("." + extension, "_block." + extension)

    new_file_name = urlunparse(
        (
            url_parts.scheme,
            url_parts.netloc,
            new_path,
            url_parts.params,
            url_parts.query,
            url_parts.fragment,
        )
    )

    return new_file_name


def write_csv_chunk(dest_path, part, lines):
    """Write a chunk of lines to a csv file."""
    file_name = os.path.join(dest_path, f"part_{part:02d}.csv")
    with open(file_name, "w", newline="") as chunk_file:
        writer = csv.writer(chunk_file)
        for line in lines:
            writer.writerow(line)


def split_local_csv_file(
    input_file, dest_path=None, chunk_size=DEFAULT_CHUNK_SIZE, skip_header=False
):
    """Split the input file into smaller parts using I/O."""
    lines = []
    stats = []
    total_rows = 0
    total_cost = 0
    chunk_row_count = 0
    chunk_cost = 0

    if not dest_path:
        file_directory = os.path.dirname(input_file)
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        dest_path = os.path.join(file_directory, base_name)

    _LOGGER.info("Split file by io for %s to %s", input_file, dest_path)

    if not os.path.exists(dest_path):
        os.makedirs(dest_path)

    with open(input_file, newline="") as csv_file:
        reader = csv.reader(csv_file, delimiter=",")

        if skip_header:
            _LOGGER.info("Skipping header")
            next(reader)

        for row in reader:

            cur_cost = float(row[17])

            total_rows = total_rows + 1
            total_cost = total_cost + cur_cost

            chunk_cost = chunk_cost + cur_cost
            chunk_row_count = chunk_row_count + 1

            lines.append(row)

            if len(lines) == chunk_size:
                part_name = f"{input_file}.part_{total_rows // chunk_size:02}.csv"

                _LOGGER.info(
                    "Partial Stats for part_%02d, %d rows, cost: %.2f",
                    total_rows // chunk_size,
                    chunk_row_count,
                    chunk_cost,
                )
                stats.append((part_name, chunk_row_count, chunk_cost))
                write_csv_chunk(dest_path, total_rows // chunk_size, lines)

                lines = []
                chunk_row_count = 0
                chunk_cost = 0

        # Write the remainder (if any)
        if lines:
            part_name = f"{input_file}.part_{total_rows // chunk_size + 1:02}.csv"
            _LOGGER.info(
                "Partial Stats for part_%02d, %d rows, cost: %.2f",
                total_rows // chunk_size + 1,
                chunk_row_count,
                chunk_cost,
            )
            stats.append((part_name, chunk_row_count, chunk_cost))
            write_csv_chunk(dest_path, total_rows // chunk_size + 1, lines)

        _LOGGER.info(
            "Total Stats for %s, %d rows, %.2f", input_file, total_rows, total_cost
        )
        stats.append((f"{input_file}", total_rows, total_cost))

        return stats


def format_bytes(size, units=(" bytes", "KB", "MB", "GB", "TB", "PB", "EB")):
    """Return a human readable string representation of bytes."""
    return (
        "%3.1f %s" % (size, units[0])
        if size < 1024
        else format_bytes(size / 1024, units[1:])
    )


async def get_chunk_stats(chunk_name: str, chunk: str, file_stats: list):
    """Get stats for the file."""
    row_count = 0
    total_cost = 0

    with StringIO(chunk) as csv_file:
        reader = csv.reader(csv_file, delimiter=",")
        for row in reader:
            cur_cost = Decimal(row[17])
            row_count = row_count + 1
            total_cost = total_cost + cur_cost

    _LOGGER.info(
        "Chunk stats for: '%s' rows: %s, Total cost: %s",
        chunk_name,
        row_count,
        total_cost,
    )
    file_stats.append((chunk_name, row_count, total_cost))
    # return total_rows, total_cost, partial_chunk_content, complete_chunk_content


async def download_file(blob_client: BlobClient):
    """Download file from blob storage."""
    download_stream = await blob_client.download_blob()
    while True:
        _LOGGER.debug("Downloading chunk")
        chunk_bytes = await download_stream.read(DEFAULT_CHUNK_SIZE)
        if not chunk_bytes:
            break
        yield chunk_bytes


async def split_file_and_upload(
    blob_client: BlobClient, blob, destination_container_client: ContainerClient
):
    """Split file and upload to destination."""
    file_stats = []
    partial_line_str = ""
    chunk_idx = 1
    total_bytes = 0

    blob_size = blob.size
    file_extension = blob.name.split(".")[-1]

    _LOGGER.debug("Splitting %s file size %s", blob.name, format_bytes(blob_size))

    async for chunk_bytes in download_file(blob_client):

        try:
            chunk_name = f"{blob.name}.part_{chunk_idx :02}.{file_extension}"
            if b"PAR1" == chunk_bytes[:4]:
                file_extension = "parqeut"
                _LOGGER.warning("PAR1 header found in chunk. Skipping file")
                return
            else:
                # Decode and join partial content
                chunk_str = partial_line_str + chunk_bytes.decode("utf-8-sig")
                has_header = chunk_str[:30] == "InvoiceSectionName,AccountName"

                # Split out last partial line
                lines = chunk_str.split("\n")
                partial_line = lines[-1]
                if has_header:
                    complete_lines = lines[1:-1]
                else:
                    complete_lines = lines[:-1]

                # Rejoin to strings
                complete_chunk_str = "\n".join(complete_lines)
                partial_line_str = "\n".join([partial_line])

                # Get stats
                _LOGGER.debug("Getting stats for %s", chunk_name)
                await get_chunk_stats(chunk_name, complete_chunk_str, file_stats)
                data = complete_chunk_str.encode("utf-8")

            # Copy to destination
            _LOGGER.debug("Uploading %s", chunk_name)
            await destination_container_client.upload_blob(
                name=chunk_name, data=data, overwrite=True
            )
            total_bytes = total_bytes + len(data)

        except UnicodeDecodeError as e:
            _LOGGER.error("Error decoding file %s", chunk_name)
            _LOGGER.error(e)

        chunk_idx += 1

    total_row_count = 0
    total_file_cost = 0
    for chunk_stat in file_stats:
        _, cunk_row_count, chunk_cost = chunk_stat
        total_row_count += cunk_row_count
        total_file_cost += chunk_cost
    _LOGGER.info(
        "Total Stats for %s, %d bytes (blob size), %d bytes (copied), %d rows, %.2f cost",
        blob.name,
        blob_size,
        total_bytes,
        total_row_count,
        total_file_cost,
    )

    if len(partial_line) > 0:
        # upload partial line
        raise NotImplementedError(
            f"Partial line upload not implemented. partial data: '{partial_line}'"
        )
