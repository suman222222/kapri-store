# utils.py
import os
import json
import logging
from datetime import datetime

# Configure logging (Real projects track events)
logging.basicConfig(
    filename='kapri_store.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def clear_screen():
    """Clears the terminal screen for a cleaner UI."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    """Prints a formatted header."""
    print("=" * 45)
    print(f"   {title.center(41)}")
    print("=" * 45)

def load_json(filepath, default_data):
    """Safely loads data from a JSON file. Returns default if file is missing or corrupted."""
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logging.warning(f"{filepath} not found. Creating a new one.")
        return default_data
    except json.JSONDecodeError:
        logging.error(f"{filepath} is corrupted. Using default data.")
        return default_data

def save_json(filepath, data):
    """Safely saves data to a JSON file."""
    try:
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)
        logging.info(f"Successfully saved data to {filepath}")
    except Exception as e:
        logging.error(f"Failed to save data to {filepath}: {e}")
        print("Error: Could not save data. Check logs.")

def get_valid_number(prompt, is_float=True):
    """Helper function to validate numeric inputs (prices and quantities)."""
    while True:
        try:
            value = float(input(prompt)) if is_float else int(input(prompt))
            if value <= 0:
                print("Input must be greater than 0. Please try again.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")