"""Helper methods for various modules."""
import csv
import logging
import logging.config
import os
import random
import string

import requests

import yaml

_LOGGER = logging.getLogger(__name__)


def get_job_id(length=8):
    """Create random job id."""
    return "".join(random.choice(string.hexdigits) for x in range(length))


def notify_complete(job_id):
    """Notify trigger that job is complete."""
    _LOGGER.info("Calling trigger to stop container")

    uri = (
        "https://myfunctionbilling.azurewebsites.net/api/DockerHTTPTrigger"
        "?code=sdYZl5NvaT/N1Lo3HRlLsBD5iig2CJE6IR2csvYi5A3PgjzCTpNNLw=="
    )

    resp = requests.get(uri + "&job_id=" + job_id)

    _LOGGER.info(resp.text)


def setup_logging(default_path="logging.yaml", default_level=logging.INFO):
    """Configure logger."""
    path = default_path
    if os.path.exists(path):
        with open(path, "rt") as config_file:
            try:
                config = yaml.safe_load(config_file.read())
                logging.config.dictConfig(config)
                config_file.close()
            except Exception as ex:  # pylint: disable=W0703
                print(ex)
                print("Error in Logging Configuration. Using default configs")
                logging.basicConfig(level=default_level)
    else:
        print("Failed to load configuration file. Using default configs")
        logging.basicConfig(level=default_level)


def get_sample(src, sample_rate):
    """Get sample records from source file for given sample rate."""
    sample_file_name = src + "-sample-" + str(sample_rate) + ".csv"
    with open(sample_file_name, "w", newline="") as sample_file:
        writer = csv.writer(sample_file)

        with open(src, newline="") as csv_file:
            reader = csv.reader(csv_file, delimiter=",")

            for _ in range(3):
                row = next(reader)
                writer.writerow(row)

            for row in reader:
                val = random.random()
                if val < sample_rate:
                    writer.writerow(row)
