from collections import deque
from typing import Deque, Dict, List, Optional


class ContextManager:
    """
    Manages lightweight conversational memory and context tracking.
    """

    MAX_HISTORY = 5

    def __init__(self) -> None:
        self.history: Deque[Dict[str, str]] = deque(
            maxlen=self.MAX_HISTORY
        )

        self.current_context: Optional[str] = None

    def update_context(self, intent: str, user_input: str) -> None:
        """
        Store the latest interaction and update active context.
        """

        interaction = {
            "intent": intent.strip(),
            "input": user_input.strip()
        }

        self.history.append(interaction)
        self.current_context = intent

    def get_last_intent(self) -> Optional[str]:
        """
        Return the most recent detected intent.
        """
        return self.current_context

    def get_history(self) -> List[Dict[str, str]]:
        """
        Return conversation history as a list.
        """
        return list(self.history)

    def clear_context(self) -> None:
        """
        Reset all stored memory/context.
        """
        self.history.clear()
        self.current_context = None

    def get_last_interaction(self) -> Optional[Dict[str, str]]:
        """
        Return the latest interaction if available.
        """
        return self.history[-1] if self.history else None
