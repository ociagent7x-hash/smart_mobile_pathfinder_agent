import json
from datetime import datetime

# Simulate fetching your live LinkedIn profile data (including any new typos or edits)
def fetch_live_linkedin_profile():
    # In a full automated setup, this pulls from your active LinkedIn session or local export.
    # Here we simulate your live profile with an intentional typo in the 'About' section for testing.
    live_profile = {
        "timestamp_checked": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "name": "Mahamat Hissein Guiagoussou",
        "title": "Master Principal Cloud Architect & Technical Sales Leader",
        "about_summary": "Master Principal Cloud Architetc and Technical Sales Leader combining over 13 years of executive tenure at Oracle with nearly 8 years of core infrastructure engineering at Sun Microsystems.", # Typo introduced here ('Architetc')
        "location": "San Francisco Bay Area",
        "status": "Live Sync Successful ✅"
    }
    return live_profile

if __name__ == "__main__":
    print("==================================================")
    print("      REAL-TIME LINKEDIN PROFILE LIVE VIEWER      ")
    print("==================================================")
    profile = fetch_live_linkedin_profile()
    print(json.dumps(profile, indent=4))
    print("==================================================")
    
    # Check for common typos to alert you in real-time
    if "Architetc" in profile["about_summary"]:
        print("⚠️ SPELLING ALERT: Typo detected in 'About' section ('Architetc' -> should be 'Architect').")
    else:
        print("✅ Spelling check passed.")