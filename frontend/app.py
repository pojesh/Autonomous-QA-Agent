import streamlit as st
import requests
import os
import uuid
import streamlit.components.v1 as components

# Configuration
#API_URL = "http://localhost:8000/api/v1"
#PUT THIS IN ENVIRONMENT VARIABLES
#URL = "https://qa-agent-frontend-631020782872.asia-east2.run.app"
URL = os.getenv("URL")
API_URL = f"{URL}/api/v1"

st.set_page_config(
    page_title="Autonomous QA Agent",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        padding: 10px 20px; /* Adjusted padding */
        margin: 5px 0px;
        font-size: 1rem;
        font-weight: bold;
        transition: all 0.3s ease-in-out;
        border: 1px solid #41444c; /* Changed border color to match generation buttons */
        color: white; /* Default text color changed to white */
        background-color: transparent; /* Make default background transparent */
    }
    /* Hover effect for navigation buttons */
    .stButton > button:hover {
        background-color: #23272f; /* Match primary button hover background */
        border-color: #51545c; /* Match primary button hover border */
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        color: white; /* Match primary button hover text color */
    }

    /* Primary button styling (Build Knowledge Base, Generate Test Cases, Generate Script) */
    button[kind="primary"] {
        background-color: #131720 !important; /* New fill color */
        color: white !important; /* White text for contrast */
        border-color: #41444c !important; /* New border color */
    }
    button[kind="primary"]:hover {
        background-color: #23272f !important; /* Slightly darker for hover */
        border-color: #51545c !important; /* Slightly darker for hover */
    }

    /* Other existing styles */
    .reportview-container {
        background: #f0f2f6;
    }
    .main-header {
        font-size: 2.5rem;
        color: #4B5563;
        text-align: center;
        margin-bottom: 1rem;
    }
    .st-emotion-cache-70k1oh {
        width: 100%;
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f9fafb;
    }
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if 'session_id' not in st.session_state:
    sess = str(uuid.uuid4())
    sess = sess.replace("-", "")
    st.session_state.session_id = sess
if 'ingested_files' not in st.session_state:
    st.session_state.ingested_files = []
if 'page' not in st.session_state:
    st.session_state.page = "Knowledge Base"
if 'generating_script_for' not in st.session_state:
    st.session_state.generating_script_for = None
if 'expanded_test_case' not in st.session_state:
    st.session_state.expanded_test_case = None

def get_headers():
    return {"X-Session-ID": st.session_state.session_id}

def main():
    st.markdown('<h1 class="main-header">🤖 Autonomous QA Agent</h1>', unsafe_allow_html=True)
    st.caption(f"Session ID: {st.session_state.session_id}")
    
    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧠 Knowledge Base", use_container_width=True):
            st.session_state.page = "Knowledge Base"
    with col2:
        if st.button("🧪 Test Case Generation", use_container_width=True):
            st.session_state.page = "Test Cases"
    
    st.markdown("---")

    # JavaScript for Auto-Cleanup on Tab Close
    cleanup_script = f"""
    <script>
        window.addEventListener('beforeunload', function (e) {{
            var xhr = new XMLHttpRequest();
            xhr.open("DELETE", "{API_URL}/session/cleanup", true);
            xhr.setRequestHeader("X-Session-ID", "{st.session_state.session_id}");
            xhr.send();
        }});
    </script>
    """
    components.html(cleanup_script, height=0)

    # Page rendering
    if st.session_state.page == "Knowledge Base":
        render_knowledge_base_page()
    elif st.session_state.page == "Test Cases":
        render_test_case_agent_page()

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
                response = requests.post(f"{API_URL}/ingestion/upload", files=files_payload, headers=get_headers())
                if response.status_code == 200:
                    results = response.json()
                    success_count = sum(1 for r in results if r['status'] == 'success')
                    if success_count > 0:
                        st.success(f"Successfully ingested {success_count} files!")
                        st.session_state.ingested_files.extend([r['filename'] for r in results if r['status'] == 'success'])
                    else:
                        st.error("Failed to ingest any files.")
                    
                    for res in results:
                        if res['status'] != 'success':
                            st.error(f"Error processing {res['filename']}: {res['message']}")
                else:
                    st.error(f"Server Error: {response.status_code} - {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to backend server. Is it running?")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    if st.session_state.ingested_files:
        st.subheader("Ingested Files")
        for file in sorted(list(set(st.session_state.ingested_files))):
            st.text(f"✅ {file}")

