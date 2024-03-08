import argparse
import traceback
from typing import List

import numpy as np
import pandas
from pandas import DataFrame, Series
import xml.etree.ElementTree as ET
from xmlschema import XMLSchema
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig
from xsdata.models.datatype import XmlDate

from ojs import Issue, IssueIdentification, Sections, Section, Articles, Article, ArticleStage, SubmissionFile, \
    SubmissionFileStage, Embed, Publication, Author, Authors, ArticleGalley, SubmissionFileRef, Id, LocalizedNode, \
    IssueGalley, IssueGalleys, Title


def create_submission_file(file_name: str, file_id: int, files_folder: str, publication_date: str) -> SubmissionFile:
    submission_file = SubmissionFile()
    submission_file.stage = SubmissionFileStage.SUBMISSION
    submission_file.file_id = file_id
    submission_file.id_attribute = file_id
    add_localized_node(submission_file.name, "en", file_name)
    submission_file.created_at = XmlDate.from_string(publication_date)
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
    publication.date_published = XmlDate.from_string(article_data["publication_date"])
    title = Title()
    title.content.append(article_data["title"])
    title.locale = "en"
    publication.title.append(title)
    add_localized_node(publication.abstract, "en", article_data["abstract"])
    publication.pages = article_data["page_number"]

    add_authors(article_data, publication)

    galley = ArticleGalley()
    galley.name = article_data["file"]
    galley.locale = "en"
    galley.seq = 0
    ref = SubmissionFileRef()
    ref.id = article_data["id"]
    galley.submission_file_ref.append(ref)
    publication.article_galley.append(galley)

    return publication


def add_authors(article_data: Series, publication: Publication):
    global author_id
    authors = Authors()
    for seq, key in enumerate(filter(lambda key: key.startswith("author_given_name"), article_data.keys())):
        given_name = article_data[key]

        if given_name is np.nan:
            break

        family_name = article_data[key.replace("given_name", "family_name")]
        author = Author()
        add_localized_node(author.givenname, "en", given_name)
        add_localized_node(author.familyname, "en", family_name)
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
        article.locale = "en"
        article.stage = ArticleStage.PRODUCTION
        article.current_publication_id = article_data["id"]
        article.status = "3"
        article.submission_file = create_submission_file(
            article_data["file"], article_data.get("id"), files_folder, article_data["publication_date"]
        )
        article.publication = create_publication(article_data, section_ref)
        articles.article.append(article)

    return articles


def add_identification(issue_data: DataFrame, issue: Issue, journal_name: str):
    identification = IssueIdentification()
    identification.year = int(issue_data["year"].iloc[0])
    identification.volume = int(issue_data["volume"].iloc[0])
    identification.number = int(issue_data["issue"].iloc[0])
    identification.title = journal_name
    issue.issue_identification = identification


def add_localized_node(localized_nodes: List[LocalizedNode], locale: str, content: str):
    node = LocalizedNode()
    node.content.append(content)
    node.locale = locale
    localized_nodes.append(node)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv_file", type=str, required=True)
    parser.add_argument("--files_path", type=str, required=True)
    parser.add_argument("--output_path", type=str, required=True)
    parser.add_argument("--journal_name", type=str, required=True)

    args = parser.parse_args()

    data = pandas.read_csv(args.csv_file, delimiter=";")

    publiations = data["publication"].unique()

    config = SerializerConfig(
        indent="  ",
        ignore_default_attributes=True,
        schema_location="http://pkp.sfu.ca native.xsd",
        # no_namespace_schema_location=None
    )
    xml_serializer = XmlSerializer(config=config)
    xml_schema = XMLSchema("./xsd/native.xsd")
    for issue_identifier in publiations:
        try:
            publication_data = data[data["publication"].isin([issue_identifier])]

            year = publication_data["year"].iloc[0]
            issue_number = publication_data["issue"].iloc[0]
            file_name = f"{year}_{issue_number}.xml"
            print(publication_data["id"].iloc[0], ": ", file_name)

            issue = Issue()
            add_identification(publication_data, issue, args.journal_name)
            galleys = IssueGalleys()
            issue.issue_galleys = galleys

            sections = Sections()
            articles_section = Section()
            articles_section.ref = "ART"
            add_localized_node(articles_section.title, "en", "Articles")
            articles_section.seq = 0
            add_localized_node(articles_section.policy, "en", "Section default policy")
            articles_section.abstract_word_count = 250
            sections.section.append(articles_section)

            issue.articles = create_articles(publication_data, articles_section.ref, args.files_path)
            issue.published = 1
            issue.current = 0
            issue.date_published = XmlDate.from_string(publication_data["publication_date"].iloc[0])

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
