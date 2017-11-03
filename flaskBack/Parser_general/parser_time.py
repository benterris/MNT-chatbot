"""
Ici on trouve les fonctions relatives au parsing des dates, principalement
utilisées par Parser_general.parse
"""
from http_helper import http_date
from datetime import datetime, timedelta
from Parser_general.parser_city import simplify
import re



def date_with_needed(message):
    """
        Renvoie un dictionnaire avec toutes les informations relatives aux dates
        contenues dans le message, de la forme :
        {
            'date_arrivee' -> {
                'datetime' -> date et h detectées au format '2017-10-03T09:00:00.000-07:00'
                'jour' -> jour si spécifié, au format '03/10/2017'
                'heure' -> heure si spécifiée, au format '09:00:00'
                'date_text' -> section de la phrase de l'utilisateur correspondant à la date et l'h
                'date_grain' -> précision temporelle de la demande de l'utilisateur :
                                        'minute', 'hour', 'day', 'week'...
            }
            'date_depart' -> idem que date_arrivee mais pour la date de départ
            'dates_inconnues' -> liste des dates trouvées sans avoir pu les
                                labelliser (pour chacune même format que
                                        date_depart ou date_arrivee)
        }
    """

    # On récupère les informations prétraitées
    all_dicts = get_time_data(message)

    # On les placera dans dict_dates une fois complètement traitées
    dict_dates = {}
    unknown_dates = []

    for date_data in all_dicts :
        datetimeStr = date_data['datetime']
        # On récupère séparément la date et l'heure dans des string formatées
        # comme on le veut
        dateStr, timeStr = to_str_date_time(datetimeStr)

        # specified : 'day' ou 'hour' ou les deux : indique ce à quoi il faut
        # s'intéresser dans la date de Duckling
        specified = select_grain(date_data)

        date = {}

        if 'day' in specified :
            date['jour'] = dateStr
        if 'hour' in specified :
            date['heure'] = timeStr

        # Récupération des infos et renommage des clés
        date['datetime'] = date_data['datetime']
        date['date_text'] = date_data['date_text']
        date['date_grain'] = date_data['grain']

        # determiner si les dates sont celles de départ ou d'arrivée :
        departOuArrivee = is_depart_or_arrivee(date_data['date_text'], message)
        if departOuArrivee == 'depart' :
            dict_dates['date_depart'] = date
        elif departOuArrivee == 'arrivee' :
            dict_dates['date_arrivee'] = date
        else : # dans le cas où on ne peut pas décider
            unknown_dates.append(date)

    # Dans le cas où on n'a que deux dates inconnues, et pas d'autres dates,
    # alors on peut supposer que la première date est celle d'arrivée et la
    # seconde celle de départ puisqu'elles sont restées dans l'ordre d'énonciation
    # du message
    if len(unknown_dates) == 2 and 'depart' not in dict_dates.keys() and 'arrivee' not in dict_dates.keys() :
        dict_dates['date_depart'] = unknown_dates.pop()
        dict_dates['date_arrivee'] = unknown_dates.pop()

    if unknown_dates:
        dict_dates['dates_inconnues'] = unknown_dates

    return dict_dates


def get_time_data(message):
    """
        Récupère les données de temps contenues dans message, avec Duckling
        Renvoie {'datetime' : temps en string formatée, 'grain', 'date_text'}
    """

    req_data = http_date(message)
    all_dicts = []

    # On doit déduire quelles sont les dates importantes de la forme de la
    # requête
    for data in req_data:
        if data['dim'] == 'time':
            date_data = {}
            if data['value']['type'] == 'interval':
                # Ici deux possibilités :
                # Ou bien l'intervalle est dû à un mot
                # type 'ce soir' ou 'demain après-midi' -> values 1 seule data,
                # Ou bien c'est dû à deux dates comme 'du 15 au 20' -> values
                # contient 3 valeurs

                # Cas dû à un mot : renvoyer 1 date
                if len(data['value']['values']) == 1:
                    date_data['datetime'] = data['value']['from']['value']
                    date_data['grain'] = data['value']['from']['grain']
                    date_data['date_text'] = data['body']
                    date_data['type'] = 'interval'
                    all_dicts.append(date_data)

                # cas dû à deux dates : renvoyer les deux dates
                elif len(data['value']['values']) == 3:
                    # pour la date de début d'intervalle :
                    date_data['datetime'] = data['value']['from']['value']
                    date_data['grain'] = data['value']['from']['grain']
                    date_data['date_text'] = data['body']
                    date_data['type'] = 'interval'
                    all_dicts.append(date_data)
                    # Pour la date de fin d'intervalle :
                    # Duckling renvoie +1 à la valeur définie par grain pour
                    # la date de fin d'intervalle, on doit donc corriger l'offset
                    # dans la cas jour (cf. correct_superior_offset_duckling)

                    date_to = {}
                    date_to['datetime'] = correct_superior_offset_duckling(data['value']['to']['value'], data['value']['to']['grain'])
                    date_to['grain'] = data['value']['to']['grain']
                    date_to['type'] = 'interval'
                    date_to['date_text'] = 'no_new_text' # le texte est déjà compris dans la borne inférieure de l'intervalle, pas besoin de l'avoir à nouveau ici
                    all_dicts.append(date_to)
                else :
                    print('Erreur : format du retour de Duckling inconnu : data["value"]["value"] pour le type intervalle de longueur inconnue : ', len(data['value']['values']))

            elif data['value']['type'] == 'value':
                date_data['datetime'] = data['value']['value']
                date_data['grain'] = data['value']['grain']
                date_data['values'] = data['value']['values']
                date_data['date_text'] = data['body']
                date_data['type'] = 'value'
                all_dicts.append(date_data)
            else :
                print('Erreur : format du retour de Duckling inconnu : data["value"]["type"] inconnu : ', data['value']['type'])

    return all_dicts


