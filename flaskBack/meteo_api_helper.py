"""
    Script pour utiliser l'API météo choisie : DarkSky.
    Choix de DarkSky car elle autorise beaucoup de requêtes par jour.
    Offre des informations météo à 7 jours.
"""

import requests
import datetime
import pythonconfig
import json

#Import du fichier avec les différentes gares et villes de France.
file = open(pythonconfig.gares_json_path)
data = json.load(file)

def city_name_to_geo(city : str):


    i = 0
    while data[i].get("fields").get("commune") != city.capitalize() and i <= 3003:
        i += 1
    if data[i].get("fields").get("commune") == city.capitalize():
        geo_city = data[i].get('fields').get('wgs_84')
        return geo_city
    else:
        print("Erreur : pas de position géographique pour la ville " + city)
        return None


def get_weather_for_city_and_date(city : str, date : str):
    """
        Fonction qui sort la météo en fonction du jour et du lieu.
        Météo sous la forme d'un dictionnaire avec 3 informations : état du ciel, la probabilité de pluie, la température max.
    """
    payload = {
        "exclude" : '[currently, minutely, hourly, alerts, flags]',
        "lang" : 'fr',
        'units' : 'si'
    }
    geo_city = city_name_to_geo(city)
    if not geo_city: return None
    geo_city_str = str(geo_city[0]) + ', ' + str(geo_city[1])
    date_sec = datetime.datetime.strptime(date , '%d/%m/%Y').timestamp()
    r = requests.get(pythonconfig.api_adress  +pythonconfig.api_key + '/' + geo_city_str, params = payload)
    days = r.json().get('daily')['data']
    for day in days:
        if day['time'] == date_sec :
            meteo = {
                'text_meteo' : day['summary'],
                'chance_of_rain' : str(int(float(day['precipProbability'])*100)) +'%',
                'max_temp' : str(int(day['apparentTemperatureMax'])),
                'date' : date_sec_to_date(day['time']),
            }
            return meteo
    return None


def date_sec_to_date(time : str):
    """
        Fonction qui permet de convertir la date au format adaptée pour l'API.
    """
    time = int(time)
    date = datetime.date.fromtimestamp(time)
    return date.strftime('%d/%m')
