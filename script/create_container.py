#!/usr/bin/python
"""Create container."""
import json
import logging
import os

from billing import container as bc
from billing import util


def main():
    """Start or Stop a new container."""
    azure_auth_config = os.environ.get("AZURE_AUTH")
    container_config = os.environ.get("BILLING_CONTAINER_CONFIG")
    container_envs = os.environ.get("BILLING_CONTAINER_ENVS")
    container_registry_config = os.environ.get("CONTAINER_REGISTRY_CONFIG")

    if not azure_auth_config:
        raise ValueError(
            "Parameter auth_file_path is required. "
            "Have you set the AZURE_AUTH environment variable?"
        )
    if not container_config:
        raise ValueError(
            "Parameter container_info is required. "
            "Have you set the BILLING_CONTAINER_CONFIG environment variable?"
        )
    if not container_envs:
        raise ValueError(
            "Parameter container_envs is required. "
            "Have you set the BILLING_CONTAINER_ENVS environment variable?"
        )
    if not container_registry_config:
        raise ValueError(
            "Parameter container_registry_config is required. "
            "Have you set the CONTAINER_REGISTRY_CONFIG env variable?"
        )

    azure_auth = json.loads(azure_auth_config)
    container_info = json.loads(container_config)
    container_env_vars = json.loads(container_envs)
    registry_credentials = json.loads(container_registry_config)

    bc.create_container(
        azure_auth, registry_credentials, container_info, container_env_vars
    )
    # bc.stop_container(azure_auth, rg_name, container_group_name)
    # bc.start_container(azure_auth, rg_name, container_group_name)


if __name__ == "__main__":
    util.setup_logging()
    _LOGGER = logging.getLogger(__name__)
    _LOGGER.info("Starting script")

    main()
