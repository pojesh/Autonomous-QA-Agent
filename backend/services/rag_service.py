import json
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

async def generate_test_cases(query: str) -> List[Dict[str, Any]]:
    logger.info(f"Generating test cases for query: {query}")
    
    vector_store = get_vector_store()
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
            
        return test_cases
    except Exception as e:
        logger.error(f"Error generating test cases: {e}", exc_info=True)
        raise e

async def generate_selenium_script(test_case: Dict[str, Any]) -> str:
    logger.info(f"Generating script for test case: {test_case.get('test_id')}")
    
    vector_store = get_vector_store()
    
    # Retrieve HTML context (specifically looking for checkout.html or similar)
    # We might want to retrieve everything or specific HTML chunks.
    # For now, let's retrieve based on "HTML structure" or "checkout page"
    html_docs = vector_store.similarity_search("checkout.html HTML structure form inputs buttons", k=3)
    html_context = "\n\n".join([doc.page_content for doc in html_docs])
    
    # Retrieve other relevant docs
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
            
        return content.strip()
    except Exception as e:
        logger.error(f"Error generating script: {e}", exc_info=True)
        raise e
