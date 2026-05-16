from pathlib import Path
from cryptography.fernet import Fernet
from dotenv import load_dotenv, set_key
import os

# Load environment variables once
load_dotenv()

LOG_FILE = Path("chat_logs.enc")
ENV_FILE = Path(".env")


def get_or_create_key() -> bytes:
    """
    Returns the encryption key from environment variables.
    Generates and stores one if it doesn't exist.
    """
    key = os.getenv("ENCRYPTION_KEY")

    if key:
        return key.encode()

    # Generate new key
    new_key = Fernet.generate_key()

    # Save to .env
    set_key(str(ENV_FILE), "ENCRYPTION_KEY", new_key.decode())

    return new_key


# Create cipher once (better performance)
cipher = Fernet(get_or_create_key())


def log_conversation(user_text: str, bot_text: str) -> None:
    """
    Encrypts and appends a chat interaction to the log file.
    """
    try:
        log_entry = (
            f"User: {user_text.strip()} | "
            f"Bot: {bot_text.strip()}\n"
        ).encode("utf-8")

        encrypted_entry = cipher.encrypt(log_entry)

        with LOG_FILE.open("ab") as file:
            file.write(encrypted_entry + b"\n")

    except Exception as error:
        print(f"[LOG ERROR] Failed to write encrypted log: {error}")
