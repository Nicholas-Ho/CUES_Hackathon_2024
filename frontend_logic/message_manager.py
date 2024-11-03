class MessageManager:
    def __init__(self, default_msg):
        self.default_msg = default_msg
        self.messages = []

    def add_message(self, msg):
        self.messages.append(msg)
    
    def pop_messages(self):
        """
        Flushes out all messages and returns them, including the default message
        """
        messages = self.messages
        self.messages = []
        return messages + [("\n" if len(messages) > 0 else "") + self.default_msg]