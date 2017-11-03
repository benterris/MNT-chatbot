from Conversations.conv_training import ConvTraining
from Conversations.conv_voyage import ConvVoyage
from Conversations.conv_name_info import ConvNameInfo
from Conversations.conv_small_talk import ConvSmallTalk
from Conversations.conv_arbre import ConvArbre
import http_helper
from Conversations.abstract_conv import AbstractConv

class ConvHandler(AbstractConv):
    """
    Classe définissant la reponse caractérisée par :
        - L'intent du message
        - Le statut de la conversation (ie pour le moment est-on en entrainement ?) int?
        - L'interlocuteur.
        état de la conversation : caractérisé par :
            la conversation en cours : current_conv : voyage, training, hotel, personal_infos
            l'état de la conversation choisie :current_conv_state :ongoing, ended

    """


    start_conv = "initialisation"
    status_ongoing = 'handler'
    status_finished = None

    def __init__(self, user):
        self.user = None
        self.status = self.status_ongoing
        self.current_conv = ConvNameInfo(self, 'bonjour')
        self.info_asked = None
        self.user = None


    def response(self, message: str, dict={}):
        infos_in_message = http_helper.http_parse(message, 'classify')
        if infos_in_message:
            if self.current_conv.status:
                response = self.current_conv.response(infos_in_message, message)
            else :
                response = self.no_conv_handler(infos_in_message, message)
            # print(self.current_conv.status)
            return response
        else :
            return 'Le service est indisponible actuellement, veuillez contacter le SVP au 09.69.36.87.81'

    def question_generator(self):
        return 'Que puis-je faire pour vous ?'

    def no_conv_handler(self, infos_in_message : dict, message : str): #initialisation sur intent
        small_talk_classes = ['pas_compris', 'bonjour', 'etat', 'blague', 'fort', 'capacites', 'mauvais',
        'merci', 'aurevoir', 'oror', 'meteo']
        tree_classes = ['vpn']
        classe = infos_in_message.get('intent')
        if classe in small_talk_classes: classe = 'small_talk'
        if classe in tree_classes: classe = 'arbre'
        convs = {
            'arbre' : ConvArbre,
            'train' : ConvVoyage,
            'hotel' : ConvVoyage,
            'personnal_infos' : ConvNameInfo,
            'small_talk' : ConvSmallTalk,
            'entrainement' : ConvTraining,
        }
        if classe in convs.keys():
            self.current_conv = convs.get(classe)(self, infos_in_message.get('intent'))
            response = self.current_conv.response(infos_in_message, message)
        else:
            response = "Je n'ai pas compris ce que vous vouliez dire... Je suis désolé, je ne suis qu'un simple robot. En cas de problème, vous pouvez contacter le SVP au 09.69.36.87.81"
        return response
