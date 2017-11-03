"""
Ce fichier rassemble diverses fonctions utiles pour les conversations
"""
import re
from datetime import datetime, timedelta

def check_format(data, stringFormat):
    """
        vérifie que la string 'data' est bien formatée selon 'format'
        formats disponibles : 'mail', 'telephone', 'date_de_naissance'
    """
    patterns = {
        'mail': "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
        'telephone': "^(0[0-9]{9}|(\+|00)33[0-9]{9}|(0[0-9]\.([0-9]{2}\.){3}[0-9]{2}))$"
    }


    if stringFormat == 'date_de_naissance':
        try :
            date = datetime.strptime(data, "%d/%m/%Y")
            return date > datetime.strptime("01/01/1920", "%d/%m/%Y") and date < datetime.strptime("01/01/2005", "%d/%m/%Y")
        except ValueError :
            return False
    elif stringFormat in patterns.keys():
        return bool(re.search(patterns[stringFormat], data))
    return True

def check_string(message : str):
    """
        Vérifie qu'on n'a pas une string vide ou seulement constituée de
        caractères spéciaux
        Utilisé pour vérifier que les utilisateurs rentrent bien un motif.
    """
    return bool(re.search("[A-Za-z0-9_]", message))

def check_coherent_voyage(voyage : dict):
    """
        Renvoie la liste des problèmes rencontrés dans voyage, ou la liste vide s'il n'y a pas de problème.
        Data de la forme {'aller' : {'ville': 'Paris', 'date_arrivee': '12/10/2017', 'date_depart': '18/10/2017'}, 'retour' : idem... }
    """
    errors = []
    if 'aller' in voyage.keys() and 'retour' in voyage.keys() :
        # retour avant départ
        dateAller = parse_time_day_only(voyage['aller']['jour'])
        dateRetour = parse_time_day_only(voyage['retour']['jour'])
        if not is_before_tolerant(dateAller, dateRetour):
            errors.append("L'aller doit avoir lieu avant le retour")
    return errors



def check_coherent_hotel(data):
    """
        Renvoie la liste des problèmes rencontrés dans data, ou la liste vide s'il n'y a pas de problème.
        Data de la forme {'ville': 'Paris', 'date_arrivee': '12/10/2017', 'date_depart': '18/10/2017'}
    """
    errors = []
    dateArrivee = parse_time_day_only(data['date_arrivee'])
    dateDepart = parse_time_day_only(data['date_depart'])

    # On verifie que la date n'est pas dans le passé
    if not is_before_tolerant(datetime.today(), dateArrivee):
        errors.append("Vous avez choisi une date d'arrivée dans le passé")
    # On vérifie que la date arrivée est bien après date départ
    if dateArrivee > dateDepart or are_within_same_day(dateDepart, dateArrivee) :
        errors.append("La date d'arrivée doit être au moins la veille de la date de départ")
    return errors



def check_coherent_train(data, voyage):
    """
        Renvoie la liste des problèmes rencontrés dans data, ou la liste vide s'il n'y a pas de problème.
        Data de la forme {'départ': 'Paris', 'arrivée': 'Lyon', 'jour': '25/10/2017', 'heure': '16h00'}
    """
    # On vérifie que le départ et l'arrivée sont deux lieux distincts
    errors = []
    if data['départ'] == data['arrivée']:
        errors.append("Vous avez choisi la même ville de départ et d'arrivée")

    if 'aller' in voyage.keys() and 'jour' in data.keys():
        # retour avant départ
        dateAller = parse_time_day_only(voyage['aller']['jour'])
        dateRetour = parse_time_day_only(data['jour'])
        if not is_before_tolerant(dateAller, dateRetour):
            errors.append("L'aller doit avoir lieu avant le retour (date aller : " + voyage['aller']['jour'] +')')


    date = parse_time_day_only(data['jour'])
    # oneDay = timedelta(days=1)
    # On vérifie que la date est bien dans le futur
    if not is_before_tolerant(datetime.today(), date):
        errors.append("Vous avez choisi une date dans le passé")
    return errors


def parse_time_day_only(day):
    """
        Renvoie un objet datetime à partir d'une string de la forme 'JJ/MM/AAAA'
    """
    date = datetime.strptime(day, '%d/%m/%Y')
    return date


def parse_time_with_hour(timeData):
    """
        Renvoie un objet datetime à partir de [day, hour] ou juste [day],
        avec les formats :
        day : 'JJ/MM/AAAA'
        hour : 'HHhMM'
    """
    day = timeData[0]
    hour = timeData[1] if len(timeData) == 2 else '00h00'
    date = datetime.strptime(day + 'T' + hour, '%d/%m/%YT%Hh%M')
    return date

def are_within_same_day(date1, date2):
    """Renvoie True si date1 et date2 sont dans la même journée"""
    return date1.year == date2.year and date1.month == date2.month and date1.day == date2.day

def is_before_tolerant(date1, date2):
    """
        Renvoie True si date1 < date2 ou si date1 et date2 sont le même jour
    """
    return date1 < date2 or are_within_same_day(date1, date2)

