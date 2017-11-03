
def set_sentence_for_self_user(user):
    return 'Bienvenue, ' + user['prenom'] + ' ' + user['nom']

def set_sentence_for_other_traveler(user):
    return user['prenom'] + ' ' + user['nom'] + ' a bien été ajouté(e) au voyage'

def set_sentence_for_user_not_found_first(message):
    return "Nous n'avons pas trouvé l'email " + message + " en base de données." \
            " Est-il tapé correctement ? Vous pouvez entrer 'oui', ou bien le corriger."

def set_sentence_for_user_not_found_second(message):
    return "Nous n'avons pas non plus trouvé l'email " + message +\
            ". Entrez 'suivant' pour créer un compte, ou bien corrigez l'email ci-dessus."

def set_sentence_for_account_creation(mail):
    return "Nous allons créer un compte pour l'email " + mail

sentences_self = {
    'first_question' : 'Pour commencer, entrez votre adresse mail :',
    'user_found' : set_sentence_for_self_user,
    'user_not_found_first' : set_sentence_for_user_not_found_first,
    'user_not_found_second' :set_sentence_for_user_not_found_second,
    'wrong_mail' : "Votre email semble mal tapé, veuillez l'écrire à nouveau",
    'wrong_format': "Votre réponse n'a pas le format requis. Veuillez la corriger :",
    'account_creation' : set_sentence_for_account_creation,
    'validate' : 'Ok, vos informations ont bien été enregistrées dans la base de données.'
                 ' Je m\'en souviendrai pour la prochaine fois ',
    'questions' :{
        'prenom' : "Entrez votre prénom :",
        'nom' : "Entrez votre nom :",
        'statut' : "Etes-vous un salarié ou un administrateur ?",
        'lieu_de_travail' : "Entrez votre lieu de travail :",
        'section_service' : "Entrez votre section ou service :",
        'mail' : "Entrez votre e-mail :",
        "telephone" : "Entrez votre numéro de téléphone :",
        'date_de_naissance' : "Entrez votre date de naissance (au format JJ/MM/AAAA) :",
        'grand_voyageur' : "Avez-vous une carte grand voyageur SNCF ? "
                           "Si oui entrez directement le numéro de votre carte.",
        'reductions' : "Avez-vous une carte de réduction SNCF (autre que grand voyageur) ? "
                       "Si oui entrez directement la référence :"
    }
}

sentences_traveler = {
    'first_question' : "Veuillez entrer l'adresse mail du voyageur",
    'user_found' : set_sentence_for_other_traveler,
    'user_not_found_first' : set_sentence_for_user_not_found_first,
    'user_not_found_second': set_sentence_for_user_not_found_second,
    'wrong_mail' : "l'adresse mail semble mal tapée, veuillez l'écrire à nouveau",
    'wrong_format' : "Votre réponse n'a pas le format requis. Veuillez la corriger :",
    'account_creation' : set_sentence_for_account_creation,
    'validate' : 'Ok, ces informations ont bien été enregistrées dans la base de données. '
                 'Je m\'en souviendrai pour la prochaine fois ',
    'questions' : {
        'prenom' : "Entrez le prénom du voyageur :",
        'nom' : "Entrez le nom du voyageur :",
        'statut' : "le voyageur est-il un salarié ou un administrateur ?",
        'lieu_de_travail' : "Entrez le lieu de travail du voyageur :",
        'section_service' : "Entrez la section ou service du voyageur :",
        'mail' : "Entrez l'e-mail du voyageur :",
        "telephone" : "Entrez le numéro de téléphone du voyageur :",
        'date_de_naissance' : "Entrez la date de naissance du voyageur (au format JJ/MM/AAAA) :",
        'grand_voyageur' : " Le voyageur a-t-il une carte grand voyageur SNCF ? "
                           "Si oui entrez directement le numéro de la carte.",
        'reductions' : "Le voyageur a-t-il une carte de réduction SNCF (autre que grand voyageur)"
                       " ? Si oui entrez directement la référence :"
    }
}
