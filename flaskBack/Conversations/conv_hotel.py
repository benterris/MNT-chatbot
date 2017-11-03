from Conversations.abstract_conv import AbstractConv
from Conversations.conv_helper import check_coherent_hotel
from Conversations.conv_helper import hotel_number_nights
from Conversations.conv_helper import check_for_relevant_infos
from Conversations.conv_annulation import ConvAnnulation
from Conversations.conv_small_talk import ConvSmallTalk
import Conversations.convconfigs.conv_hotel_config as config


class ConvHotel(AbstractConv):
    '''
        Classe pour gérer tous les aspects de la conversation liée à la réservation d'hôtel.
        Très similaire à la conversation de train
    '''

    #status_conv : int
    #infos : {}
    status_ongoing = None
    status_finished = None
    ville = None
    relevant_keys = None
    current_conv = None
    infos_needed = None
    sentences = None

    def __init__(self, handler, classe):
        self.set_from_config(classe)
        self.status = self.status_ongoing
        self.info_asked = None
        self.validation = False
        self.handler = handler
        self.infos = {}
        self.add_infos_from_handler()

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

    def confirmation(self, message: str, infos_in_message : dict): #À revoir
        if message in config.dict_hotel.keys():
            desired_hotel = config.dict_hotel[message]
            self.infos['hotel_wanted'] = desired_hotel
            self.status = self.status_finished
            self.handler.add_infos(self.infos)
            return self.handler.question_generator()
        if infos_in_message.get('intent') == 'oui':
            self.status = self.status_finished
            self.handler.add_infos(self.infos)
            return self.handler.question_generator()
        else:
            self.validation = False
            return self.no_conv_handler(infos_in_message, message)


    def add_date_arrival_or_departure(self, arrival_or_departure : str, datetime : dict):
        date = datetime.get('jour')
        self.infos[arrival_or_departure] = date
        if arrival_or_departure in self.infos_needed :
            self.infos_needed.remove(arrival_or_departure)
        if 'date_arrivee' and "date_depart" in self.infos.keys():
            self.infos['nights'] = str(hotel_number_nights(self.infos.get('date_arrivee'), self.infos.get('date_depart')))


    def add_city(self, city : str):
        self.infos['ville'] = city
        if 'ville' in self.infos_needed :
            self.infos_needed.remove('ville')

    def question_generator(self):
        response = ''
        questions = config.questions
        if self.infos_needed:
            for key in self.infos_needed:
                self.info_asked = key
                return questions[key]
        else:
            errors = check_coherent_hotel(self.infos)
            if errors:
                return errors[0] + '\n Veuillez corriger vos informations.'
            self.validation = True
            for key in config.dict_hotel.keys() :
                response += key + ' : ' + config.dict_hotel[key] +'\n'
            return response + self.sentences["favorite_hotel"]

    def response_generator(self):
        response = "Vous voulez un hôtel"
        if "date_arrivee" in self.infos.keys():
            response += " du " + self.infos.get('date_arrivee')
        if "date_depart" in self.infos.keys():
            response += " au " + self.infos.get('date_depart')
        if 'nights' in self.infos.keys():
            response += '\n ce qui correspond à ' + self.infos.get('nights') + ' nuit(s)'
        if "ville" in self.infos.keys():
            if self.infos.get('ville') != 'Paris' and 'ville' not in self.infos_needed :
                response = self.sentences['out_of_paris_hotel']
                return response
            else :
                response += ' à ' + self.infos.get('ville')
        return response + '\n' + self.question_generator()

    def infos_given_to_infos(self, infos_given : dict):
        type_of_infos_given = infos_given.keys()
        for key in type_of_infos_given:
            if key in self.ville:
                self.add_city(infos_given.get(key))
            if key == 'villes_inconnues':
                cities = infos_given.get('villes_inconnues')
                self.set_infos_for_unknown_cities(cities)
            elif key == "date_depart" or key =="date_arrivee":
                self.add_date_arrival_or_departure(key, infos_given.get(key))
            elif key == "dates_inconnues":
                datetimes = infos_given.get('dates_inconnues')
                self.set_info_for_unknown_dates(datetimes)

    def set_infos_for_unknown_cities(self, unknown_cities : []):
        if len(unknown_cities)==1:
            city = unknown_cities[0]
            self.add_city(city)

    def set_info_for_unknown_dates(self, unknown_dates : []):
        if len(unknown_dates)==1:
            datetime = unknown_dates[0]
            if self.info_asked:  # cas ou on a demandé un truc a l'interlocuteur
                self.add_date_arrival_or_departure(self.info_asked, datetime)
            else:
                # on suppose que si le bot recoit une date sans qu'on lui ait rien avoir demandé c'est la date d'arrivée
                if 'date_arrivee' in self.infos_needed:
                    self.add_date_arrival_or_departure('date_arrivee', datetime)
                elif 'date_depart' in self.infos_needed:
                    self.add_date_arrival_or_departure('date_depart', datetime)

    def no_conv_handler(self, infos_given : dict, message : str):
        response = ""
        if infos_given.get('intent')== 'annuler':
            self.current_conv = ConvAnnulation(self)
            return self.current_conv.response(infos_given, message)
        if self.validation:
            return self.confirmation(message, infos_given)
        self.infos_given_to_infos(infos_given)
        if not check_for_relevant_infos(infos_given, self.relevant_keys):
            response = ConvSmallTalk(self, infos_given.get('intent')).response(infos_given, message) + "\n"
        response = response + self.response_generator()
        return response

    def small_talk(self, infos_in_message : dict, message):
        """
            Fonction qui permet d'inclure le small talk dans une conversation de réservation d'hôtel.
        """
        response = ConvSmallTalk(self, infos_in_message.get('intent')).response(infos_in_message, message)
        return response

    def set_to_state(self, infos: dict):
        self.infos = infos
        for key in infos.keys():
            if key in self.infos_needed:
                self.infos_needed.remove(key)

    def add_infos_from_handler(self):
        voyage = self.handler.voyage
        infos = {'ville': 'Paris'}
        if voyage.get('retour'):
            infos['date_depart'] = voyage.get('retour').get('jour')
        if voyage.get('aller'):
            infos['date_arrivee'] = voyage.get('aller').get('jour')
        if voyage.get('hotel'):
            infos = voyage.get('hotel')
        self.infos = infos
        self.set_to_state(infos)


    def set_from_config(self, classe : str):
        self.ville = config.ville
        self.relevant_keys = config.relevant_keys
        self.infos_needed = config.infos_needed
        self.status_ongoing = config.status_ongoing
        self.sentences = config.sentences