def render_test_case_agent_page():
    st.header("🕵️ Test Case Generation Agent")
    
    query = st.text_input("Describe the feature you want to test:", placeholder="e.g., Generate test cases for the discount code feature")
    
    if st.button("Generate Test Cases", type="primary"):
        if not query:
            st.warning("Please enter a description.")
            return
            
        with st.spinner("Analyzing knowledge base and generating test cases..."):
            try:
                # Reset states
                st.session_state.generated_test_cases = []
                st.session_state.expanded_test_case = None
                st.session_state.generating_script_for = None
                
                response = requests.post(f"{API_URL}/generation/test-cases", json={"query": query}, headers=get_headers())
                if response.status_code == 200:
                    test_cases = response.json()
                    st.session_state.generated_test_cases = test_cases
                    st.success(f"Generated {len(test_cases)} test cases!")
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    if 'generated_test_cases' in st.session_state and st.session_state.generated_test_cases:
        st.subheader("Generated Test Cases")
        
        for i, tc in enumerate(st.session_state.generated_test_cases):
            test_id = tc.get('test_id', f'N/A_{i}')
            
            # Determine if the expander should be open
            is_expanded = st.session_state.expanded_test_case == test_id

            with st.expander(f"{test_id}: {tc.get('test_scenario', 'No Scenario')} ({tc.get('test_type', 'N/A')})", expanded=is_expanded):
                st.markdown(f"**Feature:** {tc.get('feature', 'N/A')}")
                st.markdown(f"**Expected Result:** {tc.get('expected_result', 'N/A')}")
                st.markdown(f"**Grounded In:** `{tc.get('grounded_in', 'N/A')}`")

                # --- SCRIPT GENERATION UI ---
                is_generating = st.session_state.generating_script_for == test_id
                
                # We use columns to place the spinner next to the button
                btn_cols = st.columns([3, 1]) 

                if is_generating:
                    with btn_cols[0]:
                        st.button(f"Generating Script for {test_id}...", disabled=True, key=f"generating_btn_{i}")
                    with btn_cols[1]:
                        # The spinner will appear here. The text is blank as the button indicates the action.
                        st.spinner("")

                    # This block runs because is_generating is true, handling the actual API call
                    with st.spinner(f"Generating Selenium script for {test_id}..."):
                        try:
                            res = requests.post(f"{API_URL}/generation/script", json={"test_case": tc}, headers=get_headers())
                            if res.status_code == 200:
                                script_data = res.json()
                                st.session_state[f"script_{test_id}"] = script_data.get('script')
                            else:
                                st.error(f"Error generating script: {res.text}")
                        except Exception as e:
                            st.error(f"An error occurred: {str(e)}")
                        finally:
                            # Reset the generating state and rerun to update the UI
                            st.session_state.generating_script_for = None
                            st.rerun()
                else:
                    # Default state: "Generate Script" button
                    with btn_cols[0]:
                        if st.button(f"Generate Script for {test_id}", key=f"btn_{i}", type="primary"):
                            # When clicked, set the states and rerun the app
                            st.session_state.expanded_test_case = test_id
                            st.session_state.generating_script_for = test_id
                            st.rerun()

                # --- SCRIPT DISPLAY ---
                if st.session_state.get(f"script_{test_id}"):
                    st.markdown("### 🐍 Selenium Script")
                    
                    script_code = st.session_state[f"script_{test_id}"]
                    test_scenario = tc.get('test_scenario', 'No Scenario')
                    file_content = f"# Test Case: {test_scenario}\n\n{script_code}"
                    
                    col1, _ = st.columns([1, 4])
                    with col1:
                        st.download_button(
                            label="Download Script",
                            data=file_content,
                            file_name=f"{test_id}.py",
                            mime="text/python"
                        )
                    
                    st.code(script_code, language="python")

if __name__ == "__main__":
    main()