from Conversations.conv_train import ConvTrain
from Conversations.conv_hotel import ConvHotel
from Conversations.conv_annulation import ConvAnnulation
from Conversations.conv_small_talk import ConvSmallTalk
from Conversations.conv_name_info import ConvNameInfo
from fiche_voyage import FicheVoyage
from Conversations.abstract_conv import AbstractConv
from Conversations.conv_helper import check_coherent_voyage, string_list, string_recap, check_string
import Conversations.convconfigs.conv_voyage_config as config

class ConvVoyage(AbstractConv):
    """
       Conversation pour gérer le voyage,
       plusieurs états possibles :
        - info_gathering : On manque d'infos sur le voyage donc on crée une conv train ou hotel
        - yes_no_question_asked : On vient de poser une question oui/non on appel donc yes_no_answer()
        - confirmation_asked : On a toute les infos on vient d'afficher le récap on attend appel conv_recap()
        - modify_travelers : Etat dans lequel on se place quand l'utilisateur demande a modifier un voyageur, on appel
                            question_for_modify_travelers()
    """

    status_ongoing = "voyage"
    status_finished = None
    current_conv = None
    hotel_asked = False
    sentences = None
    infos_needed = None

    def __init__(self, handler, classe : str):
        self.user = None
        self.traveler = None #ca va etre le voyageur
        self.set_from_config(classe)
        self.travelers = []
        self.info_asked = classe
        self.voyage = {}
        self.complement = {}
        self.error = False
        self.status = self.status_ongoing
        self.handler = handler
        self.status_conv = 'info_gathering'

    def response(self, infos_in_message : dict, message : str):
        if self.current_conv and self.current_conv.status:
            response = self.current_conv.response(infos_in_message, message)
        else :
            response = self.no_conv_handler(infos_in_message, message)
        return response

    def no_conv_handler(self, infos_in_message : dict, message : str):
        """
            Méthode appelée si on a pas de conversations autre en cours, suivant l'etat courant
            genère la réponse appropriée.
        """
        if infos_in_message.get('intent')=='annuler':
            self.current_conv = ConvAnnulation(self)
            response = self.current_conv.response(infos_in_message, message)
            return response
        if self.info_asked == 'train': self.info_asked = 'aller'
        possible_status = {
            'info_gathering' : self.create_conv_and_answer,
            'yes_no_question_asked' : self.yes_no_answer,
            'confirmation_asked' : self.confirmation_answer,
            'modify_travelers' : self.modify_travelers
        }
        if self.status_conv in possible_status.keys() :
            response = possible_status.get(self.status_conv)(infos_in_message, message)
            return response

    def create_conv_and_answer(self, infos_in_message : dict, message : str):
        """
            Permt de créer la conversation souhaitée (train ou hotel) ou degénérer la reponse appropriée
        """
        possible_info_asked = {
            'aller' : ConvTrain,
            'retour' : ConvTrain,
            'hotel' : ConvHotel,
            'voyageur' : ConvNameInfo,
            'voyageur_add' : ConvNameInfo,
        }
        if self.info_asked in possible_info_asked.keys():
            self.current_conv = possible_info_asked[self.info_asked](self, '')
            response = self.current_conv.response(infos_in_message, message)
        elif self.info_asked == 'voyageurs' :
            self.status_conv = 'modify_travelers'
            response = self.question_for_modifying_traveler()
        elif self.info_asked == 'motif' :
            self.complement['motif'] = message
            if check_string(self.complement['motif']):
                if 'motif' in self.infos_needed :
                    self.infos_needed.remove('motif')
                self.info_asked = None
            else :
                self.status_conv = 'info_gathering'
            response = self.question_generator()
        elif self.info_asked == 'commentaires' :
            if 'commentaires' in self.infos_needed :
                self.infos_needed.remove('commentaires')
            self.complement['commentaires'] = message
            self.info_asked = None
            response = self.question_generator()
        else :
            response = self.question_generator()
        return response

    def question_generator(self):
        """
            Permet de poser la question correspondant aux infos manquante pour le voyage

        """
        self.status_conv = 'yes_no_question_asked'
        questions = config.questions
        if not self.voyage.get('voyageurs') and 'voyageur_add' not in self.infos_needed:
            self.infos_needed.append('voyageur_add')
        if self.infos_needed:
            if self.is_hotel_needed() and 'hotel' not in self.infos_needed and 'hotel' not in self.voyage:
                self.infos_needed.insert(1, 'hotel')
                self.hotel_asked = True
            key = self.infos_needed[0]
            self.info_asked = key
            return questions[key]
        else :
            self.status_conv = 'confirmation_asked'
            return self.conv_recap()

    def conv_recap(self):
        """
            Récapitulatif du voyage et check de cohérence
        """
        response = "Récapitulatif de votre voyage : \n\n"
        response += string_recap(self.voyage) + '\n'
        items  = self.voyage.keys()
        response += string_recap(self.complement) + '\n'
        itemsComplement  = self.complement.keys()
        errors = check_coherent_voyage(self.voyage)
        if errors:
            response += errors[0]
            response += "\nVeuillez corriger vos informations : entrez le nom de l'item à modifier parmi ("
            response += string_list(items) + ", " + string_list(itemsComplement) + ")"
            self.error = True
            return response
        self.validation = True
        if 'hotel' in self.voyage.keys():
            response += "Pour votre réservation, nous allons sélectionner un hotel parmi nos hotels partenaires. \n \n "
        response = response + "Si cela vous convient, entrez 'oui'\n" \
                   + "Sinon entrez le nom de l'item à modifer (" + string_list(items) + ", " + string_list(itemsComplement) + ")"
        return response

    def confirmation_answer(self, infos_in_message : dict, message : str):
        if infos_in_message.get('intent') == 'oui' and not self.error:
            return self.confirm_voyage()
        elif message.strip().lower() in self.voyage.keys() :
            self.info_asked = message.strip().lower()
            self.status_conv = 'info_gathering'
            self.error = False
            return self.create_conv_and_answer(infos_in_message, message)
        elif message.strip().lower() in self.complement.keys() :
            self.status_conv = 'info_gathering'
            self.info_asked = None
            self.infos_needed.append(message)
            self.error = False
            return self.create_conv_and_answer(infos_in_message, message)
        elif message == 'bololololo':
            return self.question_generator()
        else:
            return ConvSmallTalk(self, infos_in_message.get('intent')).response(infos_in_message, message) \
            + '\n' +self.question_generator()

    def yes_no_answer(self, infos_in_message: dict, message: str):
        if infos_in_message.get('intent') == 'oui' or self.info_asked in ["motif", "commentaires"]:
            if self.info_asked == 'voyageur_solo':
                if 'voyageur' in self.infos_needed: self.infos_needed.remove('voyageur')
                if 'voyageur_add' in self.infos_needed: self.infos_needed.remove('voyageur_add')
                self.add_infos(self.handler.user)
            return self.create_conv_and_answer(infos_in_message, message)
        elif infos_in_message.get('intent') == 'non':
            if self.info_asked == 'voyageur':
                self.add_infos(self.handler.user)
            if self.info_asked in self.infos_needed:
                self.infos_needed.remove(self.info_asked)
            return self.question_generator()
        elif message == 'bololololo':
            return self.question_generator()
        else:
            return ConvSmallTalk(self, infos_in_message.get('intent')).response(infos_in_message, message) \
                   + '\n' + self.question_generator()



    """
        Suivent toutes les fontcions d'aide pour cette conversation
    """



    def modify_travelers(self, infos_in_message : dict, message : str):
        if message.isdigit() and int(message) <= len(self.voyage.get('voyageurs')) and int(message) > 0 :
            choice = int(message)
            self.voyage.get('voyageurs').remove(self.voyage.get('voyageurs')[choice - 1])
            return self.question_for_modifying_traveler()
        elif message.lower().strip() == 'ajouter':
            self.info_asked = 'voyageur_add'
            self.infos_needed.append('voyageur_add')
            return self.create_conv_and_answer(infos_in_message, message)
        else :
            return self.question_generator()

    def question_for_modifying_traveler(self):
        if 'voyageurs' in self.voyage.keys():
            i = 0
            response  = 'Pour enlever un voyageur entrez son numéro : \n'
            for traveler in self.voyage['voyageurs']:
                i += 1
                response+= str(i) + ' : ' + traveler['prenom'] + ' ' + traveler['nom'] + ' (' +traveler['mail']+')' +'\n'
            response += "Pour ajouter d'autres voyageurs entrez 'ajouter', sinon entrez 'fin'"
            return response
        else : ''

    def add_infos(self, infos : dict):
        if self.info_asked == 'voyageur' or self.info_asked == 'voyageur_add' or self.info_asked == 'voyageur_solo':
            self.travelers.append(infos)
            self.voyage['voyageurs'] = self.travelers
        else :
            self.voyage[self.info_asked] = infos
        if self.info_asked in self.infos_needed and self.info_asked != 'voyageur_add':
            self.infos_needed.remove(self.info_asked)

    def confirm_voyage(self):
        if 'hotel' in self.voyage.keys() or 'aller' in self.voyage.keys() or 'retour' in self.voyage.keys():
            response = 'Mail récapitulatif envoyé !'
        else :
            response = 'Réservation vide - Pas de mail envoyé'
        self.send_infos()
        self.status = None
        return response

    def is_hotel_needed(self):
        hotel_is_needed = False
        if self.hotel_asked :
            return False
        if self.voyage.get('aller'):
            if self.voyage.get('aller').get('arrivée') == 'Paris':
                hotel_is_needed = True
        if self.voyage.get('retour'):
            if self.voyage.get('retour').get('départ') == 'Paris':
                hotel_is_needed = True
        return hotel_is_needed

    def send_infos(self):
        f = FicheVoyage(self.handler.user)
        f.add_voyage(self.voyage, self.complement)
        if 'hotel' in self.voyage.keys() or 'aller' in self.voyage.keys() or 'retour' in self.voyage.keys():
            print("Création des fiches voyage...")
            f.createFiche_Train()
            f.createFiche_Hotel()
            print("Fiches créées.")
            print("Envoi des fiches par mail...")
            f.sendFiche(self.voyage)
            print("Mails envoyés.")
        else :
            print("Réservation vide - Pas de mail envoyé")


    def set_from_config(self, classe):
        self.infos_needed = config.infos_needed
