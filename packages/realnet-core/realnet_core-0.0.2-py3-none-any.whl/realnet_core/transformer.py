from abc import ABC, abstractmethod


class Transformer(ABC):

    @abstractmethod
    def transform(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        return self.transform(args, kwargs)


class ItemTransformer(Transformer):

    def transform(self, *args, **kwargs):
        pass


class TypeTransformer(Transformer):

    def transform(self, *args, **kwargs):
        pass


class DataTransformer(Transformer):

    def transform(self, *args, **kwargs):
        pass