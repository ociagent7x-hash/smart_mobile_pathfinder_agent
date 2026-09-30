"""
Pathfinder Agent (Streamlit UI - High-Contrast Enterprise Theme)
-----------------------------------------------------------------
Description: Enterprise command center featuring high-contrast UI styling 
where text is fully visible on dark backgrounds without requiring mouse hover.
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
# 1. PAGE CONFIGURATION & HIGH-CONTRAST STYLING
# ==========================================
st.set_page_config(
    page_title="Pathfinder Agent | Enterprise Command Center",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# High-Contrast Corporate Theme Injection (Ensuring white text on dark buttons/backgrounds)
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

    /* HIGH-CONTRAST BUTTONS (Explicit White Text on Dark Backgrounds) */
    div.stButton > button {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.2s ease-in-out !important;
    }
    div.stButton > button:hover {
        background-color: #0284c7 !important;
        color: #ffffff !important;
        border-color: #ffffff !important;
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.6) !important;
    }

    /* Primary Action Buttons */
    button[kind="primary"] {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        color: #ffffff !important;
        border: 1px solid #38bdf8 !important;
    }
    button[kind="primary"]:hover {
        background: linear-gradient(135deg, #0369a1 0%, #075985 100%) !important;
        border-color: #ffffff !important;
        color: #ffffff !important;
    }

    /* Download Buttons High-Contrast */
    div.stDownloadButton > button {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 1px solid #38bdf8 !important;
        font-weight: 600 !important;
    }
    div.stDownloadButton > button:hover {
        background-color: #0284c7 !important;
        color: #ffffff !important;
        border-color: #ffffff !important;
    }

    /* Link Buttons High-Contrast */
    div.stLinkButton > a {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 1px solid #38bdf8 !important;
        font-weight: 600 !important;
        text-align: center !important;
        border-radius: 8px !important;
    }
    div.stLinkButton > a:hover {
        background-color: #0284c7 !important;
        color: #ffffff !important;
        border-color: #ffffff !important;
    }

    /* File Uploader High-Contrast Fixes */
    [data-testid="stFileUploader"] section {
        background-color: #111827 !important;
        border: 2px dashed #38bdf8 !important;
    }
    [data-testid="stFileUploader"] label, 
    [data-testid="stFileUploader"] small, 
    [data-testid="stFileUploader"] span,
    [data-testid="stFileUploader"] div {
        color: #ffffff !important;
    }

    /* Tab Titles Visibility & High Contrast */
    [data-baseweb="tab-list"] {
        background-color: #111827 !important;
        border-radius: 8px;
        padding: 4px;
    }
    [data-baseweb="tab"] {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    [data-baseweb="tab"]:hover {
        color: #38bdf8 !important;
        background-color: #1e293b !important;
        border-radius: 6px;
    }
    [aria-selected="true"] {
        color: #ffffff !important;
        background-color: #0284c7 !important;
        border-radius: 6px;
    }

    /* Text Inputs, Selectboxes & Textareas */
    input, textarea, select {
        background-color: #111827 !important;
        color: #ffffff !important;
        border: 1px solid #334155 !important;
    }
    input:focus, textarea:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 5px rgba(56, 189, 248, 0.5) !important;
        color: #ffffff !important;
    }
    
    /* Selectbox dropdown text visibility */
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

if 'company_name_input' not in st.session_state:
    st.session_state['company_name_input'] = st.session_state['current_company']
if 'job_title_input' not in st.session_state:
    st.session_state['job_title_input'] = st.session_state['current_title']
if 'job_description_textarea' not in st.session_state:
    st.session_state['job_description_textarea'] = st.session_state['current_jd_text']


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
        hide_input_label = "👁️️ Restore Input Hub" if st.session_state['hide_input_column'] else "⚡ Hide Input Hub (Focus View)"
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
        col_display, col_nav = st.columns([1.1, 1.1], gap="large")
        active_columns = [None, col_display, col_nav]
    else:
        col_input, col_display, col_nav = st.columns([1.0, 1.1, 1.0], gap="medium")
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
                    st.session_state['company_name_input'] = ""
                    st.session_state['job_title_input'] = ""
                    st.session_state['job_description_textarea'] = ""
                    st.rerun()

            template_keys = ["-- Enter or Select Company/Job --"] + list(st.session_state['company_templates'].keys()) + ["+ Add New Job Opening", "-- Public URL / Custom --"]
            
            selected_template = st.selectbox("Select Template or Add New", template_keys, key="select_template_box")

            if selected_template and selected_template not in ["-- Enter or Select Company/Job --", "+ Add New Job Opening", "-- Public URL / Custom --"]:
                if st.session_state.get('current_company') != selected_template:
                    comp_data = st.session_state['company_templates'][selected_template]
                    st.session_state['current_company'] = selected_template
                    st.session_state['current_title'] = comp_data["title"]
                    st.session_state['current_jd_text'] = comp_data["jd"]
                    st.session_state['company_name_input'] = selected_template
                    st.session_state['job_title_input'] = comp_data["title"]
                    st.session_state['job_description_textarea'] = comp_data["jd"]
                    st.rerun()

            if selected_template == "+ Add New Job Opening":
                st.markdown("---")
                st.markdown("**Create New Job Opening**")
                new_comp_name = st.text_input("New Company Name (Directory)", placeholder="e.g. PGandE", key="new_comp_input")
                new_job_title = st.text_input("New Job Title", placeholder="e.g. Lead Solutions Architect", key="new_title_input")
                new_job_jd = st.text_area("Job Description / Requirements", placeholder="Paste description...", height=80, key="new_jd_textarea")
                
                if st.button("Save & Select Opening", use_container_width=True, key="save_new_opening_btn"):
                    if new_comp_name and new_job_title:
                        safe_comp_name = new_comp_name.replace(" ", "")
                        st.session_state['company_templates'][safe_comp_name] = {
                            "title": new_job_title,
                            "jd": new_job_jd if new_job_jd else "Custom infrastructure architecture role."
                        }
                        st.session_state['current_company'] = safe_comp_name
                        st.session_state['current_title'] = new_job_title
                        st.session_state['current_jd_text'] = st.session_state['company_templates'][safe_comp_name]["jd"]
                        st.session_state['company_name_input'] = safe_comp_name
                        st.session_state['job_title_input'] = new_job_title
                        st.session_state['job_description_textarea'] = st.session_state['company_templates'][safe_comp_name]["jd"]
                        st.success(f"Added {safe_comp_name} successfully.")
                        st.rerun()
                    else:
                        st.error("Provide at least a Company Name and Job Title.")

            job_url = st.text_input("Public Job URL (Optional)", placeholder="https://company.com/careers/role", key="job_url_input")
            if job_url:
                with st.spinner("Fetching job requirements..."):
                    fetched_text = fetch_job_from_url(job_url)
                    if fetched_text:
                        inf_comp, inf_title = infer_metadata_from_text(fetched_text)
                        st.session_state['current_jd_text'] = fetched_text
                        st.session_state['current_company'] = inf_comp
                        st.session_state['current_title'] = inf_title
                        st.session_state['company_name_input'] = inf_comp
                        st.session_state['job_title_input'] = inf_title
                        st.session_state['job_description_textarea'] = fetched_text
                        st.rerun()

            st.markdown("---")
            uploaded_jd_file = st.file_uploader("Upload Job Description File", type=["pdf", "txt"], key="jd_file_uploader")
            
            if uploaded_jd_file is not None:
                file_hash = uploaded_jd_file.name + str(uploaded_jd_file.size)
                if st.session_state.get('last_processed_file') != file_hash:
                    extracted_jd_text = ""
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
                            st.session_state['company_name_input'] = inf_comp
                            st.session_state['job_title_input'] = inf_title
                            st.session_state['job_description_textarea'] = extracted_jd_text.strip()
                            st.session_state['last_processed_file'] = file_hash
                            st.success(f"Parsed successfully! Company set to: **{inf_comp}**")
                            st.rerun()
                    except Exception as e:
                        st.error(f"Error parsing uploaded file: {e}")

            company_name = st.text_input("Company Name / Directory", key="company_name_input")
            st.session_state['current_company'] = company_name

            job_title = st.text_input("Job Title", key="job_title_input")
            st.session_state['current_title'] = job_title

            job_description_input = st.text_area("Target Job Description:", key="job_description_textarea", height=130)
            st.session_state['current_jd_text'] = job_description_input

            st.markdown("---")
            uploaded_profile_file = st.file_uploader("Upload Updated LinkedIn Profile (PDF)", type=["pdf"], key="profile_file_uploader")
            if uploaded_profile_file is not None:
                save_profile_path = INPUT_DIR / "Profile.pdf"
                with open(save_profile_path, "wb") as f:
                    f.write(uploaded_profile_file.getbuffer())
                st.success("Profile.pdf updated live.")
                st.rerun()

            st.markdown("---")
            if st.button("Generate All Application Assets", type="primary", use_container_width=True, key="generate_assets_action_btn"):
                profile_pdf_path = INPUT_DIR / "Profile.pdf"
                
                if not company_name or company_name.strip() == "":
                    st.error("Please enter a valid Company Name / Directory.")
                elif not os.path.exists(profile_pdf_path):
                    st.error("Profile.pdf not found in input/. Please upload your LinkedIn profile PDF.")
                else:
                    file_mtime = os.path.getmtime(profile_pdf_path)
                    generation_timestamp = datetime.fromtimestamp(file_mtime).strftime("%Y-%m-%d %H:%M:%S")
                    safe_company_dir = OUTPUT_DIR / company_name.replace(" ", "")
                    safe_company_dir.mkdir(parents=True, exist_ok=True)
                    
                    master_profile_text = extract_master_profile_text(INPUT_DIR)
                    
                    with st.spinner(f"Synthesizing customized multi-page executive application suite for {company_name}..."):
                        try:
                            formatted_markdown_resume = generate_comprehensive_resume(
                                master_profile_text, job_title, company_name, generation_timestamp
                            )

                            formatted_markdown_cover = f"""# Mahamat Hissein Guiagoussou
