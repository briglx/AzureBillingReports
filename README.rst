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
