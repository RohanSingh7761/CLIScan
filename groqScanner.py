import os
from groq import Groq
import json
from dotenv import load_dotenv

# Extensions to check
ALLOWED_EXTENSIONS = [".py", ".js", ".ts", ".sh", ".java", ".rb"]
EXCLUDED_DIRS = ["venv", ".git", "__pycache__", "node_modules"]
EXCLUDED_FILES = ["auth.py", "scanner.py", ".env", "groqScanner.py", "main.py", "fixer.py", "report.py"]

# Initialize Groq client
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# LLM prompt message
SYSTEM_MESSAGE = {
    "role": "system",
    "content": "You are a code security checker with intent checking as well, you will be provided with a code, you have to check it full and find out its intent, whether it has some hidden malicious function or line of code hidden somewhere in it. Give output in json that should always only have \"explanation\", \"malicious_block\" (bool), if malicious block found then \"changes_to_make\" with however many points needed but dont include the point numbers but if possible try to include line number, and if not found then a null"
}


def is_valid_file(filename):
    return any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS) and filename not in EXCLUDED_FILES


def analyze_file_with_groq(filepath):
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
            code = file.read()

        response = client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            messages=[SYSTEM_MESSAGE, {"role": "user", "content": code}],
            temperature=0.6,
            max_completion_tokens=4096,
            top_p=0.95,
            stream=False,
            response_format={"type": "json_object"},
        )

        result = response.choices[0].message.content
        return filepath, result

    except Exception as e:
        return filepath, json.dumps({
            "explanation": f"Error analyzing file: {str(e)}",
            "malicious_block": False,
            "changes_to_make": None
        })


def pre_run_safety_check(directory="."):
    print("🔍 Starting Pre-run Safety Check...\n")

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        for filename in files:
            if is_valid_file(filename):
                full_path = os.path.join(root, filename)
                filepath, raw_output = analyze_file_with_groq(full_path)

                try:
                    result = json.loads(raw_output)
                    if result["malicious_block"]:
                        print(f"❌ {filepath}: Malicious code found")
                        print(f"   Explanation: {result['explanation']}")
                        for i, change in enumerate(result["changes_to_make"], 1):
                            print(f"   {i}. {change}")
                        print()
                    else:
                        print(f"✅ {filepath}: Safe to run\n")
                except Exception as e:
                    print(f"⚠️  {filepath}: Failed to parse response\n{raw_output}\n")


if __name__ == "__main__":
    pre_run_safety_check()
