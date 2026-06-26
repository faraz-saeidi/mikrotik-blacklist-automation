# Dynamic Network Blacklist Automation (AbuseIPDB + Python + MikroTik)

This project automates network edge protection by querying malicious IP addresses from the **AbuseIPDB API**, converting them into a MikroTik compatible RouterOS script, and dynamically loading them into a firewall address list with an automatic 24-hour expiration (Timeout).

## 🚀 Key Features
- **Automated Scheduling:** Ubuntu/Windows updates the blacklist centrally; MikroTik fetches it periodically.
- **Dynamic Firewall Management:** Every injected IP enforces a `24:00:00` timeout to preserve router RAM and CPU.
- **Native Execution:** Pure Python implementation utilizing standard environment variables for security.

## 🛠️ Repository Structure
```text
.
├── main.py             # Main script to fetch threats and compile .rsc file
├── requirements.txt    # Required python external libraries
├── .gitignore          # Instructs Git which local files to ignore
└── README.md           # Project documentation and deployment guide


⚙️ Installation & Deployment
Step 1: Initialize Environment

Navigate to the directory and set up your Python virtual environment:
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux:
source venv/bin/activate

Step 2: Install Dependencies
pip install -r requirements.txt

Step 3: Run the Script
Provide your AbuseIPDB API token inside your environment variables before execution:
# Windows (CMD):
set ABUSEIPDB_API_KEY="YOUR_ACTUAL_API_KEY"
python main.py

# Linux/Bash:
export ABUSEIPDB_API_KEY="YOUR_ACTUAL_API_KEY"
python main.py


Step 4: MikroTik RouterOS Script Integration
Paste the following block into your MikroTik WinBox Terminal to set up the automated fetch schedule (replace YOUR_SERVER_IP with your host IP):

/system script
add name=update_blacklist source="/tool fetch url=\"http://YOUR_SERVER_IP/blacklist.rsc\" mode=http;\r\n/import file-name=blacklist.rsc"

/system scheduler
add name=schedule_blacklist_update interval=8h start-time=02:00:00 on-event=update_blacklist
