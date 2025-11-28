import streamlit as st
import os
import tempfile
from typing import TypedDict
from langchain_community.document_loaders import PyPDFLoader
from langgraph.graph import StateGraph, START, END
# LLM imports ko simulation ke liye rakha gaya hai
from langchain_google_genai import ChatGoogleGenerativeAI 

# ==============================================================================
# 1. STATE DEFINITION
# ==============================================================================
# HiringState (Aapke sir ke PDF se copy ki gayi)
class HiringState(TypedDict):
    resume_text: str
    jd_text: str
    resume_summary: str
    jd_summary: str
    skills_score: float
    experience_score: float
    education_score: float
    overall_score: float
    recommendation: str
    final_report: str

# LLM Setup (Simulation ya API Key se)
# Agar aap apni GEMINI API key use karna chahte hain toh is line ko uncomment karein
# os.environ["GEMINI_API_KEY"] = "YOUR_API_KEY"
try:
    llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash')
except Exception:
    llm = None
    
# ==============================================================================
# 2. NODES (Functions)
# ==============================================================================

# Node 1: Document Loading (Updated for Streamlit File Upload)
def load_documents(resume_file, jd_file) -> dict:
    # Streamlit ke liye, files ko temporary location par save karna zaroori hai
    
    # 1. Resume File Handling
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_resume_file:
        tmp_resume_file.write(resume_file.read())
        resume_path = tmp_resume_file.name
        
    # 2. JD File Handling
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_jd_file:
        tmp_jd_file.write(jd_file.read())
        jd_path = tmp_jd_file.name

    try:
        # Resume Load aur Text Extract
        resume_loader = PyPDFLoader(resume_path)
        resume_pages = resume_loader.load()
        resume_text = "\n".join(page.page_content for page in resume_pages)

        # Job Description Load aur Text Extract
        jd_loader = PyPDFLoader(jd_path)
        jd_pages = jd_loader.load()
        jd_text = "\n".join(page.page_content for page in jd_pages)
        
        return {'resume_text': resume_text, 'jd_text': jd_text}
    
    finally:
        # Temporary files ko delete karna
        os.remove(resume_path)
        os.remove(jd_path)


# Node 2: Information Extraction (LLM Summary Simulation)
def extract_info(state: HiringState) -> HiringState:
    st.info("🔄 Extracting Information...")
    if not llm:
        resume_summary = "Skills: Python, LangGraph, Cloud. Experience: 5 yrs. Education: Masters."
        jd_summary = "Required Skills: Python, LangGraph, Cloud. Experience: Senior Dev (3+ yrs). Education: CS Degree."
        return {'resume_summary': resume_summary, 'jd_summary': jd_summary}
    # Agar llm set hai toh actual call yahan aayega
    return state # LLM logic yahan implement hoga

# Node 3: Scoring and Comparison (Calculation)
def compare_and_score(state: HiringState) -> HiringState:
    st.info("🔄 Comparing documents and calculating score...")
    
    # Sample Scores (Yahan aapka comparison logic aayega)
    skills = 90.0
    experience = 75.0
    education = 95.0
    
    # Weighted Score Calculation
    overall_score = (skills * 0.50) + (experience * 0.30) + (education * 0.20)
    
    return {
        'skills_score': skills,
        'experience_score': experience,
        'education_score': education,
        'overall_score': round(overall_score, 2)
    }

# Node 4A/B/C: Conditional Action Nodes
def execute_one_interview_process(state: HiringState) -> HiringState:
    st.success("✅ Path Selected: One Interview (High Fit)")
    return {'recommendation': 'One Interview'}

def execute_two_interview_process(state: HiringState) -> HiringState:
    st.warning("⚠️ Path Selected: Two Interviews (Moderate Fit)")
    return {'recommendation': 'Two Interviews'}

def execute_rejection_process(state: HiringState) -> HiringState:
    st.error("❌ Path Selected: Rejected (Low Fit)")
    return {'recommendation': 'Rejected'}

