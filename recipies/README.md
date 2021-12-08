# Azure Cost Optimization Recipies

Azure Cost Optimization Recipies is a collection of reports built on top of a common dataset.

The Recipies include:

- Sample Reports
- Common Data Sets
- Development Environment

# Sample Reports

Create a new report using the common data set using the development environment. 

- Start the local Sql Database docker image
- Open the `RecipiesReport.pbit` template
- Point to the Database

# Common Data Set

The purpose of the Common Data Set is to standardize on the various data sets used to create meaningful reports for Azure Cost Optimzation and to provide a sample database for local development.

|Table | Source | Fields | Sorted | Typed |
|------|--------|--------|-------|--------|
| Regions | Blob - download/regions/azure regionsv2.json | Yes | Yes | No |
| Advisor | Blob - download/advisor/merged/advisor.json| Yes | Yes | No |
| ISFData | Blob - download/isfratio/isfratio.csv | Yes | Yes | Yes |
| Reservation Transactions | Blob - download/restransactions/restransactions.json | Yes | Yes | No |
| ActualCost | DB | Yes | No (OK) | Yes |
| AmortizedCost | DB | Yes | No (OK) | Yes |
| Reservation Details | DB |Yes | Yes | Yes |
| Subscriptinos | Billing data | NA | NA | NA |
| Reservation Recommendations | blob - download/resrecommendations/merged/reservation_merged.json| Yes | Yes | No |
| Meters | Reservation Recomendations | NA | NA | NA |
| PriceList | Blob - download/pricesheet/pricesheet.json | Yes | Yes | No |
| Marketplace | Blob - download/marketplace/marketplace.json |  Yes | Yes | No |
| Date | Calculated | NA | NA | NA |

## Relationships

| Table Left | Table Right | Cardinality | Cross Filter |
| -----------|-------------|-------------|--------------|
| ActualCosts.Date | Date.DateAsTextAlt | Many to one | Both |
| ActualCost.MeterId | Meters.meterId | Many to one | Single |
| ActualCost.ResourceLocation | Regions.name | Many to one | Single |
| ActualCosts.SubscriptonId | Subscriptions.SubscriptionId | Many to one | Single |
| AmortizedCost.Date | Date.DateAsTextAlt | Many to one | Single |
| AmortizedCost.ResourceLocation | Regions.name | Many to one | Single |
| AmortizedCost.SubscriptionId | Subscriptions.SubscriptionId | Many to one | Single |
| Reservation Recomendatins.subscriptionId | Subscriptions.SubscriptionId | Many to one | Single |

## Regions Table

| Field | Type | Notes |
|-------|------|-------|
| displayName | nvarchar(25) | |
| geographyGroup | nvarchar(20) NULL | |
| id | nvarchar(100) | |
| latitude | Decimal(8,6) NULL | |
| longitude | Decimal(9,6) NULL | |
| name | nvarchar(25) | |
| pairedRegion | nvarchar(25) NULL | |
| physicalLocation | nvarchar(35) NULL | |
| regionCategory | nvarchar(15) | | 
| regionalDisplayName | nvarchar(50) | |
| regionType | nvarchar(10) | |
| subscriptionId | nvarchar(50) | |

Example Data. See full dataset [/sampledata/Regions.csv](sampledata/Regions.csv)

