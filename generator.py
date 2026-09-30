"""
=============================================================================
Module:      generator.py
Description: Asset synthesis engine handling local PDF generation via ReportLab, 
             cloud storage integrations, and executive document structuring.
Author:      Mahamat Hissein GUIAGOUSSOU
Last Updated: September 29, 2026 at 8:15 PM
=============================================================================
"""

import os
import re
import urllib.parse
from pathlib import Path
from pypdf import PdfReader
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


def extract_master_profile_text(input_dir):
    """Extracts raw text from the master Profile.pdf if available."""
    profile_path = Path(input_dir) / "Profile.pdf"
    if profile_path.exists():
        try:
            reader = PdfReader(str(profile_path))
            raw_text = "".join([page.extract_text() or "" for page in reader.pages])
            if len(raw_text.strip()) > 100:
                return raw_text.strip()
        except Exception:
            pass
    return ""


def markdown_to_reportlab_story(md_text, styles, is_resume=False):
    """Converts structured Markdown string into a controlled ReportLab Flowables story."""
    story = []
    lines = md_text.splitlines()

    normal_style = styles["Normal"]
    h1_style = styles["Heading1"]
    h2_style = styles["Heading2"]
    h3_style = styles["Heading3"]
    bullet_style = styles["BulletText"]

    spacer_mult = 0.55 if is_resume else 1.0

    for line in lines:
        stripped = line.strip()
        if not stripped:
            story.append(Spacer(1, int(3 * spacer_mult)))
            continue

        if stripped == "[PAGE_BREAK]":
            story.append(PageBreak())
            continue

        if stripped in ["---", "***", "___"]:
            story.append(Spacer(1, int(2 * spacer_mult)))
            story.append(HRFlowable(width="100%", thickness=0.75, color=colors.HexColor("#334155"), spaceBefore=2, spaceAfter=4))
            continue

        formatted_line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', stripped)
        formatted_line = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2" color="#0284c7"><u>\1</u></a>', formatted_line)

        if line.startswith("# "):
            story.append(Paragraph(formatted_line[2:], h1_style))
            story.append(Spacer(1, int(4 * spacer_mult)))
        elif line.startswith("## "):
            story.append(Spacer(1, int(5 * spacer_mult)))
            story.append(Paragraph(formatted_line[3:], h2_style))
            story.append(Spacer(1, int(2 * spacer_mult)))
        elif line.startswith("### "):
            story.append(Spacer(1, int(4 * spacer_mult)))
            story.append(Paragraph(formatted_line[4:], h3_style))
            story.append(Spacer(1, int(1 * spacer_mult)))
        elif line.startswith("* ") or line.startswith("- "):
            story.append(Paragraph(f"• {formatted_line[2:]}", bullet_style))
            story.append(Spacer(1, int(1 * spacer_mult)))
        else:
            story.append(Paragraph(formatted_line, normal_style))
            story.append(Spacer(1, int(2 * spacer_mult)))

    return story


def build_pdf_document(output_path, md_text, is_resume=False):
    """Generates a PDF document with strict margin and leading controls."""
    margin = 30 if is_resume else 36

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        leftMargin=margin,
        rightMargin=margin,
        topMargin=margin,
        bottomMargin=margin
    )

    styles = getSampleStyleSheet()
    
    styles.add(ParagraphStyle(
        name="Heading1Custom",
        parent=styles["Heading1"],
        fontSize=15 if is_resume else 18,
        leading=18 if is_resume else 22,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=3,
        fontName="Helvetica-Bold"
    ))
    
    styles.add(ParagraphStyle(
        name="Heading2Custom",
        parent=styles["Heading2"],
        fontSize=10.5 if is_resume else 12,
        leading=13 if is_resume else 15,
        textColor=colors.HexColor("#0284c7"),
        spaceBefore=4,
        spaceAfter=2,
        fontName="Helvetica-Bold"
    ))
    
    styles.add(ParagraphStyle(
        name="Heading3Custom",
        parent=styles["Heading3"],
        fontSize=9.0 if is_resume else 10,
        leading=11 if is_resume else 13,
        textColor=colors.HexColor("#1e293b"),
        spaceBefore=3,
        spaceAfter=1,
        fontName="Helvetica-Bold"
    ))
    
    styles["Normal"].fontSize = 8.2 if is_resume else 9.0
    styles["Normal"].leading = 10.5 if is_resume else 12.5
    styles["Normal"].textColor = colors.HexColor("#334155")
    styles["Normal"].fontName = "Helvetica"

    styles.add(ParagraphStyle(
        name="BulletText",
        parent=styles["Normal"],
        leftIndent=8,
        firstLineIndent=-5,
        spaceAfter=1
    ))

    custom_styles = {
        "Normal": styles["Normal"],
        "Heading1": styles["Heading1Custom"],
        "Heading2": styles["Heading2Custom"],
        "Heading3": styles["Heading3Custom"],
        "BulletText": styles["BulletText"]
    }

    story = markdown_to_reportlab_story(md_text, custom_styles, is_resume=is_resume)
    doc.build(story)


