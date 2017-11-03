"""
    classe permettant la création de conversation unique pour une session donnée.
"""
from conv_handler import ConvHandler


class Controller:
    conversations = {}

    def get_conversation(self, user):
        if self.conversations.get(user):
            return self.conversations.get(user)
        else:
            self.create_conversation(user)
        return self.conversations.get(user)

    def create_conversation(self, user):
        self.conversations[user] = ConvHandler(user)

    def destroy_conversation(self, user):
        self.conversations.pop(user)

    def handle_message(self, message, user):
        conversation = self.get_conversation(user)
        response = conversation.response(message)
        return response
