# Multi-Format Document Question-Answering Assistant

An AI-powered document question-answering system that allows users to upload documents in multiple formats and ask questions based on their content.

The project uses document processing, embeddings, vector search, and Retrieval-Augmented Generation (RAG) to provide relevant answers with source references.

## Project Overview

The goal of this project is to build an intelligent assistant that understands information from different document formats and answers user questions using uploaded documents.

Users can upload documents, and the system processes their content to make it searchable and available for question answering.

## Key Features

- Upload documents in multiple formats.
- Validate file extensions, sizes, and file content.
- Generate unique UUIDs for uploaded documents.
- Store uploaded documents securely.
- Store document metadata in PostgreSQL.
- Extract text from different document formats.
- Preserve page, slide, sheet, and section metadata where supported.
- Clean and normalize extracted text.
- Split extracted text into smaller chunks.
- Generate embeddings for document chunks.
- Retrieve relevant document content using vector search.
- Generate answers using an LLM.
- Provide source references for generated answers.

## Supported Document Formats

| Format | Extension |
|---|---|
| PDF | `.pdf` |
| Word | `.docx` |
| PowerPoint | `.pptx` |
| Excel | `.xlsx` |
| CSV | `.csv` |
| Text | `.txt` |
| HTML | `.html` |
| JSON | `.json` |
| Markdown | `.md` |

Format availability depends on the corresponding validation and extraction implementation.

## Technology Stack

### Frontend
- React.js
- JavaScript
- HTML
- CSS
- Axios
- Vite

### Backend
- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic

### Database
- PostgreSQL

### Document Processing
- PyMuPDF
- python-docx
- python-pptx
- openpyxl
- pandas
- BeautifulSoup
- Tesseract OCR (for scanned PDFs, if configured)

### Generative AI and RAG
- Embeddings
- Vector Search
- Large Language Models (LLMs)
- Retrieval-Augmented Generation (RAG)

## System Architecture

### Document Processing Workflow

```text
             User
              |
              v
       React Frontend
              |
              v
        FastAPI Backend
              |
              v
      File Validation
              |
              v
       Document Upload
              |
        +-----+------+
        |            |
        v            v
   File Storage   PostgreSQL
        |          Metadata
        |            |
        +-----+------+
              |
              v
      Document Extraction
              |
              v
       Text Cleaning
              |
              v
       Text Chunking
              |
              v
     Embedding Generation
              |
              v
       Vector Database
              |
              v
       Semantic Retrieval
              |
              v
         LLM Answer
              |
              v
      Source References
              |
              v
          User
```

### Storage Architecture

Actual uploaded documents are stored in file storage, while PostgreSQL stores their metadata and file paths.

This separation helps manage uploaded files independently from document records.

## Project Structure

```text
multi-format-document-qa/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   │
│   │   ├── models/
│   │   │   └── document.py
│   │   │
│   │   ├── schemas/
│   │   │
│   │   ├── routes/
│   │   │   ├── upload.py
│   │   │   └── extraction.py
│   │   │
│   │   ├── services/
│   │   │   ├── document_extractor.py
│   │   │   └── file_validation.py
│   │   │
│   │   └── utils/
│   │       └── text_cleaner.py
│   │
│   ├── storage/
│   │   └── uploads/
│   │
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── index.html
│
├── .gitignore
├── README.md
└── docker-compose.yml
```

The structure is representative. Update it as additional modules are integrated into the repository.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/kanchanairajyalakshmi/multi-format-document-qa.git

cd multi-format-document-qa
```

### 2. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create a Python virtual environment:

```bash
python3 -m venv venv
```

Activate the virtual environment on macOS/Linux:

```bash
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file inside the backend directory.

```env
DATABASE_URL=postgresql+psycopg://document_user:YOUR_PASSWORD@localhost:5432/document_qa_db
MAX_FILE_SIZE_MB=20
```

Replace `YOUR_PASSWORD` with your actual PostgreSQL password and configure the database credentials.

