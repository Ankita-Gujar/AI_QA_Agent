import fitz
import os


def read_pdf(pdf_path):

    doc = fitz.open(pdf_path)

    pdf_data = {

        "file_name": os.path.basename(pdf_path),

        "total_pages": len(doc),

        "pages": []

    }

    # ----------------------------------------------------
    # Read Every Page
    # ----------------------------------------------------

    for page_number, page in enumerate(doc, start=1):

        page_info = {

            "page_number": page_number,

            "width": page.rect.width,

            "height": page.rect.height,

            "rotation": page.rotation,

            "paragraphs": [],

            "images": [],

            "tables": []

        }

        text_dict = page.get_text("dict")

        paragraph_id = 1

        # ----------------------------------------------------
        # Paragraph Extraction
        # ----------------------------------------------------

        for block in text_dict["blocks"]:

            if block["type"] != 0:
                continue

            full_text = ""

            font_name = ""

            font_size = 0

            font_color = 0

            bold = False

            italic = False

            line_count = 0

            span_count = 0

            for line in block["lines"]:

                line_count += 1

                for span in line["spans"]:

                    span_count += 1

                    full_text += span["text"]

                    font_name = span["font"]

                    font_size = span["size"]

                    font_color = span["color"]

                    bold = "bold" in font_name.lower()

                    italic = "italic" in font_name.lower()

                full_text += "\n"

            x0, y0, x1, y1 = block["bbox"]

            page_info["paragraphs"].append({

                "id": paragraph_id,

                "text": full_text.strip(),

                "bbox": block["bbox"],

                "x": x0,

                "y": y0,

                "width": x1 - x0,

                "height": y1 - y0,

                "font_name": font_name,

                "font_size": font_size,

                "font_color": font_color,

                "bold": bold,

                "italic": italic,

                "line_count": line_count,

                "span_count": span_count,

                "text_length": len(full_text.strip())

            })

            paragraph_id += 1

        # ----------------------------------------------------
        # Image Extraction
        # ----------------------------------------------------

        image_id = 1

        for img in page.get_images(full=True):

            xref = img[0]

            rects = page.get_image_rects(xref)

            if not rects:
                continue

            for rect in rects:

                page_info["images"].append({

                    "id": image_id,

                    "bbox": (

                        rect.x0,

                        rect.y0,

                        rect.x1,

                        rect.y1

                    ),

                    "x": rect.x0,

                    "y": rect.y0,

                    "width": rect.width,

                    "height": rect.height

                })

                image_id += 1

        # ----------------------------------------------------
        # Table Extraction
        # (Placeholder - We'll implement later)
        # ----------------------------------------------------

        page_info["tables"] = []

        pdf_data["pages"].append(page_info)

    doc.close()

    return pdf_data