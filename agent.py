import os
from dotenv import load_dotenv
import google.generativeai as genai
from notifier import send_email_notification

# Load environment variables from .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def evaluate_job_match(profile_text: str, job_description: str) -> str:
    """
    Uses Gemini to analyze the fit between a candidate's profile and a job description.
    """
    prompt = f"""
    You are an expert career and recruitment advisor. 
    Analyze the candidate profile against the provided job description.
    
    Provide a professional, clear evaluation structured as follows:
    1. **Match Score**: (e.g., 90/100)
    2. **Key Strengths**: Why the candidate fits well.
    3. **Skill Gaps / Risks**: Any missing requirements or potential flags.
    4. **Recommendation**: Should the candidate apply or skip?

    ---
    CANDIDATE PROFILE:
    {profile_text}

    ---
    JOB DESCRIPTION:
    {job_description}
    """

    # Using Gemini 1.5 Flash for fast, accurate text analysis
    model = genai.GenerativeModel("gemini-3.8-flash")
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    print("[*] Pathfinder Agent initialized.")
    
    # --- STEP 1: Paste your manual inputs here ---
    my_linkedin_profile = """
    Principal Cloud Architect & Cloud Engineer with 20+ years of experience in systems architecture.
    Specializing in Oracle Cloud Infrastructure (OCI), Infrastructure as Code (Terraform, OpenTofu, Ansible),
    Kubernetes (OKE), multi-cloud networking, and enterprise cloud migrations (AWS to OCI).
    """
    
    target_job_description = """
    We are seeking a Principal Resident Architect / Cloud Engineer with deep expertise in OCI, Terraform, 
    and Kubernetes. Must have 15+ years of experience leading enterprise cloud migrations, stakeholder workshops, 
    and infrastructure automation.
    """
    
    print("[*] Evaluating match with Gemini...")
    evaluation_result = evaluate_job_match(my_linkedin_profile, target_job_description)
    
    print("\n--- GEMINI EVALUATION RESULTS ---")
    print(evaluation_result)
    
    # Format output for HTML email
    email_html = f"""
    <h2>Smart Mobile Pathfinder Agent - Job Match Report</h2>
    <div style="font-family: Arial, sans-serif; line-height: 1.6;">
        <pre style="white-space: pre-wrap; font-family: inherit;">{evaluation_result}</pre>
    </div>
    """
    
    print("\n[*] Sending evaluation report via email...")
    send_email_notification(
        subject="Pathfinder Agent: Job Match Evaluation Report",
        html_content=email_html
    )