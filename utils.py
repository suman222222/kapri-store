# utils.py
import os

def clear_screen():
    """Clears the terminal screen for a cleaner UI."""
  
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    """Prints a formatted header."""
    print("=" * 45)
    print(f"   {title.center(41)}")
    print("=" * 45)
