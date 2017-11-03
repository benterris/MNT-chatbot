"""
    Script utilisé pour l'entraînement du bot.
    Doit être lancé lorsqu'on modifie les données d'entraînement, pour renouveller
    le classifier.
"""

import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.externals import joblib
import Classifier.spacyjob
import pythonconfig
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.svm import SVC
from Parser_general.parser_city import simplify


def setData():
    data = [];
    for path in data_paths:
        with open(path, 'r') as f:
            data_i = f.readlines()
            f.close()
        data_i = [sentence.strip() for sentence in data_i]
        data.append(data_i)
    return data

data = setData()


Xtrain = np.array([Classifier.spacyjob.sentence_to_vector("A plus")])
classes = ['aurevoir', 'blague','bonjour','capacites', 'etat', 'fort', 'hotel', 'mauvais','merci', 'meteo', 'personnal_infos','train', 'vpn']
ytrain =[classes[0]]
j = 0

for class_set in data:

    for example in class_set:
        Xtrain = np.vstack((Xtrain, Classifier.spacyjob.sentence_to_vector(simplify(example))))
        ytrain.append(classes[j])
    j += 1

ytrain = np.array(ytrain)


print('Entrainement du classifier...')
clf = SVC(kernel='linear', C=0.025, probability=True)
clf.fit(Xtrain, ytrain)
print('Classifier entraîné.')
joblib.dump(clf, pythonconfig.botfile)
