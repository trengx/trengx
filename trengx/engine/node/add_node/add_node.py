from abc import ABC, abstractmethod

class AddNode(ABC):
    def __init__(self, driver, node):
        self.driver = driver
        self.node = node
        self.id = node['id']
        self.label = node['label']
        self.name = node['name']
        self.value = node['value']
        self.grad = node['grad']

    @abstractmethod
    def execute(self):
        pass
    



