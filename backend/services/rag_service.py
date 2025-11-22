import json
import os
from typing import List, Dict, Any
from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnablePassthrough
from backend.services.ingestion_service import get_vector_store
from backend.services.prompts import TEST_CASE_GENERATION_PROMPT, SELENIUM_SCRIPT_GENERATION_PROMPT
from backend.core.config import get_settings
from backend.core.logging import logger

settings = get_settings()

def get_llm():
    return ChatGroq(
        temperature=0,
        model_name="openai/gpt-oss-20b", 
        api_key=settings.GROQ_API_KEY
    )

async def generate_test_cases(query: str, session_id: str) -> List[Dict[str, Any]]:
    logger.info(f"Generating test cases for query: {query} in session: {session_id}")
    
    collection_name = f"session_{session_id}"
    vector_store = get_vector_store(collection_name=collection_name)
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    
    llm = get_llm()
    
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | TEST_CASE_GENERATION_PROMPT
        | llm
    )
    
    try:
        response = await chain.ainvoke(query)
        content = response.content
        
        # Basic cleanup if LLM returns markdown code blocks
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
            
        test_cases = json.loads(content)
        
        # Ensure it's a list
        if isinstance(test_cases, dict):
            test_cases = [test_cases]
            
        logger.info(f"Generated {len(test_cases)} test cases for session {session_id}")
        return test_cases
    except Exception as e:
        logger.error(f"Error generating test cases: {e}", exc_info=True)
        raise e

async def generate_selenium_script(test_case: Dict[str, Any], session_id: str) -> str:
    logger.info(f"Generating script for test case: {test_case.get('test_id')} in session: {session_id}")
    
    collection_name = f"session_{session_id}"
    vector_store = get_vector_store(collection_name=collection_name)
    
    # Try to load full HTML from session storage
    session_dir = os.path.join("backend", "sessions", session_id)
    html_context = ""
    
    if os.path.exists(session_dir):
        for filename in os.listdir(session_dir):
            if filename.lower().endswith(".html"):
                try:
                    with open(os.path.join(session_dir, filename), 'r', encoding='utf-8') as f:
                        html_context += f"\n\n--- FILE: {filename} ---\n{f.read()}"
                except Exception as e:
                    logger.error(f"Error reading HTML file {filename}: {e}")

    # If no HTML found on disk, fallback to vector store (though ingestion should have saved it)
    if not html_context:
        logger.warning("No HTML file found in session storage, falling back to vector search.")
        html_docs = vector_store.similarity_search("checkout.html HTML structure form inputs buttons", k=3)
        html_context = "\n\n".join([doc.page_content for doc in html_docs])
    
    # Retrieve other relevant docs (specs, guides)
    doc_docs = vector_store.similarity_search(str(test_case), k=3)
    doc_context = "\n\n".join([doc.page_content for doc in doc_docs])
    
    llm = get_llm()
    
    chain = SELENIUM_SCRIPT_GENERATION_PROMPT | llm
    
    try:
        response = await chain.ainvoke({
            "test_case": json.dumps(test_case, indent=2),
            "html_context": html_context,
            "doc_context": doc_context
        })
        
        content = response.content
        
        # Cleanup
        if "```python" in content:
            content = content.split("```python")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
            
        script_content = content.strip()
        logger.info(f"Generated script for {test_case.get('test_id')} in session {session_id}")
        return script_content
    except Exception as e:
        logger.error(f"Error generating script: {e}", exc_info=True)
        raise e
