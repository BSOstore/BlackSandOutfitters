import json
import os

DATA_FILE = os.path.join('data', 'sites.json')

def load_sites():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_sites(sites):
    with open(DATA_FILE, 'w') as f:
        json.dump(sites, f, indent=2)
