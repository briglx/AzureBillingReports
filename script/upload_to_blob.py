#!/usr/bin/python
"""Script to upload billing data to blob storage."""
import sys
import os
import requests
from azure.storage.blob import BlobServiceClient, BlobBlock
from tqdm import tqdm as progress


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


def copy_blob_as_remote(blob_url, copied_blob):
    """Copy blob as append file."""
    # Copies as Append file
    copied_blob.start_copy_from_url(blob_url)
    props = copied_blob.get_blob_properties()
    print(props.copy.status)


def copy_blob_as_github_suggested(blob_url, copied_blob):
    """Copy append as block via github suggession."""
    # client = BlobServiceClient.from_connection_string(connection_string)
    # copied_blob = client.get_blob_client(container_name, dest_file_name)

    # Upload empty file
    chunk_size = 10 * 10 * 10 * 10 * 10 * 1024

    copied_blob.upload_blob(b"")

    resp = requests.get(blob_url, stream=True)
    total_size = int(resp.headers.get("content-length", 0))

    # your_block_id = "1234"

    i = 0
    running = 0
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

    committed, _ = copied_blob.get_block_list("all")

    prog.close()

    assert total_size == len(committed)

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
#     print(properties)


def copy_blob(blob_url, dest_file_name, container_name, connection_string):
    """Copy remote blob file to destination container."""
    client = BlobServiceClient.from_connection_string(connection_string)
    copied_blob = client.get_blob_client(container_name, dest_file_name)

    # copy_blob_as_blocks(blob_url, copied_blob)

    # copy_blob_as_remote(blob_url, copied_blob)

    copy_blob_as_github_suggested(blob_url, copied_blob)


def upload_file(src, container_name, connection_string):
    """Upload file to azure."""
    print("Uploading " + src)

    client = BlobServiceClient.from_connection_string(connection_string)

    container_client = client.get_container_client(container_name)

    with open(src, "rb") as data:
        blob = container_client.upload_blob(name=src, data=data)
        properties = blob.get_blob_properties()
        print(properties)


def main(argv):
    """Upload file to Azure blob."""
    file_name = argv[0]
    container_name = argv[1] or os.environ.get("STORAGE_CONTAINER_NAME")
    connection_string = argv[2] or os.environ["STORAGE_CONNECTION_STRING"]

    if file_name is None:
        raise TypeError("Parameter file_name can not be empty.")

    if container_name is None:
        raise TypeError("Parameter container_name can not be empty.")

    if connection_string is None:
        raise TypeError("Parameter connection_string can not be empty.")

    # upload_file(file_name, container_name, connection_string)

    from urllib.parse import urlparse
    a = urlparse(file_name)
    _name = os.path.basename(a.path)

    dest_file_name = _name.replace(".csv", "_block.csv")
    copy_blob(file_name, dest_file_name, container_name, connection_string)


if __name__ == "__main__":
    main(sys.argv[1:])
