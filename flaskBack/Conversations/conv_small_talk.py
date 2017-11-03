from Conversations.abstract_conv import AbstractConv
import random
import meteo_api_helper as api_meteo
from datetime import datetime
from Data.phrasebot import Blague, Etat, Bonjour, Aurevoir, Capacites, Fort, Merci, Mauvais

class ConvSmallTalk(AbstractConv):
    status = None
    def __init__(self, handler , classe):
        pass

    def response(self, infos_in_message : dict, message : str):
        #La classe correspond à l'intention détectée dans la phrase envoyé par l'utilisateur. Elle est fournie par le parser.
        classe = infos_in_message.get('intent')
        #Si détection de la classe bonjour, génération aléatoire d'une réponse adaptée a bonjour parmi une sélection
        if classe == 'bonjour':
            bonjour = Bonjour
            for i in range(0,1):
                choix_bonjour = random.choice(bonjour)
                response = choix_bonjour[0]
        #Si détection de la classe état (i.e "comment vas tu ?"), génération aléatoire d'une réponse adaptée a état parmi une sélection
        elif classe == 'etat':
            etat = Etat
            for i in range(0,1):
                choix_etat = random.choice(etat)
                response = choix_etat[0]
        #Si détection de la classe blague, génération aléatoire d'une blague
        elif classe == 'blague':
            blague = Blague
            for i in range(0,1):
                choix_blague = random.choice(blague)
                response = choix_blague[0] + "\n" + choix_blague[1]
        #Si détection de la classe fort (i.e "t'es trop fort"), génération aléatoire d'une réponse adaptée a fort parmi une sélection.
        elif classe == 'fort':
            fort = Fort
            for i in range(0,1):
                choix_fort = random.choice(fort)
                response = choix_fort[0]
        #Si détection de la classe capacités (i.e "Que sais tu faire ?"), génération aléatoire d'une réponse adaptée à capacités parmi une sélection.
        elif classe == 'capacites':
            capacites = Capacites
            for i in range(0,1):
                choix_capacites = random.choice(capacites)
                response = choix_capacites[0]
        #Si détection de la classe mauvais (i.e "t'es mauvais."), génération aléatoire d'une réponse adaptée à mauvais parmi une sélection.
        elif classe == 'mauvais':
            mauvais = Mauvais
            for i in range(0,1):
                choix_mauvais = random.choice(mauvais)
                response = choix_mauvais[0]
        #Si détection de la classe merci, génération aléatoire d'une réponse adaptée à merci parmi une sélection.
        elif classe == 'merci':
            merci = Merci
            for i in range(0,1):
                choix_merci = random.choice(merci)
                response = choix_merci[0]
        #Si détection de la classe au revoir, génération aléatoire d'une réponse adaptée à au revoir parmi une sélection.
        elif classe == 'aurevoir' :
            aurevoir = Aurevoir
            for i in range(0,1):
                choix_aurevoir = random.choice(aurevoir)
                response = choix_aurevoir[0]
        #Si détection de la classe "oror" (i.e "a ou b ??"), génération d'une réponse (i.e soit a soit b)
        elif classe == 'oror' :
            L = message.split(' ou ')
            if(len(L) == 2):
                op1 = L[0]
                op2 = L[1][:-3]
                response = op1 if hash_to_int(op1) > hash_to_int(op2) else op2
        #Si détection de la classe "pas_compris", réponse automatique pour expliquer qu'un bot n'a pas des capacités humaines.
        elif classe == 'pas_compris' :
            response = "Je suis désolée, je ne suis qu'un simple robot, je n'ai pas compris. \n" \
                       " Si vous avez un problème, vous pouvez joindre le SVP au 09 69 36 87 81."
        #Si détection de la classe "météo", appel de la fonction météo.
        elif classe == 'meteo':
            response = response_meteo(infos_in_message, message)
        else :
            response = ''
        return response


def hash_to_int(string):
    res = 0
    for x in string:
        res += ord(x)
        res %= 23
    return res

def response_meteo(infos_in_message : dict, message: str):
    """
        Renvoie la météo en réponse à un message de l'utilisateur où l'intention détectée était météo.
        Nécéssité d'avoir deux informations : date < 7 jours et ville (en France).
    """
    ville_keys = ['départ', 'arrivée']
    date_keys = ['date_arrivee', 'date_arrivée']
    city = None
    date = None
    for key in infos_in_message.keys():
        if key in ville_keys:
            city = infos_in_message.get(key)
        if key == 'villes_inconnues':
            city = infos_in_message.get(key)[0]
        if key in date_keys:
            date = infos_in_message.get(key)['jour']
        if key == 'dates_inconnues':
            date = infos_in_message.get(key)[0]['jour']
    if city:
        if not date :
            #date d'aujd
            date = datetime.now().strftime('%d/%m/%Y')
        meteo = api_meteo.get_weather_for_city_and_date(city, date)
        if meteo:
            response = 'Le ' + date + ' à ' + city + ' :\n'
            response += '- État du ciel : ' + meteo.get('text_meteo') + '\n'
            response += '- Température : ' + meteo.get('max_temp') + '°C' + '\n'
            response += '- Probabilité de pluie : ' + meteo.get('chance_of_rain')
        else :
            # Si un utilisateur demande la météo au-dela de 7 jours. Limitation à 7 jours dûe à l'API.
            return "Désolé, la météo n'est pas disponible pour cette date !"
    else :
        #Si l'utilisateur n'a pas fourni assez d'information.
        response = 'Veuillez indiquer une ville et une date pour obtenir la météo'
    return response
