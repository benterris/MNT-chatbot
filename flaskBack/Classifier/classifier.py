"""
Ici on classifie les intentions des phrases de l'utilisateur
"""

import Classifier.spacyjob as spacyjob
from sklearn.externals import joblib
import pythonconfig

clf = joblib.load(pythonconfig.botfile)
minCertitudeRelative = .7
smallTalk = ['aurevoir', 'blague', 'bonjour', 'capacites', 'etat', 'fort', 'mauvais', 'merci']

def classify(testSentence):
    """
        Renvoie l'intention de testSentence (parmi ['aurevoir', 'blague','bonjour','capacites',
        'etat', 'fort', 'hotel', 'mauvais','merci', 'meteo', 'personnal_infos','train', 'vpn']) ou 'not_sure' si
        la probabilité d'avoir bien classifié l'intention est inférieure à maxCertitude
    """


    # Vectorisation de la phrase à tester en un vecteur de dimension 300
    vec = spacyjob.sentence_to_vector(testSentence)


    # Classification du vecteur dans l'une des classes ci-dessus à l'aide du classifier entraîné
    probas = clf.predict_proba(spacyjob.line_to_vector(vec))
    predict = clf.predict(spacyjob.line_to_vector(vec))[0]
    print('Phrase reçue : ' + testSentence + ', intent détecté : ' + predict)


    #On cherche si l'intent le plus probable est suffisamment loin du second plus probable
    listProbas = list(probas[0])
    # Probabilité de l'intent le plus probable
    max1 = max(listProbas)
    listProbas.remove(max1)
    # Probabilité du second plus probable
    max2 = max(listProbas)

    # Les deux intents les plus probables doivent être suffisamment distincts
    # i.e. leur écart relatif doit être supérieur à minCertitudeRelative
    if (max1 - max2)/max1 < minCertitudeRelative:
        print('Intention trop incertaine')
        return 'not_sure'
    return predict
