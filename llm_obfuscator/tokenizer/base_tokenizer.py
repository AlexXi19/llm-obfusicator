from abc import ABC, abstractmethod

class BaseTokenizer(ABC):
    @abstractmethod
    def tokenize(self, text: str) -> list:
        pass

    @abstractmethod
    def detokenize(self, tokens: list) -> str:
        pass


