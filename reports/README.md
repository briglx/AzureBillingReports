# Azure Billing Comparison to Point in Time

This reposistory demonstrates how to compare cost to a specific point in time.

![Point in time Report](../docs/PointInTimeReport.png)
<!-- s![Whiteboard Diagram](../docs/Whiteboard.png) -->

- First obtain your enrollment id and a valid api authentication key.
- Configure your environment
- Fetch and Filter the data
    
- Open the `/reports/PointInTimeAggregateLimitedColumns.pbit` template file


## Configure Environment

- Copy Project to Local Computer
- Create and Activate a Python Virtual Environment
- Install Project

```bash
# Copy Project to local computer
cd /path/to/src/
git clone https://github.com/briglx/AzureBillingReports.git
cd /path/to/src/AzureBillingReports

# Create Python Virtual Environment and activate
python -m venv .venv
.venv\Scripts\activate

# Install Project
python -m pip install -r requirements.txt
python -m pip install -e .

```

## Fetch and Filter Data

- Run the `get_usage_data.py` script to get the latest billing usage data. This will download and save the billing data into a csv file.
- Run the `filter_data.py` script to filter the usage data. This will filter out any data before the minimum date.

```bash
python script/get_usage_data.py --eid <enrollment_id> --auth_key <api_auth_key>
#a new file called usage-2021-11-11T14-19-09+00-00.csv will be created

python script/filter_data.py --path <path/to/csv> --min_date <2021-05-30>
#a new file called usage-2021-11-11T14-19-09+00-00.csv-filtered.csv will be created
```

## Open the Report

- Open the `/reports/PointInTimeAggregateLimitedColumns.pbit` template file
- Provide the full path to the filtered downloaded csv file.
