"""
Script de comparaison des performances des différents types de classifiers
sur nos données. Il est optionnel et peut être lancé à titre informatif, pour
améliorer les capacités de reconnaissances du bot.
"""
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

import numpy as np
from sklearn.externals import joblib
import Classifier.spacyjob
import pythonconfig


h = .02  # step size in the mesh

# Type de classifiers utilisables
# classifiers = [
#     KNeighborsClassifier(3),
#     KNeighborsClassifier(5),
#     KNeighborsClassifier(11),
#     SVC(kernel="linear", C=0.025),
#     SVC(kernel="linear", C=0.1),
#     SVC(kernel="linear", C=0.1),
#     SVC(gamma=2, C=1),
#     GaussianProcessClassifier(1.0 * RBF(1.0), warm_start=True),
#     DecisionTreeClassifier(max_depth=5),
#     RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
#     MLPClassifier(alpha=1, max_iter=800),
#     AdaBoostClassifier(),
#     GaussianNB(),
#     QuadraticDiscriminantAnalysis()]

classifiers = [
    SVC(kernel="linear", C=0.025, probability=True),
    SVC(kernel="linear", C=0.1),
    SVC(kernel="linear", C=0.5),
    SVC(kernel="linear", C=1)
]



X, y = make_classification(n_features=2, n_redundant=0, n_informative=2,
                           random_state=1, n_clusters_per_class=1)
rng = np.random.RandomState(2)
X += 2 * rng.uniform(size=X.shape)
linearly_separable = (X, y)

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
        Xtrain = np.vstack((Xtrain, Classifier.spacyjob.sentence_to_vector(example)))
        ytrain.append(classes[j])
    j += 1

ytrain = np.array(ytrain)


ourSet = (Xtrain, ytrain)
datasets = [ourSet]


for ds_cnt, ds in enumerate(datasets):
    X, y = ds
    X = StandardScaler().fit_transform(X)
    X_train, X_test, y_train, y_test = \
        train_test_split(X, y, test_size=.4, random_state=42)
    for clf in classifiers:
        clf.fit(X_train, y_train)
        score = clf.score(X_test, y_test)
        print(str(clf) + ' \n' + str(score) + '\n\n')
