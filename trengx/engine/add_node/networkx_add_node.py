from .add_node import AddNode

class NetworkXAddNode(AddNode):
    def add_to_graph(self):
        if not isinstance(self.label, str):
            raise TypeError('label must be a string')
        if not isinstance(self.id, str):
            raise TypeError('id must be a string')
        if not isinstance(self.name, str):
            raise TypeError('name must be a string')
        if not isinstance(self.grad, float):
            raise TypeError('grad must be a float')
        self.driver.add_node(self.id, label=self.label, name=self.name, value=self.value, grad=self.grad)