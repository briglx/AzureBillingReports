# Prep

Various tools to prepare the data for the data pipeline.

* `exports.py` - Exports data from a database to a CSV file.
* `split_file.py` - Splits a large file into smaller files.

## `exports.py`

Get most recent files from Azure Blob Storage.

Parameters:
- connection_string: The connection string to the Azure Blob Storage.
- container_name: The name of the container in the Azure Blob Storage.
- prefix: The prefix of the files to download.

Examples
```bash
python exports.py --connection_string $connection_string --container_name $container_name --prefix $prefix
```

## `..\billing\split_file.py`

Splits a large file into smaller files.

Parameters:
- input_file: The file to split.
- output_dir: The directory to save the split files.
- batch_size: The number of lines to include in each split file. Default is 500000.

Examples
```bash
python split_file.py --file $input_file --output_dir $output_dir --batch $batch_size
```
