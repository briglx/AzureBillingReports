"""Function to start Billing Container."""
import datetime
import json
import logging
import os

import azure.functions as func
from azure.common.client_factory import get_client_from_json_dict
from azure.mgmt.containerinstance import ContainerInstanceManagementClient


def get_container_client(azure_auth):
    """Get Container Client."""
    if azure_auth is not None:
        logging.info("Authenticating Azure using credentials")
        auth_config_dict = json.loads(azure_auth)
        client = get_client_from_json_dict(
            ContainerInstanceManagementClient, auth_config_dict
        )
    else:
        logging.error(
            "\nFailed to authenticate to Azure. Have you set the"
            " AZURE_AUTH environment variable?\n"
        )
    return client


def main(mytimer: func.TimerRequest) -> None:
    """Start billing container."""
    cur_time = datetime.datetime.utcnow()
    cur_time = cur_time.replace(tzinfo=datetime.timezone.utc, microsecond=0)
    utc_timestamp = cur_time.isoformat()

    azure_auth = os.environ.get("AZURE_AUTH")
    rg_name = os.environ.get("BILLING_CONTAINER_RG")
    container_group_name = os.environ.get("BILLING_CONTAINER_GROUP_NAME")

    if not azure_auth:
        raise ValueError(
            "Parameter azure_auth is required. "
            "Have you set the AZURE_AUTH environment variable?"
        )
    if not rg_name:
        raise ValueError(
            "Parameter rg_name is required."
            "Have you set the BILLING_CONTAINER_RG env variable?"
        )
    if not container_group_name:
        raise ValueError(
            "Parameter container_group_name is required. "
            "Have you set the BILLING_CONTAINER_GROUP_NAME env variable?"
        )

    # Get client
    aci_client = get_container_client(azure_auth)

    logging.info("starting container")
    aci_client.container_groups.start(rg_name, container_group_name)

    if mytimer.past_due:
        logging.info("The timer is past due!")

    logging.info("Python timer trigger function ran at %s", utc_timestamp)
