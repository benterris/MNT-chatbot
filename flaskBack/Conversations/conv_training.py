# TODO: a supprimer ?

import pythonconfig

class ConvTraining :

    status_ongoing = "training"
    status_finished = None

    def __init__(self, handler, classe):
        self.training_status = 0
        self.status = self.status_ongoing




    def write_data(self, path, sentence):
        with open(path, 'a') as f:
            f.write('\n'+sentence)
            f.close()


    def response(self, message : str, infos_in_message : dict): #a revoir
        return 'a revoir'
        # if self.training_status == 0 :
        #     self.training_status = 1
        #     self.status = self.status_ongoing
        #     return "Tu vas me donner des phrases pour arréter dis moi 'fin' \nCommene par des phrases pour prendre un train "
        # elif self.training_status == 1 :
        #     if message.lower() != "fin" and message.lower()!="suite":
        #         cities = parser_city.search_cities(message)
        #         for city in cities:
        #             index = parser_city.simplify(message).index(parser_city.simplify(city))
        #             message = message[:index] + "ville" + message[index + len(city):]
        #         self.write_data(pythonconfig.training_data_train_path, message)
        #         self.status = self.status_ongoing
        #         return "Ok encore ! \nsi tu n'as plus d'idée tu peux entrer 'suite'"
        #     elif message.lower() == "suite":
        #         self.training_status = 2
        #         self.status = self.status_ongoing
        #         return "Ok on va passer aux phrases de Bonjour \n entre tes phrases"
        #     else:
        #         self.training_status = 0
        #         self.status = self.status_finished
        #         return "Ok on a fini"
        # elif self.training_status == 2:
        #     if message.lower() != "fin" and message.lower()!="suite":
        #         self.write_data(pythonconfig.training_data_bonjour_path, message)
        #         self.status = self.status_ongoing
        #         return "Ok encore ! \nsi tu n'as plus d'idée tu peux entrer 'fin'"
        #     elif message.lower() == "suite":
        #         self.training_status = 2
        #         self.status = self.status_ongoing
        #         return "Ok on va passer aux phrases de Bonjour"
        #     else:
        #         self.training_status = 0
        #         self.status = self.status_finished
        #         return "Ok on a fini"
