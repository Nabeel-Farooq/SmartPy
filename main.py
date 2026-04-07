import os
from dotenv import load_dotenv

from core.nlp_engine import parse_intent, extract_city
from core.context_manager import ContextManager
from modules.weather import get_weather
from modules.tasks import add_task, view_tasks
from modules.secure_logs import log_conversation

# Initialize state
load_dotenv()
memory = ContextManager()

def handle_query(user_input):
    intent = parse_intent(user_input)
    memory.update_context(intent, user_input)
    
    if intent == "greeting":
        return "Hello! How can I help you today?"
        
    elif intent == "weather":
        city = extract_city(user_input)
        return get_weather(city)
        
    elif intent == "add_task":
        # Strip trigger words to get the actual task
        task = user_input.lower().replace("add to list", "").replace("remind me to", "").strip()
        if not task:
            return "What would you like me to add to your list?"
        return add_task(task)
        
    elif intent == "view_tasks":
        return view_tasks()
        
    elif intent == "exit":
        return "Shutting down securely. Goodbye!"
        
    else:
        return "I'm not quite sure how to help with that yet. Try asking about the weather or adding a task."

def main():
    print("System: Initializing SmartPy Chatbot...")
    print("System: NLP Engine online. Secure logging active.")
    print("-" * 50)
    print("SmartPy: Hello! I am your AI personal assistant.")
    
    while True:
        try:
            user_input = input("\nYou: ")
            
            if not user_input.strip():
                continue
                
            response = handle_query(user_input)
            print(f"SmartPy: {response}")
            
            # Log the data securely
            log_conversation(user_input, response)
            
            if parse_intent(user_input) == "exit":
                break
                
        except KeyboardInterrupt:
            print("\nSmartPy: Force quitting. Logs secured. Goodbye!")
            break

if __name__ == "__main__":
    main()