def generate_comprehensive_resume(master_profile_text, job_title, company_name, timestamp):
    """Synthesizes a complete executive resume including full experience, complete education, and appendixes."""
    return f"""# Mahamat Hissein Guiagoussou
**San Francisco Bay Area | mail2mahamat@gmail.com | +1 (408) 313-7157**  
[LinkedIn Profile](https://www.linkedin.com/in/mahamathisseinguiagoussou/) | Dossier Generated: {timestamp}  

## EXECUTIVE SUMMARY
Master Principal Cloud Architect and Technical Sales Leader combining over 13 years of executive tenure at Oracle with nearly 8 years of core infrastructure engineering at Sun Microsystems. Recognized for decades as a top Customer and Field Engineer, acting as a recognized Subject Matter Expert (SME) on Infrastructure as Code (IaC) and Terraform. Proven technical authority specializing in Oracle Kubernetes Engine (OKE) provisioning automation (see Appendixes), enterprise cloud transformation, and multi-cloud architectures. Expert in leading complex customer onboarding lifecycles, driving high-stakes architectural implementations, and ensuring long-term operational success for mission-critical enterprise workloads tailored specifically for **{company_name}** targeting the **{job_title}** position.

---

## CORE COMPETENCIES & TECHNICAL EXPERTISE
* **Master Customer Engineering & Lead Architecture:** Technical Pre-Sales, Proof-of-Concepts (PoCs), Customer Enablement, Oracle Customer Success alignment, Technical Advisorship, Oracle Kubernetes Engine (OKE) Cluster Architecture Deployment Automation, Container Orchestration, Scalable Microservices, Enterprise Onboarding & Operational Handover.
* **Multi-Cloud & Systems Architecture:** Oracle Cloud Infrastructure (OCI), AWS, Azure, GCP, High-Performance Compute (HPC), Distributed Parallel File Systems, Data Center Networking.
* **Systems & Technical Leadership:** Deep Linux OS Knowledge, High-Stakes Proof-of-Concepts (PoCs), Technical Pre-Sales, Cross-Functional Leadership, AIOps/MLOps Pipelines.
* **Infrastructure as Code (IaC) & Terraform (SME):** Subject Matter Expert (SME) in Terraform, OpenTofu, Automated Landing Zones, Infrastructure Automation, Configuration Management, Ansible.

---

## PROFESSIONAL EXPERIENCE & TENURE

### Master Principal Architect, Cloud Migration & AI/MLOps Solutions Practice Lead
**Oracle | June 2026 - Present | San Francisco Bay Area**
* Lead strategic enterprise customer engagements and overall business opportunities as a senior Customer Engineer, bridging core cloud infrastructure automation with modern AI platforms and Oracle Kubernetes Engine (OKE) architectures deployment and operation automation.
* Heavy Infrastructure as Code (IaC) & Terraform Integration: Leverage Infrastructure as Code (IaC) and Terraform to engineer scalable containerized architecture patterns, balancing native Kubernetes (OKE) implementations with automated operational toolchains for high-throughput AI workloads.
* Orchestrate end-to-end customer onboarding lifecycles spanning initial discovery, governance, source-to-target architecture design, landing-zone readiness, migration planning, wave validation, pilot execution, production cutover, and operational handover.
* Publish multi-part technical blog series and hands-on live labs (see Appendixes) for Oracle Kubernetes Engine (OKE) to empower and enable OCI developers, architects, and implementers with best practices in cloud automation and infrastructure deployment.

### Multi-Cloud Solutions Automation Practice Lead
**Oracle | March 2023 - Present | Pleasanton, CA**
* Spearheaded the development of advanced cloud solutions that transformed service onboarding and accelerated digital execution for Oracle's top tier clients.
* Designed and implemented robust automation processes across complex multi-cloud environments, integrating AWS, Azure, GCP, and OCI architectures.
* Achieved a 35% increase in deployment efficiency and a 25% reduction in time-to-market through strategic automation roadmaps and streamlined operational processes.
* Collaborated closely with engineering and external partner teams to enhance product innovation, ensure robust governance, and align technical roadmaps with enterprise demands.

### Master Principal Cloud Architect
**Oracle | November 2020 - Present | San Francisco Bay Area**
* Architected and delivered large-scale enterprise cloud transformations, guiding major customers through complex migration roadmaps, cloud readiness assessments, and high-availability workload designs.
* Established standardized Infrastructure as Code (IaC) frameworks and automation patterns, driving consistency, security, and velocity across multi-tier cloud deployments.
* Partnered with executive stakeholders, product development, and technical delivery teams to align cloud architectures with long-term business goals, scalability requirements, and governance standards.

### Principal Sales Customer Engineer & Technical Staff
**Oracle | May 2013 - June 2015 | Santa Clara, CA**
* Partnered with senior executives to define strategic vision and technical goals for the Oracle Communication Digital Store (Oracle CDS), collaborating closely with internal engineering, QA, and support teams alongside external consulting partners.
* Led comprehensive RFI/RFP responses, technical prototypes, and high-impact proofs-of-concept (PoCs) to translate business strategy into scalable, production-ready architectures.
* Directed new customer deployments and migration initiatives to accommodate unexpected enterprise growth, ensuring zero-downtime transitions and robust platform scalability.

### Technical Account Manager & Field Engineer Lead
**Sun Microsystems | June 2003 - December 2010 | Santa Clara, CA**
* Managed global technical evaluations, pre-production deployments, and international project delivery for core enterprise Java platforms and distributed file content architectures.
* Guided major enterprise providers through complex deployment stages, geo-redundant configurations, and compliance documentation across the US, Europe, and Africa.

---

## EDUCATION & CERTIFICATIONS
* **Ph.D. Candidate (Innovative Technology / Mobile Agents & Heterogeneous Networks):** École de technologie supérieure
* **Master's Degree in Computer Science (Parallel Computing & Distributed Systems):** University of Yaoundé, Cameroon
* **Bachelor's Degree in Mathematics, Statistics, and Computer Science:** University of Yaoundé, Cameroon
* **Key Certifications:** HashiCorp Certified Terraform Associate, Oracle Cloud Infrastructure 2023 Certified Multicloud Architect Associate, Certified OCI Master Principal Architect / Cloud Automation Practice Specialist.

---

## APPENDIXES: OKE BEST PRACTICES AUTOMATION & LIVE-LABS AND MORE
1. [Build Once, Import Everywhere: Golden Image Distribution Across OCI Tenancies and Regions (Sept 17, 2026)](https://www.linkedin.com/in/mahamathisseinguiagoussou/) — LinkedIn Contribution
2. [Deploy and Use OKE Clusters with Simple and Advanced Terraform Modules and Best Practices, Oracle Live Lab (Sep 1, 2026)](https://www.oracle.com) — Oracle Learning Guide
3. [Deploy Oracle Cloud Infrastructure Kubernetes Engine (OKE) using Best Practices and Automation, Oracle Education (Feb 20, 2026)](https://www.oracle.com) — Oracle Education Guide
4. [Deploy Oracle Cloud Infrastructure Kubernetes Engine (OKE) using Advanced Terraform Modules, Oracle Publications (Oct 30, 2025)](https://www.oracle.com) — Oracle Architecture Center
5. [Create Oracle Cloud Infrastructure Kubernetes Engine Cluster using Terraform, Oracle Publications (Jul 11, 2025)](https://www.oracle.com) — Oracle Help Center
6. [Configure Private DNS Zones, Views, and Resolvers to Accelerate OCI Architect Professional Certification with Terraform, Oracle Publications (Nov 19, 2024)](https://www.oracle.com) — Oracle Help Center
7. [Accelerating Oracle Cloud Infrastructure Architect Professional Certification with Terraform Automation, Oracle Publications (Aug 30, 2024)](https://www.oracle.com) — Oracle Learn Live Lab
"""


