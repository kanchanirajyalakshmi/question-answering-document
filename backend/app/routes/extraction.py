from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.document import Document
from app.services.document_extractor import extract_document

router = APIRouter(
    prefix="/documents",
    tags=["Document Extraction"]
)


@router.post("/{document_id}/extract")
def extract_uploaded_document(
    document_id: str,
    db: Session = Depends(get_db)
):
    document = db.query(Document).filter(
        Document.id == document_id
    ).first()

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    try:
        result = extract_document(
            document.file_path,
            document_id=document_id
        )

        result["filename"] = document.original_filename

        document.status = "extracted"
        db.commit()

        return {
            "success": True,
            "message": "Document extracted successfully",
            "data": result
        }

    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Stored document file not found"
        )

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error)
        )