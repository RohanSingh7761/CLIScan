import os
import requests

API_KEY = "sk_test_1234567890abcdef"

def download_file(url):
    response = requests.get(url, headers={"Authorization": f"Bearer {API_KEY}"})
    if response.status_code == 200:
        with open("output.txt", "w") as f:
            f.write(response.text)
    else:
        print("Failed to download")

def run_user_command():
    cmd = input("Enter a system command to run: ")
    os.system(cmd)

def evaluate_expression():
    expr = input("Enter a Python expression: ")
    result = eval(expr)
    print(f"Result: {result}")

if __name__ == "__main__":
    print("1. Download File")
    print("2. Run System Command")
    print("3. Evaluate Expression")

    choice = input("Choose an option: ")

    if choice == "1":
        download_file("https://example.com/data")
    elif choice == "2":
        run_user_command()
    elif choice == "3":
        evaluate_expression()
    else:
        print("Invalid option")
