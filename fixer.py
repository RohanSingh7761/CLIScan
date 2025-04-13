import sys
import os
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_MESSAGE = {
    "role": "system",
    "content": "You are a security-focused code fixer. Given code, analyze and fix security vulnerabilities or malicious blocks like threats to pc or hiddent blocks etc. Return only valid, working code in your reply, nothing else, no remarks no convo message no extra quotes. Also in the code itself include comments what the user now needs to do whatever required, like if you changed a harcoded api key to os.environ then add a comment in front of it telling user to put the var in .env. Also instead of removing dangerous calls like OS call, fix them with a better method if possible, if not then you can comment them out fully including function definition and calls and write why you commented it."
}

def sanitize_llm_output(raw_response: str) -> str:
    """
    Cleans the LLM response by:
    - Removing <think>...</think> blocks
    - Stripping triple backticks and optional language tags
    """
    # Remove <think>...</think> content (non-greedy match)
    raw_response = re.sub(r"<think>.*?</think>\s*", "", raw_response, flags=re.DOTALL)

    # Extract code inside triple backticks (``` or ```python etc.)
    code_match = re.search(r"```(?:\w+\n)?(.*?)```", raw_response, re.DOTALL)

    if code_match:
        return code_match.group(1).strip()
    else:
        return raw_response.strip()

def fix_file(filepath):
    if not os.path.isfile(filepath):
        print(f"❌ File not found: {filepath}")
        return

    with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
        code = file.read()

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[SYSTEM_MESSAGE, {"role": "user", "content": code}],
            temperature=0.4,
            max_completion_tokens=4096,
            top_p=0.9,
            stream=False
        )

        fixed_code_raw = response.choices[0].message.content
        fixed_code = sanitize_llm_output(fixed_code_raw)

        # Overwrite the file with fixed code
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(fixed_code)

        print(f"✅ Fixed and updated: {filepath}")
    except Exception as e:
        print(f"⚠️  Error fixing file: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] != "--fix":
        print("Usage: python fixer.py --fix <filename>")
    else:
        filename = sys.argv[2]
        fix_file(filename)
