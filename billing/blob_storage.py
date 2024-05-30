"""Module to manage billing data with blob storage."""

from datetime import datetime, timedelta
import logging
import subprocess
import time
from urllib.parse import urlparse, urlunparse

from azure.storage.blob import (
    AccountSasPermissions,
    BlobBlock,
    BlobServiceClient,
    ResourceTypes,
    generate_account_sas,
)
import requests
from tqdm import tqdm as progress

_LOGGER = logging.getLogger(__name__)


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


def copy_blob_as_azcopy(src_url, dest_url):
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
    args = [
        "azcopy",
        "copy",
        src_url,
        dest_url,
        "--blob-type",
        "BlockBlob",
        "--output-type",
        "json",
    ]

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
