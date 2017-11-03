"""
Ici on trouve les fonctions relatives au parsing des villes, principalement
utilisées par Parser_general.parse
"""
import unidecode
import re
from pythonconfig import gares_json_path
import json

def get_city_dict(message, cities):
    """
        Seule fonction appelée depuis l'extérieur
        Renvoie un dictionnaire avec toutes les informations sur les villes
        contenues dans le message
        {
            'départ' : ville de départ,
            'arrivée' : ville d'arrivée,
            'villes_inconnues' : tableau de noms de villes qu'on n'a pas su
                                    classer entre départ et arrivée
        }
    """
    res = {}
    unknown_cities = []

    # recherche parmi les villes de celles auxquelles on peut attribuer clairement un label origine/destination
    for city in cities:
        pDepart = re.search('(de |depuis )' + simplify(city), simplify(message))
        pArrivee = re.search('(vers |a |à |pour )' + simplify(city), simplify(message))

        if pDepart:
            res['départ'] = city
        elif pArrivee:
            res['arrivée'] = city
        else:
            unknown_cities.append(city)

    # si on n'a pas pu classer les villes mais qu'on en a trouvé 2, on donne le label "depart" à la première du message et "arrivee" à la seconde
    if len(unknown_cities) == 2 and not res.get('départ') and not res.get('arrivée') :
        res['départ'] = unknown_cities.pop(0)
        res['arrivée'] = unknown_cities.pop(0)

    if unknown_cities:
        res['villes_inconnues'] = unknown_cities
    return res

def search_cities(message):
    """
        Renvoie les noms de villes contenus dans message.
        Dans le cas de plusieurs villes qui sont des sous-chaînes les unes des
        autres (i.e. lyon inclus dans paris gare de lyon), on prend la plus grande
        présente dans le message
    """
    cities = []
    # recherche des villes dans le fichier de villes
    for x in L:
        # on ne cherche que des mots entiers i.e. entre espaces ou au début ou à la fin de string
        p = re.search('(.*\s|^)' + simplify(x) + '(\s.*|$)', simplify(message))
        if p:
            cities.append(x)

    # Nettoyage : on enlève les villes dont les noms sont des substrings d'autres villes
    # (les villes matchées au noms les + longs sont les plus pertinentes)
    cities = list(set(cities))
    for x in cities:
        for y in cities:
            if x != y:
                xSimple = simplify(x)
                ySimple = simplify(y)
                if xSimple in ySimple:
                    cities.remove(x)
                elif ySimple in xSimple:
                    cities.remove(y)

    # trier les villes du tableau par ordre d'apparition
    def indexSort(s):
        return simplify(message).index(simplify(s))
    cities.sort(key=indexSort)

    return cities


def simplify(s):
    """Enlève les accents, majuscules et tirets d'une string"""
    s = unidecode.unidecode(s).lower().replace('-', ' ')
    return s


def load_cities():
    """Chargement des noms de villes à partir du fichier"""
    with open(gares_json_path) as f:
        data = json.load(f)
        R = []
        for x in data:
            commune = x.get('fields').get('commune')
            if commune :
                R.append(commune)
        # on supprime les duplicata dûs aux villes à plusieurs gares
        R = list(set(R))
    return R

L = load_cities()
