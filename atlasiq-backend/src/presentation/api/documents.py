from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session
import uuid
import PyPDF2
from src.infrastructure.database.config import get_db
from src.infrastructure.database.models import DocumentModel
from src.domain.services.document_rag import DocumentRAGService

router = APIRouter(prefix="/api/v1/documents", tags=["documents"])

@router.post("/upload")
async def upload_document(
    project_id: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        content = ""
        if file.filename.endswith(".pdf"):
            reader = PyPDF2.PdfReader(file.file)
            for page in reader.pages:
                content += page.extract_text() + "\n"
        elif file.filename.endswith(".txt"):
            content = (await file.read()).decode("utf-8")
        else:
            raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported")

        doc_id = str(uuid.uuid4())
        
        # Ingest to Qdrant
        rag_service = DocumentRAGService()
        rag_service.ingest_document(project_id, content, doc_id)
        
        # Save to DB
        db_doc = DocumentModel(
            id=doc_id,
            project_id=project_id,
            filename=file.filename,
            content_type=file.content_type,
            vector_id=doc_id
        )
        db.add(db_doc)
        db.commit()
        
        return {"id": doc_id, "filename": file.filename, "status": "indexed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
