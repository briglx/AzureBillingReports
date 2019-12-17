"""Module to manage billing container."""
import json
import logging
from azure.common.client_factory import get_client_from_json_dict
from azure.mgmt.containerinstance import ContainerInstanceManagementClient
from azure.mgmt.containerinstance.models import (
    ContainerGroup,
    Container,
    ResourceRequests,
    ResourceRequirements,
    OperatingSystemTypes,
)

_LOGGER = logging.getLogger(__name__)


def create_container_group(aci_client, resource_group, container):
    """Create a new container group."""
    container_group_name, container_image_name = container
    _LOGGER.info("Creating container group '%s'...", container_group_name)

    # Configure the container
    container_resource_requests = ResourceRequests(memory_in_gb=1, cpu=1.0)
    container_resource_requirements = ResourceRequirements(
        requests=container_resource_requests
    )
    container = Container(
        name=container_group_name,
        image=container_image_name,
        resources=container_resource_requirements,
    )

    group = ContainerGroup(
        location=resource_group[1],
        containers=[container],
        os_type=OperatingSystemTypes.linux,
    )

    # Create the container group
    aci_client.container_groups.create_or_update(
        resource_group[0], container_group_name, group
    )

    _LOGGER.info("Created Container group '%s'", container_group_name)


def get_container_client(azure_auth):
    """Get Container Client."""
    if azure_auth is not None:
        _LOGGER.info("Authenticating Azure using credentials")
        auth_config_dict = json.loads(azure_auth)
        client = get_client_from_json_dict(
            ContainerInstanceManagementClient, auth_config_dict
        )
        # client = get_client_from_auth_file(ContainerInstanceManagementClient)
    else:
        _LOGGER.error(
            "\nFailed to authenticate to Azure. Have you set the"
            " AZURE_AUTH_LOCATION environment variable?\n"
        )

    return client


def start_container(aci_client, resource_group, container_group_name):
    """Start container."""
    _LOGGER.info("starting container")
    rg_name = resource_group[0]
    aci_client.container_groups.start(rg_name, container_group_name)


def stop_container(aci_client, resource_group, container_group_name):
    """Stop container."""
    _LOGGER.info("stopping container")
    rg_name = resource_group[0]
    aci_client.container_groups.stop(rg_name, container_group_name)


def create_container(aci_client, resource_group, container):
    """Create a new container."""
    _LOGGER.info("create container")
    create_container_group(aci_client, resource_group, container)
