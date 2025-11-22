# Autonomous QA Agent

An intelligent, autonomous QA agent capable of constructing a "testing brain" from project documentation. It generates test cases and executable Selenium scripts using Groq LLM and Milvus vector database.

## Features

- **Knowledge Base Ingestion**: Upload PDF, Markdown, JSON, HTML files to build a vector knowledge base.
- **Test Case Generation**: Generate comprehensive test cases grounded in your documentation.
- **Selenium Script Generation**: Convert test cases into runnable Python Selenium scripts.
- **Modern UI**: Built with Streamlit for a seamless user experience.
- **Robust Backend**: FastAPI backend with modular architecture and structured logging.

## Project Structure

- `backend/`: FastAPI application
    - `api/`: Routers and Schemas
    - `core/`: Configuration and Logging
    - `services/`: Business logic (Ingestion, RAG)
- `frontend/`: Streamlit application
- `Project Assets/`: Sample project files with `support_docs_description.txt` file(do not upload to knowledge base)

## Prerequisites

- Python 3.9+
- [Groq API Key](https://console.groq.com/)
- [Milvus Zilliz Cloud](https://zilliz.com/) (URI and Token)

## Setup

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/pojesh/Autonomous-QA-Agent.git
    cd Autonomous-QA-Agent
    ```

2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    # Windows Powershell
    ./venv/Scripts/Activate
    # Linux/Mac
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment**:
    - Rename `.env.example` to `.env` (or create `.env`).
    - Add your API keys:
        ```env
        GROQ_API_KEY=your_groq_api_key
        MILVUS_URI=your_milvus_uri
        MILVUS_TOKEN=your_milvus_token
        LOG_LEVEL=INFO
        ```

## Running the Application

You can run both the backend and frontend using the provided script:

**Windows Powershell**:
```bash
./run.bat
```

**Manual Start**:

1.  **Start Backend**:
    ```bash
    uvicorn backend.main:app --reload --port 8000
    ```

2.  **Start Frontend** (in a new terminal):
    ```bash
    streamlit run frontend/app.py
    ```

## Usage

1.  **Build Knowledge Base**:
    - Go to the "Knowledge Base" page.
    - Upload support documents `product_specs.md`, `ui_ux_guide.txt`, `accessibility_compliance.json`, `error_meesage_dictionary.json` and `api_endpoints.json`.
    - Upload target site html `checkout.html`.
    - Click "Build Knowledge Base".

2.  **Generate Test Cases**:
    - Go to "Test Case Generation Agent".
    - Enter a query like "Generate test cases for the discount code feature".
    - View the generated test cases.

3.  **Generate Scripts**:
    - Expand a test case card.
    - Click "Generate Script".
    - Copy or download the generated Python Selenium script.

## Usage Example

1. Upload Documents video clip
<img src="videos/upload_documents.mp4" alt="upload docs" width="300" />

2. create knowledge base 
<img src="videos/create_knowledge_base.mp4" alt="create knowledge base" width="300" />

3. create test cases 
<img src="videos/create_test_cases.mp4" alt="create test cases" width="300" />

4. generate script
<img src="videos/generate_script.mp4" alt="generate script" width="300" />

5. run scripts
<img src="videos/run_scripts.mp4" alt="run scripts" width="300" />

## results screenshots

## test site description

