#!/usr/bin/python
"""Script to merge temp records into main."""
import argparse
import logging
import os

import pyodbc
from pyodbc import ProgrammingError

# pylint: disable=C0103
# pylint: disable=W0621


SQL_GET_MERGE_RECORDS = (
    "SELECT Min([Date]) as MinDate"
    + ", Max([Date]) as MaxDate"
    + ", count(*) as RecordCount"
    + ", [_FileName] "
    + "FROM [dbo].[fact_UsageSummary_Temp] "
    + "WHERE [_MergeDate] = '' "
    + "group by [_FileName] order by [MinDate]"
)
SQL_MERGE_RECORDS = "{CALL [dbo].[fact_UsageSummaryMergeTemp]  (?,?,?)}"


def main(connection_string):
    """Merge temp records into main table."""
    count = 0

    cnxn = pyodbc.connect(connection_string)
    cursor = cnxn.cursor()

    cursor.execute(SQL_GET_MERGE_RECORDS)
    rows = cursor.fetchall()

    for row in rows:
        min_date, max_date, _, file_name = row
        params = (file_name, min_date, max_date)
        try:
            cursor.execute(SQL_MERGE_RECORDS, params)
        except ProgrammingError:
            # Sometimes it doesn't work first time
            _LOGGER.warning("Trying second time.")
            cursor.execute(SQL_MERGE_RECORDS, params)
        except Exception as ex:
            _LOGGER.error("Unexpected error %s", ex)
        finally:
            _LOGGER.info("Row %s", count)
            count = count + 1


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    _LOGGER = logging.getLogger(__name__)
    _LOGGER.info("Starting script")

    parser = argparse.ArgumentParser(
        description="Merge Usage Summary Temp records.", add_help=True,
    )
    parser.add_argument("--connection_string", "-c", help="Connection String")
    args = parser.parse_args()

    # Use environment variables if arguments are not passed
    connection_string = args.connection_string or os.environ.get("DB_CONNECTION_STRING")

    main(connection_string)
    _LOGGER.info("Done.")
