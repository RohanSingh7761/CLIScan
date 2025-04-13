# from auth import authenticate, logout
import questionary
from scanner import scan_directory
from groqScanner import pre_run_safety_check
import sys
from fixer import fix_file
from report import generate_and_send_report

def show_menu():
    choice = questionary.select(
        "What would you like to do?",
        choices=[
            "Vulnerability Scan",
            "Pre-run Safety Check"
            # "Logout"
        ]
    ).ask()

    if choice.startswith("Vulnerability Scan"):
        scan_directory()
    elif choice.startswith("Pre-run Safety Check"):
        pre_run_safety_check()
    else:
        print("\nInvalid option.")

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--fix":
            if len(sys.argv) < 3:
                print("❌ Please provide a filename to fix.")
            else:
                fix_file(sys.argv[2])
        elif sys.argv[1] == "--rep":
            generate_and_send_report()
        else:
            print("❌ Unknown command-line option.")
    else:
        show_menu()

if __name__ == "__main__":
    main()