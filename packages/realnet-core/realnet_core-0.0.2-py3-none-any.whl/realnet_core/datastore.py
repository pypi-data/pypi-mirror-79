from abc import ABC, abstractmethod


class DataStore(ABC):

    @abstractmethod
    def put_data(self, id, data):
        pass

    @abstractmethod
    def get_data(self, id):
        pass

    @abstractmethod
    def delete_data(self, id):
        pass

