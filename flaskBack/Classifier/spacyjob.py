"""
Ici on gère la vectorisation des phrases par SpaCy et le chargement du NLP
qui est un peu long
"""

import spacy
import numpy as np

print('Chargement du modèle SpaCy...')
nlp = spacy.load('fr')
print('Modèle SpaCy chargé')


def sentence_to_vector(sentence : str):
    """
        Transformation d'une phrase en vecteur de dimension 300 à l'aide de SpaCy
    """
    return nlp(sentence).vector


def line_to_vector(line):
    return np.reshape(line, (1, len(line)))

# Autre version de vectorisation de phrase, moins performante, qui somme
# simplement les tokens des différents mots :
#
# def sentence_to_vector(sentence : str):
#     sentence = nlp(sentence)
#     result = sentence[0].vector.astype(dtype = 'float64')
#     result=np.array(result)
#     for i in range(1, len(sentence)):
#         result += sentence[i].vector.astype(dtype='float64')
#     result = np.transpose(result)
#     return result