def generate_local_documents(job_title, company_name, resume_text, cover_letter_text, references_text, output_dir):
    """Generates precise executive documents."""
    clean_company = company_name.replace(" ", "")
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    pdf_resume_path = output_path / f"Resume_{clean_company}.pdf"
    pdf_cover_path = output_path / f"CoverLetter_{clean_company}.pdf"
    pdf_refs_path = output_path / f"References_{clean_company}.pdf"

    build_pdf_document(pdf_resume_path, resume_text, is_resume=True)
    build_pdf_document(pdf_cover_path, cover_letter_text, is_resume=False)
    build_pdf_document(pdf_refs_path, references_text, is_resume=False)

    return str(pdf_resume_path), str(pdf_cover_path), str(pdf_refs_path)


def generate_executive_assets(role, company, jd, bio):
    """Bridge function mapping app.py calls directly to the comprehensive synthesis engine."""
    timestamp = "September 29, 2026 at 8:15 PM"
    resume_text = generate_comprehensive_resume(bio, role, company, timestamp)
    cover_letter_text = f"Dear {company} Hiring Team,\n\nApplying for {role}.\n\n{jd}"
    references_text = "# Professional References & Index\n\nAvailable upon request."
    
    r_path, c_path, ref_path = generate_local_documents(role, company, resume_text, cover_letter_text, references_text, "output_assets")
    
    return {
        "status": "success",
        "resume_path": r_path,
        "cover_letter_path": c_path,
        "references_path": ref_path
    }


