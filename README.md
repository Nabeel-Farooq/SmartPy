# SmartPy Chatbot – AI Personal Assistant

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

SmartPy Chatbot is an intelligent, modular Python-based digital assistant. It leverages Natural Language Processing (NLP) to understand user intent, integrates with live APIs for real-time data retrieval, and implements AES encryption for secure communication logging.

## 🚀 Key Features

- **Intent Recognition:** Uses keyword and pattern matching to classify user requests (Greetings, Weather, Tasks, etc.).
- **Live Weather Integration:** Fetches real-time weather data via OpenWeatherMap API (defaults to Karachi if no city is specified).
- **Task Management:** A built-in persistent To-Do list manager to track and view daily goals.
- **Secure Logging:** Every interaction is encrypted using the `cryptography` library (Fernet/AES) before being saved to disk, ensuring user privacy.
- **Context Awareness:** Maintains a short-term memory buffer to handle conversational flow.

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **APIs:** OpenWeatherMap
- **Security:** Cryptography (Fernet)
- **Environment:** Python-dotenv (Sensitive key management)
- **Libraries:** Requests, JSON, OS
