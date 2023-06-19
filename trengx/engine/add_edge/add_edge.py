import uuid

class AddEdge:
    def __init__(self, driver, node1, node2, id=None, label=None, second_operand=None):
        self.driver = driver
        self.node1 = node1
        self.node2 = node2
        self.id = self._generate_unique_id(id)
        self.label = label
        self.second_operand = second_operand
        self.add_to_graph()

    def _generate_unique_id(self, id):
        if id is None:
            return str(uuid.uuid1())
        return id

    def add_to_graph(self):
        raise NotImplementedError("add_to_graph method must be implemented in a subclass.")
    
    def __str__(self):
        return f"Edge(id={self.id}, node1={self.node1}, node2={self.node2}, label={self.label}, second_operand={self.second_operand})"




