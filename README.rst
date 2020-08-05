**********************************
Azure Billing Reports
**********************************
.. image:: https://travis-ci.org/briglx/AzureBillingReports.svg?branch=master
    :target: https://travis-ci.org/briglx/AzureBillingReports

The ``azure billing reports`` are an unofficial collection of reports built on top of the Azure Billing API.

Azure provides an hourly usage report for their customers. The ``azure billing reports`` use a script to fetch the data and use PowerBI M queries to parse the data info useful fields.

Overview
========

|screenshot-pipeline|



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

    docker build --pull --rm -f "Dockerfile.dev" -t azurebillingreports:latest "."

Run docker image

.. code-block:: bash

    docker run --rm -it --env-file local.env azurebillingreports:latest

    # If you want to see STDOUT use 
    docker run --rm -a STDOUT --env-file local.env azurebillingreports:latest

Deploy the image to repository. Repalce the name <registryname> with the name of your repository. After deploying, this will remove the image from your local Docker environment

.. code-block:: bash

    az acr login --name  <registryname>
    docker tag azurebillingreports <registryname>.azurecr.io/azurebillingreports:v1
    docker push <registryname>.azurecr.io/azurebillingreports:v1
    docker rmi <registryname>.azurecr.io/azurebillingreports:v1

Run the container with the following:

.. code-block:: bash

    az container create --name blxcontainergroup --resource-group blxbilling --image blxcontainerregistry.azurecr.io/azurebillingreports:v1 --registry-login-server blxcontainerregistry.azurecr.io --registry-username <acr_username> --registry-password <acr_password> --secure-environment-variables 'ENROLLMENT_ID=<enrollment_id>' 'BILLING_AUTH_KEY=<billing_auth_key>' 'STORAGE_CONTAINER_NAME=<billingfiles>' 'STORAGE_CONNECTION_STRING=<connection_string>'

Update Container Environment Variables
======================================

Export the container settings

.. code-block:: bash

    az container export -g blxbilling --name blxcontainergroup -f output.yaml

Edit the settings and recreate

.. code-block:: bash

    az container create -g blxbilling -f output.yaml


Create Docker Image repository
==============================

.. code-block:: bash

    az acr create --resource-group myResourceGroup --name myContainerRegistry007 --sku Basic


Common Issues
=============

- Request date header too old: 'Mon, 16 Dec 2019 22:00:09 GMT'
-- The docker image time has drifted. Restart docker on host container.
- API Key Expired
-- update the key found in secure environment variables


Development
===========

Style Guidelines
----------------

This project enforces quite strict `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_ and `PEP257 (Docstring Conventions) <https://www.python.org/dev/peps/pep-0257/>`_ compliance on all code submitted.

We use `Black <https://github.com/psf/black>`_ for uncompromised code formatting.

Summary of the most relevant points:

 - Comments should be full sentences and end with a period.
 - `Imports <https://www.python.org/dev/peps/pep-0008/#imports>`_  should be ordered.
 - Constants and the content of lists and dictionaries should be in alphabetical order.
 - It is advisable to adjust IDE or editor settings to match those requirements.

Ordering of imports
-------------------

Instead of ordering the imports manually, use `isort <https://github.com/timothycrosley/isort>`_.

.. code-block:: bash

    pip3 install isort
    isort -rc .

Use new style string formatting
-------------------------------

Prefer `f-strings <https://docs.python.org/3/reference/lexical_analysis.html#f-strings>`_ over ``%`` or ``str.format``.

.. code-block:: python

    #New
    f"{some_value} {some_other_value}"
    # Old, wrong
    "{} {}".format("New", "style")
    "%s %s" % ("Old", "style")

One exception is for logging which uses the percentage formatting. This is to avoid formatting the log message when it is suppressed.

.. code-block:: python

    _LOGGER.info("Can't connect to the webservice %s at %s", string1, string2)


Testing
-------

As it states in the `Style Guidelines`_ section all code is checked to verify the following:

 - All the unit tests pass
 - All code passes the checks from the linting tools

Local testing is done using `Tox <https://tox.readthedocs.io/en/latest/>`_. To start the tests, activate the virtual environment and simply run the command:

.. code-block:: bash

    tox

**Testing outside of Tox**

Running ``tox`` will invoke the full test suite. To be able to run the specific test suites without tox, you'll need to install the test dependencies into your Python environment:

.. code-block:: bash

    pip3 install -r requirements_test.txt

Now that you have all test dependencies installed, you can run tests on the project:

.. code-block:: bash

    isort -rc .
    codespell  --skip="./.*,*.csv,*.json,*.pyc,./docs/_build/*,./htmlcov/*"
    black setup.py billing merge script tests
    flake8 setup.py billing merge script tests
    pylint setup.py billing merge script tests
    pydocstyle billing merge script tests
    python -m pytest tests
    python -m pytest --cov-report term-missing --cov=billing

References
==========

- https://docs.microsoft.com/en-us/azure/container-instances/container-instances-using-azure-container-registry


.. |screenshot-pipeline| image:: https://raw.github.com/briglx/AzureBillingReports/master/docs/BillingArchitectureOverview.png