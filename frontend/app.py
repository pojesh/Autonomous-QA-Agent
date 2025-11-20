import streamlit as st
import requests
import os

# Configuration
API_URL = "http://localhost:8000/api/v1"

st.set_page_config(
    page_title="Autonomous QA Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
    }
    .reportview-container {
        background: #f0f2f6;
    }
    .main-header {
        font-size: 2.5rem;
        color: #4B5563;
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if 'ingested_files' not in st.session_state:
    st.session_state.ingested_files = []

def main():
    st.markdown('<h1 class="main-header">🤖 Autonomous QA Agent</h1>', unsafe_allow_html=True)
    
    # Sidebar for Navigation
    page = st.sidebar.radio("Navigation", ["Knowledge Base", "Test Case Agent", "Script Generator"])
    
    if page == "Knowledge Base":
        render_knowledge_base_page()
    elif page == "Test Case Agent":
        render_test_case_agent_page()
    elif page == "Script Generator":
        render_script_generator_page()

def render_knowledge_base_page():
    st.header("📚 Build Knowledge Base")
    st.markdown("Upload project documentation and HTML files to train the agent.")
    
    uploaded_files = st.file_uploader(
        "Upload Files (PDF, MD, JSON, HTML, TXT)", 
        accept_multiple_files=True,
        type=['pdf', 'md', 'json', 'html', 'txt']
    )
    
    if st.button("Build Knowledge Base", type="primary"):
        if not uploaded_files:
            st.warning("Please upload at least one file.")
            return
            
        with st.spinner("Ingesting documents..."):
            files_payload = []
            for file in uploaded_files:
                files_payload.append(('files', (file.name, file.getvalue(), file.type)))
            
            try:
                response = requests.post(f"{API_URL}/ingestion/upload", files=files_payload)
                if response.status_code == 200:
                    results = response.json()
                    success_count = sum(1 for r in results if r['status'] == 'success')
                    if success_count > 0:
                        st.success(f"Successfully ingested {success_count} files!")
                        for res in results:
                            if res['status'] == 'success':
                                st.session_state.ingested_files.append(res['filename'])
                            else:
                                st.error(f"Error processing {res['filename']}: {res['message']}")
                    else:
                        st.error("Failed to ingest files.")
                else:
                    st.error(f"Server Error: {response.status_code}")
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to backend server. Is it running?")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    if st.session_state.ingested_files:
        st.subheader("Ingested Files")
        for file in st.session_state.ingested_files:
            st.text(f"✅ {file}")

def render_test_case_agent_page():
    st.header("🕵️ Test Case Generation Agent")
    
    # Chat Interface
    query = st.text_input("Describe the feature you want to test:", placeholder="e.g., Generate test cases for the discount code feature")
    
    if st.button("Generate Test Cases", type="primary"):
        if not query:
            st.warning("Please enter a description.")
            return
            
        with st.spinner("Analyzing knowledge base and generating test cases..."):
            try:
                response = requests.post(f"{API_URL}/generation/test-cases", json={"query": query})
                if response.status_code == 200:
                    test_cases = response.json()
                    st.session_state.generated_test_cases = test_cases
                    st.success(f"Generated {len(test_cases)} test cases!")
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    # Display Test Cases
    if 'generated_test_cases' in st.session_state and st.session_state.generated_test_cases:
        st.subheader("Generated Test Cases")
        
        for i, tc in enumerate(st.session_state.generated_test_cases):
            with st.expander(f"{tc['test_id']}: {tc['test_scenario']} ({tc['test_type']})"):
                st.markdown(f"**Feature:** {tc['feature']}")
                st.markdown(f"**Expected Result:** {tc['expected_result']}")
                st.markdown(f"**Grounded In:** `{tc['grounded_in']}`")
                
                # Generate Script Button for this test case
                if st.button(f"Generate Script for {tc['test_id']}", key=f"btn_{i}"):
                    with st.spinner(f"Generating Selenium script for {tc['test_id']}..."):
                        try:
                            res = requests.post(f"{API_URL}/generation/script", json={"test_case": tc})
                            if res.status_code == 200:
                                script_data = res.json()
                                st.session_state[f"script_{tc['test_id']}"] = script_data['script']
                            else:
                                st.error(f"Error: {res.text}")
                        except Exception as e:
                            st.error(f"An error occurred: {str(e)}")
                
                # Display Script if generated
                if f"script_{tc['test_id']}" in st.session_state:
                    st.markdown("### 🐍 Selenium Script")
                    st.code(st.session_state[f"script_{tc['test_id']}"], language="python")

def render_script_generator_page():
    st.header("💻 Script Generator")
    st.info("Please use the 'Test Case Agent' page to generate scripts directly from test cases.")
    
    if 'generated_test_cases' in st.session_state and st.session_state.generated_test_cases:
        st.markdown("### Available Test Cases")
        for tc in st.session_state.generated_test_cases:
             st.text(f"{tc['test_id']}: {tc['test_scenario']}")



if __name__ == "__main__":
    main()