Never commit your `.env` file to GitHub.

### 4. Run the Backend

From the backend directory, execute:

```bash
python -m uvicorn app.main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

Swagger API Documentation:

```text
http://127.0.0.1:8000/docs
```

### 5. Frontend Setup

Open another terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install frontend dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

Use the URL displayed by Vite if it selects another port.

## API Documentation

### 1. Upload Document

**Endpoint:**

```http
POST /documents/upload
```

**Request:**

| Parameter | Type | Description |
|---|---|---|
| file | File | Document to upload |

Content-Type: `multipart/form-data`

**Example Response:**

```json
{
  "message": "Document uploaded successfully",
  "document_id": "b6332709-4814-4d96-825f-dca7366a6eb0",
  "filename": "sample.pdf",
  "file_type": ".pdf",
  "file_size": 5226,
  "status": "uploaded"
}
```

### 2. Extract Document Text

**Endpoint:**

```http
POST /documents/{document_id}/extract
```

**Path Parameter:**

| Parameter | Type | Description |
|---|---|---|
| document_id | String (UUID) | Unique ID of the uploaded document |

**Example Response:**

```json
{
  "success": true,
  "message": "Document extracted successfully",
  "data": {
    "document_id": "b6332709-4814-4d96-825f-dca7366a6eb0",
    "filename": "sample.pdf",
    "file_type": ".pdf",
    "text": "Extracted document content...",
    "total_characters": 1500,
    "sections": [
      {
        "page": 1,
        "text": "Extracted page content..."
      }
    ],
    "status": "extracted"
  }
}
```

Use Swagger UI at `/docs` to test the API endpoints.

## Database Design

### Documents Table

| Column | Data Type | Description |
|---|---|---|
| id | String(36) | Unique UUID document ID |
| original_filename | String(255) | Original uploaded filename |
| stored_filename | String(255) | Unique stored filename |
| file_path | Text | File storage location |
| file_type | String(20) | Document format |
| file_size | Integer | File size in bytes |
| status | String(30) | Document processing status |
| created_at | DateTime | Upload timestamp |

## Development Progress

- [x] Module 1 — Multi-Format File Upload and Document Ingestion
- [x] Module 2 — Multi-Format Document Text Extraction (PDF extraction verified; other formats require individual testing)
- [ ] Module 3 — Text Cleaning and Chunking
- [ ] Module 4 — Embedding Generation
- [ ] Module 5 — Vector Database and Indexing
- [ ] Module 6 — Document Retrieval
- [ ] Module 7 — LLM Integration and Answer Generation
- [ ] Module 8 — Source References and Citations
- [ ] Module 9 — Frontend Integration
- [ ] Module 10 — Testing and Deployment

## Testing

Test the backend APIs using Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Run automated tests using:

```bash
pytest -v
```

Recommended test cases:

- Upload valid documents.
- Reject unsupported file formats.
- Validate maximum file size.
- Verify unique document IDs.
- Extract text from all supported formats.
- Handle corrupted and empty documents.
- Verify page, slide, and sheet metadata.
- Handle missing document IDs.
- Verify scanned PDF OCR, if configured.

## Security Considerations

- Validate uploaded files before processing.
- Restrict file sizes and allowed formats.
- Generate unique filenames.
- Store sensitive configuration in environment variables.
- Never commit `.env` files.
- Do not expose uploaded private documents publicly.
- Protect API endpoints where authentication is required.
- Avoid logging sensitive document contents.

## Future Enhancements

- Support additional document formats.
- Improve document extraction accuracy.
- Implement intelligent text chunking.
- Add semantic search.
- Integrate vector databases.
- Implement conversational question answering.
- Add source citations and page references.
- Support document-specific conversation history.
- Deploy using Docker and AWS.
- Implement CI/CD automation.

## Contributors

Add the names and GitHub profiles of your project team members here.

## License

This project is developed for educational and learning purposes.

Add a suitable open-source license if you intend to distribute it publicly.