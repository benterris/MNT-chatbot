import unittest
import Parser_general.parser_city
import Parser_general.parse
import Parser_general.parser_time as pt
import http_helper

class TestParser(unittest.TestCase):

    def test_find_city(self):
        self.assertEqual(Parser_general.parser_city.search_cities('Je voudrais un train Paris Marseille'), ['Paris', 'Marseille'])

    def test_set_entities_label(self):
        message = 'Je voudrais un train pour Paris depuis Marseille'
        expected = {'départ': 'Marseille', 'arrivée': 'Paris', 'villes_inconnues': []}
        self.assertEqual(Parser_general.parse.parse_message(message, 'not_classify'), expected)

    def test_grain(self):
        def extract_time_data(req_data):
            for data in req_data:
                if data['dim'] == 'time':
                    return data
            return None

        self.assertEqual(['day'], pt.select_grain(extract_time_data(http_helper.http_date('demain'))))
        # self.assertEqual(['day'], pt.select_grain(extract_time_data(http_helper.http_date('dans 2 jours'))))
        self.assertEqual(['day'], pt.select_grain(extract_time_data(http_helper.http_date('après-demain'))))
        self.assertEqual(['day'], pt.select_grain(extract_time_data(http_helper.http_date('le 6 décembre'))))
        self.assertEqual(['hour'], pt.select_grain(extract_time_data(http_helper.http_date('dans 2h'))))
        self.assertEqual(['hour'], pt.select_grain(extract_time_data(http_helper.http_date('à 9h'))))
        self.assertEqual(['hour'], pt.select_grain(extract_time_data(http_helper.http_date('18h'))))
        self.assertEqual(['hour'], pt.select_grain(extract_time_data(http_helper.http_date('à midi'))))
        self.assertEqual(['hour'], pt.select_grain(extract_time_data(http_helper.http_date('à minuit'))))
        self.assertEqual(['hour'], pt.select_grain(extract_time_data(http_helper.http_date('à quatre heures'))))
        self.assertEqual(['day', 'hour'], pt.select_grain(extract_time_data(http_helper.http_date('demain à 19h'))))
        self.assertEqual(['day', 'hour'], pt.select_grain(extract_time_data(http_helper.http_date('le 15/10 à 18h'))))
        self.assertEqual(['day', 'hour'], pt.select_grain(extract_time_data(http_helper.http_date('le 15/10/2018 à 18h'))))
        self.assertEqual(['day', 'hour'], pt.select_grain(extract_time_data(http_helper.http_date('vendredi à 9h02'))))
        self.assertEqual(['day', 'hour'], pt.select_grain(extract_time_data(http_helper.http_date('vendredi à 21h02'))))