def upload_to_oci_bucket(file_path, bucket_name="A_NewPathFinder_Agent"):
    file_name = os.path.basename(file_path)
    encoded_name = urllib.parse.quote(file_name)
    namespace = os.getenv("OCI_NAMESPACE", "your-oci-namespace")
    region = os.getenv("OCI_REGION", "us-ashburn-1")
    
    try:
        import oci
        config = oci.config.from_file()
        object_storage = oci.object_storage.ObjectStorageClient(config)
        with open(file_path, "rb") as f:
            object_storage.put_object(namespace, bucket_name, file_name, f)
        return f"https://objectstorage.{region}.oraclecloud.com/n/{namespace}/b/{bucket_name}/o/{encoded_name}"
    except Exception:
        return f"https://objectstorage.{region}.oraclecloud.com/n/{namespace}/b/{bucket_name}/o/{encoded_name}"


def generate_outreach_text(company_name, job_title, pdf_resume_url, pdf_cover_url, pdf_refs_url):
    email_text = f"""Subject: Executive Application & Architecture Alignment - {job_title} at {company_name}

Dear {company_name} Executive Talent Team,

I am writing to formally express my strong interest in the {job_title} position at {company_name}. With over 13 years of enterprise cloud architecture leadership at Oracle and nearly 8 years of core infrastructure engineering tenure at Sun Microsystems, I specialize in designing and deploying secure, high-performance distributed systems, multi-cloud architectures, and automated infrastructure frameworks.

To ensure you have full visibility into my qualifications, I have prepared a tailored executive dossier optimized for your requirements:
• Executive Resume: {pdf_resume_url}
• Strategic Cover Letter: {pdf_cover_url}
• Professional References & Complete Publications Index: {pdf_refs_url}

I look forward to discussing how my technical leadership can directly accelerate {company_name}'s strategic objectives.

Best regards,
Mahamat Hissein Guiagoussou
Master Principal Cloud Architect & Technical Sales Leader
mail2mahamat@gmail.com | +1 (408) 313-7157
"""

    whatsapp_text = f"""Hi! This is Mahamat Hissein Guiagoussou. Following up regarding the {job_title} role at {company_name}. I've prepared my complete executive application package here:
Resume: {pdf_resume_url}
Cover Letter: {pdf_cover_url}
References & Index: {pdf_refs_url}
Looking forward to connecting!"""

    return email_text, whatsapp_text