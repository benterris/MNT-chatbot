"""
    Fichier de configuration avec les hôtels à Paris avec lesquels la MNT a des partenariats. 
"""

dict_hotel = {
    '1' : 'Hôtel Le Cardinal (3 rue du Cardinal Mercier, 75009 Paris)',
    '2' : 'Hôtel Villathéna (23 rue d’Athènes, 75009 Paris)',
    '3' : 'ATN Hôtel Opéra (21 rue d’Athènes, 75009 Paris)',
    '4' : 'Hôtel Monterosa (30 rue La Bruyère, 75009 Paris)',
    '5' : 'Hôtel Joyce (29 rue la Bruyère, 75009 Paris)',
    '6' : 'Hôtel Lorette (36 Rue Notre Dame de Lorette, 75009 Paris)',
    '7' : 'Timhotel Opera Blanche Fontaine (34 rue Pierre Fontaine, 75009 Paris)',
}

ville = ["départ", "arrivée"]
relevant_keys = ["départ", 'arrivée', 'date_arrivee', 'date_depart', 'villes_inconnues', 'dates_inconnues']
infos_needed = ["date_arrivee", "date_depart", "ville"]
status_ongoing = 'hotel'

sentences = {
    "favorite_hotel" : "Si vous avez une préférence entrez le numéro de l'hôtel correspondant. \n"
                        " Nous ferons le maximum pour vous satisfaire dans la limite des disponibilités. \n \n"
                        " Si vous n'avez pas de préférences, tapez 'oui' ou corrigez.",
    "out_of_paris_hotel" : "Excusez-moi, je ne gère pas la réservation d'hôtels en dehors de Paris. \n" \
                           " Entrez Paris ou annulez votre réservation.\nSi vous souhaitez un hôtel en dehors de Paris," \
                           " vous devez le réserver vous-même et faire une note de frais."
}

questions = {
        'ville' : "Où voulez-vous votre hôtel ?",
        'date_arrivee' : "Quand voulez-vous arriver à l'hôtel ?",
        'date_depart' : "Quand voulez-vous partir de l'hôtel ?"
}