def select_grain(data):
    """
        On n'a pas toujours besoin à la fois de la date et de l'heure
        Si par exemple l'utilisateur entre simplement '14h', Duckling renverra
        la date d'aujourd'hui à 14h. Il faut donc détecter que la seule info
        pertinente est l'heure.

        Renvoie ['day'], ['hour'], ou les deux, selon les informations pertinentes
    """

    oneDay = timedelta(days=1)
    fiveDays = timedelta(days=5)
    halfDay = timedelta(hours=12)

    if data['type'] == 'interval':
        if data['grain'] == 'day':
            return ['day']
        return ['day', 'hour']

    # sinon on est dans un cas 'value' et pas 'interval'
    if data['grain'] == 'day':
        return ['day']
    if data['grain'] == 'minute':
        if len(data['values']) == 1:
            return ['hour']
        if len(data['values']) == 3:
            # ici probablement forme (0,0.5,7) ou (0,7,14)
            # on checke si on a bien au moins 5 jours d'écart entre deux des dates
            d0 = to_datetime(data['values'][0]['value'])
            d1 = to_datetime(data['values'][1]['value'])
            d2 = to_datetime(data['values'][2]['value'])
            if d2 - d1 > fiveDays or d1 - d0 > fiveDays:
                return ['day', 'hour']
            return['hour']
        return ['minutes']

    if data['grain'] == 'hour':
        if len(data['values']) == 3:
            # on vérifie si l'écart entre les dates est de 1 jour ou 1/2 jour
            d0 = to_datetime(data['values'][0]['value'])
            d1 = to_datetime(data['values'][1]['value'])
            d2 = to_datetime(data['values'][2]['value'])
            if ((d2 - d1) == halfDay and (d1 - d0) == halfDay) or ((d2 - d1) == oneDay and (d1 - d0) == oneDay):
                return ['hour']
            return ['day', 'hour']
        return ['day', 'hour']
    if data['grain'] == 'week' or data['grain'] == 'month' or data['grain'] == 'quarter' or data['grain'] == 'year':
        return ['day']
    if data['grain'] == 'second':
        return ['day', 'hour']
    print('Erreur : retour de requête Duckling inattendu - cas non traité')
    print(data)
    return None



def to_datetime(strDate):
    """Transforme une string de date au format AAAA-MM-JJTHH:MM:SS en un objet datetime"""
    return datetime.strptime(strDate[:19], '%Y-%m-%dT%H:%M:%S')

def to_str_date_time(strDate):
    """
        A partir d'une string de date ('%Y-%m-%dT%H:%M:%S'), renvoie deux string formatées :
        day : '%d/%m/%Y',
        hour : '%Hh%M'
    """
    date = to_datetime(strDate)

    day = date.strftime('%d/%m/%Y')
    hour = date.strftime('%Hh%M')

    return day, hour

def is_depart_or_arrivee(date_body, message):
    """
        Indique si la date (date_body) dans le message est probablement une date d'arrivée, de départ, ou inconnue.
    """
    pArrivee = re.search("(du |de |depuis )" + simplify(date_body), simplify(message))
    pDepart = re.search("(jusque |jusqu'a |jusqu'au |au |a )" + simplify(date_body), simplify(message))
    if pArrivee :
        return 'arrivee'
    if pDepart :
        return 'depart'
    return 'inconnu'

def correct_superior_offset_duckling(dateStr, grain):
    """
        Corrige l'offset automatique de Duckling qui rajoute +1 au grain pour la
        fin de l'intervalle
    """
    date = to_datetime(dateStr)
    if grain == 'day' or grain == 'hour':
        return date_string_add_time(dateStr, -1, grain)
    # Si on n'est pas à un grain 'day' ou 'hour', ce n'est pas grave
    # (l'offset est rajouté soit aux minutes, soit à mois et plus)
    # Cas mois et plus pas assez précis de toutes façons,
    # et minute et moins pas besoin de tant de précision
    return dateStr


def date_string_add_time(dateStr, nValue, valueType):
    """
        Prend une string au format '2017-10-05T09:00:00.000-07:00' et renvoie
        une string du même format avec nValue valueType de plus : '2017-10-04T09:00:00.000-07:00'
        valueType supportées : ['day', 'hour']
    """
    units = {
        'day': timedelta(days=1),
        'hour': timedelta(hours=1)
    }

    if valueType in units.keys():
        date = to_datetime(dateStr)
        date2 = date + nValue * units[valueType]
        return date2.strftime('%Y-%m-%dT%H:%M:%S.000+01:00')
    print('Error : ValueType ' + valueType + ' pas supportée (valuteType valides : ' + str(units.keys()) + ')')
    return dateStr
