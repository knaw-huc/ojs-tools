import argparse
import os.path
import re
from datetime import date

import pandas
from pandas import DataFrame


def process_publication(publication_string: str):
    count_dash = publication_string.count(" - ")
    split_publication = publication_string.split(" - ")
    volume = split_publication[0].split(" ")[1]
    if count_dash == 2:
        year = split_publication[1]
        issue = split_publication[2]
    elif count_dash == 1:
        year_issue = split_publication[1].split("/")
        year = year_issue[0]
        if len(year_issue) == 3:
            issue = year_issue[1] + "/" + year_issue[2]
        else:
            issue = year_issue[1]

    return volume, year, issue


def process_page_number(reference_string: str):
    if not isinstance(reference_string, str):
        return ""
    elif "," in reference_string:
        return reference_string.split(", ")[-1].strip(".")
    else:
        return reference_string.split(" ")[-1]


def fix_unicode(value: str):
    if isinstance(value, str):
        unicode_chars = re.findall("(&#\\d+;)", value)

        for unicode_char in unicode_chars:
            value = value.replace(unicode_char, chr(int(unicode_char.strip("&#;"))))

        value = value.replace("&eacute;", "é")
        value = value.replace("&ecirc;", "ê")
        value = value.replace("&egrave;", "è")
        value = value.replace("&euml;", "ë")
        value = value.replace("&euro;", "€")
        value = value.replace("&iuml;", "ï")

    return value


def split_authors(authors_string: str):
    if not isinstance(authors_string, str):
        return ""

    authors_string = (authors_string.replace(" &", ",").replace(" en", ",")
                      .replace(",,", ","))

    return authors_string.split(", ")


def process_authors(data: DataFrame):
    authors_columns = {}
    authors_lists = data["auteurs"].map(lambda authors: split_authors(authors)).tolist()
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

        first_name = " ".join(author_names[0:start_of_surname])
        surname = " ".join(author_names[start_of_surname:])

    return first_name, surname


months = {"mrt": 3, "jun": 6, "sep": 9, "dec": 12}


def process_publication_date(date_string:str):
    global months
    date_split = date_string.split("-")
    month = months[date_split[1]]
    year_two_digit = int(date_split[2])
    year = year_two_digit + 2000 if year_two_digit < 88 else year_two_digit + 1900

    return str(date(year, month, int(date_split[0])))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_csv", type=str, required=True)
    parser.add_argument("--output_csv", type=str, required=True)
    parser.add_argument("--files_path", help="folder that contains the files mentioned in the input_csv",
                        type=str, required=True)
    args = parser.parse_args()
    files_path = args.files_path

    csv = pandas.read_csv(args.input_csv, delimiter=";", header=0)

    csv["titel"] = csv["titel"].map(lambda titel: fix_unicode(titel))
    csv["auteurs"] = csv["auteurs"].map(lambda auteurs: fix_unicode(auteurs))
    csv["abstract"] = csv["abstract"].map(lambda abstract: fix_unicode(abstract))

    csv["volume"], csv["year"], csv["issue"] = zip(*csv["editie"].map(lambda editie: process_publication(editie)))
    csv["page_number"] = csv["referentie"].map(lambda referentie: process_page_number(referentie))
    csv["Datum"] = csv["Datum"].map(lambda datum: process_publication_date(datum))
    csv["document"] = csv["document"].map(lambda document: os.path.join(files_path, document))
    csv = csv.assign(section_title=["Artikelen"] * len(csv))
    csv = csv.assign(section_policy=["Standaard"] * len(csv))
    csv = csv.assign(section_reference=["ART"] * len(csv))
    process_authors(csv)

    csv = csv[csv["Status"] != "Hoeft niet"]
    csv = csv.sort_values(["year", "issue", "sorteer", "page_number"])

    csv = csv.drop(["referentie", "auteurs", "Status", "sorteer"], axis=1)
    csv = csv.rename(columns={"titel": "title", "editie": "publication", "document": "file", "sorteer": "order",
                              "Datum": "publication_date"})

    csv.to_csv(args.output_csv, sep=";", index=False)
