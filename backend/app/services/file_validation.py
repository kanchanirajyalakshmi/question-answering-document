import csv
import io
import json
from pathlib import Path

import magic
import pymupdf

from app.database import settings
from docx import Document as DocxDocument
from pptx import Presentation
from openpyxl import load_workbook


MAX_FILE_SIZE = settings.MAX_FILE_SIZE_MB * 1024 * 1024

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".pptx",
    ".xlsx",
    ".txt",
    ".csv",
    ".html",
    ".json",
    ".md"
}


def validate_extension(filename: str):

    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError("Unsupported file format")

    return extension


def validate_file_size(content: bytes):

    if len(content) == 0:
        raise ValueError("Empty files are not allowed")

    if len(content) > MAX_FILE_SIZE:
        raise ValueError("File exceeds maximum size of 10 MB")


def validate_actual_content(content: bytes, extension: str):

    mime_type = magic.from_buffer(
        content[:2048],
        mime=True
    )

    if extension == ".pdf":

        if not content.startswith(b"%PDF-"):
            raise ValueError("Invalid PDF file")

        doc = pymupdf.open(stream=content, filetype="pdf")
        doc.close()

    elif extension == ".docx":

        if not content.startswith(b"PK"):
            raise ValueError("Invalid DOCX file")

        DocxDocument(io.BytesIO(content))

    elif extension == ".pptx":

        if not content.startswith(b"PK"):
            raise ValueError("Invalid PPTX file")

        Presentation(io.BytesIO(content))

    elif extension == ".xlsx":

        if not content.startswith(b"PK"):
            raise ValueError("Invalid XLSX file")

        workbook = load_workbook(
            io.BytesIO(content),
            read_only=True
        )

        workbook.close()

    elif extension == ".json":

        text = content.decode("utf-8-sig")
        json.loads(text)

    elif extension == ".csv":

        text = content.decode("utf-8-sig")

        reader = csv.reader(io.StringIO(text))

        for row in reader:
            pass

    elif extension in [".txt", ".md"]:

        content.decode("utf-8-sig")

    elif extension == ".html":

        text = content.decode("utf-8-sig").lower()

        if "<html" not in text and "<!doctype html" not in text:
            raise ValueError("Invalid HTML document")

    return mime_type
