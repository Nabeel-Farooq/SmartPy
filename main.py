import re
from typing import Final

from dotenv import load_dotenv

from core.context_manager import ContextManager
from core.nlp_engine import extract_city, parse_intent

from modules.secure_logs import log_conversation
from modules.tasks import add_task, view_tasks
from modules.weather import get_weather

# Load environment variables
load_dotenv()

# Initialize chatbot memory
memory = ContextManager()

# Reusable responses
WELCOME_MESSAGE: Final[str] = (
    "Hello! I am your AI personal assistant."
)

UNKNOWN_COMMAND_MESSAGE: Final[str] = (
    "I'm not sure how to help with that yet.\n"
    "Try asking about:\n"
    "• Weather\n"
    "• Tasks\n"
    "• Reminders"
)

# Trigger phrases used for task cleanup
TASK_PATTERNS: Final[list[str]] = [
    r"add to list",
    r"remind me to",
    r"add task",
    r"todo",
    r"to-do",
]


def clean_task_input(user_input: str) -> str:
    """
    Extract clean task text from user input.
    """

    cleaned = user_input.strip()

    for pattern in TASK_PATTERNS:
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)

    return cleaned.strip(" .,!?")


def handle_weather(user_input: str) -> str:
    """
    Handle weather-related queries.
    """

    city = extract_city(user_input)

    if not city:
        return "Please tell me which city you want the weather for."

    return get_weather(city)


def handle_add_task(user_input: str) -> str:
    """
    Handle task creation requests.
    """

    task = clean_task_input(user_input)

    if not task:
        return "What would you like me to add to your list?"

    return add_task(task)


def handle_query(user_input: str) -> str:
    """
    Process user input and return chatbot response.
    """

    try:
        intent = parse_intent(user_input)

        # Store interaction context
        memory.update_context(intent, user_input)

        handlers = {
            "greeting": lambda: "Hello! How can I help you today?",
            "weather": lambda: handle_weather(user_input),
            "add_task": lambda: handle_add_task(user_input),
            "view_tasks": view_tasks,
            "exit": lambda: "Shutting down securely. Goodbye!",
        }

        handler = handlers.get(intent)

        if handler:
            return handler()

        return UNKNOWN_COMMAND_MESSAGE

    except Exception as error:
        return f"An unexpected error occurred: {error}"


def print_startup_banner() -> None:
    """
    Display startup information.
    """

    print("System: Initializing SmartPy Chatbot...")
    print("System: NLP Engine online.")
    print("System: Secure logging active.")
    print("-" * 50)
    print(f"SmartPy: {WELCOME_MESSAGE}")


def main() -> None:
    """
    Main chatbot runtime loop.
    """

    print_startup_banner()

    while True:

        try:
            user_input = input("\nYou: ").strip()

            # Ignore empty input
            if not user_input:
                continue

            response = handle_query(user_input)

            print(f"SmartPy: {response}")

            # Securely log interaction
            log_conversation(user_input, response)

            # Exit handling
            if parse_intent(user_input) == "exit":
                break

        except KeyboardInterrupt:
            print("\nSmartPy: Force quitting. Logs secured. Goodbye!")
            break

        except EOFError:
            print("\nSmartPy: Input stream closed. Exiting safely.")
            break

        except Exception as error:
            print(f"\n[CRITICAL ERROR] {error}")


if __name__ == "__main__":
    main()
