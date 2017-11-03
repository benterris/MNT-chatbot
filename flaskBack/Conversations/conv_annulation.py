from Conversations.abstract_conv import AbstractConv

class ConvAnnulation(AbstractConv):
    '''
        Classe pour gérer les cas d'annulation.
    '''

    status_finished = None
    status_ongoing = 'annulation'

    def __init__(self, conv_to_cancel):
        """

        :param conv_to_cancel: la conversation à annuler
        """
        self.conv_to_cancel = conv_to_cancel
        self.state = None
        self.status = self.status_ongoing


    def response(self, infos_in_message : dict, message : str):
        if self.state == 'confirmation':
            return self.confirmation(message, infos_in_message)
        return self.cancel_message_conv(self.conv_to_cancel.status)


    def cancel_message_conv(self, status : str):
        """
            Si l'utilisateur a manifesté l'intention d'annuler une réservation, on le fait confirmer
            pour s'assurer que c'est bien l'action qu'il voulait effectuer.
        """

        self.state = 'confirmation'
        convs = {
            'train' : 'Voulez-vous annuler la réservation de ce train ? oui/non',
            'voyage' : 'Voulez-vous annuler la réservation de votre voyage ? oui/non',
            'hotel' : 'Voulez- vous annuler la réservation de votre hôtel ? oui/non',
            'vpn' : "Voulez annuler la demande d'aide à la Connexion à distance ? oui/non"
        }
        if status in convs.keys():
            self.state = 'confirmation'
            return convs.get(status)

    def confirmation(self, message : str, infos_in_message : dict):
        """
            Si l'utilisateur a bien confirmé son désir d'annuler une action, elle est annulée et on l'informe.
            on change le message en 'bololololo' pour signifer qu'il faut annuler et que la confirmation ne doit
            pas etre traitée par la conversation suivante
        """

        if infos_in_message.get('intent')== 'oui':
            self.conv_to_cancel.status = None
            return 'Votre demande a bien été annulée \n' + self.conv_to_cancel.handler\
                .question_generator()
        else :
            self.state = None
            self.status = self.status_finished
            return self.conv_to_cancel.response({}, 'bololololo')
