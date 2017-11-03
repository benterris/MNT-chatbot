"""
Fichier qui rassemble les fonctions d'analyse du message de l'utilisateur.
De l'extérieur, pour extraire l'intention et les informations générales du message,
on doit appeler la fonction parse_message.
"""

import Parser_general.parser_city as pc
import Parser_general.parser_time as pt
from http_helper import http_date
from Classifier.classifier import classify
from urllib import parse
import re


def parse_message(message : str, toClassify : str):
    """
    Input : message le message à parser, toClassify = {'classify'|'not_classify'} qui spécifie si il y a besoin de classifier la sortie
    Renvoie un dictionnaire pouvant contenir :
    {
       'départ' -> ville de départ
       'arrivée' -> ville d'arrivée
       'villes_inconnues' -> liste des villes trouvées sans avoir pu les labelliser
       'date_arrivee' -> {
           'datetime' -> date et h detectées au format '2017-10-03T09:00:00.000-07:00'
           'jour' -> jour si spécifié, au format '03/10/2017'
           'heure' -> heure si spécifiée, au format '09:00:00'
           'date_text' -> section de la phrase de l'utilisateur correspondant à la date et l'h
           'date_grain' -> précision temporelle de la demande de l'utilisateur : 'minute', 'hour', 'day', 'week'...
       }
       'date_depart' -> idem que date_arrivee mais pour la date de départ
       'dates_inconnues' -> liste des dates trouvées sans avoir pu les labelliser (pour chacune même format que date_depart ou date_arrivee)
       'intent' -> si demandé (toClassify == 'classify'), on classifie le message parmi :
                ['aurevoir', 'blague','bonjour','capacites', 'etat', 'fort',
                 'hotel', 'mauvais','merci', 'meteo', 'personnal_infos','train',
                 'vpn', 'annuler', 'oui', 'entrainement', 'non', 'oror', 'not_sure']
    }
    """

    # Le message arrive avec caractère échappés pour l'URL
    # Il faut lui rendre sa forme originelle
    message = parse.unquote_plus(message)

    # Parsing villes
    dict_cities = pc.get_city_dict(message, pc.search_cities(message))

    # Utilisation de Duckling pour le parsing des villes
    dict_date = pt.date_with_needed(message)

    # On rassemble les informations relatives aux villes et aux dates
    dict_cities.update(dict_date)
    dict_total = dict_cities

    # On cherche à classifier l'intention de l'utilisateur si demandé
    if toClassify == 'classify':
        # on clean d'abord le message
        dict_total['intent'] = classify(clean_before_classify(message, dict_total))

    # Certains intents sont parsés directement (voir is_of_type_message)
    # Ils n'ont pas besoin de passer par le classifier, et écrasent l'intent
    # trouvé par le classifier le cas échéant
    for typeMsg in ['annuler', 'oui', 'entrainement', 'non', 'oror']:
        if is_of_type_message(message, typeMsg):
            dict_total['intent'] = typeMsg

    return dict_total


def clean_before_classify(message, dict_total):
    """
        Les valeurs spécifiques pour les noms de villes et dates n'ont pas à
        intervenir dans la classification. On remplace ici toutes les occurences de
        noms de villes et d'indications de dates respectivement par "ville" et
        "date".
    """
    # remplacement des noms de villes par "ville"
    if dict_total.get('départ'):
        message = replace_occurrence(message, dict_total.get('départ'), 'ville')
    if dict_total.get('arrivée'):
        message = replace_occurrence(message, dict_total.get('arrivée'), 'ville')
    if dict_total.get('villes_inconnues'):
        for city in dict_total.get('villes_inconnues'):
            message = replace_occurrence(message, city, 'ville')

    # remplacement des indications de dates par "date"
    if dict_total.get('dates_inconnues'):
        for date in dict_total.get('dates_inconnues'):
            message = replace_occurrence(message, date.get('date_text'), 'date')
    if dict_total.get('date_depart'):
        message = replace_occurrence(message, dict_total.get('date_depart').get('date_text'), 'date')
    if dict_total.get('date_arrivee'):
        message = replace_occurrence(message, dict_total.get('date_arrivee').get('date_text'), 'date')

    # Remplacement de 'vpn' ou 'cga' par 'ornithorynque'
    # Ici fix rapide : les mots 'vpn' et 'cga' n'existent pas dans le modèle
    # Spacy et donnent donc des vecteurs nuls. Plutot qu'entrainer un nouveau
    # modèle spacy pour trouver leur vecteur (ce qui serait la meilleure méthode
    # mais demanderait beaucoup de temps), nous avons choisi de remplacer
    # toutes leurs occurences par un mot peu usité mais existant dans le modèle Spacy
    message = re.sub('vpn|cga', 'ornithorynque', message)

    return pc.simplify(message)

def replace_occurrence(message, pattern, replaceWith):
    """Renvoie message dans lequel on a remplacé pattern par replaceWith"""

    # no_new_text : dans le cas d'un intervalle de temps, à cause du
    # fonctionnement de Duckling le texte correspondant aux deux extrémités est
    # identique, on a donc remplacé un des deux par "no_new_text"
    # (cf.parser_time.get_time_data) qu'on ne remplace pas
    if pattern != 'no_new_text' and pc.simplify(pattern) in pc.simplify(message):
        start = pc.simplify(message).index(pc.simplify(pattern))
        end = start + len(pattern)
        return message[:start] + replaceWith + message[end:]
    return message

def get_time_data(message):
    """Filtre les données renvoyées par Duckling pour ne sélectionner qu'une seule date"""
    req_data = http_date(message)
    date_data = []
    # On ne prend que la première date
    for data in req_data:
        if data['dim'] == 'time':
            return data
    return None


def is_of_type_message(message, typeMsg):
    """
        Renvoie True si message est du type typeMsg, parmi ['annuler', 'oui', 'non', 'entrainement']
    """
    # patterns qu'on identifie comme indiquant un type de message
    patterns = {
        'annuler': 'stop|annuler|cancel|quitter|arreter|recommencer|annule|annulation|quit|end|arrete',
        'oui': 'ou+i+|ok|ye+s+|suite|suivant',
        'non': 'non|no|nope',
        'oror': '.* ou .* \?\?',
        'entrainement': 'entrainement'
    }
    if typeMsg in patterns.keys():
        # On ne matche que des mots entiers (i.e. entre deux espace / au début / à la fin de la string)
        p = re.search('(.*\s|^)(' + patterns[typeMsg] + ')(\s.*|$)', pc.simplify(message))
        if p:
            return True
        return False
    print('Erreur : typeMsg invalide (' + typeMsg + '), doit être dans ' + str(dict.keys()))
    return False
