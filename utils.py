# utils.py
import json
import os

USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_user(username, password):
    users = load_users()
    username_lower = username.lower()
    
    # Case-insensitive uniqueness check
    for existing_user in users:
        if existing_user.lower() == username_lower:
            return False  # Username already exists
    
    users[username] = password
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)
    return True
