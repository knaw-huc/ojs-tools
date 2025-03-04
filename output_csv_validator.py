import argparse
import re
from datetime import date
import os.path

import numpy as np
import pandas
from pandas import DataFrame, Series

columns = [
    {
        "name": "id",
        "required": True,
        "nullable": False,
        "type": int
    },
    {
        "name": "title",
        "required": True,
        "nullable": False,
        "type": str
    },
    {
        "name": "publication",
        "required": True,
        "nullable": False,
        "type": str
    },
    {
        "name": "abstract",
        "required": True,
        "nullable": True,
        "type": str
    },
    {
        "name": "file",
        "required": True,
        "nullable": False,
        "type": str
    },
    {
        "name": "publication_date",
        "required": True,
        "nullable": False,
        "type": date
    },
    {
        "name": "volume",
        "required": True,
        "nullable": False,
        "type": int
    },
    {
        "name": "year",
        "required": True,
        "nullable": False,
        "type": int
    },
    {
        "name": "issue",
        "required": True,
        "nullable": False,
        "type": str
    },
    {
        "name": "page_number",
        "required": True,
        "nullable": True,
        "type": str
    },
    {
        "name": "section_title",
        "required": True,
        "nullable": False,
        "type": str
    },
    {
        "name": "section_policy",
        "required": True,
        "nullable": False,
        "type": str
    },
    {
        "name": "section_reference",
        "required": True,
        "nullable": False,
        "type": str
    },
    {
        "name": "doi",
        "required": False,
        "nullable": True,
        "type": str
    },
    {
        "name": "author_given_name_0",
        "required": True,
        "nullable": False,
        "type": str
    },
    {
        "name": "author_family_name_0",
        "required": True,
        "nullable": True,
        "type": str
    },
    {
        "name": "author_given_name_1",
        "required": False,
        "nullable": True,
        "type": str
    },
    {
        "name": "author_family_name_1",
        "required": False,
        "nullable": True,
        "type": str
    },
    {
        "name": "author_given_name_2",
        "required": False,
        "nullable": True,
        "type": str
    },
    {
        "name": "author_family_name_2",
        "required": False,
        "nullable": True,
        "type": str
    },
    {
        "name": "author_given_name_3",
        "required": False,
        "nullable": True,
        "type": str
    },
    {
        "name": "author_family_name_3",
        "required": False,
        "nullable": True,
        "type": str
    },
    {
        "name": "author_given_name_4",
        "required": False,
        "nullable": True,
        "type": str
    },
    {
        "name": "author_family_name_4",
        "required": False,
        "nullable": True,
        "type": str
    },
    {
        "name": "author_given_name_5",
        "required": False,
        "nullable": True,
        "type": str
    },
    {
        "name": "author_family_name_5",
        "required": False,
        "nullable": True,
        "type": str
    },
    {
        "name": "author_given_name_6",
        "required": False,
        "nullable": True,
        "type": str
    },
    {
        "name": "author_family_name_6",
        "required": False,
        "nullable": True,
        "type": str
    },
    {
        "name": "author_given_name_7",
        "required": False,
        "nullable": True,
        "type": str
    },
    {
        "name": "author_family_name_7",
        "required": False,
        "nullable": True,
        "type": str
    },
    {
        "name": "author_given_name_8",
        "required": False,
        "nullable": True,
        "type": str
    },
    {
        "name": "author_family_name_8",
        "required": False,
        "nullable": True,
        "type": str
    },
    {
        "name": "author_given_name_9",
        "required": False,
        "nullable": True,
        "type": str
    },
    {
        "name": "author_family_name_9",
        "required": False,
        "nullable": True,
        "type": str
    },
    {
        "name": "keywords",
        "required": False,
        "nullable": True,
        "type": str
    }
]


def validate_writers(index:int , row: Series):
    for seq, given_name_key in enumerate(filter(lambda key: key.startswith("author_given_name"), row.keys())):
        family_name_key = given_name_key.replace("given_name", "family_name")

        if row[given_name_key] is np.nan and row[family_name_key] is not np.nan:
            print(f"Row with index {index} has empty value for column {given_name_key} and non empty value for column {family_name_key}. Writers should be identified by at least a given name.")

    pass


def validate_csv(csv: DataFrame):
    expected_columns = list(map(lambda column: column["name"], filter(lambda column: column["required"], columns)))

    actual_columns = list(csv.columns)

    missing_columns = [column for column in expected_columns if column not in actual_columns]

    if len(missing_columns) > 0:
        print("missing columns: ", missing_columns)

    iso_date_pattern = r"'^\d{4}-\d{2}-\d{2}$'"

    for index, row in csv.iterrows():
        index = index + 2
        for column in columns:
            if column["name"] not in missing_columns:
                column_name = column["name"]
                if not column["nullable"]:
                    value = row[column_name]
                    column_type = column["type"]
                    if value is np.nan:
                        print(f"Row with index {index} has empty value for non-empty column {column_name}.")
                    elif column_type == date:
                        if not (isinstance(value, str) or not re.match(iso_date_pattern, value)):
                            print(f"'{value}' is not a valid date string for {column_name} for row with index {index}")
                    elif not isinstance(value, column_type):
                        print(f"Expected {column_type} for column {column_name} but found {type(value)} for row with "
                              f"index {index}")

        validate_writers(index, row)

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
