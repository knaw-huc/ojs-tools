import argparse

import pandas
import re

from pandas import DataFrame


def process_editie(editie_string: str):
    count_dash = editie_string.count(" - ")
    split_editie = editie_string.split(" - ")
    jaargang = split_editie[0].split(" ")[1]
    if count_dash == 2:
        jaar = split_editie[1]
        nummer = split_editie[2]
    elif count_dash == 1:
        jaar_nummer = split_editie[1].split("/")
        jaar = jaar_nummer[0]
        nummer = jaar_nummer[1]

    return jaargang, jaar, nummer


def process_page_number(referentie_string: str):
    # if isinstance(referentie_string, str)
    #     page_range = referentie_string.split(", ")[-1].strip(".").split("-")
    #     from_page = page_range[0]
    #     to_page = page_range[-1]
    #     return from_page, to_page
    # else:
    #     return "", ""
    return referentie_string.split(", ")[-1].strip(".") if isinstance(referentie_string, str) else ""


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
    global index
    authors_columns = {}
    authors_lists = data["auteurs"].map(lambda authors: split_authors(authors)).tolist()
    ordered_authors_lists = authors_lists.copy()
    ordered_authors_lists.sort(key=len, reverse=True)
    max_authors = len(ordered_authors_lists[0])
    for i in range(max_authors):
        authors_columns["auteur_voornaam_" + str(i)] = []
        authors_columns["auteur_achternaam_" + str(i)] = []
    for row in authors_lists:
        for index in range(max_authors):
            first_name = ""
            surname = ""
            if index < len(row):
                first_name, surname = split_author_names(row[index])

            authors_columns["auteur_voornaam_" + str(index)].append(first_name)
            authors_columns["auteur_achternaam_" + str(index)].append(surname)

    for i in range(max_authors):
        column_firstname = "auteur_voornaam_" + str(i)
        data[column_firstname] = authors_columns[column_firstname]
        column_surname = "auteur_achternaam_" + str(i)
        data[column_surname] = authors_columns[column_surname]


def split_author_names(name_string: str):
    first_name = ""
    surname = ""
    author_names = name_string.split(" ")
    if len(author_names) == 1:
        first_name = author_names[0]
    elif len(author_names) == 2:
        first_name = author_names[0]
        surname = author_names[1]
    else:
        prefixes = ["van", "de", "den", "der", "ten", "ter"]
        lowest_prefix_index = 1000
        for prefix in prefixes:
            if prefix in author_names and author_names.index(prefix) < lowest_prefix_index:
                lowest_prefix_index = author_names.index(prefix)

        start_of_surname = lowest_prefix_index if lowest_prefix_index < len(author_names) else -1
        first_name = " ".join(author_names[0:start_of_surname])
        surname = " ".join(author_names[start_of_surname:])

    return first_name, surname


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_csv", type=str, required=True)
    parser.add_argument("--output_csv", type=str, required=True)
    args = parser.parse_args()

    csv = pandas.read_csv(args.input_csv, delimiter=";", header=0)

    csv["titel"] = csv["titel"].map(lambda titel: fix_unicode(titel))
    csv["auteurs"] = csv["auteurs"].map(lambda auteurs: fix_unicode(auteurs))
    csv["abstract"] = csv["abstract"].map(lambda abstract: fix_unicode(abstract))

    csv["jaargang"], csv["jaar"], csv["nummer"] = zip(*csv["editie"].map(lambda editie: process_editie(editie)))
    csv["pagina"] = csv["referentie"].map(lambda referentie: process_page_number(referentie))
    # csv["van_pagina"], csv["tot_pagina"] = zip(*csv["referentie"].map(lambda referentie: process_page_number(referentie)))
    process_authors(csv)

    csv = csv.drop(["referentie", "auteurs"], axis=1)

    csv.to_csv(args.output_csv, sep=";", index=False)
