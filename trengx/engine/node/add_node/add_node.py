from abc import ABC, abstractmethod

class AddNode(ABC):
    def __init__(self, driver):
        self.driver = driver

    @abstractmethod
    def execute(self, node):
        pass
    



