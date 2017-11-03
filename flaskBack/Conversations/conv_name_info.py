import unidecode

import Conversations.convconfigs.conv_name_info_config as conf
import http_helper
from Conversations.abstract_conv import AbstractConv
from Conversations.conv_helper import check_format, check_string


class ConvNameInfo(AbstractConv):
    """
        Conversation pour la gestion des informations personnelles de l'utilisateur.
        On peut l'utiliser pour enregistrer un nouvel utilisateur ou pour modifier
        un utilisateur existant
    """

    # Utilisation :
    # Régler status_ongoing et status_finished sur les valeurs qu'on veu récupérer
    # De l'extérieur, appeler response :
    #   ConvNameInfo.response(message):
    #       Input : message : le message à traiter
    #       Output : response : le texte de réponse du bot



    status_ongoing = "personnal_infos"
    status_finished = None

    # status_conv :
    # 0-> début
    # 1 -> check si user dans database
    # 2 -> vérifie si email bien tapé
    # 3 -> infos en récupération
    # 4 -> en confirmation
    # 5 -> ok confirmé
    def __init__(self, handler, classe):
        self.status_conv = 0
        self.user = None
        self.infos = {}
        self.info_needed = ['prenom', 'nom', 'statut',
            'lieu_de_travail', 'section_service', 'telephone','date_de_naissance', 'grand_voyageur',
             'reductions'] # réductions pas nécessaires
        self.handler = handler
        self.status = self.status_ongoing
        self.info_asked = None
        self.tmp_email = None
        if self.handler.status =="voyage":
            self.sentences = conf.sentences_traveler
        else :
            self.sentences = conf.sentences_self
        if handler.user:
            self.set_state_change_personnal_infos(handler.user)

    def response(self, infos_in_message : dict, message : str):
        """Fonction appelée de l'extérieur : renvoie la réponse établie ici"""
        response = self.treat_message(infos_in_message, message)
        if self.status_conv != 5:
            self.status = self.status_ongoing
            return response
        if self.status_conv == 5:
            self.status = self.status_finished
            return response # mais aussi envoyer une update de statut !

    def add_user(self):
        if self.handler.status != 'voyage':
            self.handler.user = self.infos
        elif self.handler.status == 'voyage':
            self.handler.traveler = self.infos
            self.handler.add_infos(self.user)

    def set_state_change_personnal_infos(self, user):
        """
            Dans le cas d'un changement d'informations personnelles, on doit
            appeler cette méthode avec l'utilisateur à modifier en argument
        """
        self.status_conv = 6
        self.infos = user
        self.user = user
        if not self.infos :
            print("Erreur : conv_name_info est appelée pour modifier un utilisateur, mais n'a pas reçu d'utilisateur existant en argument")
        else :
            # on supprime l'user pour pouvoir enregistrer le nouveau
            http_helper.http_delete(user['mail'])

    def question_generator(self):
        """
            Génère les questions suivantes en fonction des informations manquantes
        """
        for key in self.info_needed:
            self.info_asked = key
            return self.sentences['questions'][key]



    def treat_message(self, infos_in_message : dict ,message : str):
        """
            Logique des différentes étapes de la conversation.
            On a plusieurs états :
            0 -> Début de la conversation, demande du mail
            1 -> Vérification de l'existence de l'utilisateur en bdd. Si oui,
                 conversation finie.
            2 -> Sinon, on vérifie que l'utilisateur n'a pas fait une faute de
                 frappe en tapant son mail et on reste dans cet état tant qu'il
                 ne confirme pas que son mail est correct.
            3 -> On demande les informations les unes après les autres
            4 -> Une fois qu'on a toutes les infos on demande une confirmation
                 et on permet de modifier si besoin
            5 -> Confirmation de l'utilisateur, on sort de la conversation
            6 -> Etat spécial pour la modification (pas création) d'utilisateur,
                 on passe les états 0 à 3
        """
        # Début
        if self.status_conv == 0 :
            self.status_conv = 1
            return self.sentences['first_question']
        # Check si email est dans la base
        if self.status_conv == 1 :
            if check_format(message, 'mail'):
                if self.get_user(infos_in_message, message.lower()) :
                    # Si oui, la conversation est terminée (= état 5)
                    self.status_conv = 5
                    self.add_user()
                    return self.sentences['user_found'](self.user) + "\n" + self.handler.question_generator()
                else :
                    # Sinon, on vérifie que ce n'est pas une faute de frappe (= état 2)
                    self.status_conv = 2
                    self.tmp_email = message
                    return self.sentences['user_not_found_first'](message)
            else :
                return self.sentences['wrong_mail']

        # Permettre de corriger l'email s'il est mal tapé
        if self.status_conv == 2 :
            if infos_in_message['intent'] == 'oui':
                # Si l'email est bien tapé, mais n'existe pas, alors début de la création du compte
                self.status_conv = 3
                self.infos['mail'] = self.tmp_email.lower()
                return self.sentences['account_creation'](self.tmp_email)+ '\n' + self.question_generator()
            else :
                # Si on a plutot un nouvel email qu'une confirmation, on réitère le processus précédent
                if check_format(message, 'mail'):
                    if self.get_user(infos_in_message, message.lower()) :
                        self.status_conv = 5
                        self.add_user()
                        return self.sentences['user_found'](self.user)+ "\n" + self.handler.question_generator()
                    else :
                        self.status_conv = 2
                        self.tmp_email = message.lower()
                        return self.sentences['user_not_found_second'](message)
                else :
                    return self.sentences['wrong_mail']


        # En récupération d'informations
        if self.status_conv == 3:
            if self.info_asked in self.info_needed :
                if check_format(message, self.info_asked) and check_string(message):
                    self.infos[self.info_asked] = message
                    self.info_needed.remove(self.info_asked)
                    if self.info_needed : # si on a encore des infos à demander
                        return self.question_generator()
                    else : # si on a terminé avec les questions, demande de confirmation
                        self.status_conv = 4
                        self.info_asked = None
                        return self.generate_confirmation_message()
                else :
                    return self.sentences['wrong_format']
            else :
                print('Erreur : information demandée (' + self.info_asked + ") pas dans les informations nécessaires (" + str(self.info_needed) + ")")

        # Phase de confirmation
        elif self.status_conv == 4 :
            if infos_in_message['intent'] == 'oui' :
                # Confirmation : tout est ok, on termine la conversation
                self.status_conv = 5
                self.save_to_db()
                self.add_user()
                return self.sentences['validate'] + '\n'+ self.handler.question_generator()
            if self.info_asked :
                # Si on était en modification après récap
                self.infos[self.info_asked] = message
                self.info_asked = None
                return "J'ai bien modifié ce champ. " + self.generate_confirmation_message()
            if self.parse_change(self.simplify(message)) in self.infos.keys() :
                # Si on était sur le récap et que l'user rentre un champ à modifier
                self.info_asked = self.parse_change(self.simplify(message))
                return "Veuillez entrer une nouvelle valeur pour le champ " + message + " :"
            return "Je n'ai pas compris, veuillez indiquer le champ à modifier ou tapez 'ok'."

        elif self.status_conv == 6 :
            # Etat spécial pour la modification : on va directement au récap
            # sans vérifier si le mail existe
            self.status_conv = 4
            return self.generate_confirmation_message()




    def save_to_db(self):
        """Fonction d'enregistrement en base de données"""
        if self.user :
            http_helper.http_delete(self.user['mail'])
        http_helper.http_bdd(self.infos)
        self.user = http_helper.http_get_user(self.infos['mail'])
        if not self.user :
            print("Erreur lors de l'enregistrement de l'utilisateur en base de données")



    def generate_confirmation_message(self):
        confirmation_message = 'Voici les informations que vous avez entrées :\n'
        confirmation_message += 'Prénom : ' + self.infos.get('prenom') + '\n'
        confirmation_message += 'Nom : ' + self.infos.get('nom') + '\n'
        confirmation_message += 'E-mail : ' + self.infos.get('mail') + '\n'
        confirmation_message += 'Numéro de téléphone : ' + self.infos.get('telephone') + '\n'
        confirmation_message += 'Statut : ' + self.infos.get('statut') + '\n'
        confirmation_message += 'Lieu de travail : ' + self.infos.get('lieu_de_travail') + '\n'
        confirmation_message += 'Section ou service : ' + self.infos.get('section_service') + '\n'
        confirmation_message += 'Date de naissance : ' + self.infos.get('date_de_naissance') + '\n'
        confirmation_message += 'Grand Voyageur : ' + self.infos.get('grand_voyageur') + '\n'
        confirmation_message += 'Carte de réduction : ' + self.infos.get('reductions') + '\n'
        confirmation_message += 'Si ces informations sont exactes, entrez "ok". Sinon, entrez le nom du champ à corriger.'
        return confirmation_message

    def simplify(self, s):
        """Enlève les accents, majuscules et tirets d'une string"""
        s = unidecode.unidecode(s).lower().replace('-', ' ')
        return s

    def parse_change(self, champ):
        """
            Fonction utilisée au moment de la sélection des champs à modifier après récap
            Transforme l'entrée de l'utilisateur pour que les match avec les noms des champs soient plus permissifs
        """
        if champ == 'e mail' or champ == 'mail' or champ == 'email':
            return 'mail'
        if champ == 'numero de telephone' or champ == 'numero telephone' or champ == 'numero':
            return 'telephone'
        if champ == 'lieu travail' or champ == 'lieu de travail' or champ == 'lieu':
            return 'lieu_de_travail'
        if champ == 'section' or champ == 'service' or champ == 'section ou service':
            return 'section_service'
        if champ == 'date de naissance' or champ == 'date' or champ == 'date naissance' or champ == 'naissance':
            return 'date_de_naissance'
        if champ == 'carte de reduction' or champ == 'carte reduction' or champ == 'carte' or champ == 'reduction':
            return 'reductions'
        if champ == 'voyageur' or champ == 'grand voyageur':
            return 'grand_voyageur'
        return champ

    def get_user(self,infos_in_message : dict , message : str):
        """
            Fonction qui récupère un utilisateur en base de données à partir de son mail
        """
        user = http_helper.http_get_user(message)
        if user:
            self.infos = user
            self.user = user
            return True
        else:
            return False
