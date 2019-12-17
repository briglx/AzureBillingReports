#!/usr/bin/python
"""Create container."""
import os
import logging
from billing import util, container as bc


def main():
    """Start or Stop a new container."""
    azure_auth = os.environ.get("AZURE_AUTH")
    rg_name = os.environ.get("BILLING_CONTAINER_RG_NAME")
    rg_region = os.environ.get("BILLING_CONTAINER_RG_REGION")
    container_group_name = os.environ.get("BILLING_CONTAINER_GROUP_NAME")
    image_name = os.environ.get("BILLING_CONTAINER_IMAGE_NAME")

    if not azure_auth:
        raise ValueError(
            "Parameter auth_file_path is required. "
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
    aci_client = bc.get_container_client(azure_auth)
    resource_group = (rg_name, rg_region)
    container = (container_group_name, image_name)
    bc.create_container(aci_client, resource_group, container)
    # bc.stop_container(aci_client, rg_name, container_group_name)
    # bc.start_container(aci_client, rg_name, container_group_name)


if __name__ == "__main__":
    util.setup_logging()
    _LOGGER = logging.getLogger(__name__)
    _LOGGER.info("Starting script")

    main()
