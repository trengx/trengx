import uuid

class AddNode:
    def __init__(self, driver, id=None, label=None, name=None, value=None, grad=None):
        self.driver = driver
        self.id = self._generate_unique_id(id)
        self.label = label
        self.name = name
        self.value = value
        self.grad = grad
        self.add_to_graph()

    def _generate_unique_id(self, id):
        if id is None:
            return str(uuid.uuid1())
        return id

    def add_to_graph(self):
        raise NotImplementedError("add_to_graph method must be implemented in a subclass.")
    
    def __str__(self):
        return f"Node(id={self.id}, label={self.label}, name={self.name}, value={self.value}, grad={self.grad})"