**San Francisco Bay Area | mail2mahamat@gmail.com | +1 (408) 313-7157**  

## COVER LETTER: {job_title} at {company_name}

Dear {company_name} Executive Hiring Team,

As an enterprise cloud architect and technical sales leader combining over 13 years of cloud architecture leadership at Oracle with an extensive background in distributed systems (R&D) at Sun Microsystems, I was immediately drawn to your mission. Your foundational work in building robust enterprise infrastructure aligns perfectly with my background in scaling complex distributed systems, OCI tenancies, and automated infrastructure frameworks.

Throughout my executive tenure at Oracle, I have led strategic enterprise customer engagements, multi-cloud automation initiatives, and production-grade Kubernetes deployments. Bringing this proven technical authority to {company_name} will ensure immediate operational excellence and accelerated cloud delivery.

I look forward to discussing how my experience can support your engineering goals.

Best regards,  
**Mahamat Hissein Guiagoussou**
"""

                            formatted_markdown_references = f"""# Mahamat Hissein Guiagoussou
**Professional References & Complete Publications Index | Dossier Timestamp: {generation_timestamp}**  

## SECTION 1: RECOMMENDATIONS & ENDORSEMENTS

### 1. TARGETED FEATURED RECOMMENDATION (Best Fit for {job_title} at {company_name})
* **Enterprise Cloud Director / VP Engineering (Strategic Client Partner):** "Mahamat consistently demonstrates master-level architecture authority across multi-cloud and enterprise environments. His mastery of OCI tenancy designs, automated Kubernetes cluster deployments, and Terraform frameworks directly accelerated our enterprise migration timelines by months while eliminating operational friction."

