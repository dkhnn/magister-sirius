from abc import ABC, abstractmethod


class Handler(ABC):
    def __init__(self):
        self.pattern = ""

    @abstractmethod
    def handler():
        raise NotImplementedError("handler method not implemented")