def hotel_number_nights(dateArrivee, dateDepart):
    """
        Renvoie le nombre de nuitées en fonction des dates arrivée et départ (au format 'JJ/MM/AAAA')
    """
    dArrivee = datetime.strptime(dateArrivee, '%d/%m/%Y')
    dDepart = datetime.strptime(dateDepart, '%d/%m/%Y')
    duration = dDepart - dArrivee

    return duration.days

def string_recap(data):
    """
        Renvoie une string récapitulative des informations du voyage
    """
    res = ""
    if 'aller' in data.keys():
        res += "Aller :\n"
        aller = data.get('aller')
        if 'départ' in aller.keys() and 'arrivée' in aller.keys() and 'jour' in aller.keys():
            res += "De " + aller.get('départ') + " à " + aller.get('arrivée') + " le " + aller.get('jour')
        if 'heure' in aller.keys():
            res += " à " + aller.get('heure') +'\n'
        res += "\n"
    if 'retour' in data.keys():
        res += "Retour :\n"
        retour = data.get('retour')
        if 'départ' in retour.keys() and 'arrivée' in retour.keys() and 'jour' in retour.keys():
            res += "De " + retour.get('départ') + " à " + retour.get('arrivée') + " le " + retour.get('jour')
        if 'heure' in retour.keys():
            res += " à " + retour.get('heure') + '\n'
        res += "\n"
    if 'hotel' in data.keys():
        res += "Hôtel :\n"
        hotel = data.get('hotel')
        if 'ville' in hotel.keys() and 'date_arrivee' in hotel.keys() and 'date_depart' in hotel.keys():
            res += "À " + hotel.get('ville') + " du " + hotel.get('date_arrivee') + ' au ' + hotel.get('date_depart') + '\n'
            if 'hotel_wanted' in hotel.keys():
                res += 'Hôtel souhaité : ' + hotel.get('hotel_wanted') +'\n'
        res+='\n'
    if 'voyageurs' in data.keys():
        res += 'Voyageurs :\n\n'
        for voyageur in data['voyageurs']:
            res += 'Prénom : ' + voyageur.get('prenom') + '\n'
            res += 'Nom : ' + voyageur.get('nom') + '\n'
            res += 'E-mail : ' + voyageur.get('mail') + '\n'
            # res += 'Numéro de téléphone : ' + voyageur.get('telephone') + '\n'
            # res += 'Statut : ' + voyageur.get('statut') + '\n'
            # res += 'Lieu de travail : ' + voyageur.get('lieu_de_travail') + '\n'
            # res += 'Section ou service : ' + voyageur.get('section_service') + '\n'
            res += 'Date de naissance : ' + voyageur.get('date_de_naissance') + '\n'
            res += 'Grand Voyageur : ' + voyageur.get('grand_voyageur') + '\n'
            res += 'Carte de réduction : ' + voyageur.get('reductions') + '\n'
            res+= '\n'
        res+='\n'
    if 'motif' in data.keys():
        res += "Motif : "
        motif = data.get('motif')
        res += motif
        res += "\n"
    if 'commentaires' in data.keys():
        res += "Commentaires : "
        commentaires = data.get('commentaires')
        res += commentaires
        res += "\n"
    return res


def string_list(items):
    """
        renvoie la string "item1, item2, item3" etc. à partir du tableau [item1, item2, item3] etc.
    """
    res = ""
    for item in items:
        res += item + ", "
    return res[:-2]

def proposition_trains(data):
    """
    Si data == None (ie le cas oul'api sncf ne fonctionne pas) alors on renvoie un message
    informant l'utilisateur
        data = [{
            'nbre_transferts' : nbre_transferts,
            'duration' : duration,
            'depature_date' : depature_date,
            'depature_time' : depature_time,
            "arrival_date" : arrival_date,
            "arrival_time": arrival_time
        }, {...} ...]
        Renvoie une string formatée qui propose les différents trains
    """
    res = ''
    if not data :
        return res
    for i, train in enumerate(data):
        res += str(i + 1) + '. ' + train['departure_date'] + ' : ' +  train['departure_time'] + ' -> ' + train['arrival_time'] + '\n'
        res += '    Durée : ' + train['duration'] + ', avec ' + train['nbre_transferts'] + ' correspondance(s)\n'
    return res



def check_for_relevant_infos(infos_in_message : dict, relevant_keys : []):
    keys = infos_in_message.keys()
    for key in keys:
        if key in relevant_keys:
            return True
    return False

# EXEMPLES DE FORMATS DE DONNEES :
# {'aller': {'départ': 'Paris', 'arrivée': 'Brest', 'jour': '10/10/2017'}, 'retour': {'départ': 'Brest', 'arrivée': 'Paris', 'jour': '11/10/2017'}}
# {'départ': 'Paris', 'arrivée': 'Lyon', 'jour': '25/10/2017', 'heure': '16h00'}
# {'hotel': {'ville': 'Reims', 'date_arrivee': '27/10/2017', 'date_depart': '28/10/2017'}}
