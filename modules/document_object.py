from dataclasses import dataclass, field


# -------------------------------------------------------
# Paragraph Object
# -------------------------------------------------------

@dataclass
class ParagraphObject:

    id: int

    page: int

    text: str

    bbox: tuple

    x: float
    y: float

    width: float
    height: float

    font_name: str

    font_size: float

    font_color: int

    bold: bool

    italic: bool

    line_count: int

    span_count: int

    text_length: int


# -------------------------------------------------------
# Image Object
# -------------------------------------------------------

@dataclass
class ImageObject:

    id: int

    page: int

    bbox: tuple

    x: float
    y: float

    width: float
    height: float


# -------------------------------------------------------
# Table Object
# -------------------------------------------------------

@dataclass
class TableObject:

    id: int

    page: int

    bbox: tuple

    x: float
    y: float

    width: float
    height: float

    rows: int = 0

    columns: int = 0


# -------------------------------------------------------
# Page Object
# -------------------------------------------------------

@dataclass
class PageObject:

    page_number: int

    width: float

    height: float

    rotation: int

    paragraphs: list = field(default_factory=list)

    images: list = field(default_factory=list)

    tables: list = field(default_factory=list)


# -------------------------------------------------------
# Document Object
# -------------------------------------------------------

@dataclass
class DocumentObject:

    file_name: str

    total_pages: int

    pages: list = field(default_factory=list)


# -------------------------------------------------------
# Build Document Object Model
# -------------------------------------------------------

def build_document_object(pdf_data):

    document = DocumentObject(

        file_name=pdf_data["file_name"],

        total_pages=pdf_data["total_pages"]

    )

    for page in pdf_data["pages"]:

        page_object = PageObject(

            page_number=page["page_number"],

            width=page["width"],

            height=page["height"],

            rotation=page["rotation"]

        )

        # ---------------------------------------------------
        # Paragraphs
        # ---------------------------------------------------

        for para in page["paragraphs"]:

            paragraph = ParagraphObject(

                id=para["id"],

                page=page["page_number"],

                text=para["text"],

                bbox=para["bbox"],

                x=para["x"],

                y=para["y"],

                width=para["width"],

                height=para["height"],

                font_name=para["font_name"],

                font_size=para["font_size"],

                font_color=para["font_color"],

                bold=para["bold"],

                italic=para["italic"],

                line_count=para["line_count"],

                span_count=para["span_count"],

                text_length=para["text_length"]

            )

            page_object.paragraphs.append(paragraph)

        # ---------------------------------------------------
        # Images
        # ---------------------------------------------------

        for img in page["images"]:

            image = ImageObject(

                id=img["id"],

                page=page["page_number"],

                bbox=img["bbox"],

                x=img["x"],

                y=img["y"],

                width=img["width"],

                height=img["height"]

            )

            page_object.images.append(image)

        # ---------------------------------------------------
        # Tables
        # ---------------------------------------------------

        for tbl in page["tables"]:

            table = TableObject(

                id=tbl["id"],

                page=page["page_number"],

                bbox=tbl["bbox"],

                x=tbl["x"],

                y=tbl["y"],

                width=tbl["width"],

                height=tbl["height"],

                rows=tbl.get("rows", 0),

                columns=tbl.get("columns", 0)

            )

            page_object.tables.append(table)

        document.pages.append(page_object)

    return document