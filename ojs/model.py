from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import List, Optional
from xsdata.models.datatype import XmlDate

__NAMESPACE__ = "http://pkp.sfu.ca"


@dataclass
class Agencies:
    class Meta:
        name = "agencies"
        namespace = "http://pkp.sfu.ca"

    agency: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    locale: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


class ArticleStage(Enum):
    SUBMISSION = "submission"
    EXTERNAL_REVIEW = "externalReview"
    EDITORIAL = "editorial"
    PRODUCTION = "production"


@dataclass
class Citation:
    class Meta:
        name = "citation"
        namespace = "http://pkp.sfu.ca"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


@dataclass
class Citations:
    class Meta:
        name = "citations"
        namespace = "http://pkp.sfu.ca"

    citation: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    locale: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Disciplines:
    class Meta:
        name = "disciplines"
        namespace = "http://pkp.sfu.ca"

    discipline: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    locale: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


class EmbedEncoding(Enum):
    BASE64 = "base64"


@dataclass
class Href:
    class Meta:
        name = "href"

    src: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    mime_type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


class IdAdvice(Enum):
    UPDATE = "update"
    IGNORE = "ignore"


@dataclass
class Keywords:
    class Meta:
        name = "keywords"
        namespace = "http://pkp.sfu.ca"

    keyword: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    locale: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Languages:
    class Meta:
        name = "languages"
        namespace = "http://pkp.sfu.ca"

    language: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    locale: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class LocalizedNode:
    class Meta:
        name = "localizedNode"

    locale: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "pattern": r"([a-z]{2,3})((_[A-Z]{2})?)(@[a-z]{0,})?",
        },
    )
    content: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class Remote:
    class Meta:
        name = "remote"

    src: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Subjects:
    class Meta:
        name = "subjects"
        namespace = "http://pkp.sfu.ca"

    subject: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    locale: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class SubmissionFileRef:
    class Meta:
        name = "submission_file_ref"

    id: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


class SubmissionFileStage(Enum):
    PUBLIC = "public"
    SUBMISSION = "submission"
    NOTE = "note"
    REVIEW_FILE = "review_file"
    REVIEW_ATTACHMENT = "review_attachment"
    FINAL = "final"
    FAIR_COPY = "fair_copy"
    EDITOR = "editor"
    COPYEDIT = "copyedit"
    PROOF = "proof"
    PRODUCTION_READY = "production_ready"
    ATTACHMENT = "attachment"
    QUERY = "query"
    REVIEW_REVISION = "review_revision"
    DEPENDENT = "dependent"


@dataclass
class Embed:
    class Meta:
        name = "embed"

    encoding: Optional[EmbedEncoding] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    mime_type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    content: Optional[bytes] = field(
        default=None,
        metadata=dict(format="base64")
    )


@dataclass
class Id:
    class Meta:
        name = "id"
        namespace = "http://pkp.sfu.ca"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
        },
    )
    advice: IdAdvice = field(
        default=IdAdvice.IGNORE,
        metadata={
            "type": "Attribute",
        },
    )
    content: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class Identity:
    class Meta:
        name = "identity"

    givenname: List[LocalizedNode] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://pkp.sfu.ca",
            "min_occurs": 1,
        },
    )
    familyname: List[LocalizedNode] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://pkp.sfu.ca",
        },
    )
    affiliation: List[LocalizedNode] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://pkp.sfu.ca",
        },
    )
    country: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://pkp.sfu.ca",
        },
    )
    email: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://pkp.sfu.ca",
            "required": True,
        },
    )
    url: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://pkp.sfu.ca",
        },
    )
    orcid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://pkp.sfu.ca",
        },
    )
    biography: List[LocalizedNode] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://pkp.sfu.ca",
        },
    )


@dataclass
class IssueIdentification:
    class Meta:
        name = "issue_identification"
        namespace = "http://pkp.sfu.ca"

    volume: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    number: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    year: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    title: List[LocalizedNode] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )


@dataclass
class Title(LocalizedNode):
    class Meta:
        name = "title"
        namespace = "http://pkp.sfu.ca"


@dataclass
class UserGroup:
    class Meta:
        name = "user_group"
        namespace = "http://pkp.sfu.ca"

    role_id: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    context_id: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    is_default: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    show_title: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    permit_self_registration: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    permit_metadata_edit: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    name: List[LocalizedNode] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    abbrev: List[LocalizedNode] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    stage_assignments: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Author(Identity):
    class Meta:
        name = "author"
        namespace = "http://pkp.sfu.ca"

    primary_contact: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    user_group_ref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    include_in_browse: bool = field(
        default=True,
        metadata={
            "type": "Attribute",
        },
    )
    seq: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    id: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Cover:
    class Meta:
        name = "cover"
        namespace = "http://pkp.sfu.ca"

    cover_image: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    cover_image_alt_text: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    embed: Optional[Embed] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    locale: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class IssueFile:
    class Meta:
        name = "issue_file"
        namespace = "http://pkp.sfu.ca"

    file_name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    file_type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    file_size: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    content_type: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    original_file_name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    date_uploaded: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    date_modified: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    embed: Optional[Embed] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Representation:
    class Meta:
        name = "representation"
        namespace = "http://pkp.sfu.ca"

    id: List[Id] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    name: List[LocalizedNode] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    seq: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    submission_file_ref: List[SubmissionFileRef] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    remote: Optional[Remote] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    locale: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    url_path: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Section:
    class Meta:
        name = "section"
        namespace = "http://pkp.sfu.ca"

    id: List[Id] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    abbrev: List[LocalizedNode] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    policy: List[LocalizedNode] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    title: List[LocalizedNode] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    ref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    review_form_id: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    seq: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    editor_restricted: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    meta_indexed: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    meta_reviewed: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    abstracts_not_required: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    hide_title: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    hide_author: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    abstract_word_count: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class SubmissionFile:
    class Meta:
        name = "submission_file"
        namespace = "http://pkp.sfu.ca"

    id: List[Id] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    creator: List[LocalizedNode] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    description: List[LocalizedNode] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    name: List[LocalizedNode] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    publisher: List[LocalizedNode] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    source: List[LocalizedNode] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    sponsor: List[LocalizedNode] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    subject: List[LocalizedNode] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    submission_file_ref: Optional[SubmissionFileRef] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    file: List["SubmissionFile.File"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    caption: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    copyright_owner: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    created_at: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    credit: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    date_created: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    direct_sales_price: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    file_id: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    genre: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id_attribute: Optional[int] = field(
        default=None,
        metadata={
            "name": "id",
            "type": "Attribute",
        },
    )
    language: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    sales_type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    source_submission_file_id: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    stage: Optional[SubmissionFileStage] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    terms: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    updated_at: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    uploader: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    viewable: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )

    @dataclass
    class File:
        href: Optional[Href] = field(
            default=None,
            metadata={
                "type": "Element",
            },
        )
        embed: Optional[Embed] = field(
            default=None,
            metadata={
                "type": "Element",
            },
        )
        id: Optional[int] = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )
        filesize: Optional[int] = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )
        extension: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )


@dataclass
class UserGroups:
    class Meta:
        name = "user_groups"
        namespace = "http://pkp.sfu.ca"

    user_group: List[UserGroup] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class ArticleGalley(Representation):
    class Meta:
        name = "article_galley"
        namespace = "http://pkp.sfu.ca"

    approved: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    galley_type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Authors:
    class Meta:
        name = "authors"
        namespace = "http://pkp.sfu.ca"

    author: List[Author] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Covers:
    class Meta:
        name = "covers"
        namespace = "http://pkp.sfu.ca"

    cover: List[Cover] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class IssueGalley:
    class Meta:
        name = "issue_galley"
        namespace = "http://pkp.sfu.ca"

    label: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    id: List[Id] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    issue_file: Optional[IssueFile] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    locale: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Sections:
    class Meta:
        name = "sections"
        namespace = "http://pkp.sfu.ca"

    section: List[Section] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class IssueGalleys:
    class Meta:
        name = "issue_galleys"
        namespace = "http://pkp.sfu.ca"

    issue_galley: List[IssueGalley] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )


@dataclass
class Pkppublication:
    class Meta:
        name = "pkppublication"
        namespace = "http://pkp.sfu.ca"

    id: List[Id] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    title: List[Title] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    prefix: List[LocalizedNode] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    subtitle: List[LocalizedNode] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    abstract: List[LocalizedNode] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    coverage: List[LocalizedNode] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    type_value: List[LocalizedNode] = field(
        default_factory=list,
        metadata={
            "name": "type",
            "type": "Element",
        },
    )
    source: List[LocalizedNode] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    rights: List[LocalizedNode] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    license_url: Optional[str] = field(
        default=None,
        metadata={
            "name": "licenseUrl",
            "type": "Element",
        },
    )
    copyright_holder: List[LocalizedNode] = field(
        default_factory=list,
        metadata={
            "name": "copyrightHolder",
            "type": "Element",
        },
    )
    copyright_year: Optional[int] = field(
        default=None,
        metadata={
            "name": "copyrightYear",
            "type": "Element",
        },
    )
    keywords: List[Keywords] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    agencies: List[Agencies] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    languages: List[Languages] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    disciplines: List[Disciplines] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    subjects: List[Subjects] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    authors: Optional[Authors] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    article_galley: List[ArticleGalley] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    representation: List[Representation] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    citations: List[Citations] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    date_submitted: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    date_published: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    version: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    status: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    primary_contact_id: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    url_path: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Publication(Pkppublication):
    class Meta:
        name = "publication"
        namespace = "http://pkp.sfu.ca"

    issue_identification: Optional[IssueIdentification] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    pages: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    covers: Optional[Covers] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    issue_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "issueId",
            "type": "Element",
        },
    )
    section_ref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    seq: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    access_status: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Submission:
    class Meta:
        name = "submission"
        namespace = "http://pkp.sfu.ca"
        schemaLocation = "http://pkp.sfu.ca native.xsd"

    id: List[Id] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    submission_file: List[SubmissionFile] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    publication: List[Publication] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    pkppublication: List[Pkppublication] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    status: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    current_publication_id: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    date_submitted: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    submission_progress: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    locale: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Article(Submission):
    class Meta:
        name = "article"
        namespace = "http://pkp.sfu.ca"

    stage: Optional[ArticleStage] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Articles:
    class Meta:
        name = "articles"
        namespace = "http://pkp.sfu.ca"

    article: List[Article] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )


@dataclass
class Issue:
    class Meta:
        name = "issue"
        namespace = "http://pkp.sfu.ca"

    id: List[Id] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    description: List[LocalizedNode] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    issue_identification: Optional[IssueIdentification] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    date_published: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    date_notified: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    last_modified: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    open_access_date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    sections: Optional[Sections] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    covers: Optional[Covers] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    issue_galleys: Optional[IssueGalleys] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    articles: Optional[Articles] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    journal_id: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    published: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    current: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    access_status: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    url_path: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Issues:
    class Meta:
        name = "issues"
        namespace = "http://pkp.sfu.ca"

    issue: List[Issue] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