### 2. ADDITIONAL RECENT RECOMMENDATIONS (Top Latest)
* **Principal Cloud Architect & Peer Lead:** "Working alongside Mahamat on complex multi-client engagements has been extraordinary. His deep infrastructure knowledge combined with executive presence makes him an unmatched technical leader."
* **Senior Director of Cloud Engineering:** "Mahamat’s technical acumen in high-performance computing and Infrastructure as Code is world-class. He bridges business strategy and deep technical execution effortlessly."
* **Enterprise Account General Manager:** "Mahamat is a visionary technical sales leader. His leadership during our major enterprise onboarding strategy sessions set the benchmark for client success across the entire region."

---

## SECTION 2: APPENDIXES — OKE BEST PRACTICES AUTOMATION & LIVE-LABS
*(Complete unsummarized list of professional contributions and active reference publications)*

1. [Build Once, Import Everywhere: Golden Image Distribution Across OCI Tenancies and Regions (Sept 17, 2026)](https://www.linkedin.com/in/mahamathisseinguiagoussou/) — LinkedIn Contribution
2. [Deploy and Use OKE Clusters with Simple and Advanced Terraform Modules and Best Practices, Oracle Live Lab (Sep 1, 2026)](https://www.oracle.com) — Oracle Learning Guide
3. [Deploy Oracle Cloud Infrastructure Kubernetes Engine (OKE) using Best Practices and Automation, Oracle Education (Feb 20, 2026)](https://www.oracle.com) — Oracle Education Guide
4. [Deploy Oracle Cloud Infrastructure Kubernetes Engine (OKE) using Advanced Terraform Modules, Oracle Publications (Oct 30, 2025)](https://www.oracle.com) — Oracle Architecture Center
5. [Create Oracle Cloud Infrastructure Kubernetes Engine Cluster using Terraform, Oracle Publications (Jul 11, 2025)](https://www.oracle.com) — Oracle Help Center
6. [Configure Private DNS Zones, Views, and Resolvers to Accelerate OCI Architect Professional Certification with Terraform, Oracle Publications (Nov 19, 2024)](https://www.oracle.com) — Oracle Help Center
7. [Accelerating Oracle Cloud Infrastructure Architect Professional Certification with Terraform Automation, Oracle Publications (Aug 30, 2024)](https://www.oracle.com) — Oracle Learn Live Lab
"""

                            formatted_markdown_about_yourself = f"""# Interview Prep: "Tell me about yourself"
**Target Role:** {job_title} at {company_name}  
**Candidate:** Mahamat Hissein Guiagoussou  

"I am a Master Principal Cloud Architect and Technical Sales Leader with over 13 years of executive cloud tenure at Oracle and nearly 8 years of core infrastructure engineering background at Sun Microsystems. Currently at Oracle, I lead strategic enterprise customer engagements, multi-cloud automation initiatives, and production-grade Kubernetes (OKE) and Infrastructure as Code deployments. I am eager to bring this expertise to **{company_name}** for the **{job_title}** role."
"""

                            formatted_markdown_why_hire_you = f"""# Interview Prep: "Why should we hire you?"
**Target Role:** {job_title} at {company_name}  
**Candidate:** Mahamat Hissein Guiagoussou  

"You should hire me because I bring an immediate synthesis of deep enterprise architecture expertise, multi-cloud mastery, and customer-facing technical leadership specifically tailored to **{company_name}**. From automated golden image distribution to large-scale OCI migrations, I deliver robust operational frameworks from day one."
"""

                            pdf_resume_path, pdf_cover_path, pdf_refs_path = generate_local_documents(
                                job_title=job_title,
                                company_name=company_name,
                                resume_text=formatted_markdown_resume,
                                cover_letter_text=formatted_markdown_cover,
                                references_text=formatted_markdown_references,
                                output_dir=safe_company_dir
                            )
                            
                            pdf_resume_url = upload_to_oci_bucket(pdf_resume_path, bucket_name="A_NewPathFinder_Agent")
                            pdf_cover_url = upload_to_oci_bucket(pdf_cover_path, bucket_name="A_NewPathFinder_Agent")
                            pdf_refs_url = upload_to_oci_bucket(pdf_refs_path, bucket_name="A_NewPathFinder_Agent")
                            
                            email_text, whatsapp_text = generate_outreach_text(company_name, job_title, pdf_resume_url, pdf_cover_url, pdf_refs_url)
                            
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
                            st.session_state['generated_success'] = True
                            st.session_state['generation_timestamp'] = generation_timestamp
                            
                            st.success(f"Application suite generated successfully in `{safe_company_dir.name}/`.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error during generation/upload: {e}")

    # ------------------------------------------
    # COLUMN 2: REAL-TIME OUTPUT & DOWNLOADS
    # ------------------------------------------
    with active_columns[1]:
        st.markdown('<div class="section-header">📊 Real-Time Output & Downloads</div>', unsafe_allow_html=True)
        
        if not st.session_state.get('generated_success', False):
            st.markdown("**Current LinkedIn Profile Preview**")
            master_pdf_path = INPUT_DIR / "Profile.pdf"
            if os.path.exists(master_pdf_path):
                with open(master_pdf_path, "rb") as f:
                    b64_profile = base64.b64encode(f.read()).decode('utf-8')
                st.markdown(f'<iframe src="data:application/pdf;base64,{b64_profile}" width="100%" height="560px" type="application/pdf"></iframe>', unsafe_allow_html=True)
            else:
                st.warning("Profile.pdf not found in input directory.")
        else:
            st.markdown(f"**Profile Timestamp:** {st.session_state.get('generation_timestamp', '')}")
            st.markdown("---")
            
            st.markdown("#### Executive Assets")
            
            res_txt, res_p1, res_p2 = st.columns([2.4, 0.8, 0.9])
            with res_txt:
                st.markdown("**Generated Resume:**")
            with res_p1:
                with open(st.session_state['last_resume_path'], "rb") as f:
                    st.download_button("📥 PDF", f, file_name=os.path.basename(st.session_state['last_resume_path']), mime="application/pdf", key="dl_res_pdf_inline", use_container_width=True)
            with res_p2:
                with open(st.session_state['last_resume_path'], "rb") as f:
                    st.download_button("📝 Word", f, file_name=os.path.basename(st.session_state['last_resume_path']).replace(".pdf", ".docx"), mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", key="dl_res_doc_inline", use_container_width=True)

            cov_txt, cov_p1, cov_p2 = st.columns([2.4, 0.8, 0.9])
            with cov_txt:
                st.markdown("**Cover Letter:**")
            with cov_p1:
                with open(st.session_state['last_cover_path'], "rb") as f:
                    st.download_button("📥 PDF", f, file_name=os.path.basename(st.session_state['last_cover_path']), mime="application/pdf", key="dl_cov_pdf_inline", use_container_width=True)
            with cov_p2:
                with open(st.session_state['last_cover_path'], "rb") as f:
                    st.download_button("📝 Word", f, file_name=os.path.basename(st.session_state['last_cover_path']).replace(".pdf", ".docx"), mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", key="dl_cov_doc_inline", use_container_width=True)

            ref_txt, ref_p1, ref_p2 = st.columns([2.4, 0.8, 0.9])
            with ref_txt:
                st.markdown("**References & Publications:**")
            with ref_p1:
                with open(st.session_state['last_refs_path'], "rb") as f:
                    st.download_button("📥 PDF", f, file_name=os.path.basename(st.session_state['last_refs_path']), mime="application/pdf", key="dl_refs_pdf_inline", use_container_width=True)
            with ref_p2:
                with open(st.session_state['last_refs_path'], "rb") as f:
                    st.download_button("📝 Word", f, file_name=os.path.basename(st.session_state['last_refs_path']).replace(".pdf", ".docx"), mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", key="dl_refs_doc_inline", use_container_width=True)

            st.markdown("---")
            st.markdown("### Generated Communications")
            st.markdown("**Email Outreach**")
            with st.container(height=110):
                st.code(st.session_state['email_text'], language="text")
                
            st.markdown("**WhatsApp Outreach**")
            with st.container(height=80):
                st.code(st.session_state['whatsapp_text'], language="text")

            st.markdown("---")
            st.markdown("### Interview Prep Suggestions")
            with st.container(border=True):
                st.markdown(st.session_state['md_about_yourself'])
                st.markdown("---")
                st.markdown(st.session_state['md_why_hire_you'])

    # ------------------------------------------
    # COLUMN 3: SEQUENTIAL RENDERED TABS
    # ------------------------------------------
    with active_columns[2]:
        st.markdown('<div class="section-header">🧭 Output Navigator</div>', unsafe_allow_html=True)
        st.markdown("Inspect sequential generated assets and rendered formats.")
        
        if st.session_state.get('generated_success', False):
            tab_md_res, tab_md_cov, tab_md_refs, tab_pdf_res, tab_pdf_cov, tab_pdf_refs, tab_comm1 = st.tabs([
                "MD Resume", "MD Cover", "MD References", 
                "PDF Resume", "PDF Cover", "PDF References", 
                "Outreach"
            ])
            
            with tab_md_res:
                st.markdown("#### Rendered Resume Markdown")
                st.markdown(st.session_state['md_resume'])
                
            with tab_md_cov:
                st.markdown("#### Rendered Cover Letter Markdown")
                st.markdown(st.session_state['md_cover'])

            with tab_md_refs:
                st.markdown("#### Rendered References & Publications Markdown")
                st.markdown(st.session_state['md_refs'])
                
            with tab_pdf_res:
                st.markdown("#### PDF Resume Viewer")
                with open(st.session_state['last_resume_path'], "rb") as f:
                    b64 = base64.b64encode(f.read()).decode('utf-8')
                st.markdown(f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="450px" type="application/pdf"></iframe>', unsafe_allow_html=True)
                st.link_button("Open in OCI Bucket", st.session_state['pdf_resume_url'], use_container_width=True)
                
            with tab_pdf_cov:
                st.markdown("#### PDF Cover Letter Viewer")
                with open(st.session_state['last_cover_path'], "rb") as f:
                    b64 = base64.b64encode(f.read()).decode('utf-8')
                st.markdown(f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="450px" type="application/pdf"></iframe>', unsafe_allow_html=True)
                st.link_button("Open in OCI Bucket", st.session_state['pdf_cover_url'], use_container_width=True)
                
            with tab_pdf_refs:
                st.markdown("#### PDF References & Index Viewer")
                with open(st.session_state['last_refs_path'], "rb") as f:
                    b64 = base64.b64encode(f.read()).decode('utf-8')
                st.markdown(f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="450px" type="application/pdf"></iframe>', unsafe_allow_html=True)
                st.link_button("Open in OCI Bucket", st.session_state['pdf_refs_url'], use_container_width=True)
                
            with tab_comm1:
                st.markdown("#### Email Outreach Text")
                st.code(st.session_state['email_text'], language="text")
                st.markdown("#### WhatsApp Outreach Text")
                st.code(st.session_state['whatsapp_text'], language="text")
        else:
            st.warning("Not generated yet. Please click **Generate All Application Assets** first.")