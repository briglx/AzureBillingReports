#!/usr/bin/python
"""Script to upload billing data to blob storage."""
import sys
import os
from azure.storage.blob import BlobServiceClient


def copy_blob(blob_url, dest_file_name, container_name, connection_string):
    """Copy remote blob file to destination container."""
    client = BlobServiceClient.from_connection_string(connection_string)
    copied_blob = client.get_blob_client(container_name, dest_file_name)
    copied_blob.start_copy_from_url(blob_url)
    props = copied_blob.get_blob_properties()
    print(props.copy.status)


def upload_file(src, container_name, connection_string):
    """Upload file to azure."""
    print(f"Uploading {src}")

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

    upload_file(file_name, container_name, connection_string)


if __name__ == "__main__":
    main(sys.argv[1:])
