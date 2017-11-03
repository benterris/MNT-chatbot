# On suppose que le cwd est à la racine :
training_data_aurevoir_path = "Data/Entrainement/aurevoir"
training_data_blague_path = "Data/Entrainement/blague"
training_data_bonjour_path = "Data/Entrainement/bonjour"
training_data_capacites_path = "Data/Entrainement/capacites"
training_data_etat_path = "Data/Entrainement/etat"
training_data_fort_path = "Data/Entrainement/fort"
training_data_hotel_path = "Data/Entrainement/hotel"
training_data_mauvais_path = "Data/Entrainement/mauvais"
training_data_merci_path = "Data/Entrainement/merci"
training_data_meteo_path = "Data/Entrainement/meteo"
training_data_personnal_infos_path = "Data/Entrainement/personnal_infos"
training_data_train_path = "Data/Entrainement/train"
training_data_vpn_path = "Data/Entrainement/vpn"

training_data_train_clean_path = "Data/Entrainement/train_clean"
# cities_list_path = "Data/liste_villes.txt"
gares_json_path = "Data/gares.json"

botfile = "Classifier/nnclassifier.pkl"

"""
    Data_paths pour l'entrainement du bot
"""
data_paths = [training_data_aurevoir_path,
    training_data_blague_path,
    training_data_bonjour_path,
    training_data_capacites_path,
    training_data_etat_path,
    training_data_fort_path,
    training_data_hotel_path,
    training_data_mauvais_path,
    training_data_merci_path,
    training_data_meteo_path,
    training_data_personnal_infos_path,
    training_data_train_path,
    training_data_vpn_path]

"""
    URL utilisée pour les requêtes HTTP (cf. http_helper)
"""
api_url = 'http://localhost:5000'
api_classify = api_url +'/classify/'
api_parse = api_url + '/parser/'
api_dates = 'http://localhost:8000/parse'
api_bdd = api_url + '/add_bdd'
api_user = api_url + '/users'
api_modify = api_url + '/user_modify'
api_delete = api_url + '/delete_bdd'


"""
    Token pour utiliser l'API SNCF.
"""
token_sncf = "9bbf8d47-bc30-4fb0-b544-43ee74f5c85d"
url_sncf_journeys = 'https://api.sncf.com/v1/coverage/sncf/journeys'

"""
    Données pour utiliser l'API météo : Darksky.
"""
api_key = '4800bc96c5b1d4ad0e21ee57aac84084'
api_adress = 'https://api.darksky.net/forecast/'


"""
    Donnée utilisée pour l'envoi du mail.
"""
adressfrom = 'chatbot.projetDTY@gmail.com'
mot_de_passe = 'testtesttest'
cc = ['chatbot.projetDTY@gmail.com']
