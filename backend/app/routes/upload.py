import os
import uuid

from pathlib import Path

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.document import Document

from app.schemas.document import DocumentUploadResponse

from app.services.file_validation import (
    validate_extension,
    validate_file_size,
    validate_actual_content
)


router = APIRouter(
    prefix="/documents",
    tags=["Document Upload"]
)


UPLOAD_DIR = Path("storage/uploads")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


@router.post(
    "/upload",
    response_model=DocumentUploadResponse
)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required"
        )

    original_filename = Path(file.filename).name

    if len(original_filename) > 255:
        raise HTTPException(
            status_code=400,
            detail="Filename is too long"
        )

    try:

        extension = validate_extension(
            original_filename
        )

        content = await file.read()

        validate_file_size(content)

        file_type = validate_actual_content(
            content,
            extension
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="File content is invalid or corrupted"
        )

    document_id = str(uuid.uuid4())

    stored_filename = (
        document_id + extension
    )

    file_path = UPLOAD_DIR / stored_filename

    try:

        with open(file_path, "xb") as output_file:
            output_file.write(content)

        document = Document(
            id=document_id,
            original_filename=original_filename,
            stored_filename=stored_filename,
            file_path=str(file_path),
            file_type=extension,
            file_size=len(content),
            status="uploaded"
        )

        db.add(document)

        db.commit()

        db.refresh(document)

    except Exception:

        db.rollback()

        if file_path.exists():
            os.remove(file_path)

        raise HTTPException(
            status_code=500,
            detail="Failed to store document"
        )

    finally:

        await file.close()

    return DocumentUploadResponse(
        document_id=document.id,
        filename=document.original_filename,
        file_type=document.file_type,
        file_size=document.file_size,
        status=document.status,
        message="Document uploaded successfully"
    )
