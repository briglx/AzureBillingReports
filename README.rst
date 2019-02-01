**********************************
Azure Billing Reports
**********************************

The ``azure billing reports`` are an unofficial collection of reports built on top of the Azure Billing API.

Azure provides an hourly usage report for their customers. The ``azure billing reports`` use a script to fetch the data and use PowerBI M queries to parse the data info useful fields.

Getting Started
==========

- First obtain your enrollment id and a valid api authentication key.
- Run the fetchdata.py script to get the latest billing data. This will download and save the billing data into a csv file.

.. code-block:: bash

    python fetchdata.py enrollment_id api_auth_key

- Open the AzureBillingViaCsv.pbit template file
- Provide the full path to the downloaded csv file.