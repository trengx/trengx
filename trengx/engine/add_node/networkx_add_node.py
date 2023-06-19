from .add_node import AddNode

class NetworkXAddNode(AddNode):
    def add_to_graph(self):
        self.driver.add_node(self.id, label=self.label, name=self.name, value=self.value, grad=self.grad)