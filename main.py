import os
import requests

# Fetch the API key from system environment variables
API_KEY = os.getenv('ABUSEIPDB_API_KEY')
# Path to save the MikroTik script file
OUTPUT_PATH = "blacklist.rsc"

def fetch_abuse_ips():
    if not API_KEY:
        print("[-] Error: ABUSEIPDB_API_KEY environment variable is not set!")
        return

    # AbuseIPDB API Endpoint for fetching blacklist
    url = 'https://api.abuseipdb.com/api/v2/blacklist'
    headers = {
        'Accept': 'application/json',
        'Key': API_KEY
    }
    params = {
        'confidenceMinimum': '100', # Top malicious IPs
        'limit': '5000'            # Fetch top 5,000 threats
    }

    print("[*] Contacting AbuseIPDB API...")
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        response.raise_for_status()
        data = response.json().get('data', [])
        
        # Writing the MikroTik RouterOS script
        with open(OUTPUT_PATH, "w") as f:
            # Clear previous lists to avoid duplicates and conflicts
            f.write("/ip firewall address-list remove [find list=Internet_Blacklist]\n\n")
            f.write("/ip firewall address-list\n")
            
            counter = 0
            for item in data:
                ip = item.get('ipAddress')
                # Filter for IPv4 addresses only
                if ip and ":" not in ip:
                    # Enforce a dynamic 24-hour timeout for automatic cleanup
                    f.write(f"add list=Internet_Blacklist address={ip} timeout=24:00:00\n")
                    counter += 1
                    
        print(f"[+] Success! Generated {OUTPUT_PATH} with {counter} active malicious IPs.")

    except Exception as e:
        print(f"[-] API Fetch failed: {e}")

if __name__ == "__main__":
    fetch_abuse_ips()