from abc import ABC, abstractmethod

class AbstractConv(ABC):

    @abstractmethod
    def response(self, infos_in_message : dict, message : str):
        pass
