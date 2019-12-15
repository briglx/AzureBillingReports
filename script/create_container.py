#!/usr/bin/python
"""Create container."""
import os
import json
from azure.common.client_factory import get_client_from_json_dict
from azure.mgmt.containerinstance import ContainerInstanceManagementClient
from azure.mgmt.containerinstance.models import (
    ContainerGroup,
    Container,
    ContainerGroupNetworkProtocol,
    ContainerPort,
    IpAddress,
    Port,
    ResourceRequests,
    ResourceRequirements,
    OperatingSystemTypes,
)


def create_container_group(
    aci_client, resource_group, container_group_name, container_image_name
):
    """Create a new container group."""
    print("Creating container group '{0}'...".format(container_group_name))

    # Configure the container
    container_resource_requests = ResourceRequests(memory_in_gb=1, cpu=1.0)
    container_resource_requirements = ResourceRequirements(
        requests=container_resource_requests
    )
    container = Container(
        name=container_group_name,
        image=container_image_name,
        resources=container_resource_requirements,
        # ports=[ContainerPort(port=80)],
    )

    # ports = [Port(protocol=ContainerGroupNetworkProtocol.tcp, port=80)]
    # group_ip_address = IpAddress(
    #     ports=ports, dns_name_label=container_group_name, type="Public"
    # )
    group = ContainerGroup(
        location=resource_group[1],
        containers=[container],
        os_type=OperatingSystemTypes.linux,
        # ip_address=group_ip_address,
    )

    # Create the container group
    aci_client.container_groups.create_or_update(
        resource_group[0], container_group_name, group
    )

    print(f"Created Container group '{container_group_name}'")


def get_container_client(azure_auth):
    """Get Container Client."""
    if azure_auth is not None:
        print("Authenticating Azure using credentials")
        auth_config_dict = json.loads(azure_auth)
        client = get_client_from_json_dict(
            ContainerInstanceManagementClient,
            auth_config_dict
        )
        # client = get_client_from_auth_file(ContainerInstanceManagementClient)
    else:
        print(
            "\nFailed to authenticate to Azure. Have you set the"
            " AZURE_AUTH_LOCATION environment variable?\n"
        )

    return client


def start_container(aci_client, rg_name, container_group_name):
    """Start container."""
    print("starting container")
    aci_client.container_groups.start(rg_name, container_group_name)


def stop_container(aci_client, rg_name, container_group_name):
    """Stop container."""
    print("stopping container")
    aci_client.container_groups.stop(rg_name, container_group_name)


def create_container(aci_client, rg_name, container_group_name):
    """Create a new container."""
    # rg_name = "blxbilling"
    resource_group_region = "eastus"
    # container_group_name = "blxcontainergroup"
    container_image_app = "blxcontainerregistry.azurecr.io/azurebillingreports:v1"

    resource_group = (rg_name, resource_group_region)

    create_container_group(
        aci_client, resource_group, container_group_name, container_image_app
    )


if __name__ == "__main__":
    azure_auth = os.environ.get("AZURE_AUTH")
    rg_name = os.environ.get("BILLING_CONTAINER_RG")
    container_group_name = os.environ.get("BILLING_CONTAINER_GROUP_NAME")

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
    aci_client = get_container_client(azure_auth)
    create_container(aci_client, rg_name, container_group_name)
    # stop_container(aci_client, rg_name, container_group_name)
    # start_container(aci_client, rg_name, container_group_name)
