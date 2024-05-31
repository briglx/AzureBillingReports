"""Split billing files into smaller parts."""

import csv
import logging
import os

import pandas as pd

from . import BILLING_DTYPES, DEFAULT_CHUNK_SIZE

_LOGGER = logging.getLogger(__name__)

PROJ_DIR = os.path.dirname(__file__)
# Define the chunk size (number of lines per part file)


# def run_azcopy(src, dest, recursive=False):
#     """Run azcopy command to copy files."""
#     azcopy_command = [azcopy_path, "copy", src, dest]
#     if recursive:
#         azcopy_command.append("--recursive=true")
#     subprocess.call(azcopy_command)


def split_file_by_pandas(input_file, dest_path, chunk_size=DEFAULT_CHUNK_SIZE):
    """Split the input file into smaller parts using pandas."""
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)

    for i, chunk in enumerate(
        pd.read_csv(input_file, dtype=BILLING_DTYPES, skiprows=1, chunksize=chunk_size)
    ):
        chunk.to_csv(os.path.join(dest_path, f"part_{i:02d}.csv"), index=False)


def write_chunk(dest_path, part, lines):
    """Write a chunk of lines to a file."""
    file_name = os.path.join(dest_path, f"part_{part:02d}.csv")
    with open(file_name, "w") as f_out:
        f_out.writelines(lines)


# def split_file(input_file, dest_path, chunk_size=DEFAULT_CHUNK_SIZE):
#     """Fetch main data."""
#     assert len(input_file) > 0

#     if not dest_path:
#         file_directory = os.path.dirname(input_file)
#         base_name = os.path.splitext(os.path.basename(input_file))[0]
#         dest_path = os.path.join(file_directory, base_name)

#     # split_by_pandas(file_name, output_dir)
#     split_csv_file(input_file, dest_path, chunk_size)

#     # # remove original file
#     # try:
#     #     os.remove(file_name)
#     #     print(f"File '{file_name}' deleted successfully.")
#     # except FileNotFoundError:
#     #     print(f"Error: File '{file_name}' not found.")


# if __name__ == "__main__":
#     util.setup_logging()
#     # _LOGGER = logging.getLogger(__name__)
#     _LOGGER.info("Starting script via main")

#     stats = split_csv_file("./temp/Azure_Actual_20230501-20230531_csv_Azure_ActualCost_v20230605T004903Z_574afa1e-0724-4291-a5f9-e82743b07f23.csv", skip_header=True, chunk_size=500000)
#     print(f"total stats: rows: {stats[-1][1]}, cost: {stats[-1][2]}")

#     parser = argparse.ArgumentParser(
#         description="Split File into Parts.",
#         add_help=True,
#     )
#     parser.add_argument(
#         "--file",
#         "-f",
#         help="Path to the file",
#     )
#     parser.add_argument(
#         "--output_dir",
#         "-o",
#         help="Output directory",
#     )
#     parser.add_argument(
#         "--chunk_size",
#         "-b",
#         help="Batch size",
#     )
#     parser.add_argument(
#         "--azcopy_path",
#         "-a",
#         help="Path to azcopy",
#     )
#     args = parser.parse_args()

#     FILE_PATH = args.client_id or os.environ.get("FILE_PATH")
#     OUTPUT_DIR = args.output_dir or os.environ.get("OUTPUT_DIR")
#     CHUNK_SIZE = args.chunk_size or os.environ.get("CHUNK_SIZE") or DEFAULT_CHUNK_SIZE
#     AZCOPY_PATH = (
#         args.azcopy_path or os.environ.get("AZCOPY_PATH") or DEFAULT_AZCOPY_PATH
#     )

#     now = datetime.datetime.now()
#     local_data_path = os.getenv("local_data_path")
#     run_time = now.strftime("%Y%m%d_%H%M")

#     # get path to azcopy
#     azcopy_file = os.getenv("azcopy_path")
#     azcopy_path = os.path.join(proj_dir, azcopy_file)

#     # Construct the absolute path to the 'data' folder
#     dest_path = os.path.join(proj_dir, "data", run_time)

#     if not FILE_PATH:
#         raise ValueError(
#             "file path is required. Have you set the FILE_PATH env variable?"
#         )

#     if not OUTPUT_DIR:
#         raise ValueError(
#             "output directory is required. Have you set the OUTPUT_DIR env variable?"
#         )

#     if not CHUNK_SIZE:
#         raise ValueError(
#             "batch size is required. Have you set the CHUNK_SIZE env variable?"
#         )

#     main(FILE_PATH, OUTPUT_DIR, CHUNK_SIZE)
