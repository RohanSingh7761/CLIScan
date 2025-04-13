import os
import re
import time

# Define patterns to search for vulnerabilities
PATTERNS = {
    "Hardcoded API Key / Secret": re.compile(r"(key|secret|token|password|apikey|access_token)\s*=\s*['\"]?[A-Za-z0-9_\-]{8,}['\"]?", re.IGNORECASE),
    "TODO Comment": re.compile(r"#\s*TODO|//\s*TODO|/\* TODO", re.IGNORECASE),
    "Dangerous Functions (eval, exec, system)": re.compile(r"\b(eval|exec|os\.system|subprocess\.call|os\.popen|open\(|subprocess\.Popen|subprocess\.run|os\.fork)\b", re.IGNORECASE),
    "Sensitive Data (e.g., credit card numbers)": re.compile(r"\b(?:\d{4}[- ]?){3}\d{4}|\b(?:\d{3}-\d{2}-\d{4}|\d{9})\b", re.IGNORECASE),
    "File Inclusion Vulnerabilities": re.compile(r"open\(\s*['\"]?.*['\"]?\s*\)", re.IGNORECASE),
    "Unvalidated User Input (SQL Injection)": re.compile(r"(\b(?:SELECT|INSERT|UPDATE|DELETE|DROP)\b.*?['\";])", re.IGNORECASE),
    "Unencrypted Sensitive Data": re.compile(r"(encrypt|decrypt|cleartext|plaintext)", re.IGNORECASE)
}

ALLOWED_EXTENSIONS = [".py", ".js", ".ts", ".env", ".json", ".txt", ".sh", ".html", ".css", ".rb", ".java"]
EXCLUDED_DIRS = ["venv", ".git", "__pycache__", ".tox", "node_modules"]
EXCLUDED_FILES = ["auth.py", "scanner.py", ".env", "groqScanner.py", "safeFileEg.py", "fixer.py", "report.py"]

def scan_directory(directory="."):
    print("\n🔍 Scanning for vulnerabilities...\n")
    time.sleep(1)

    found_any = False

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]

        for file in files:
            if file in EXCLUDED_FILES:
                continue
            if any(file.endswith(ext) for ext in ALLOWED_EXTENSIONS):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()
                        for i, line in enumerate(lines, 1):
                            for label, pattern in PATTERNS.items():
                                if pattern.search(line):
                                    found_any = True
                                    print(f"{label} → {filepath}:{i}")
                                    print(f"    {line.strip()}\n")
                                    time.sleep(0.5) 
                except Exception as e:
                    print(f"⚠️ Could not read {filepath}: {e}")

    if not found_any:
        print("✅ No major vulnerabilities found.\n")
