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
    return Milvus(
        embedding_function=embeddings,
        connection_args={
            "uri": settings.MILVUS_URI,
            "token": settings.MILVUS_TOKEN
        },
        collection_name=collection_name,
        auto_id=True
    )

async def process_file(file: UploadFile) -> int:
    logger.info(f"Processing file: {file.filename}")
    
    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

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
            # JSON handling might need specific jq_schema depending on structure
            # For now, generic text loading or custom logic might be better
            # Using a simple text loader for JSON content if structure varies
            import json
            with open(tmp_path, 'r') as f:
                text = json.dumps(json.load(f), indent=2)
            from langchain_core.documents import Document
            documents = [Document(page_content=text, metadata={"source": file.filename})]
        elif ext == ".html":
            loader = BSHTMLLoader(tmp_path)
            documents = loader.load()
        elif ext == ".txt":
            from langchain_community.document_loaders import TextLoader
            loader = TextLoader(tmp_path)
            documents = loader.load()
        else:
            raise ValueError(f"Unsupported file type: {ext}")

        # Add metadata
        for doc in documents:
            doc.metadata["source"] = file.filename

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

        # Ingest into Milvus
        vector_store = get_vector_store()
        vector_store.add_documents(chunks)
        
        logger.info(f"Successfully ingested {len(chunks)} chunks for {file.filename}")
        return len(chunks)

    except Exception as e:
        logger.error(f"Error processing {file.filename}: {e}", exc_info=True)
        raise e
    finally:
        os.unlink(tmp_path)
