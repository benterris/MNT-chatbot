from Conversations.abstract_conv import AbstractConv
from Conversations.conv_annulation import ConvAnnulation
from Conversations.conv_helper import check_coherent_train, check_for_relevant_infos, proposition_trains
from Conversations.conv_small_talk import ConvSmallTalk
import Conversations.convconfigs.conv_train_config as config
import train_api_helper as api_sncf
import meteo_api_helper as api_meteo

class ConvTrain(AbstractConv):
    '''
        Classe pour gérer tous les aspects de la conversation liée à la réservation de train.
    '''

    status_ongoing = "train"
    status_finished = None
    current_conv = None
    relevant_keys = ["départ", 'arrivée', 'date_arrivee', 'date_depart', 'villes_inconnues', 'dates_inconnues']
    trains_wanted = None
    request = None
    sentences = None
    def __init__(self, handler, classe):
        self.status = self.status_ongoing
        self.annulation = False
        self.proposals = None
        self.infos_needed = ["départ", "arrivée", "jour", "heure"]
        self.set_from_config(classe)
        self.info_asked = None
        self.validation = False
        self.infos = {}
        self.handler = handler
        self.add_infos_from_handler()


    def response(self, infos_in_message: dict, message : str):
        if not self.current_conv:
            return self.no_conv_handler(infos_in_message, message)
        else :
            return self.annulation_handler(infos_in_message, message)

    def annulation_handler(self, infos_in_message : dict, message : str):
        response = self.current_conv.response(infos_in_message, message)
        if self.current_conv.status:
            return response
        else :
            return self.no_conv_handler(infos_in_message, message)

    def confirmation(self, message: str, infos_in_message : dict):
        """
            Traite la réponse lorsqu'on est à l'étape de confirmation.
        """
        if self.proposals:
            if message.isdigit() and int(message) <= len(self.proposals) and int(message) > 0 :
                choice = int(message)
                train_chosen = self.proposals[choice - 1]
                self.infos['jour'] = train_chosen['departure_date']
                self.infos['heure'] = train_chosen['departure_time']
                self.status = self.status_finished
                self.handler.add_infos(self.infos)
                response = self.message_meteo() + self.handler.question_generator()
                return response
            else:
                self.validation = False
                return self.no_conv_handler(infos_in_message, message)
        else :
            if infos_in_message.get('intent') == 'oui':
                self.status = self.status_finished
                self.handler.add_infos(self.infos)
                response = self.message_meteo() + self.handler.question_generator()
                return  response
            else :
                self.validation = False
                return self.no_conv_handler(infos_in_message, message)


    def add_location(self, arrival_or_departure : str, city : str):
        self.infos[arrival_or_departure] = city
        if arrival_or_departure in self.infos_needed :
            self.infos_needed.remove(arrival_or_departure)

    def message_meteo(self):
        meteo = api_meteo.get_weather_for_city_and_date(self.infos.get('arrivée'), self.infos.get('jour'))
        if meteo:
            response = "Météo à votre arrivée : \n"
            response += '- État du ciel : ' + meteo.get('text_meteo') +'\n'
            response += '- Température : ' + meteo.get('max_temp') + '°C' + '\n'
            response += '- Probabilité de pluie : ' + meteo.get('chance_of_rain') + '\n'
        else :
            response =''
        return response

    def add_jour(self, jour : str):
        self.infos['jour'] = jour
        if 'jour' in self.infos_needed :
            self.infos_needed.remove('jour')

    def add_heure(self, heure : str):
        self.infos['heure'] = heure
        if 'heure' in self.infos_needed :
            self.infos_needed.remove('heure')

    def question_generator(self):
        if self.infos_needed:
            self.info_asked = self.infos_needed[0]
            return self.sentences[self.info_asked]
        else:
            errors = check_coherent_train(self.infos, self.handler.voyage)
            if errors:
                return errors[0] + '\nVeuillez corriger vos informations.'
            self.validation = True
            res = self.fetch_data_trains(self.infos)
            if self.proposals :
                return res + self.sentences['ask_train_number']
            else :
                res += self.sentences['no_train_available']
                return res



    def response_generator(self):
        response = "Vous voulez un train"
        if "départ" in self.infos.keys():
            response += " de " + self.infos.get('départ')
        if "arrivée" in self.infos.keys():
            response += " pour " + self.infos.get('arrivée')
        if "jour" in self.infos.keys():
            response += ' le ' + self.infos.get('jour')
        if "heure" in self.infos.keys():
            response += ' à ' + self.infos.get('heure')
        return response + '\n' + self.question_generator()

    def fetch_data_trains(self, infos):
        departure_or_arrival = 'departure'
        self.request = api_sncf.set_request(
            infos.get('départ'), infos.get('arrivée'),
            infos.get('jour'), infos.get('heure'), 'departure')
        data = api_sncf.get_possible_trips_from_request(self.request, departure_or_arrival)
        self.proposals = data
        return proposition_trains(data)

    def infos_given_to_infos(self, infos_given : dict):
        type_of_infos_given = infos_given.keys()
        for key in type_of_infos_given:
            if key == 'date_départ' or key == 'date_arrivée':
                self.add_date_time(infos_given.get(key))
            if key == 'dates_inconnues':
                self.set_info_for_unknown_dates(infos_given.get(key))
            elif key == "départ" or key =="arrivée":
                self.add_location(key, infos_given.get(key))
            elif key == "villes_inconnues":
                cities = infos_given.get('villes_inconnues')
                self.set_info_for_unknown_cities(cities)

    def set_info_for_unknown_dates(self, unknwown_dates : []):
        if len(unknwown_dates) == 1 :
            date = unknwown_dates[0]
            self.add_date_time(date)

    def set_info_for_unknown_cities(self, unknown_cities : []):
        if len(unknown_cities)==1:
            city = unknown_cities[0]
            if self.info_asked:  # cas ou on a demandé un truc a l'interlocuteur
                self.add_location(self.info_asked, city)
            else:                                            # on suppose que si le bot recoit une ville sans qu'on lui ait rien avoir demandé c'est la ville d'arrivée
                if 'arrivée' in self.infos_needed:
                    self.add_location('arrivée', city)
                elif 'départ' in self.infos_needed:
                    self.add_location('départ', city)

    def no_conv_handler(self, infos_given : dict, message : str):
        response = ''
        if infos_given.get('intent')== 'annuler':
            self.current_conv = ConvAnnulation(self)
            return self.current_conv.response(infos_given, message)
        if self.validation:
            return self.confirmation(message, infos_given)
        self.infos_given_to_infos(infos_given)
        if not check_for_relevant_infos(infos_given, self.relevant_keys):
            response = ConvSmallTalk(self, infos_given.get('intent')).response(infos_given, message) + '\n'
        response += self.response_generator()
        return response


    def set_to_state(self, infos : dict):
        for key in infos.keys():
            if key in self.infos_needed:
                self.infos_needed.remove(key)

    def add_infos_from_handler(self):
        """
            Permet de récupérer les infos du voyages qui ont déjà été entrées pour ne pas le redemander
        """
        voyage = self.handler.voyage
        infos = {}
        if self.handler.info_asked == 'aller':
            if voyage.get('retour'):
                infos['départ'] = voyage.get('retour').get('arrivée')
                infos['arrivée'] = voyage.get('retour').get('départ')
            if voyage.get('hotel'):
                infos['arrivée'] = voyage.get('hotel').get('ville')
                infos['jour'] = voyage.get('hotel').get('date_arrivee')
            if voyage.get('aller'):
                infos = voyage.get('aller')
        if self.handler.info_asked == 'retour':
            if voyage.get('aller'):
                infos['départ'] = voyage.get('aller').get('arrivée')
                infos['arrivée'] = voyage.get('aller').get('départ')
            if voyage.get('hotel'):
                infos['départ'] = voyage.get('hotel').get('date_arrivee')
                infos['jour'] = voyage.get('hotel').get('date_depart')
            if voyage.get('retour'):
                infos = voyage.get('retour')
        self.infos = infos
        self.set_to_state(infos)



    def add_date_time(self, date : dict):
        for key in date.keys():
            if key == "jour":
                self.add_jour(date.get(key))
            elif key == "heure":
                self.add_heure(date.get(key))


    def set_from_config(self, classe):
        self.sentences = config.sentences_train