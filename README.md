# Multi-Format Document Question-Answering Assistant

An AI-powered document question-answering system that allows users to upload documents in multiple formats and ask questions based on their content.

The project uses document processing, embeddings, vector search, and Retrieval-Augmented Generation (RAG) to provide relevant answers with source references.

## Project Overview

The goal of this project is to build an intelligent assistant that can understand information from different document formats and answer user questions using the uploaded documents.

Users can upload documents, and the system will process them to make their content searchable and available for question answering.

## Key Features

- Upload multiple document formats.
- Validate file extensions, sizes, and file content.
- Generate unique document IDs.
- Store uploaded documents securely.
- Store document metadata in PostgreSQL.
- Extract text from different document formats.
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

*Format availability depends on the corresponding validation and extraction implementation.*

## Technology Stack

### Frontend
- React.js
- JavaScript
- HTML
- CSS
- Axios

### Backend
- Python
- FastAPI
- Uvicorn
- SQLAlchemy

### Database
- PostgreSQL

### Document Processing
- PyMuPDF
- python-docx
- python-pptx
- openpyxl

### Generative AI and RAG
- Embeddings
- Vector Search
- Large Language Models (LLMs)
- Retrieval-Augmented Generation (RAG)

## System Architecture

```mermaid
flowchart TD
    A["User"] --> B["React Frontend"]
    B --> C["FastAPI Backend"]
    C --> D["Document Upload"]
    D --> E["Document Processing"]
    E --> F["Text Extraction"]
    F --> G["Text Chunking"]
    G --> H["Embedding Generation"]
    H --> I["Vector Database"]
    I --> J["Relevant Context Retrieval"]
    J --> K["LLM"]
    K --> L["Answer with Source References"]
    L --> B
```

## Document Upload Workflow — Module 1

```mermaid
flowchart TD
    A["React Frontend"] --> B["Select Document"]
    B --> C["FastAPI Upload API"]
    C --> D["Validate Extension"]
    D --> E["Validate File Size"]
    E --> F["Validate Actual File Content"]
    F --> G["Generate Unique Document ID"]
    G --> H["Store File Securely"]
    H --> I["Save Metadata in PostgreSQL"]
    I --> J["Return Upload Status"]
    J --> K["Display Success in React"]
```

## Storage Architecture

Actual uploaded documents are stored in file storage, while PostgreSQL stores their metadata and file paths.

```mermaid
flowchart LR
    A["React User"] --> B["FastAPI"]
    B --> C["File Storage"]
    B --> D[("PostgreSQL")]
    C --> E["Actual Document"]
    D --> F["Document ID"]
    D --> G["Filename and File Path"]
    D --> H["File Type and Size"]
    D --> I["Upload Status"]
```

## Project Structure

```text
multi-format-document-qa/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models/
│   │   ├── schemas/
│   │   └── routes/
│   │       └── upload.py
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

*The folder structure above is illustrative. Adjust it to match your actual repository.*

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/kanchanairajyalakshmi/multi-format-document-qa.git
cd multi-format-document-qa
```

### 2. Backend Setup

```bash
cd backend

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file inside the backend directory.

```env
DATABASE_URL=postgresql+psycopg://document_user:YOUR_PASSWORD@localhost:5432/document_qa_db
```

Replace `YOUR_PASSWORD` with your actual PostgreSQL password.

Never commit your `.env` file to GitHub.

### 4. Run the Backend

```bash
python -m uvicorn app.main:app --reload
```

Backend URL:

`http://127.0.0.1:8000`

Swagger API Documentation:

`http://127.0.0.1:8000/docs`

### 5. Frontend Setup

Open another terminal:

```bash
cd frontend

npm install

npm run dev
```

Frontend URL:

`http://localhost:5173`

## API Documentation

### Upload Document

**Endpoint:**

`POST /documents/upload`

**Request:**

- Method: POST
- Content-Type: multipart/form-data
- Parameter: file

**Example Response:**

```json
{
  "message": "File uploaded successfully",
  "document_id": "123",
  "filename": "resume.pdf",
  "file_type": "pdf",
  "status": "uploaded"
}
```

Use Swagger UI at `/docs` to test the API.

## Database Design

### Documents Table

| Column | Description |
|---|---|
| id | Unique document ID |
| original_filename | Original filename |
| stored_filename | Unique stored filename |
| file_path | File storage location |
| file_type | Document format |
| file_size | File size in bytes |
| status | Upload status |
| created_at | Upload timestamp |

## Development Progress

- [x] Module 1 — Multi-Format File Upload & Document Ingestion
- [ ] Module 2 — Multi-Format Document Text Extraction
- [ ] Module 3 — Text Cleaning and Chunking
- [ ] Module 4 — Embedding Generation
- [ ] Module 5 — Vector Database and Indexing
- [ ] Module 6 — Document Retrieval
- [ ] Module 7 — LLM Integration and Answer Generation
- [ ] Module 8 — Source References and Citations
- [ ] Module 9 — Frontend Integration
- [ ] Module 10 — Testing and Deployment

## Security Considerations

- Validate uploaded files before processing.
- Restrict file size and allowed formats.
- Generate unique filenames.
- Store sensitive configuration in environment variables.
- Do not expose uploaded private documents publicly.
- Protect API endpoints where authentication is required.

## Future Enhancements

- Support additional document formats.
- Improve document extraction accuracy.
- Add semantic search.
- Implement conversational question answering.
- Add source citations and page references.
- Deploy using Docker and AWS.
- Implement CI/CD automation.

## Contributors

Add the names and GitHub profiles of your project team members here.

## License

This project is developed for educational and learning purposes. Add a suitable open-source license if you intend to distribute it publicly.
