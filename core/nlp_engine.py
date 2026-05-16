from typing import Optional
import re

# Intent keyword mapping
INTENT_KEYWORDS = {
    "weather": {
        "weather",
        "temperature",
        "forecast",
        "hot",
        "cold",
        "rain",
        "sunny",
        "climate"
    },
    "add_task": {
        "remind",
        "task",
        "todo",
        "to-do",
        "add to list",
        "remember this"
    },
    "view_tasks": {
        "show tasks",
        "list tasks",
        "my list",
        "view tasks",
        "tasks"
    },
    "greeting": {
        "hello",
        "hi",
        "hey",
        "greetings"
    },
    "exit": {
        "exit",
        "quit",
        "bye",
        "goodbye",
        "stop"
    }
}


def parse_intent(user_input: str) -> str:
    """
    Classify user input into a supported intent.
    """

    if not user_input or not user_input.strip():
        return "unknown"

    text = user_input.lower().strip()

    for intent, keywords in INTENT_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return intent

    return "unknown"


def extract_city(user_input: str) -> Optional[str]:
    """
    Extract a city name from phrases like:
    - weather in Karachi
    - forecast in New York
    - temperature in London
    """

    if not user_input:
        return None

    # Regex looks for text after "in"
    match = re.search(r"\bin\s+([a-zA-Z\s]+)", user_input, re.IGNORECASE)

    if not match:
        return None

    city = match.group(1).strip()

    # Remove trailing punctuation
    city = re.sub(r"[^\w\s]", "", city)

    return city.title() if city else None
