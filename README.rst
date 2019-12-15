**********************************
Azure Billing Reports
**********************************
.. image:: https://travis-ci.org/briglx/AzureBillingReports.svg?branch=master
    :target: https://travis-ci.org/briglx/AzureBillingReports

The ``azure billing reports`` are an unofficial collection of reports built on top of the Azure Billing API.

Azure provides an hourly usage report for their customers. The ``azure billing reports`` use a script to fetch the data and use PowerBI M queries to parse the data info useful fields.

Getting Started
==========

- First obtain your enrollment id and a valid api authentication key.
- Run the `get_usage_data.py` script to get the latest billing usage data. This will download and save the billing data into a csv file.
- Run the 'get_ri_recommendations.py` script to get the latest reserved instance recommendations.

.. code-block:: bash

    python get_usage_data.py enrollment_id api_auth_key

    python get_ri_recommendations.py enrollment_id api_auth_key

    python get_price_list.py enrollment_id api_auth_key

- Open the AzureBillingViaCsv.pbit template file
- Provide the full path to the downloaded csv file.

Building and Deploying
==========

Build docker image

.. code-block:: bash

    docker build --rm -f "Dockerfile.dev" -t azurebillingreports:latest

Run docker image

.. code-block:: bash

    docker run --rm -it --env-file local.env azurebillingreports:latest

Deploy the image to repository. Repalce the name <registryname> with the name of your repository. After deploying, this will remove the image from your local Docker environment

.. code-block:: bash

    az acr login --name  <registryname>.azurecr.io
    docker tag azurebillingreports <registryname>.azurecr.io/azurebillingreports:v1
    docker push <registryname>.azurecr.io/azurebillingreports:v1
    docker rmi <registryname>.azurecr.io/azurebillingreports:v1

Run the container with the following:

.. code-block:: bash

    az container create --name blxcontainergroup --resource-group blxbilling --image blxcontainerregistry.azurecr.io/azurebillingreports:v1 --registry-login-server blxcontainerregistry.azurecr.io --registry-username <acr_username> --registry-password <acr_password> --secure-environment-variables 'ENROLLMENT_ID=<enrollment_id>' 'BILLING_AUTH_KEY=<billing_auth_key>' 'STORAGE_CONTAINER_NAME=<billingfiles>' 'STORAGE_CONNECTION_STRING=<connection_string>'

References

- https://docs.microsoft.com/en-us/azure/container-instances/container-instances-using-azure-container-registry