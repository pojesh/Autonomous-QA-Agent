from langchain_core.prompts import PromptTemplate

TEST_CASE_GENERATION_PROMPT = PromptTemplate(
    template="""
    You are an expert QA Automation Engineer. Your goal is to generate comprehensive test cases based on the provided project documentation and HTML context.
    
    Context:
    {context}
    
    User Request: {question}
    
    Instructions:
    1. Analyze the provided context (requirements, UI guides, API docs, HTML).
    2. Generate positive and negative test cases relevant to the user request.
    3. Ensure each test case is grounded in the documentation.
    4. Output the result in a structured JSON format with the following keys:
       - test_id
       - feature
       - test_scenario
       - expected_result
       - test_type (Positive/Negative)
       - grounded_in (Source document filename)
    
    Output JSON only. Do not include markdown formatting like ```json.
    """,
    input_variables=["context", "question"]
)

SELENIUM_SCRIPT_GENERATION_PROMPT = PromptTemplate(
    template="""
    You are an expert Selenium Python Automation Engineer. Your goal is to generate a robust, executable Selenium script for a specific test case.
    
    Test Case:
    {test_case}
    
    HTML Context (Target Page):
    {html_context}
    
    Documentation Context:
    {doc_context}
    
    Instructions:
    1. Use Python and Selenium WebDriver.
    2. Use `webdriver.Chrome()` (assume chromedriver is in PATH or use webdriver_manager).
    3. Use explicit waits (`WebDriverWait`) for element interactions.
    4. Use precise selectors based on the provided HTML (ID, Name, CSS Selector, XPath).
    5. Implement the steps defined in the test case.
    6. Add assertions to verify the expected result.
    7. Include comments explaining the steps.
    8. Handle potential errors gracefully (try/except).
    9. The script should be a complete, runnable standalone file.
    
    Output the Python code only. Do not include markdown formatting like ```python.
    """,
    input_variables=["test_case", "html_context", "doc_context"]
)
