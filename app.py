"""
=============================================================================
Module:      app.py
Description: Pathfinder Agent Enterprise Command Center UI
             - Three-column layout restored: Input Hub (Left), Real-Time Middle Display, Outreach & Cloud Sync (Right)
             - High-end professional executive styling with polished primary action buttons
             - Freeze-proof file uploader handlers to prevent screen freezing/looping loops
Author:      Mahamat Hissein GUIAGOUSSOU
Last Updated: September 29, 2026 at 8:42 PM
=============================================================================
"""

import streamlit as st
import os
import io
import base64
from datetime import datetime
from pathlib import Path
from pypdf import PdfReader
import urllib.request
import html.parser
import re

from generator import generate_comprehensive_resume, extract_master_profile_text, generate_local_documents, upload_to_oci_bucket, generate_outreach_text

# ==========================================
# 1. PAGE CONFIGURATION & EXECUTIVE POLISHED STYLING
# ==========================================
st.set_page_config(
    page_title="Pathfinder Agent | Enterprise Command Center",
    page_icon="🛡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    /* Global App Background & Font */
    .stApp {
        background-color: #0b0f19;
        color: #f8fafc;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Executive Hero Banner */
    .executive-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0284c7 100%);
        border: 2px solid #0284c7;
        border-radius: 14px;
        padding: 26px 36px;
        margin-bottom: 25px;
        color: #ffffff;
        box-shadow: 0 12px 30px -10px rgba(2, 132, 199, 0.3);
    }
    .executive-banner h1 {
        font-size: 2.1rem;
        font-weight: 800;
        color: #ffffff !important;
        margin-bottom: 8px;
    }
    .executive-banner p {
        font-size: 1.05rem;
        color: #e2e8f0 !important;
        margin-bottom: 0px;
    }

    /* Section Headings */
    .section-header {
        background: linear-gradient(90deg, #1e293b 0%, #0f172a 100%);
        border-left: 6px solid #38bdf8;
        padding: 12px 18px;
        border-radius: 6px;
        font-size: 1.2rem;
        font-weight: 700;
        color: #ffffff !important;
        margin-bottom: 18px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.4);
    }

    /* PROFESSIONAL STANDARD BUTTONS */
    div.stButton > button {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
        color: #f8fafc !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.2rem !important;
        transition: all 0.2s ease-in-out !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        color: #ffffff !important;
        border-color: #38bdf8 !important;
        box-shadow: 0 4px 12px rgba(56, 189, 248, 0.3) !important;
    }

    /* PRIMARY ACTION BUTTON ("Generate All Application Assets") - Polished Executive Red/Accent Theme */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #e11d48 0%, #be123c 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        border: 1px solid #f43f5e !important;
        border-radius: 8px !important;
        padding: 0.7rem 1.4rem !important;
        box-shadow: 0 4px 15px rgba(225, 29, 72, 0.4) !important;
        letter-spacing: 0.3px;
    }
    div.stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #be123c 0%, #9f1239 100%) !important;
        color: #ffffff !important;
        border-color: #ffffff !important;
        box-shadow: 0 6px 20px rgba(225, 29, 72, 0.6) !important;
    }

    /* DOWNLOAD & LINK BUTTONS (Professional Styling) */
    div.stDownloadButton > button, div.stLinkButton > a {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
        color: #ffffff !important;
        border: 1px solid #0284c7 !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.2rem !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.3) !important;
        transition: all 0.2s ease-in-out !important;
    }
    div.stDownloadButton > button:hover, div.stLinkButton > a:hover {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        border-color: #ffffff !important;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.4) !important;
    }

    /* FILE UPLOADER STYLING */
    [data-testid="stFileUploader"] section {
        background-color: #111827 !important;
        border: 2px dashed #38bdf8 !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }
    [data-testid="stFileUploader"] section button {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease-in-out !important;
    }
    [data-testid="stFileUploader"] section button div,
    [data-testid="stFileUploader"] section button span,
    [data-testid="stFileUploader"] section button p {
        color: #000000 !important;
    }
    [data-testid="stFileUploader"] section button svg {
        fill: #000000 !important;
        color: #000000 !important;
    }
    [data-testid="stFileUploader"] section button:hover {
        background-color: #0f172a !important;
        color: #ffffff !important;
        border: 2px solid #ffffff !important;
    }
    [data-testid="stFileUploader"] section button:hover span,
    [data-testid="stFileUploader"] section button:hover div,
    [data-testid="stFileUploader"] section button:hover p {
        color: #ffffff !important;
    }

    /* Tabs Styling */
    [data-baseweb="tab-list"] {
        background-color: #111827 !important;
        border-radius: 8px;
        padding: 4px;
    }
    [data-baseweb="tab"] {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    [data-baseweb="tab"]:hover {
        color: #38bdf8 !important;
        background-color: #1e293b !important;
    }
    [aria-selected="true"] {
        color: #ffffff !important;
        background-color: #0284c7 !important;
    }

    /* Inputs, Selectboxes & Textareas */
    input, textarea, select {
        background-color: #111827 !important;
        color: #ffffff !important;
        border: 1px solid #334155 !important;
        border-radius: 6px !important;
    }
    input:focus, textarea:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 8px rgba(56, 189, 248, 0.4) !important;
        color: #ffffff !important;
    }
    [data-baseweb="select"] div {
        color: #ffffff !important;
        background-color: #111827 !important;
    }
</style>
""", unsafe_allow_html=True)

# Base paths
BASE_DIR = Path(os.path.expanduser("~")) / "mguiagous" / "smart_mobile_pathfinder_agent"
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"

INPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================
# 2. HELPER FUNCTIONS
# ==========================================
class CleanHTMLTextExtractor(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.is_ignored_tag = False
        self.ignored_tags = {'script', 'style', 'header', 'footer', 'nav', 'noscript'}

    def handle_starttag(self, tag, attrs):
        if tag.lower() in self.ignored_tags:
            self.is_ignored_tag = True

    def handle_endtag(self, tag):
        if tag.lower() in self.ignored_tags:
            self.is_ignored_tag = False

    def handle_data(self, data):
        if not self.is_ignored_tag:
            cleaned = data.strip()
            if cleaned:
                self.text.append(cleaned)

    def get_text(self):
        return ' '.join(self.text)


def fetch_job_from_url(url):
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            html_content = response.read().decode('utf-8', errors='ignore')
            parser = CleanHTMLTextExtractor()
            parser.feed(html_content)
            return re.sub(r'\s+', ' ', parser.get_text())[:3000]
    except Exception as e:
        return f"Could not auto-fetch URL directly ({e}). Please paste description text below."


def infer_metadata_from_text(text):
    inferred_title = "Master Principal Cloud Architect"
    inferred_company = "TargetCompany"
    text_lower = text.lower()
    
    if "weka" in text_lower:
        inferred_company = "WEKA"
    elif "pg&e" in text_lower or "pge" in text_lower or "pacific gas" in text_lower:
        inferred_company = "PGandE"
    elif "oracle" in text_lower:
        inferred_company = "OracleEngineering"
    elif "css" in text_lower:
        inferred_company = "CSS"
        
    if "sales engineer" in text_lower or "solutions engineer" in text_lower:
        inferred_title = "Senior Sales Engineer / Solutions Architect"
    elif "resident architect" in text_lower:
        inferred_title = "Principal Resident Architect"
    elif "infrastructure" in text_lower or "cloud engineer" in text_lower:
        inferred_title = "Cloud Infrastructure Engineer"
    elif "consultant" in text_lower:
        inferred_title = "Principal Cloud & Infrastructure Architect (Consultant)"
        
    return inferred_company, inferred_title


def load_weka_job_description():
    possible_paths = [
        INPUT_DIR / "WEKA" / "WEKA-JOB-Description.pdf",
        INPUT_DIR / "WEKA-JOB-Description.pdf"
    ]
    for jd_path in possible_paths:
        if os.path.exists(jd_path):
            try:
                reader = PdfReader(io.BytesIO(open(jd_path, "rb").read()))
                raw_text = "".join([page.extract_text() or "" for page in reader.pages])
                if len(raw_text.strip()) > 10:
                    return raw_text.strip()
            except Exception:
                pass
    return "Seeking an Enterprise Cloud Solutions Architect to scale high-performance AI data pipelines and OCI infrastructure."


# ==========================================
# 3. INITIALIZE SESSION STATE
# ==========================================
if 'company_templates' not in st.session_state:
    st.session_state['company_templates'] = {
        "WEKA": {
            "title": "Senior Sales Engineer / Solutions Architect",
            "jd": load_weka_job_description()
        },
        "CSS": {
            "title": "Principal Resident Architect",
            "jd": "Seeking an experienced Principal Resident Architect specializing in enterprise cloud migrations, OCI tenancy design, and Infrastructure as Code."
        },
        "OracleEngineering": {
            "title": "Cloud Infrastructure Engineer",
            "jd": "Looking for a senior cloud engineer to design, automate, and scale OCI services and Kubernetes clusters (OKE)."
        },
        "PGandE": {
            "title": "Principal Cloud & Infrastructure Architect (Consultant)",
            "jd": "Seeking a senior infrastructure and cloud architecture expert for strategic initiatives involving enterprise cloud modernization, grid data pipeline security, and robust automation frameworks."
        }
    }

if 'generated_success' not in st.session_state:
    st.session_state['generated_success'] = False
if 'current_company' not in st.session_state:
    st.session_state['current_company'] = ""
if 'current_title' not in st.session_state:
    st.session_state['current_title'] = ""
if 'current_jd_text' not in st.session_state:
    st.session_state['current_jd_text'] = ""
if 'hide_input_column' not in st.session_state:
    st.session_state['hide_input_column'] = False
if 'full_profile_view' not in st.session_state:
    st.session_state['full_profile_view'] = False

# ==========================================
# 4. HERO BANNER & LAYOUT CONTROLS
# ==========================================
st.markdown("""
<div class="executive-banner">
    <h1>🛡️ Pathfinder Agent &bull; Enterprise Command Center</h1>
    <p>High-contrast accessible workspace for synthesizing multi-page executive application portfolios and cloud deployment assets.</p>
</div>
""", unsafe_allow_html=True)

col_ctrl1, col_ctrl2 = st.columns([2, 5])
with col_ctrl1:
    toggle_profile_label = "📖 Collapse Full Profile" if st.session_state['full_profile_view'] else "🔍 Expand Full LinkedIn Profile"
    if st.button(toggle_profile_label, use_container_width=True, key="toggle_profile_view_btn"):
        st.session_state['full_profile_view'] = not st.session_state['full_profile_view']
        st.rerun()

with col_ctrl2:
    if st.session_state.get('generated_success', False):
        hide_input_label = "👁 Restore Input Hub" if st.session_state['hide_input_column'] else "⚡ Hide Input Hub (Focus View)"
        if st.button(hide_input_label, key="toggle_input_visibility"):
            st.session_state['hide_input_column'] = not st.session_state['hide_input_column']
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

if st.session_state['full_profile_view']:
    st.markdown('<div class="section-header">📄 Full LinkedIn Profile Master View</div>', unsafe_allow_html=True)
    master_pdf_path = INPUT_DIR / "Profile.pdf"
    if os.path.exists(master_pdf_path):
        with open(master_pdf_path, "rb") as f:
            b64_profile = base64.b64encode(f.read()).decode('utf-8')
        st.markdown(f'<iframe src="data:application/pdf;base64,{b64_profile}" width="100%" height="850px" type="application/pdf"></iframe>', unsafe_allow_html=True)
    else:
        st.warning("Profile.pdf not found in input directory.")
else:
    if st.session_state.get('hide_input_column', False):
        # Focus View: Middle Display (Left) & Outreach (Right)
        col_display, col_nav = st.columns([1.2, 1.0], gap="large")
        active_columns = [None, col_display, col_nav]
    else:
        # Standard Three-Column Layout: Input Hub (Left), Generated Portfolio/Middle Display (Middle), Outreach & Cloud Sync (Right)
        col_input, col_display, col_nav = st.columns([1.0, 1.2, 1.0], gap="medium")
        active_columns = [col_input, col_display, col_nav]

    # ------------------------------------------
    # COLUMN 1: INPUT & CONTROL HUB
    # ------------------------------------------
    if not st.session_state.get('hide_input_column', False):
        with active_columns[0]:
            st.markdown('<div class="section-header">📥 Input & Control Hub</div>', unsafe_allow_html=True)
            
            if st.session_state.get('generated_success', False):
                st.success("Application suite successfully generated.")
                if st.button("Reset Session State", use_container_width=True, key="reset_session_btn"):
                    st.session_state['generated_success'] = False
                    st.session_state['current_company'] = ""
                    st.session_state['current_title'] = ""
                    st.session_state['current_jd_text'] = ""
                    st.rerun()

            template_keys = ["-- Enter or Select Company/Job --"] + list(st.session_state['company_templates'].keys()) + ["+ Add New Job Opening"]
            selected_template = st.selectbox("Select Template or Add New", template_keys, key="select_template_box")

            if selected_template and selected_template not in ["-- Enter or Select Company/Job --", "+ Add New Job Opening"]:
                if st.session_state.get('current_company') != selected_template:
                    comp_data = st.session_state['company_templates'][selected_template]
                    st.session_state['current_company'] = selected_template
                    st.session_state['current_title'] = comp_data["title"]
                    st.session_state['current_jd_text'] = comp_data["jd"]
                    st.rerun()

            if selected_template == "+ Add New Job Opening":
                st.markdown("---")
                st.markdown("**Create New Job Opening**")
                new_comp_name = st.text_input("New Company Name", placeholder="e.g. PGandE")
                new_job_title = st.text_input("New Job Title", placeholder="e.g. Lead Solutions Architect")
                new_job_jd = st.text_area("Job Description / Requirements", placeholder="Paste description...", height=80)
                
                if st.button("Save & Select Opening", use_container_width=True):
                    if new_comp_name and new_job_title:
                        safe_comp_name = new_comp_name.replace(" ", "")
                        st.session_state['company_templates'][safe_comp_name] = {
                            "title": new_job_title,
                            "jd": new_job_jd if new_job_jd else "Custom infrastructure architecture role."
                        }
                        st.session_state['current_company'] = safe_comp_name
                        st.session_state['current_title'] = new_job_title
                        st.session_state['current_jd_text'] = st.session_state['company_templates'][safe_comp_name]["jd"]
                        st.success(f"Added {safe_comp_name} successfully.")
                        st.rerun()

            job_url = st.text_input("Public Job URL (Optional)", placeholder="https://company.com/careers/role")
            if job_url:
                with st.spinner("Fetching job requirements..."):
                    fetched_text = fetch_job_from_url(job_url)
                    if fetched_text:
                        inf_comp, inf_title = infer_metadata_from_text(fetched_text)
                        st.session_state['current_jd_text'] = fetched_text
                        st.session_state['current_company'] = inf_comp
                        st.session_state['current_title'] = inf_title
                        st.rerun()

            st.markdown("---")
            uploaded_jd_file = st.file_uploader("Upload Job Description File", type=["pdf", "txt"], key="jd_file_uploader_safe")
            if uploaded_jd_file is not None:
                file_hash = uploaded_jd_file.name + str(uploaded_jd_file.size)
                if st.session_state.get('last_processed_jd_file') != file_hash:
                    try:
                        if uploaded_jd_file.type == "application/pdf":
                            reader = PdfReader(io.BytesIO(uploaded_jd_file.getvalue()))
                            extracted_jd_text = "".join([page.extract_text() or "" for page in reader.pages])
                        else:
                            extracted_jd_text = uploaded_jd_file.getvalue().decode("utf-8", errors="ignore")
                        
                        if extracted_jd_text.strip():
                            inf_comp, inf_title = infer_metadata_from_text(extracted_jd_text)
                            st.session_state['current_jd_text'] = extracted_jd_text.strip()
                            st.session_state['current_company'] = inf_comp
                            st.session_state['current_title'] = inf_title
                            st.session_state['last_processed_jd_file'] = file_hash
                            st.success(f"Parsed successfully! Company set to: **{inf_comp}**")
                            st.rerun()
                    except Exception as e:
                        st.error(f"Error parsing file: {e}")

            company_name = st.text_input("Company Name / Directory", value=st.session_state.get('current_company', 'WEKA'))
            job_title = st.text_input("Job Title", value=st.session_state.get('current_title', 'Senior Sales Engineer / Solutions Architect'))
            job_description_input = st.text_area("Target Job Description:", value=st.session_state.get('current_jd_text', ''), height=130)

            st.markdown("---")
            uploaded_profile_file = st.file_uploader("Upload Updated LinkedIn Profile (PDF)", type=["pdf"], key="profile_file_uploader_safe")
            if uploaded_profile_file is not None:
                profile_hash = uploaded_profile_file.name + str(uploaded_profile_file.size)
                if st.session_state.get('last_processed_profile_file') != profile_hash:
                    save_profile_path = INPUT_DIR / "Profile.pdf"
                    with open(save_profile_path, "wb") as f:
                        f.write(uploaded_profile_file.getbuffer())
                    st.session_state['last_processed_profile_file'] = profile_hash
                    st.success("Profile.pdf updated live.")
                    st.rerun()

            st.markdown("---")
            if st.button("Generate All Application Assets", type="primary", use_container_width=True):
                profile_pdf_path = INPUT_DIR / "Profile.pdf"
                if not company_name or company_name.strip() == "":
                    st.error("Please enter a valid Company Name.")
                elif not os.path.exists(profile_pdf_path):
                    st.error("Profile.pdf not found in input/.")
                else:
                    safe_company_dir = OUTPUT_DIR / company_name.replace(" ", "")
                    safe_company_dir.mkdir(parents=True, exist_ok=True)
                    master_profile_text = extract_master_profile_text(INPUT_DIR)
                    
                    with st.spinner(f"Synthesizing customized multi-page executive application suite for {company_name}..."):
                        formatted_markdown_resume = generate_comprehensive_resume(
                            master_profile_text, job_title, company_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        )
                        formatted_markdown_cover = f"# Cover Letter: {job_title} at {company_name}\n\nDear Hiring Team,\n\nAs an enterprise cloud architect..."
                        formatted_markdown_references = f"# Professional References & Publications\n\n1. OKE Automation Guide (Oracle Live Labs)"
                        formatted_markdown_about_yourself = f"# Tell me about yourself\n\nMaster Principal Cloud Architect with 13+ years at Oracle..."
                        formatted_markdown_why_hire_you = f"# Why should we hire you?\n\nImmediate enterprise cloud leadership..."

                        pdf_resume_path, pdf_cover_path, pdf_refs_path = generate_local_documents(
                            job_title, company_name, formatted_markdown_resume, formatted_markdown_cover, formatted_markdown_references, safe_company_dir
                        )
                        
                        pdf_resume_url = upload_to_oci_bucket(pdf_resume_path, bucket_name="A_NewPathFinder_Agent")
                        pdf_cover_url = upload_to_oci_bucket(pdf_cover_path, bucket_name="A_NewPathFinder_Agent")
                        pdf_refs_url = upload_to_oci_bucket(pdf_refs_path, bucket_name="A_NewPathFinder_Agent")
                        
                        email_text, whatsapp_text = generate_outreach_text(company_name, job_title, pdf_resume_url, pdf_cover_url, pdf_refs_url)
                        
                        st.session_state['generated_success'] = True
                        st.session_state['last_resume_path'] = pdf_resume_path
                        st.session_state['last_cover_path'] = pdf_cover_path
                        st.session_state['last_refs_path'] = pdf_refs_path
                        st.session_state['pdf_resume_url'] = pdf_resume_url
                        st.session_state['pdf_cover_url'] = pdf_cover_url
                        st.session_state['pdf_refs_url'] = pdf_refs_url
                        st.session_state['md_resume'] = formatted_markdown_resume
                        st.session_state['md_cover'] = formatted_markdown_cover
                        st.session_state['md_refs'] = formatted_markdown_references
                        st.session_state['md_about_yourself'] = formatted_markdown_about_yourself
                        st.session_state['md_why_hire_you'] = formatted_markdown_why_hire_you
                        st.session_state['email_text'] = email_text
                        st.session_state['whatsapp_text'] = whatsapp_text
                        st.rerun()

    # ------------------------------------------
    # COLUMN 2: MIDDLE LAYER (Real-time Profile Preview / Generated Portfolio)
    # ------------------------------------------
    with active_columns[1]:
        if st.session_state.get('generated_success', False):
            st.markdown('<div class="section-header">📋 Generated Executive Portfolio</div>', unsafe_allow_html=True)
            tab_names = ["📄 Tailored Resume", "✉️ Cover Letter", "📚 References", "💡 Tell About Yourself", "🎯 Why Hire You"]
            tabs = st.tabs(tab_names)
            
            with tabs[0]:
                st.markdown(st.session_state.get('md_resume', ''))
            with tabs[1]:
                st.markdown(st.session_state.get('md_cover', ''))
            with tabs[2]:
                st.markdown(st.session_state.get('md_refs', ''))
            with tabs[3]:
                st.markdown(st.session_state.get('md_about_yourself', ''))
            with tabs[4]:
                st.markdown(st.session_state.get('md_why_hire_you', ''))
        else:
            st.markdown('<div class="section-header">📄 Real-Time Master LinkedIn Profile</div>', unsafe_allow_html=True)
            master_pdf_path = INPUT_DIR / "Profile.pdf"
            if os.path.exists(master_pdf_path):
                with open(master_pdf_path, "rb") as f:
                    b64_profile = base64.b64encode(f.read()).decode('utf-8')
                st.markdown(f'<iframe src="data:application/pdf;base64,{b64_profile}" width="100%" height="750px" type="application/pdf"></iframe>', unsafe_allow_html=True)
            else:
                st.info("Master `Profile.pdf` not found in `input/` directory. Upload your LinkedIn Profile PDF on the left to preview it here in real-time.")

    # ------------------------------------------
    # COLUMN 3: RIGHT OUTREACH & CLOUD SYNC & DOWNLOADS
    # ------------------------------------------
    with active_columns[2]:
        st.markdown('<div class="section-header">🚀 Outreach & Cloud Sync</div>', unsafe_allow_html=True)
        if st.session_state.get('generated_success', False):
            st.markdown("**📥 Download Generated Asset Package**")
            
            res_p = st.session_state.get('last_resume_path')
            cov_p = st.session_state.get('last_cover_path')
            ref_p = st.session_state.get('last_refs_path')
            
            if res_p and os.path.exists(res_p):
                with open(res_p, "rb") as f:
                    st.download_button("📥 Download Resume PDF", f, file_name=Path(res_p).name, mime="application/pdf", use_container_width=True)
            if cov_p and os.path.exists(cov_p):
                with open(cov_p, "rb") as f:
                    st.download_button("📥 Download Cover Letter PDF", f, file_name=Path(cov_p).name, mime="application/pdf", use_container_width=True)
            if ref_p and os.path.exists(ref_p):
                with open(ref_p, "rb") as f:
                    st.download_button("📥 Download References PDF", f, file_name=Path(ref_p).name, mime="application/pdf", use_container_width=True)
            
            st.markdown("---")
            st.markdown("**OCI Object Storage Cloud URLs**")
            st.code(st.session_state.get('pdf_resume_url', ''), language="text")
            st.code(st.session_state.get('pdf_cover_url', ''), language="text")
            
            st.markdown("---")
            st.markdown("**Recruiter Email Outreach**")
            st.text_area("Email Draft", value=st.session_state.get('email_text', ''), height=130)
            
            st.markdown("**WhatsApp Quick Pitch**")
            st.text_area("WhatsApp Message", value=st.session_state.get('whatsapp_text', ''), height=70)
        else:
            st.info("Once you generate your application suite, direct PDF download buttons, cloud storage URLs, and recruiter outreach templates will appear here.")