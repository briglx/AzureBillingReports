"""Test the methods in prep/exports.py."""

import os
from unittest.mock import Mock, patch

# load_dotenv()
from billing.blob_storage import (
    copy_most_recent_files,
    get_blob_service_client_from_url,
    get_most_recent_files,
    split_file_and_upload,
)

# from dotenv import load_dotenv


TEST_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=testaccount;AccountKey=testkey;EndpointSuffix=core.windows.net"
TEST_ACCOUNT_NAME = "testaccount"
TEST_ACCOUNT_URL = f"https://{TEST_ACCOUNT_NAME}.blob.core.windows.net"
TEST_CONTAINER_NAME = "testcontainer"
TEST_PREFIX = "mytestpath"
TEST_SAS_TOKEN = "sv=2019-12-12&ss=bfqt&srt=sco&sp=rwdlacupx&se=2021-10-01T00:00:00Z&st=2020-10-01T00:00:00Z&spr=https&sig=1234567890"
TEST_URL = f"https://{TEST_ACCOUNT_NAME}.blob.core.windows.net/{TEST_CONTAINER_NAME}/{TEST_PREFIX}?{TEST_SAS_TOKEN}"

PATCH_CLIENT_PATH = "billing.blob_storage.BlobServiceClient"


def test_get_blob_service_client_from_url():
    """Test getting a blob client from a url with a sas token."""
    with patch(PATCH_CLIENT_PATH) as mock_client:
        # mock_blob_service_client.return_value = Mock()
        _, container_name, prefix = get_blob_service_client_from_url(TEST_URL)

        assert mock_client.called
        assert len(mock_client.mock_calls) == 1
        mock_client.assert_called_once_with(
            account_url=TEST_ACCOUNT_URL, credential=TEST_SAS_TOKEN
        )

        assert container_name == TEST_CONTAINER_NAME
        assert prefix == TEST_PREFIX


def test_get_blob_service_client_from_url_no_mock():
    """Test getting a blob client from a url with a sas token."""

    no_mock_client, container_name, prefix = get_blob_service_client_from_url(TEST_URL)

    assert no_mock_client.account_name == TEST_ACCOUNT_NAME
    assert container_name == TEST_CONTAINER_NAME
    assert prefix == TEST_PREFIX


def test_get_most_recent_files():
    """Test getting the list of most recent files for a given storage account."""

    with patch(PATCH_CLIENT_PATH) as mock_client:
        test_blob_service_client, container_name, prefix = (
            get_blob_service_client_from_url(TEST_URL)
        )
        billing_file_infos = get_most_recent_files(
            test_blob_service_client, TEST_PREFIX
        )

        assert mock_client.called
        assert len(billing_file_infos) == 0


def test_copy_most_recent_files():
    """Test getting a blob client from a url with a sas token."""

    # mock_blob_service_client.return_value = Mock()
    test_url = f"{TEST_URL}"
    dest_url = f"https://{TEST_ACCOUNT_NAME}.blob.core.windows.net/latest/{TEST_PREFIX}?{TEST_SAS_TOKEN}"

    with patch(PATCH_CLIENT_PATH) as mock_client:

        copy_most_recent_files(test_url, dest_url)
        assert mock_client.called
