import argparse
import os.path
import traceback
import xml.etree.ElementTree as ET
from typing import List

import base64

import numpy as np
import pandas
from pandas import DataFrame, Series, isna
from xmlschema import XMLSchema
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig
from xsdata.models.datatype import XmlDate

from ojs import Issue, IssueIdentification, Sections, Section, Articles, Article, ArticleStage, SubmissionFile, \
    SubmissionFileStage, Embed, Publication, Author, Authors, ArticleGalley, SubmissionFileRef, Id, LocalizedNode, \
    IssueGalleys, Title, IdAdvice, Keywords


class SubmissionFileCreator:
    def __init__(self, genre: str, default_locale: str):
        self.default_locale = default_locale
        self.genre = genre

    def create_submission_file(self, file_id: int, publication_date: str, file_path: str=None, 
                                base64_file: str = None, file_extension: str = None, file_name: str = None) -> SubmissionFile:

        """
        file_id: unique file ID, required
        publication_date: the date of publication of the file, required

        either one of these two is required:
        file_path: path to a file on disk
        base64_file: base64-encoded content of a file

        only required if using bse64_file:
        file_name: if not provided inferred from the file path (or defaults to 'file_<file_id>' for Base64 input)
        file extension: extension of the file
        """

        #check if either file path or base 64 file, and not both:
        if file_path and base64_file:
            raise ValueError(f"{file_id}: Provide either 'file_path' or 'base64_file', but not both.")
        if not file_path and not base64_file:
            raise ValueError(f"{file_id}: Either 'file_path' or 'base64_file' must be provided.")

        submission_file = SubmissionFile()
        submission_file.stage = SubmissionFileStage.PROOF
        submission_file.file_id = file_id
        submission_file.id_attribute = file_id

        #check what the source of the file is
        if file_path:
            #read from the file path
            file_name = file_name or os.path.basename(file_path)
            with open(file_path, mode="rb") as file:
                file_bytes = file.read()
                file_size = len(file_bytes)
            # Extract file extension from file path
            file_extension = file_extension or file_path.split(".")[-1]

        elif base64_file:
            #use base64 input
            if not file_extension:
                raise ValueError(f"{file_id}: file extension must be provided when using base64_file")

            #estimate file size    
            file_bytes = base64.b64decode(base64_file)
            file_size = len(file_bytes)
            
            #set file name
            #file_name or 
            file_name = f"file_{file_id}"

        #add localized name
        add_localized_node(submission_file.name, self.default_locale, file_name)

        #set date and genre
        submission_file.created_at = XmlDate.from_string(publication_date)
        submission_file.genre = self.genre

        #create metadata
        file_holder = SubmissionFile.File()
        file_holder.id = file_id
        file_holder.filesize = file_size
        
        #embed file content
        embed = Embed()
        embed.encoding = "base64"
        embed.content = base64_file if base64_file else base64.b64encode(file_bytes).decode("utf-8")
        file_holder.embed = embed
        
        file_holder.extension = file_extension

        submission_file.file = file_holder

        return submission_file


class AuthorAdder:
    def __init__(self, user_group_ref: str, default_locale: str):
        self.default_locale = default_locale
        self.user_group_ref = user_group_ref
        self.author_id: int = 1

    def add_authors(self, article_data: Series, publication: Publication):
        authors = Authors()

        for seq, key in enumerate(filter(lambda key: key.startswith("author_given_name"), article_data.keys())):
            given_name = article_data[key]

            if given_name is np.nan:
                break

            family_name = article_data[key.replace("given_name", "family_name")]
            affiliation_key = key.replace("given_name", "affiliation")
            author = Author()
            
            # Ensure locale is used correctly
            add_localized_node(author.givenname, self.default_locale, given_name)
            add_localized_node(author.familyname, self.default_locale, family_name)

            # Handle author affiliation
            if affiliation_key in article_data and article_data[affiliation_key] is not np.nan:
                add_localized_node(author.affiliation, self.default_locale, article_data[affiliation_key])

            # Handle missing country
            country_key = key.replace("given_name", "country")

            if country_key in article_data and article_data[country_key] is not np.nan:
                author.country = article_data[country_key]  # Assign directly (non-localized)
            else:
                author.country = ""  # Default to an empty string if missing

            #Handle missing email
            email_key = key.replace("given_name", "email")

            if email_key in article_data and article_data[email_key] is not np.nan:
                author.email = article_data[email_key]  # Assign directly (non-localized)
            else:
                author.email = ""  # Default to an empty string if missing


            author.seq = seq
            author.id = self.author_id
            self.author_id += 1
            author.user_group_ref = self.user_group_ref

            authors.author.append(author)

        if len(authors.author) > 0:
            publication.authors = authors
            publication.primary_contact_id = authors.author[0].id


