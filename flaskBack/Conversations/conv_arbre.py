from Conversations.abstract_conv import AbstractConv
import Conversations.convconfigs.conv_arbre_config as config
from Conversations.conv_annulation import ConvAnnulation

class ConvArbre(AbstractConv):

    status_ongoing = "arbre"
    status_finished = None
    previous_question = None
    tree = None

    def __init__(self, handler, classe : str):
        self.status_conv = 0
        self.set_from_config(classe)
        self.handler = handler
        self.status = self.status_ongoing
        self.current_conv = None

    def response(self, infos_in_message: dict, message : str):
        if not self.current_conv:
            response = self.no_conv_handler(infos_in_message, message)
        else :
            response =  self.annulation_handler(infos_in_message, message)
        return response

    def annulation_handler(self, infos_in_message : dict, message : str): #facile pas d'autre convs que annulation
        response = self.current_conv.response(infos_in_message, message)
        if self.current_conv.status:
            return response
        else :
            return self.no_conv_handler(infos_in_message, message)

    def no_conv_handler(self, infos_given : dict, message : str):
        response = ""
        if infos_given.get('intent')== 'annuler':
            self.current_conv = ConvAnnulation(self)
            return self.current_conv.response(infos_given, message)
        else :
            response = response + self.question_generator(message, infos_given)
            return response

    def question_generator(self, message : str, infos_in_message : dict):
        if infos_in_message.get('intent') == 'oui' or infos_in_message.get('intent') == 'non':
            self.previous_question = self.tree.get(self.previous_question).get(infos_in_message.get('intent'))
            response = self.previous_question
            if self.previous_question in config.ending_questions.values():
                response += '\n' + self.handler.question_generator()
                self.status= self.status_finished
            return response
        else :
            return self.previous_question


    def set_from_config(self, classe):
        if classe in config.possible_classes.keys():
            self.tree = config.possible_classes[classe]
            self.previous_question = config.starting_question[classe]
