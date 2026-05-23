import os
from pathlib import Path
from typing import Final

from cryptography.fernet import Fernet, InvalidToken
from dotenv import load_dotenv, set_key

# Load environment variables
load_dotenv()

# File paths
LOG_FILE: Final[Path] = Path("chat_logs.enc")
ENV_FILE: Final[Path] = Path(".env")

# Environment variable name
ENCRYPTION_ENV_KEY: Final[str] = "ENCRYPTION_KEY"


def get_or_create_key() -> bytes:
    """
    Retrieve encryption key from environment variables.
    Generate and store a new one if missing.
    """

    key = os.getenv(ENCRYPTION_ENV_KEY)

    if key:
        return key.encode("utf-8")

    # Generate secure encryption key
    new_key = Fernet.generate_key()

    # Save generated key to .env file
    set_key(
        dotenv_path=str(ENV_FILE),
        key_to_set=ENCRYPTION_ENV_KEY,
        value_to_set=new_key.decode("utf-8"),
    )

    return new_key


# Initialize cipher once
cipher = Fernet(get_or_create_key())


def build_log_entry(user_text: str, bot_text: str) -> bytes:
    """
    Create a formatted log entry.
    """

    log_entry = (
        f"User: {user_text.strip()}\n"
        f"Bot: {bot_text.strip()}\n"
        f"{'-' * 50}\n"
    )

    return log_entry.encode("utf-8")


def encrypt_entry(entry: bytes) -> bytes:
    """
    Encrypt log entry bytes.
    """

    return cipher.encrypt(entry)


def decrypt_entry(entry: bytes) -> str:
    """
    Decrypt a single encrypted log entry.
    """

    decrypted = cipher.decrypt(entry)

    return decrypted.decode("utf-8")


def log_conversation(user_text: str, bot_text: str) -> None:
    """
    Encrypt and append a chat interaction
    to the encrypted log file.
    """

    try:
        log_entry = build_log_entry(user_text, bot_text)

        encrypted_entry = encrypt_entry(log_entry)

        with LOG_FILE.open("ab") as file:
            file.write(encrypted_entry + b"\n")

    except Exception as error:
        print(f"[LOG ERROR] Failed to write encrypted log: {error}")


def read_logs() -> str:
    """
    Read and decrypt all chat logs.
    """

    if not LOG_FILE.exists():
        return "No encrypted logs found."

    decrypted_logs: list[str] = []

    try:
        with LOG_FILE.open("rb") as file:

            for line in file.readlines():

                encrypted_line = line.strip()

                if not encrypted_line:
                    continue

                try:
                    decrypted_logs.append(
                        decrypt_entry(encrypted_line)
                    )

                except InvalidToken:
                    decrypted_logs.append(
                        "[WARNING] Corrupted or invalid log entry.\n"
                    )

        return "".join(decrypted_logs).strip()

    except Exception as error:
        return f"Failed to read encrypted logs: {error}"


def clear_logs() -> str:
    """
    Delete encrypted log file.
    """

    try:
        if LOG_FILE.exists():
            LOG_FILE.unlink()
            return "Encrypted logs cleared successfully."

        return "No log file found."

    except Exception as error:
        return f"Failed to clear logs: {error}"
