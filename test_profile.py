import json
import os
from pathlib import Path

# Define the master LinkedIn profile structure for Mahamat Hissein Guiagoussou
MHGLinkedInProfile = {
    "name": "Mahamat Hissein Guiagoussou",
    "title": "Master Principal Cloud Architect & Technical Sales Leader",
    "location": "San Francisco Bay Area",
    "email": "mail2mahamat@gmail.com",
    "phone": "+1 (408) 313-7157",
    "linkedin_url": "https://www.linkedin.com/in/mahamathisseinguiagoussou/",
    "summary": "Master Principal Cloud Architect and Technical Sales Leader combining over 13 years of executive tenure at Oracle with nearly 8 years of core infrastructure engineering at Sun Microsystems.",
    "core_competencies": [
        "Sales Engineering & Architecture",
        "Multi-Cloud & Systems Architecture (OCI, AWS, Azure, GCP)",
        "Infrastructure as Code (Terraform, OpenTofu, Ansible)",
        "Kubernetes (OKE) & Container Orchestration",
        "AIOps/MLOps Pipelines"
    ],
    "latest_recommendations": [
        {
            "author": "Enterprise Cloud Director / VP Engineering (Strategic Client Partner)",
            "text": "Mahamat consistently demonstrates master-level architecture authority across multi-cloud and OCI environments..."
        },
        {
            "author": "Principal Cloud Architect & Colleague (Oracle Engineering)",
            "text": "Working alongside Mahamat on OKE cluster automation and enterprise landing zones has been remarkable..."
        },
        {
            "author": "Global Field Engineering Director (Sun Microsystems & Oracle Leadership)",
            "text": "Mahamat is a powerhouse in technical pre-sales, complex PoCs, and mission-critical customer delivery..."
        }
    ]
}

def display_console_view():
    print("==================================================")
    print("       MHGLinkedInProfile CONSOLE INSPECTOR       ")
    print("==================================================")
    print(json.dumps(MHGLinkedInProfile, indent=4))
    print("==================================================\n")

if __name__ == "__main__":
    # 1. Print initial state
    print("--> Initial Console View:")
    display_console_view()
    
    # 2. Test a small change (e.g. updating title or adding a skill)
    print("--> Applying test change...")
    MHGLinkedInProfile["title"] = "Master Principal Cloud Architect & Enterprise AI Infrastructure Lead"
    MHGLinkedInProfile["core_competencies"].append("Enterprise AI Infrastructure & Accelerated Compute")
    
    # 3. Print updated state reflecting on screen/console
    print("--> Updated Console View:")
    display_console_view()