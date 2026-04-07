def parse_intent(user_input):
    """Classifies the user's text into an actionable intent."""
    text = user_input.lower()
    
    if any(word in text for word in ["weather", "temperature", "forecast", "hot", "cold"]):
        return "weather"
    elif any(word in text for word in ["remind", "task", "todo", "to-do", "add to list"]):
        return "add_task"
    elif any(word in text for word in ["show tasks", "list tasks", "my list"]):
        return "view_tasks"
    elif any(word in text for word in ["hello", "hi", "hey", "greetings"]):
        return "greeting"
    elif any(word in text for word in ["exit", "quit", "bye", "goodbye"]):
        return "exit"
    else:
        return "unknown"

def extract_city(user_input):
    """A simple extractor to find the city name after the word 'in'."""
    words = user_input.lower().split()
    if "in" in words:
        try:
            city_index = words.index("in") + 1
            return " ".join(words[city_index:]).title()
        except IndexError:
            return None
    return None