"""Get most recent files from Azure Blob Storage."""

from azure.storage.blob import BlobServiceClient


def get_most_recent_file(connection_string, container_name, prefix):
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
