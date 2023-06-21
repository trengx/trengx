from abc import ABC, abstractmethod

class AddEdge(ABC):
    def __init__(self, driver):
        self.driver = driver

    @abstractmethod
    def execute(self, edge):
        pass
    
    





