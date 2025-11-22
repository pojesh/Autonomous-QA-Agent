import os
from typing import List
from fastapi import UploadFile
from langchain_community.document_loaders import PyMuPDFLoader, UnstructuredMarkdownLoader, JSONLoader, BSHTMLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_milvus import Milvus
from backend.core.config import get_settings
from backend.core.logging import logger
import tempfile
import shutil

settings = get_settings()

# Initialize Embeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Initialize Milvus
def get_vector_store(collection_name: str = "qa_agent_knowledge_base"):
    logger.info(f"Connecting to Milvus collection: {collection_name}")
    return Milvus(
        embedding_function=embeddings,
        connection_args={
            "uri": settings.MILVUS_URI,
            "token": settings.MILVUS_TOKEN
        },
        collection_name=collection_name,
        auto_id=True,
        drop_old=False 
    )

async def process_file(file: UploadFile, session_id: str) -> int:
    logger.info(f"Processing file: {file.filename} for session: {session_id}")
    
    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    # Create session directory
    session_dir = os.path.join("backend", "sessions", session_id)
    os.makedirs(session_dir, exist_ok=True)

    try:
        # Load Document
        documents = []
        ext = os.path.splitext(file.filename)[1].lower()
        
        if ext == ".pdf":
            loader = PyMuPDFLoader(tmp_path)
            documents = loader.load()
        elif ext == ".md":
            loader = UnstructuredMarkdownLoader(tmp_path)
            documents = loader.load()
        elif ext == ".json":
            import json
            with open(tmp_path, 'r') as f:
                text = json.dumps(json.load(f), indent=2)
            from langchain_core.documents import Document
            documents = [Document(page_content=text, metadata={"source": file.filename})]
        elif ext == ".html":
            # Save full HTML for RAG
            html_path = os.path.join(session_dir, file.filename)
            shutil.copy(tmp_path, html_path)
            
            with open(tmp_path, 'r', encoding='utf-8') as f:
                raw_html = f.read()
                from langchain_core.documents import Document
                documents = [Document(
                    page_content=raw_html, 
                    metadata={"source": file.filename, "type": "html_source"}
                )]
        elif ext == ".txt":
            from langchain_community.document_loaders import TextLoader
            loader = TextLoader(tmp_path)
            documents = loader.load()
        else:
            raise ValueError(f"Unsupported file type: {ext}")

        # Add metadata
        for doc in documents:
            doc.metadata["source"] = file.filename
            doc.metadata["session_id"] = session_id
            if doc.metadata.get("type") == "html_source":
                doc.metadata["type"] = "html_source"
            else:
                doc.metadata["type"] = "document"

        # Split Text
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )
        chunks = text_splitter.split_documents(documents)
        
        if not chunks:
            logger.warning(f"No chunks created for {file.filename}")
            return 0

        # Ingest into Milvus with session-specific collection
        collection_name = f"session_{session_id}"
        vector_store = get_vector_store(collection_name=collection_name)
        vector_store.add_documents(chunks)
        
        logger.info(f"Successfully ingested {len(chunks)} chunks for {file.filename} into {collection_name}")
        return len(chunks)

    except Exception as e:
        logger.error(f"Error processing {file.filename}: {e}", exc_info=True)
        raise e
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
