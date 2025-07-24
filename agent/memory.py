class Memory:
    def __init__(self):
        self.history = []

    def add_user_message(self, content: str):
        self.history.append({"role": "user", "content": content})

    def add_assistant_message(self, content: str):
        self.history.append({"role": "assistant", "content": content})

    def get_context(self, number):
        return self.history[-number:]
