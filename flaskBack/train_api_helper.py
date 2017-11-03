"""
    Méthodes pour la connexion à l'api de la sncf
"""

import requests
import pythonconfig
import json
import datetime

file = open(pythonconfig.gares_json_path)
data = json.load(file)
token = pythonconfig.token_sncf

#Remarque : type du fichier = liste
def city_name_to_code(city : str) :
    """
        Retourne le code commune SNCF correspondant à la ville (cf /Dta/gares.json)
    """
    i = 0
    while data[i].get("fields").get("commune") != city.capitalize() and i<=3003:
        i +=1
    if data[i].get("fields").get("commune") == city.capitalize() :
        code_commune_avec_tiret = data[i].get("fields").get("departement_commune")
        code_commune = code_commune_avec_tiret.replace('-','')
        return code_commune
    else :
        print("Erreur : pas de code commune trouvé pour la ville " + city)
        return None

def convert_to_datetime(date : str, time : str):
    if not time :
        time = '06h00'
    date_time = datetime.datetime.strptime(date+'T'+time, '%d/%m/%YT%Hh%M').strftime('%Y%m%dT%H%M%S')
    return date_time

def convert_from_datetime(date_time : str):
    dateTtime = datetime.datetime.strptime(date_time, '%Y%m%dT%H%M%S').strftime('%d/%m/%YT%Hh%M')
    datetimelist = dateTtime.split('T')
    return datetimelist


def set_request(departure, arrival, date, time, arrival_or_depature : str):
    """Effecture la requete à l'api de la sncf"""
    departure_code = city_name_to_code(departure)
    arrival_code = city_name_to_code(arrival)
    date_time = convert_to_datetime(date, time)
    payload = {'to': 'admin:fr:' + arrival_code,
               'from': 'admin:fr:' + departure_code,
               'datetime': date_time,
               'max_nb_journeys': 4, #on affiche 4 trajets
               'min_nb_journeys': 4,
               'datetime_represents': arrival_or_depature} #hmmm a voir
    return requests.get(pythonconfig.url_sncf_journeys, params = payload, auth = (token, '')).json()


def get_possible_trips_from_request(request : requests, departure_or_arrival : str):
    """Traite la requete pour extraire les trajets existants"""
    journeys = request.get('journeys')
    if not journeys : return None
    possible_trips = []
    if departure_or_arrival == 'arrival' : journeys = journeys[::-1]
    for journey in journeys:
        infos = set_infos_from_journey(journey)
        possible_trips.append(infos)
    return possible_trips


def set_infos_from_journey(journey : dict):
    duration_s = journey.get('duration')
    duration = '{:02}h{:02}min'.format(duration_s//3600, duration_s%3600//60)
    nbre_transferts = journey.get('nb_transfers')
    depature_date, depature_time = convert_from_datetime(journey.get('departure_date_time'))[0], \
                                   convert_from_datetime(journey.get('departure_date_time'))[1]
    arrival_date , arrival_time = convert_from_datetime(journey.get('arrival_date_time'))[0], \
                                  convert_from_datetime(journey.get('arrival_date_time'))[1]
    infos = {
        'nbre_transferts' : str(nbre_transferts),
        'duration' : str(duration),
        'departure_date' : depature_date,
        'departure_time' : depature_time,
        "arrival_date" : arrival_date,
        "arrival_time":arrival_time
    }
    return infos


# Début de méthodes pour prendre les trains suivants ou précédents
def set_next_request(departure, arrival, previous_request : dict):
    last_departure_datetime = previous_request.get('journeys')[-1].get('departure_date_time')
    t = datetime.datetime.strptime(last_departure_datetime, '%Y%m%dT%H%M%S')
    new_date_time_wanted = t + datetime.timedelta(minutes = 1)
    new_date_time_wanted = new_date_time_wanted.strftime('%Y%m%dT%H%M%S')
    date_time_list = convert_from_datetime(new_date_time_wanted)
    return set_request(departure, arrival, date_time_list[0], date_time_list[1], 'departure')

def set_previous_request(departure, arrival , previous_request : dict):
    last_departure_datetime = previous_request.get('journeys')[0].get('arrival_date_time')
    t = datetime.datetime.strptime(last_departure_datetime, '%Y%m%dT%H%M%S')
    new_date_time_wanted = t + datetime.timedelta(minutes=-1)
    new_date_time_wanted = new_date_time_wanted.strftime('%Y%m%dT%H%M%S')
    date_time_list = convert_from_datetime(new_date_time_wanted)
    return set_request(departure, arrival, date_time_list[0], date_time_list[1], 'arrival')
