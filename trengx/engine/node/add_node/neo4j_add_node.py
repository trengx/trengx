from .add_node import AddNode

class Neo4jAddNode(AddNode):
    def execute(self, node):
        with self.driver.session() as session:
            session.run(
                f"CREATE (:{node.label} {{id: $id, name: $name, value: $value, grad: $grad}})",
                id=node.id, 
                name=node.name, 
                value=node.value, 
                grad=node.grad
            )
