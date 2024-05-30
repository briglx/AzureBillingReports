"""Module to manage billing container."""

import logging

from azure.common.client_factory import get_client_from_json_dict
from azure.mgmt.containerinstance import ContainerInstanceManagementClient
from azure.mgmt.containerinstance.models import (
    Container,
    ContainerGroup,
    ContainerGroupRestartPolicy,
    EnvironmentVariable,
    ImageRegistryCredential,
    OperatingSystemTypes,
    ResourceRequests,
    ResourceRequirements,
)

_LOGGER = logging.getLogger(__name__)


def get_container_client(azure_auth):
    """Get Container Client."""
    if azure_auth is not None:
        _LOGGER.info("Authenticating Azure using credentials")
        client = get_client_from_json_dict(
            ContainerInstanceManagementClient, azure_auth
        )
    else:
        _LOGGER.error(
            "\nFailed to authenticate to Azure. Have you set the"
            " AZURE_AUTH_LOCATION environment variable?\n"
        )

    return client


def start_container(azure_auth, container_info):
    """Start container."""
    _LOGGER.info("starting container")
    aci_client = get_container_client(azure_auth)
    aci_client.container_groups.start(
        container_info.resource_group_name, container_info.container_name
    )


def stop_container(azure_auth, container_info):
    """Stop container."""
    _LOGGER.info("stopping container")
    aci_client = get_container_client(azure_auth)
    aci_client.container_groups.stop(
        container_info.resource_group_name, container_info.container_name
    )


def create_container(azure_auth, registry_credentials, container_info, env_vars):
    """Create a new container group."""
    _LOGGER.info("Creating container group '%s'...", container_info["groupName"])

    # Map registry credentials
    image_registry_credentials = ImageRegistryCredential(
        server=registry_credentials["server"],
        username=registry_credentials["username"],
        password=registry_credentials["password"],
    )

    # Map to Azure Container objects
    environment_variables = []
    for var in env_vars:
        environment_variables.append(
            EnvironmentVariable(name=var["name"], secure_value=var["value"])
        )

    # Configure the container
    container_resource_requests = ResourceRequests(memory_in_gb=1, cpu=1.0)
    container_resource_requirements = ResourceRequirements(
        requests=container_resource_requests
    )
    container = Container(
        name=container_info["groupName"],
        image=container_info["image"],
        resources=container_resource_requirements,
        environment_variables=environment_variables,
    )

    group = ContainerGroup(
        location=container_info["region"],
        containers=[container],
        os_type=OperatingSystemTypes.linux,
        image_registry_credentials=[image_registry_credentials],
        restart_policy=ContainerGroupRestartPolicy.never,
    )

    # Create the container group
    aci_client = get_container_client(azure_auth)
    aci_client.container_groups.create_or_update(
        container_info["resourceGroup"], container_info["groupName"], group
    )

    _LOGGER.info("Created Container group '%s'", container_info["groupName"])
