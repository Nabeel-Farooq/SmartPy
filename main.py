import re
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


def clean_task_input(user_input: str) -> str:
    """
    Remove trigger phrases to extract the actual task text.
    """

    patterns = [
        r"add to list",
        r"remind me to",
        r"add task",
        r"todo",
        r"to-do"
    ]

    cleaned = user_input.lower()

    for pattern in patterns:
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)

    return cleaned.strip()


def handle_query(user_input: str) -> str:
    """
    Process user input and return chatbot response.
    """

    intent = parse_intent(user_input)

    # Store interaction context
    memory.update_context(intent, user_input)

    try:
        match intent:

            case "greeting":
                return "Hello! How can I help you today?"

            case "weather":
                city = extract_city(user_input)
                return get_weather(city)

            case "add_task":
                task = clean_task_input(user_input)

                if not task:
                    return "What would you like me to add to your list?"

                return add_task(task)

            case "view_tasks":
                return view_tasks()

            case "exit":
                return "Shutting down securely. Goodbye!"

            case _:
                return (
                    "I'm not sure how to help with that yet.\n"
                    "Try asking about:\n"
                    "• Weather\n"
                    "• Tasks\n"
                    "• Reminders"
                )

    except Exception as error:
        return f"An unexpected error occurred: {error}"


def main() -> None:
    """
    Main chatbot runtime loop.
    """

    print("System: Initializing SmartPy Chatbot...")
    print("System: NLP Engine online.")
    print("System: Secure logging active.")
    print("-" * 50)

    print("SmartPy: Hello! I am your AI personal assistant.")

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
