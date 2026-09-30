#!/bin/bash

TARGET_DIR="$HOME/mguiagous/smart_mobile_pathfinder_agent"
cd "$TARGET_DIR" || { echo "[-] Target directory not found! Run step1_init.sh first."; exit 1; }

echo "--------------------------------------------------"
echo "[*] Step 2: Setting up virtual environment & tools..."
echo "--------------------------------------------------"

# 1. Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "[*] Creating isolated Python virtual environment (.venv)..."
    python3 -m venv .venv
fi

# 2. Activate virtual environment for this script execution
source .venv/bin/activate

# 3. Populate requirements.txt
cat << 'EOF' > requirements.txt
playwright==1.42.0
google-generativeai==0.8.3
markdown==3.5.2
python-docx==1.1.0
requests==2.31.0
python-dotenv==1.0.1
EOF
echo "[+] Created: requirements.txt"

# 4. Populate master_profile.md
cat << 'EOF' > master_profile.md
# Master Profile: Mahamat Hissein Guiagoussou
- **Role:** Principal Resident Architect & Cloud Engineer at Oracle
- **Experience:** 20+ years in computer science systems architecture and software design.
- **Core Technical Stack:** Oracle Cloud Infrastructure (OCI), Oracle Kubernetes Engine (OKE), Terraform, OpenTofu, Ansible, Bash, Python, macOS developer environment.
- **Key Expertise Areas:** Enterprise cloud migration frameworks, Infrastructure as Code automation, multi-cloud networking topologies, high-performance distributed systems.
EOF
echo "[+] Created: master_profile.md"

# 5. Create code module placeholders
touch agent.py notifier.py scout_agent.py
echo "[+] Created placeholders: agent.py, notifier.py, scout_agent.py"

# 6. Install dependencies inside the virtual environment cleanly
echo "[*] Upgrading pip inside virtual environment..."
pip install --upgrade pip

echo "[*] Installing requirements from requirements.txt..."
pip install -r requirements.txt

echo "[*] Installing Playwright Chromium browser binary..."
playwright install chromium

echo "--------------------------------------------------"
echo "[+] Setup complete! Virtual environment is ready."
echo "[!] IMPORTANT: To work in this environment later, run:"
echo "    source .venv/bin/activate"
echo "--------------------------------------------------"
