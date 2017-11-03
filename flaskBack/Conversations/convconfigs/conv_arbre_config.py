questions_vpn = {
    '1' : 'Avez-vous un poste de travail fourni par la MNT ? oui/non',
    '2' : "Avez-vous une clef RSA ? oui/non",
    '3' : "Voyez vous l'icône suivant ? oui/non *description icône*",
    '4' : "Contactez le SVP au 09 69 36 87 81",
    '5' : "Connectez-vous sur https://accesmnt.mnt.fr \n Avez-vous réussi à vous connecter ? oui/non",
    '6' : "Connectez vous sur https://acces.mnt.fr \n Avez-vous réussi à vous connecter ? oui/non",
    '7' : "Lisez la procédure qui se trouve ici sur votre poste de travail \n Avez-vous réussi à vous connecter ? oui/non",
    '8' : "Être utile est un beau métier !"
}

starting_question = {
    'vpn': questions_vpn['1']
}
ending_questions = {
    '1' : "Être utile est un beau métier !",
    '2' : "Contactez le SVP au 09 69 36 87 81"
}

tree_vpn = {
    questions_vpn['1'] : {'oui' : questions_vpn['3'],
                      'non' : questions_vpn['2']
                          },
    questions_vpn['2'] : {'oui' : questions_vpn['5'],
                      'non' : questions_vpn['6']
                          },
    questions_vpn['3'] : {'oui' : questions_vpn['7'],
                      'non' : ending_questions['2']
                          },
    questions_vpn['5'] : {'oui' : ending_questions['1'] , 'non' : ending_questions['2']},
    questions_vpn['6'] : {'oui' : ending_questions['1'] , 'non' : ending_questions['2']},
    questions_vpn['7'] : {'oui' : ending_questions['1'] , 'non' : ending_questions['2']},
}

possible_classes = {
    'vpn' : tree_vpn
}