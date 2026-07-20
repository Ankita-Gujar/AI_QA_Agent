import fitz
import os


def render_page(pdf_path, page_number, output_folder):

    os.makedirs(output_folder, exist_ok=True)

    doc = fitz.open(pdf_path)

    page = doc.load_page(page_number)

    # High resolution rendering
    matrix = fitz.Matrix(2.5, 2.5)

    pix = page.get_pixmap(matrix=matrix)

    image_path = os.path.join(
        output_folder,
        f"page_{page_number + 1}.png"
    )

    pix.save(image_path)

    doc.close()

    return image_path