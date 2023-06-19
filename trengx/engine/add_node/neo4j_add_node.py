from .add_node import AddNode
class Neo4jAddNode(AddNode):
    def add_to_graph(self):
        if type(self.id) is not str:
            self.id = str(self.id)
        with self.driver.session() as session:
            session.run(f"CREATE (:{self.label} {{id: $id, name: $name, value: $value, grad: $grad}})",
                        id=self.id, name=self.name, value=self.value, grad=self.grad)