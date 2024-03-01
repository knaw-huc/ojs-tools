import argparse
import traceback

import numpy as np
import pandas
from pandas import DataFrame, Series
import xml.etree.ElementTree as ET
from xmlschema import XMLSchema
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig
from xsdata.models.datatype import XmlDate

from ojs import Issue, IssueIdentification, Sections, Section, Articles, Article, ArticleStage, SubmissionFile, \
    SubmissionFileStage, Embed, Publication, Author, Authors, ArticleGalley, SubmissionFileRef, Id


def create_submission_file(file_name: str, file_id: int, files_folder: str) -> SubmissionFile:
    submission_file = SubmissionFile()
    submission_file.stage = SubmissionFileStage.SUBMISSION
    submission_file.file_id = file_id
    submission_file.id_attribute = file_id
    submission_file.name = file_name
    submission_file.created_at = XmlDate.today()
    submission_file.genre = "Article Text"

    with open(rf"{files_folder}/{file_name}", mode="rb") as file:
        file_bytes = file.read()
        file_size = len(file_bytes)

        file_holder = SubmissionFile.File()
        file_holder.id = file_id
        file_holder.filesize = file_size
        embed = Embed()
        embed.encoding = "base64"
        embed.content = file_bytes
        file_holder.embed = embed
        if "." in file_name:
            file_holder.extension = file_name.split(".")[-1]

        submission_file.file = file_holder

    return submission_file


author_id: int = 1


def create_publication(article_data: Series, section_ref: str) -> Publication:
    global author_id
    publication = Publication()
    publication_id = Id()
    publication_id.content.append(article_data["id"])
    publication_id.type_value = "internal"
    publication.id.append(publication_id)
    publication.section_ref = section_ref
    publication.status = 3
    publication.date_published = XmlDate.today()
    publication.title.append(article_data["titel"])
    publication.abstract.append(article_data["abstract"])
    publication.pages = article_data["pagina"]

    add_authors(article_data, publication)

    galley = ArticleGalley()
    galley.name = article_data["document"]
    galley.seq = 0
    ref = SubmissionFileRef()
    ref.id = article_data["id"]
    galley.submission_file_ref.append(ref)
    publication.article_galley.append(galley)

    return publication


def add_authors(article_data: Series, publication: Publication):
    global author_id
    authors = Authors()
    for seq, key in enumerate(filter(lambda key: key.startswith("auteur_voornaam"), article_data.keys())):
        given_name = article_data[key]

        if given_name is np.nan:
            break

        family_name = article_data[key.replace("voornaam", "achternaam")]
        author = Author()
        author.givenname = given_name
        author.familyname = family_name
        author.country = ""  # needed for a valid xml
        author.email = ""  # needed for a valid xml
        author.seq = seq
        author.id = author_id
        author_id += 1
        author.user_group_ref = "Author"

        authors.author.append(author)
    if len(authors.author) > 0:
        publication.authors = authors
        publication.primary_contact_id = authors.author[0].id


def create_articles(issue_data: DataFrame, section_ref: str, files_folder: str) -> Articles:
    articles = Articles()
    for index, article_data in issue_data.iterrows():
        article = Article()
        article.stage = ArticleStage.PRODUCTION
        article.current_publication_id = article_data["id"]
        article.status = "3"
        article.submission_file = create_submission_file(article_data["document"], article_data.get("id"), files_folder)
        article.publication = create_publication(article_data, section_ref)
        articles.article.append(article)

    return articles


def add_identification(issue_data: DataFrame, issue: Issue):
    identification = IssueIdentification()
    identification.year = int(issue_data["jaar"].iloc[0])
    identification.volume = int(issue_data["jaargang"].iloc[0])
    identification.number = int(issue_data["nummer"].iloc[0])
    identification.title = "Tijdschrift voor Hoger Onderwijs"
    issue.issue_identification = identification


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv_file", type=str, required=True)
    parser.add_argument("--files_path", type=str, required=True)
    parser.add_argument("--output_path", type=str, required=True)

    args = parser.parse_args()

    data = pandas.read_csv(args.csv_file, delimiter=";")
    data = data.sort_values(by=["jaar", "nummer", "sorteer", "pagina"])

    issues = data["editie"].unique()

    config = SerializerConfig(
        indent="  ",
        ignore_default_attributes=True,
        schema_location="http://pkp.sfu.ca native.xsd",
        # no_namespace_schema_location=None
    )
    xml_serializer = XmlSerializer(config=config)
    xml_schema = XMLSchema("./xsd/native.xsd")
    for issue_identifier in issues:
        try:
            issue_data = data[data["editie"].isin([issue_identifier])]

            year = issue_data["jaar"].iloc[0]
            number = issue_data["nummer"].iloc[0]
            file_name = f"{year}_{number}.xml"
            print(issue_data["id"].iloc[0], ": ", file_name)

            issue = Issue()
            add_identification(issue_data, issue)

            sections = Sections()
            articles_section = Section()
            articles_section.ref = "ART"
            articles_section.title = "Articles"
            articles_section.seq = 0
            articles_section.policy = "Section default policy"
            sections.section.append(articles_section)

            issue.articles = create_articles(issue_data, articles_section.ref, args.files_path)
            issue.published = 1
            issue.current = 1

            xml_string = xml_serializer.render(issue, ns_map={None: "http://pkp.sfu.ca"})
            etree = ET.fromstring(xml_string)
            xml_schema.validate(etree)
            if xml_schema.is_valid(etree):
                with open(f"{args.output_path}/{file_name}", "w") as output:
                    output.write(xml_string)
                    output.flush()

        except Exception as ex:
            print(ex)
            traceback.print_exc()
        print("----------------------------------------------------")
