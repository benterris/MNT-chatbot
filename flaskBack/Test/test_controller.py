from unittest import TestCase
from controller import Controller


class TestController(TestCase):

    def test_handle_message(self):
        c = Controller
        self.assertIs(type(c.handle_message(c, "Bonjour", "UTILISATEUR")), type('str'))


    def test_create_conversation(self):
        c = Controller
        c.create_conversation(c, 'utilisateur1')
        self.assertIsNot({}, {'utilisateur1': c.get_conversation(c, 'utilisateur1')})


    def test_destroy_conversation(self):
        c = Controller
        c.create_conversation(c, 'utilisateur1')
        c.destroy_conversation(c, 'utilisateur1')
        self.assertEqual(c.conversations, {})