class PublicationCreator:
    def __init__(self, author_adder: AuthorAdder, default_locale: str):
        self.default_locale = default_locale
        self.author_adder = author_adder

    def keywords_to_list(self, article_data_keywords):
        # If the value is not a string (e.g., NaN), return an empty list
        if not isinstance(article_data_keywords, str):
            return []
        return article_data_keywords.split('[;sep;]')


    def create_publication(self, article_data: Series, section_ref: str) -> Publication:
        publication = Publication()
        publication_id = Id()
        publication_id.content.append(article_data["id"])
        publication_id.type_value = "internal"
        publication.id.append(publication_id)
        if "doi" in article_data.keys():
            doi_id = Id()
            doi_id.advice = IdAdvice.UPDATE
            doi_id.content.append(article_data["doi"])
            doi_id.type_value = "doi"
            publication.id.append(doi_id)

        if "keywords" in article_data.keys():
            keyword_list = self.keywords_to_list(article_data["keywords"])
            if keyword_list:  # only add <keywords> if there are actual keywords
                keyword_node = Keywords()
                keyword_node.keyword.extend(keyword_list)
                keyword_node.locale = locale
                publication.keywords.append(keyword_node)
    

        publication.section_ref = section_ref
        publication.status = 3
        publication.date_published = XmlDate.from_string(article_data["publication_date"])
        title = Title()
        title.content.append(article_data["title"])

        title.locale = locale
        publication.title.append(title)
        add_localized_node(publication.abstract, locale, article_data["abstract"])
        publication.pages = article_data["page_number"]

        self.author_adder.add_authors(article_data, publication)

        galley = ArticleGalley()

        if args.file_input == 'file_path':
            galley.name = os.path.basename(article_data["file"])
        elif args.file_input == 'base64':
            galley.name = 'PDF'
        else:
            raise ValueError(f"{file_id}: Either 'file_path' or 'base64_file' must be provided.")

        galley.locale = self.default_locale
        galley.seq = 0
        ref = SubmissionFileRef()
        ref.id = article_data["id"]
        galley.submission_file_ref.append(ref)
        publication.article_galley.append(galley)

        return publication


def add_identification(issue_data: DataFrame, issue: Issue, journal_name: str):
    identification = IssueIdentification()
    identification.year = int(issue_data["year"].iloc[0])
    identification.volume = int(issue_data["volume"].iloc[0])
    identification.number = issue_data["issue"].iloc[0]
    identification.title = journal_name
    issue.issue_identification = identification


def add_localized_node(localized_nodes: List[LocalizedNode], locale: str, content: str):
    node = LocalizedNode()
    if isna(content):
        content = ""
    node.content.append(content)
    node.locale = locale
    localized_nodes.append(node)


def add_articles(issue: Issue, issue_data: DataFrame, publication_creator: PublicationCreator,
                 submission_file_creator: SubmissionFileCreator, default_locale: str, file_input: str = 'file_path'):
    added_sections = []
    sections = Sections()
    articles = Articles()

    for index, article_data in issue_data.iterrows():
        section_ref = article_data["section_reference"]
        if section_ref not in added_sections:
            section = Section()
            section.ref = section_ref
            add_localized_node(section.title, locale, article_data["section_title"])
            section.seq = 0
            add_localized_node(section.policy, locale, article_data["section_policy"])
            add_localized_node(section.abbrev, locale, section_ref)
            section.abstract_word_count = 250
            sections.section.append(section)
            added_sections.append(section_ref)

        # Create SubmissionFile based on file_input
        if file_input == 'file_path':
            submission_file = submission_file_creator.create_submission_file(
                file_id=article_data["id"],
                publication_date=article_data["publication_date"],
                file_path=article_data["file"]
            )
        elif file_input == 'base64':
            submission_file = submission_file_creator.create_submission_file(
                file_id=article_data["id"],
                publication_date=article_data["publication_date"],
                base64_file=article_data["file"],  # 'file' column contains Base64 content
                file_extension = 'pdf'
            )
        else:
            raise ValueError(f"Invalid file_input: {file_input}. Must be 'file_path' or 'base64'.")

        article = Article()
        article.locale = default_locale
        article.stage = ArticleStage.PRODUCTION
        article.current_publication_id = article_data["id"]
        article.status = "3"
        article.submission_file = submission_file
        article.publication = publication_creator.create_publication(article_data, section_ref)
        articles.article.append(article)

    issue.sections = sections
    issue.articles = articles


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv_file", type=str, required=True)
    parser.add_argument("--output_path", type=str, required=True)
    parser.add_argument("--journal_name", type=str, required=True)
    parser.add_argument("--author_group", type=str, default="Author")
    parser.add_argument("--submission_file_genre", type=str, default="Article Text")
    parser.add_argument("--locale", type=str, default="en")
    parser.add_argument("--file_input", type=str, default='file_path')

    args = parser.parse_args()

    locale = args.locale
    author_adder = AuthorAdder(args.author_group, locale)
    publication_creator = PublicationCreator(author_adder, locale)
    submission_file_creator = SubmissionFileCreator(args.submission_file_genre, locale)

    data = pandas.read_csv(args.csv_file, delimiter=";", dtype={'issue': str})

    publications = data["publication"].unique()

    config = SerializerConfig(
        indent="  ",
        ignore_default_attributes=True,
        schema_location="http://pkp.sfu.ca native.xsd",
        # no_namespace_schema_location=None
    )
    xml_serializer = XmlSerializer(config=config)
    xml_schema = XMLSchema("./xsd/native.xsd")
    for issue_identifier in publications:
        try:
            publication_data = data[data["publication"].isin([issue_identifier])]

            year = publication_data["year"].iloc[0]
            issue_number = publication_data["issue"].iloc[0].replace("/", "_")
            file_name = f"{year}_{issue_number}.xml"
            print(publication_data["id"].iloc[0], ": ", file_name)

            issue = Issue()
            add_identification(publication_data, issue, args.journal_name)
            galleys = IssueGalleys()
            issue.issue_galleys = galleys

            add_articles(issue, publication_data, publication_creator, submission_file_creator, locale, file_input=args.file_input)


            issue.published = 1
            issue.current = 0
            issue.date_published = XmlDate.from_string(publication_data["publication_date"].iloc[0])

            xml_string = xml_serializer.render(issue, ns_map={None: "http://pkp.sfu.ca"})
            etree = ET.fromstring(xml_string)
            xml_schema.validate(etree)
            if xml_schema.is_valid(etree):
                with open(f"{args.output_path}/{file_name}", "w", encoding='utf-8') as output:
                    output.write(xml_string)
                    output.flush()

        except Exception as ex:
            print(ex)
            traceback.print_exc()
        print("----------------------------------------------------")
