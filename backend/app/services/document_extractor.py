import os
import json
import pymupdf
import pandas as pd
import pytesseract

from PIL import Image
from io import BytesIO
from docx import Document
from pptx import Presentation
from openpyxl import load_workbook
from bs4 import BeautifulSoup

from app.utils.text_cleaner import clean_text


def extract_pdf(file_path):

    document = pymupdf.open(file_path)

    sections = []

    for page_number, page in enumerate(document, start=1):

        text = page.get_text("text")

        # OCR fallback for scanned pages
        if not text.strip():

            pix = page.get_pixmap(dpi=200)

            image = Image.open(
                BytesIO(pix.tobytes("png"))
            )

            text = pytesseract.image_to_string(image)

        sections.append({
            "page": page_number,
            "text": clean_text(text)
        })

    document.close()

    return sections
def extract_docx(file_path):

    doc = Document(file_path)

    sections = []

    for index, paragraph in enumerate(doc.paragraphs):

        text = clean_text(paragraph.text)

        if text:
            sections.append({
                "paragraph": index + 1,
                "text": text
            })

    # Extract tables too
    for table_index, table in enumerate(doc.tables):

        rows = []

        for row in table.rows:
            rows.append(" | ".join(
                cell.text.strip() for cell in row.cells
            ))

        sections.append({
            "table": table_index + 1,
            "text": "\n".join(rows)
        })

    return sections
def extract_pptx(file_path):

    presentation = Presentation(file_path)

    sections = []

    for slide_number, slide in enumerate(
        presentation.slides, start=1
    ):

        slide_text = []

        for shape in slide.shapes:

            if shape.has_text_frame:
                slide_text.append(shape.text)

            if shape.has_table:

                for row in shape.table.rows:
                    slide_text.append(
                        " | ".join(
                            cell.text for cell in row.cells
                        )
                    )

        sections.append({
            "slide": slide_number,
            "text": clean_text("\n".join(slide_text))
        })

    return sections
def extract_xlsx(file_path):

    workbook = load_workbook(
        file_path,
        read_only=True,
        data_only=True
    )

    sections = []

    for sheet in workbook.worksheets:

        rows = []

        for row in sheet.iter_rows(values_only=True):

            values = [
                str(value) if value is not None else ""
                for value in row
            ]

            if any(values):
                rows.append(" | ".join(values))

        sections.append({
            "sheet": sheet.title,
            "text": "\n".join(rows)
        })

    workbook.close()

    return sections
def extract_txt(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8-sig",
        errors="replace"
    ) as file:

        text = file.read()

    return [{
        "text": clean_text(text)
    }]


def extract_md(file_path):

    return extract_txt(file_path)
def extract_csv(file_path):

    dataframe = pd.read_csv(
        file_path,
        encoding="utf-8",
        on_bad_lines="skip"
    )

    text = dataframe.to_string(index=False)

    return [{
        "text": clean_text(text),
        "rows": len(dataframe),
        "columns": list(dataframe.columns)
    }]
def extract_html(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8",
        errors="replace"
    ) as file:

        html = file.read()

    soup = BeautifulSoup(html, "html.parser")

    # Remove non-visible or irrelevant elements
    for element in soup([
        "script",
        "style",
        "noscript"
    ]):
        element.decompose()

    text = soup.get_text(separator="\n")

    return [{
        "text": clean_text(text)
    }]
def extract_json(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    text = json.dumps(
        data,
        indent=2,
        ensure_ascii=False
    )

    return [{
        "text": clean_text(text)
    }]
def extract_document(file_path, document_id=None):

    if not os.path.exists(file_path):
        raise FileNotFoundError("Document not found")

    extension = os.path.splitext(file_path)[1].lower()

    extractors = {
        ".pdf": extract_pdf,
        ".docx": extract_docx,
        ".pptx": extract_pptx,
        ".xlsx": extract_xlsx,
        ".txt": extract_txt,
        ".md": extract_md,
        ".csv": extract_csv,
        ".html": extract_html,
        ".htm": extract_html,
        ".json": extract_json
    }

    if extension not in extractors:
        raise ValueError("Unsupported document format")

    sections = extractors[extension](file_path)

    # Combine extracted sections
    full_text = "\n\n".join(
        section["text"]
        for section in sections
        if section.get("text")
    )

    full_text = clean_text(full_text)

    if not full_text:
        raise ValueError("Document contains no extractable text")

    return {
        "document_id": document_id,
        "filename": os.path.basename(file_path),
        "file_type": extension,
        "text": full_text,
        "total_characters": len(full_text),
        "sections": sections,
        "status": "extracted"
    }