# Routing Function (Decision Maker)
def route_by_score(state: HiringState) -> str:
    score = state['overall_score']
    
    if score >= 85:
        return 'one_interview_node'
    elif 60 <= score < 85:
        return 'two_interviews_node'
    else:
        return 'rejected_node'

# Node 5: Report Generation
def generate_final_report(state: HiringState) -> HiringState:
    st.info("🔄 Generating final recommendation report...")
    
    report_text = f"""
📋 FINAL HIRING RECOMMENDATION REPORT
-------------------------------------
**Overall Score:** **{state['overall_score']} / 100**
**Recommendation:** **{state['recommendation']}**

**Score Breakdown:**
* Skills Match: {state['skills_score']}/100
* Experience Match: {state['experience_score']}/100
* Education Match: {state['education_score']}/100

**Summary:**
Candidate has a strong profile (Score {state['overall_score']}) and is recommended for the **{state['recommendation']}** path based on the automated assessment. Further details can be found in the raw state output.
"""
    return {'final_report': report_text}

# ==============================================================================
# 3. GRAPH ASSEMBLY AND COMPILE
# ==============================================================================

# Graph initialize aur Nodes Register karna
def get_workflow_graph():
    graph = StateGraph(HiringState)
    
    # Nodes register karna
    graph.add_node('extract_info', extract_info)
    graph.add_node('compare_and_score', compare_and_score)
    graph.add_node('one_interview_node', execute_one_interview_process)
    graph.add_node('two_interviews_node', execute_two_interview_process)
    graph.add_node('rejected_node', execute_rejection_process)
    graph.add_node('generate_report', generate_final_report)
    
    # Edges
    graph.add_edge(START, 'extract_info')
    graph.add_edge('extract_info', 'compare_and_score')
    
    # Conditional Edge
    graph.add_conditional_edges(
        "compare_and_score", 
        route_by_score, 
        {
            'one_interview_node': 'one_interview_node',
            'two_interviews_node': 'two_interviews_node',
            'rejected_node': 'rejected_node'
        }
    )
    
    # Merge Edges
    graph.add_edge('one_interview_node', 'generate_report')
    graph.add_edge('two_interviews_node', 'generate_report')
    graph.add_edge('rejected_node', 'generate_report')
    graph.add_edge('generate_report', END)

    return graph.compile()

workflow = get_workflow_graph()

# ==============================================================================
# 4. STREAMLIT UI
# ==============================================================================

st.set_page_config(page_title="LangGraph Hiring System", layout="wide")
st.title("🤖 AI Hiring Recommendation System (LangGraph)")
st.caption("Upload Candidate Resume and Job Description (PDFs) to run the conditional workflow.")

# File Uploaders
col1, col2 = st.columns(2)

with col1:
    resume_file = st.file_uploader("**Upload Candidate Resume (PDF)**", type="pdf")
with col2:
    jd_file = st.file_uploader("**Upload Job Description (PDF)**", type="pdf")

if st.button("🚀 Run Assessment", type="primary"):
    if resume_file is None or jd_file is None:
        st.error("Please upload both the Resume and the Job Description to start the assessment.")
    else:
        st.subheader("Workflow Execution")
        
        # 1. Document Loading Node (Isse pehle run karna padega)
        try:
            st.info("🔄 Step 1: Loading and parsing documents...")
            initial_state_data = load_documents(resume_file, jd_file)
        except Exception as e:
            st.error(f"Error loading documents: {e}")
            st.stop()
            
        # 2. LangGraph Workflow Invoke
        try:
            st.info("🔄 Step 2: Running LangGraph conditional workflow...")
            result = workflow.invoke(initial_state_data)
            
            st.subheader("Final Result")
            st.markdown(result['final_report'])
            
            st.subheader("Raw Workflow State (Sir's style output)")
            st.json(result)
            
        except Exception as e:
            st.error(f"Error executing workflow: {e}")

# Footer for visualization (optional)
st.sidebar.subheader("Workflow Structure")
st.sidebar.markdown("""
- **START** -> `extract_info` -> `compare_and_score`
- **compare_and_score** (Router) -> `one_interview_node` / `two_interviews_node` / `rejected_node`
- All paths merge to -> `generate_report` -> **END**
""")