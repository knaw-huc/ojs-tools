import argparse
import os.path

import numpy as np
import pandas
from pandas import DataFrame

expected_columns = list(
    ["id", "title", "publication", "abstract", "file", "publication_date", "volume", "year", "issue", "page_number",
     "section_title", "section_policy", "section_reference", "author_given_name_0", "author_family_name_0"])
non_null_columns = list(
    ["id", "title", "publication", "file", "publication_date", "volume", "year", "issue", "page_number",
     "section_title", "section_policy", "section_reference", "author_given_name_0"])


def validate_csv(csv: DataFrame):
    actual_columns = list(csv.columns)

    missing_columns = [column for column in expected_columns if column not in actual_columns]

    if len(missing_columns) > 0:
        print("missing columns: ", missing_columns)

    for index, row in csv.iterrows():
        for column in non_null_columns:
            if row[column] is np.nan:
                print(f"Row with index {index} has empty value for non-empty column {column}.")

    files = csv["file"]
    for file in files:
        if not os.path.exists(file):
            print(f"cannot find '{file}'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True)

    args = parser.parse_args()

    csv_path = args.csv
    csv = pandas.read_csv(csv_path, delimiter=';')

    validate_csv(csv)
