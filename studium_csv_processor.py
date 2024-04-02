import argparse
import os
import re

import pandas
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame

from output_csv_validator import validate_csv


def find_file(doi: str, file_path: str) -> str:
    found_files = []
    file_prefix = doi.split(".")[-1]
    for root, dir, files in os.walk(file_path):
        for file in files:
            if file.startswith(file_prefix):
                found_files.append(os.path.join(file_path, file))

    if len(found_files) != 1:
        raise RuntimeError(f"Found {len(found_files)} files expected 1")

    return found_files[0]


def fix_year_volume_and_issue(csv: DataFrame):
    different_issue_year = re.compile("^\\d-\\d{4}$")
    year_volume = {}
    for index, row in csv.iterrows():
        year = row["jaar"]
        if not year in year_volume.keys():
            year_volume[year] = row["volume"]

        issue = row["issue"]
        if different_issue_year.match(issue):
            year_issue = issue.split("-")
            csv.at[index, "jaar"] = int(year_issue[-1])
            csv.at[index, "volume"] = year_volume[int(year_issue[-1])]
            csv.at[index, "issue"] = year_issue[0]


def process_authors(data: DataFrame):
    authors_columns = {}
    authors_lists = data["authors"].map(lambda authors: authors.split(" | ")).tolist()
    ordered_authors_lists = authors_lists.copy()
    ordered_authors_lists.sort(key=len, reverse=True)
    max_authors = len(ordered_authors_lists[0])
    given_name = "author_given_name_"
    family_name = "author_family_name_"
    for i in range(max_authors):
        authors_columns[given_name + str(i)] = []
        authors_columns[family_name + str(i)] = []
    for row in authors_lists:
        for index in range(max_authors):
            first_name = ""
            surname = ""
            if index < len(row):
                first_name, surname = split_author_names(row[index])

            authors_columns[given_name + str(index)].append(first_name)
            authors_columns[family_name + str(index)].append(surname)

    for i in range(max_authors):
        column_given_name = given_name + str(i)
        data[column_given_name] = authors_columns[column_given_name]
        column_family_name = family_name + str(i)
        data[column_family_name] = authors_columns[column_family_name]


def split_author_names(name_string: str):
    first_name = ""
    surname = ""
    author_names = name_string.strip(" ").split(" ")
    if len(author_names) == 1:
        first_name = author_names[0]
    elif len(author_names) == 2:
        first_name = author_names[0]
        surname = author_names[1]
    else:
        prefixes = ["van", "de", "den", "der", "ten", "ter"]
        normalized_names = [name.casefold() for name in author_names]
        lowest_prefix_index = 1000
        for prefix in prefixes:
            if prefix.casefold() in normalized_names and normalized_names.index(prefix) < lowest_prefix_index:
                lowest_prefix_index = normalized_names.index(prefix)

        start_of_surname = -1
        if lowest_prefix_index < len(author_names):
            start_of_surname = lowest_prefix_index

        if author_names[start_of_surname - 1] == "-":
            start_of_surname = start_of_surname - 2
        elif "-" in author_names[start_of_surname - 1]:
            start_of_surname = start_of_surname - 1

        if name_string.lower() == "Van de redactie".lower():
            first_name = name_string
        else:
            first_name = " ".join(author_names[0:start_of_surname])
            surname = " ".join(author_names[start_of_surname:])

    return first_name, surname


def add_publication(csv: DataFrame):
    publications = []
    for index, row in csv.iterrows():
        publications.append(f"{row["jaar"]} / {row["issue"]}")

    csv["publication"] = publications


def process_web_page_data(link: str):
    page = requests.get(link)
    soup = BeautifulSoup(page.text, "html.parser")

    abstract_text = ""
    possible_abstracts = soup.find_all("div", {"class": "authors"})
    for abstract in possible_abstracts:
        if "Abstract" in abstract.text:
            abstract_text = abstract.text.replace("Abstract", "").strip()

    publication_date = soup.find("meta", {"name": "citation_publication_date"})

    return publication_date.attrs["content"], abstract_text


def language_to_locale(language):
    if language == "dut" or language == "nld" or language == "nl; en":
        return "nl"

    if language == "fr":
        return "fr_FR"

    return language


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_csv", type=str, required=True)
    parser.add_argument("--output_csv", type=str, required=True)
    parser.add_argument("--files_path", help="folder that contains the files mentioned in the input_csv",
                        type=str, required=True)
    args = parser.parse_args()
    files_path = args.files_path

    csv = pandas.read_csv(args.input_csv)

    csv["file"] = csv["doi"].map(lambda doi: find_file(doi, files_path))
    fix_year_volume_and_issue(csv)
    process_authors(csv)
    csv["id"] = csv.index
    csv = csv.assign(section_title=["Artikelen"] * len(csv))
    csv = csv.assign(section_policy=["Standaard"] * len(csv))
    csv = csv.assign(section_reference=["ART"] * len(csv))
    add_publication(csv)
    csv["publication_date"], csv["abstract"] = zip(*csv["link"].map(lambda link: process_web_page_data(link)))
    csv["locale"] = csv["language"].map(lambda language: language_to_locale(language))

    csv = csv[["id"] + [col for col in csv.columns if col != "id"]]
    csv = csv.rename(columns={"jaar": "year", "pages": "page_number", "titel": "title"})
    csv = csv.sort_values(["year", "issue", "doi"])
    csv = csv.drop(["doi", "link", "pdf", "xml", "authors", "keywords"], axis=1)

    validate_csv(csv)

    csv.to_csv(args.output_csv, sep=";", index=False)
