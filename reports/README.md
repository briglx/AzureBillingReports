# Azure Billing Comparison to Point in Time

This reposistory demonstrates how to compare cost to a specific point in time.

![Whiteboard Diagram](../docs/Whiteboard.png)

## Point in Time Cost Report - Getting Started
- First obtain your enrollment id and a valid api authentication key.
- Run the `/script/get_usage_data.py` script to get the latest billing usage data. This will download and save the billing data into a csv file.
- Run the `/script/filter_data.py` script to filter the usage data. This will filter out any data before the minimum date.

```bash
python get_usage_data.py --eid <enrollment_id> --auth_key <api_auth_key>
#a new file called usage-2021-11-11T14-19-09+00-00.csv will be created

python filter_data.py --path <path/to/csv> --min_date <2021-05-30>
#a new file called usage-2021-11-11T14-19-09+00-00.csv-filtered.csv will be created
```

- Open the `/reports/PointInTimeAggregateLimitedColumns.pbit` template file
- Provide the full path to the filtered downloaded csv file.