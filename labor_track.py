import sys
import os
import argparse
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Chrome_Session import chromeSession
from main import run

def is_valid_code(code):
    """Validate that the code consists of alphabetic characters."""
    if code.isalpha():
        return code
    else:
        raise argparse.ArgumentTypeError(f"Invalid code '{code}'. Code must consist of alphabetic characters only.")

def is_valid_badge(badge):
    """Validate that the badge consists of digits and has the expected length (e.g., 7 digits)."""
    if badge.isdigit():
        return badge
    else:
        raise argparse.ArgumentTypeError(f"Invalid badge '{badge}'. Badge must consist of exactly 7 digits.")

if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Run labor_track via the terminal.")
    # parser.add_argument('code', type=is_valid_code, help="Labor tracking code (must be alphabetic)")
    # parser.add_argument('badge', type=is_valid_badge, help="Badge ID (must be a number)")

    # args = parser.parse_args()

    session = chromeSession('hdc3', 12730876, 1922, True)

    # session.labor_track(args.code, args.badge)
    session.labor_track("ICQALQA", "12730876")

    session.close()
