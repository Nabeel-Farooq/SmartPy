class ContextManager:
    def __init__(self):
        self.history = []
        self.current_context = None

    def update_context(self, intent, user_input):
        self.history.append({"intent": intent, "input": user_input})
        self.current_context = intent
        
        # Keep memory lightweight (last 5 interactions)
        if len(self.history) > 5:
            self.history.pop(0)

    def get_last_intent(self):
        return self.current_context
