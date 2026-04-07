import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv, set_key

LOG_FILE = "chat_logs.enc"
ENV_FILE = ".env"

def _get_or_create_key():
    """Fetches the encryption key or generates one if it doesn't exist."""
    key = os.getenv("ENCRYPTION_KEY")
    if not key:
        key = Fernet.generate_key().decode()
        set_key(ENV_FILE, "ENCRYPTION_KEY", key)
        load_dotenv() # Reload environment variables
    return key.encode()

def log_conversation(user_text, bot_text):
    """Encrypts and appends the interaction to the log file."""
    key = _get_or_create_key()
    cipher_suite = Fernet(key)
    
    log_entry = f"User: {user_text} | Bot: {bot_text}\n".encode('utf-8')
    encrypted_entry = cipher_suite.encrypt(log_entry)
    
    with open(LOG_FILE, "ab") as file:
        file.write(encrypted_entry + b"\n")
