import os
from pathlib import Path
from datetime import datetime
from profile_data import MHGLinkedInProfile

BASE_DIR = Path(os.path.expanduser("~")) / "mguiagous" / "smart_mobile_pathfinder_agent"
INPUT_DIR = BASE_DIR / "input"

def get_semi_automated_profile():
    """
    Pulls profile data using our anti-blocking workaround:
    Reads from local staging file ('live_linkedin_about.txt') if present.
    """
    live_about_path = INPUT_DIR / "live_linkedin_about.txt"
    profile = MHGLinkedInProfile.copy()
    
    if os.path.exists(live_about_path):
        try:
            with open(live_about_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    profile["summary"] = content
                    profile["sync_source"] = "Local Snapshot File (Anti-Block Workaround)"
                    profile["sync_timestamp"] = datetime.fromtimestamp(os.path.getmtime(live_about_path)).strftime("%Y-%m-%d %H:%M:%S")
                    return profile
        except Exception:
            pass
            
    profile["sync_source"] = "Default Master Profile"
    profile["sync_timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return profile