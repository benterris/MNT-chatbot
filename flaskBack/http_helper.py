"""
    Script nécessaire pour réaliser des requêtes HTTP et relier le back et le front.
"""
import requests
import pythonconfig
from urllib import parse
import json
import re

def http_parse(msg : str, to_classify : str = 'classify'):
    """
        Requête au parser pour obtenir les informations contenues dans le message
    """
    msg = clean_msg_for_url(msg)
    to_classify = clean_msg_for_url(to_classify)
    try:
        data_in_sentence = requests.get(pythonconfig.api_parse + to_classify + '/' + msg)
        return data_in_sentence.json()
    except requests.RequestException as e:
        print(e)
    except Exception as e :
        print(e)


def http_date(msg : str):
    """
        Requête à Duckling pour récupérer les informations de date contenues dans le message
        (automatiquement appelée par le parser, inutile de l'appeler directement)
    """
    # date_in_sentence = requests.post(pythonconfig.api_dates, data = {'lang': 'fr', 'text': parse.quote(msg, safe='')})
    date_in_sentence = requests.post(pythonconfig.api_dates, data = {'lang': 'fr', 'text': msg})
    return date_in_sentence.json()

def http_bdd(user : dict):
    """
        Fonction pour aller enregistrer un utilisateur en base de données.
    """
    data = json.dumps(user)
    headers = {'Content-Type': 'application/json'}
    try :
        add_user = requests.post(pythonconfig.api_bdd, data = data, headers= headers)
        return add_user
    except requests.RequestException as e:
        print(e)
    except:
        print('Unexpected error')

def http_get_user(user_id : str):
    """
        Fonction pour aller chercher un utilisateur en base de données.
    """
    try :
        user_in_bdd = requests.get(pythonconfig.api_user+'/'+user_id)
        return user_in_bdd.json()
    except requests.RequestException as e:
        print(e)
    except:
        print('Unexpected error')


def http_delete(user_id : str):
    """
        Fonction pour supprimer un utilisateur de la base de données.
    """
    try :
        user_delete=requests.get(pythonconfig.api_delete+'/'+user_id)
        return user_delete
    except requests.RequestException as e:
        print(e)
    except:
        print('Unexpected error')


def clean_msg_for_url(msg):
    """
        Echappe les caractères problématiques pour les URL
    """
    msg = parse.quote_plus(msg)
    # remplacement des newline (%0A) par des espaces (+) :
    msg = re.sub('%0A', '+', msg)
    # suppression du slash en tete de string (fait bugger flask)
    msg = re.sub('^%2F', '+', msg)
    if msg == "":
        msg = "no_message"
    return msg
