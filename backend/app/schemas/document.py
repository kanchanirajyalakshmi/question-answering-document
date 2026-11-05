from pydantic import BaseModel


class DocumentUploadResponse(BaseModel):

    document_id: str
    filename: str
    file_type: str
    file_size: int
    status: str
    message: str
