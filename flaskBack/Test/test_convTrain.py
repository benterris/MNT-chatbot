from unittest import TestCase
from Conversations.conv_train import ConvTrain


class TestConvTrain(TestCase):
    infos_given = []
    infos_given.append({'villes inconnues':[]})
    infos_given.append({'villes inconnues': ['Ville1']})
    infos_given.append({'villes inconnues': [], "départ": 'Ville1'})
    infos_given.append({'villes inconnues': [], 'arrivée' : "Ville2"})
    infos_given.append({'villes inconnues': ['Ville1', 'Ville2'], 'départ': '', 'arrivée': ''})
    infos_given.append({'villes inconnues':['Ville1'], 'départ':'Ville2', 'arrivée': ''})
    infos_given.append({'villes inconnues': ['Ville1'], 'arrivée' : 'Ville2'})
    infos_given.append({'villes inconnues':[], 'départ':'Ville1', 'arrivée': 'Ville2'})
    infos_given.append({'villes inconnues':['Ville1', 'Ville2', 'Ville3']})
    infos_given.append({'villes inconnues': ['Ville1', 'Ville2'], "départ":"Ville3"})
    infos_given.append({'villes inconnues': ['Ville1', 'Ville2'], 'arrivée': 'Ville3'})
    infos_given.append({'villes inconnues': ['Ville1'], 'départ' : 'Ville2', 'arrivée':'Ville3'})
    infos_given.append({'villes inconnues': ['Ville1', 'Ville2', 'Ville3', 'Ville4']})
    infos_given.append({'villes inconnues': ['Ville1', 'Ville2', 'Ville3'], 'départ':'Ville4'})
    infos_given.append({'villes inconnues': ['Ville1', 'Ville2', 'Ville3'], 'arrivée': 'Ville4'})
    infos_given.append({'villes inconnues': ['Ville1', 'Ville2'], 'arrivée' : 'Ville3', 'départ': 'Ville4'})

    infos_needed = []
    infos_needed.append(['départ', 'arrivée'])
    infos_needed.append(["départ"])
    infos_needed.append(["arrivée"])

    infos_asked = []
    infos_asked.append(None)
    infos_asked.append("départ")
    infos_asked.append("arrivée")

    infos = []
    infos.append({})
    infos.append({"départ": "Ville1"})
    infos.append({"arrivée" : "Ville1"})
    infos.append({"départ" : "Ville1", "arrivée" : 'Ville2'})

    test_cases = []
    for i in range(len(infos_needed)):
        for j in range(len(infos_asked)):
            for k in range(len(infos)):
                test_cases.append({'infos_needed':infos_needed[i], 'infos_asked': infos_asked[j], 'infos':infos[k]})

    # def test_response_if_city_known(self):
    #     self.fail()
    #
    # def test_reponse_if_unknown_city(self):
    #     self.fail()

    def test_response_for_cities(self):
        conversation = ConvTrain()
        for case in self.test_cases:
            conversation.__init__()
            conversation.infos_needed = case.get('infos_needed')
            conversation.infos = case.get('infos')
            conversation.info_asked = case.get('infos_asked')
            for info_given_case in self.infos_given:
                with self.subTest(msg = "Etat du test echoué : " + str(case) +"\ninfos données : " + str(info_given_case)):
                    conversation.infos_given_to_infos(info_given_case)
                    keys = ["départ", "arrivée"]
                    for key in keys:
                        if info_given_case.get(key):
                            self.assertNotIn(key, conversation.infos_needed, "Problème 1")
                            self.assertEqual(conversation.infos.get(key),info_given_case.get(key), "Problème 2")
