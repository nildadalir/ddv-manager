from abc import ABC, abstractmethod


class BaseImporter(ABC):

    def run(self):
        data = self.load()

        validated = [
            item
            for item in data
            if self.validate(item)
        ]

        transformed = [
            self.transform(item)
            for item in validated
        ]

        self.save(transformed)


    @abstractmethod
    def load(self):
        pass


    @abstractmethod
    def validate(self, item):
        pass


    @abstractmethod
    def transform(self, item):
        pass


    @abstractmethod
    def save(self, data):
        pass