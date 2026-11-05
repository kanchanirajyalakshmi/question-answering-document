from fastapi import FastAPI

from app.database import Base, engine

from app.models.document import Document

from app.routes.upload import router as upload_router

from app.routes.extraction import router as extraction_router

from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Multi-Format Document Upload API",
    description="API for uploading and storing documents",
    version="1.0.0"
)


app.include_router(upload_router)
app.include_router(extraction_router)


@app.get("/")
def root():

    return {
        "message": "Document Upload API is running"
    }
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }
