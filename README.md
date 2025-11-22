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

## DEMONSTRATION


https://github.com/user-attachments/assets/75d48044-0e69-44f7-8c85-c32a52f7217c



## Project Assets

These files represent the "Knowledge Base" the agent will ingest to understand how the `checkout.html` application is supposed to behave.

1.  **`product_specs.md` (Business Logic)**
    *   **Purpose**: Defines the core business rules, pricing models, and functional limits of the application.
    *   **Key Contents**:
        *   **Inventory**: Specific prices for products (e.g., Mechanical Keyboard is $120).
        *   **Discount Logic**: Exact rules for codes like `SAVE15` (15% off) and `FREESHIP`.
        *   **Shipping**: Cost difference between Standard ($0) and Express ($10).
        *   **Constraints**: Limits on cart quantity (max 10 units).

2.  **`ui_ux_guide.txt` (Visual Standards)**
    *   **Purpose**: Establishes the visual design language and expected user interface behaviors. Used for UI assertion testing.
    *   **Key Contents**:
        *   **Color Palette**: Specific Hex codes for buttons (Green-600), errors (Red-600), and hover states.
        *   **Behavior**: How buttons should react when clicked (e.g., "Processing..." state).
        *   **Feedback**: Exact requirements for how success messages and error borders should appear.

3.  **`api_endpoints.json` (Backend Contract)**
    *   **Purpose**: A mock definition of the backend API. This allows the agent to generate tests that verify if the frontend sends the correct JSON payloads.
    *   **Key Contents**:
        *   **Endpoints**: Definitions for `/cart/validate-coupon` and `/orders/submit`.
        *   **Schema**: Required fields (`name`, `email`, `address`) and data types.
        *   **Responses**: Expected status codes (200, 201, 400, 404) and response bodies.

4.  **`accessibility_compliance.md` (A11y Standards)**
    *   **Purpose**: Defines the Web Content Accessibility Guidelines (WCAG 2.1) that the page must adhere to.
    *   **Key Contents**:
        *   **Focus Management**: Requirements for visible focus rings on inputs.
        *   **ARIA Attributes**: Rules for using `role="alert"` and `aria-describedby`.
        *   **Navigation**: Logical tab order expectations for keyboard users.

5.  **`error_message_dictionary.json` (Content Source of Truth)**
    *   **Purpose**: A centralized dictionary mapping error codes to specific UI text. This ensures the agent verifies the exact wording of messages, not just their presence.
    *   **Key Contents**:
        *   **Mappings**: Links abstract keys like `ERR_EMAIL_INVALID` to user-facing text: "Please enter a valid email address."
        *   **Triggers**: Explains exactly what user action causes each message to fire.


