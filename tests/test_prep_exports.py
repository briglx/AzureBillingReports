import os

from dotenv import load_dotenv

load_dotenv()

from prep.exports import get_most_recent_file


def test_get_most_recent_file():

    connection_string = os.getenv("STORAGE_CONNECTION_STRING")
    container_name = os.getenv("CONTAINER_NAME")
    prefix = os.getenv("PREFIX")

    billing_file_infos = get_most_recent_file(connection_string, container_name, prefix)

    print(billing_file_infos)

    assert len(billing_file_infos) > 0
