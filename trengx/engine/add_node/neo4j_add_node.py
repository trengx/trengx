from .add_node import AddNode
class Neo4jAddNode(AddNode):
    def add_to_graph(self):
        if not isinstance(self.label, str):
            raise TypeError('label must be a string')
        if not isinstance(self.id, str):
            raise TypeError('id must be a string')
        if not isinstance(self.name, str):
            raise TypeError('name must be a string')
        if not isinstance(self.grad, float):
            raise TypeError('grad must be a float')
        with self.driver.session() as session:
            session.run(f"CREATE (:{self.label} {{id: $id, name: $name, value: $value, grad: $grad}})",
                        id=self.id, name=self.name, value=self.value, grad=self.grad)