|displayName | geographyGroup | id | latitude | longitude | name | pairedRegion | physicalLocation | regionCategory | regionalDisplayName | regionType | subscriptionId |
|------------|-----|----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| Asia |  | /subscriptions/cd3b4810-bb97-4f99-9eaa-20c547ee30cb/locations/asia |  |  | asia |  |  | Other | Asia | Logical | cd3b4810-bb97-4f99-9eaa-20c547ee30cb |
| Australia Central | Asia Pacific | /subscriptions/cd3b4810-bb97-4f99-9eaa-20c547ee30cb/locations/australiacentral | -35.3075 | 149.1244 | australiacentral | australiacentral | Canberra | Other | (Asia Pacific) Australia Central | Physical | cd3b4810-bb97-4f99-9eaa-20c547ee30cb |
| Brazil |  | /subscriptions/cd3b4810-bb97-4f99-9eaa-20c547ee30cb/locations/brazil |  |  | brazil |  |  | Other | Brazil | Logical | cd3b4810-bb97-4f99-9eaa-20c547ee30cb |
| Brazil Southeast | South America | /subscriptions/cd3b4810-bb97-4f99-9eaa-20c547ee30cb/locations/brazilsoutheast | -22.90278 | -43.2075 | brazilsoutheast | brazilsouth | Rio | Other | (South America) Brazil Southeast | Physical | cd3b4810-bb97-4f99-9eaa-20c547ee30cb |
| Central US | US | /subscriptions/cd3b4810-bb97-4f99-9eaa-20c547ee30cb/locations/centralus | 41.5908 | -93.6208 | centralus | eastus2 | Iowa | Recommended | (US) Central US | Physical | cd3b4810-bb97-4f99-9eaa-20c547ee30cb |
| Central US (Stage) | US | /subscriptions/cd3b4810-bb97-4f99-9eaa-20c547ee30cb/locations/centralusstage |  |  | centralusstage |  |  | Other | (US) Central US (Stage) | Logical | cd3b4810-bb97-4f99-9eaa-20c547ee30cb |
| Central US EUAP | US | /subscriptions/cd3b4810-bb97-4f99-9eaa-20c547ee30cb/locations/centraluseuap | 41.5908 | -93.6208 | centraluseuap | eastus2euap |  | Other | (US) Central US EUAP | Physical | cd3b4810-bb97-4f99-9eaa-20c547ee30cb |

### Steps to Create Regions Sample data

- Download from Azure
- Transform the data
- Remove Bad Records

Download the data using the [list-locations](https://docs.microsoft.com/en-us/rest/api/resources/subscriptions/list-locations#code-try-0) api with either the `az cli` or `wget`.

```bash
# Replace with your subscription-id and bearer token
subscription_id=<subscription-id>
bearer_token=<bearer token>
regions_filename=AzureLocations.json

# az cli example
az account list-locations > $regions_filename

# wget example
header='--header=Authorization: Bearer $bearer_token'
wget "$header" https://management.azure.com/subscriptions/$subscription_id/locations?api-version=2020-01-01 -O azure $regions_filename
```

Transform the data using the PowerBi Template.

- Open the `sampledata/RegionsFromAzureListLocations.pbit` and select the path to the downloaded `sampledata/AzureLocations.json` file.
- On the `Raw Data` tab, select the dataset click `Export Data` from the elipse.
- Save the file as `sampledata/Regions.csv`

Remove bad records by:

- Remove the header row
- Remove the `,` (comma) and `"` (quote)s from `"Tokyo, Saitama"` to `Tokyo Saitama`

## Reservation Recommendations Table

| Field | Type | Notes |
|-------|------|-------|
| AnnualSavings | Number | Calculated AnnualSavings = 'Reservation Recommendations'[netSavings]/SUBSTITUTE(SUBSTITUTE('Reservation Recommendations'[Look Back Period],"Last",""),"Days","")*365 |

    TBD 

# Development

Docker commands to manage the sql image. 

```bash
# Build the image
docker build --pull --rm -f "Dockerfile.dev" -t aco-recipies:latest "."

# Run a new recipies container. This loads default data.
docker run --env-file local.env -p 1433:1433 --hostname aco_recipies --name aco_recipies --detach aco-recipies:latest

# Get a shell to the container
docker container exec -it aco_recipies /bin/bash

# Stop the container to keep the current state.
docker container stop aco_recipies

# Start the stopped container. Does not reload data. 
docker container start aco_recipies

# Remove a container
docker container rm aco_recipies

# Quick Build. Kills the image after run
docker run --rm -it --env-file local.env -p 1433:1433 --hostname aco_recipies aco-recipies:latest
```

# References
- Sql Server Express on Docker https://docs.microsoft.com/en-us/sql/linux/quickstart-install-connect-docker?view=sql-server-linux-ver15&pivots=cs1-powershell
- MSSQL Node Docker Example https://github.com/twright-msft/mssql-node-docker-demo-app
- Configure and Customize SQL Container https://docs.microsoft.com/en-us/sql/linux/sql-server-linux-docker-container-configure?view=sql-server-ver15&pivots=cs1-bash
- Attach to a Container https://linuxize.com/post/how-to-connect-to-docker-container/
- Azure Api list Locations https://docs.microsoft.com/en-us/rest/api/resources/subscriptions/list-locations#code-try-0