from neo4j import Driver as Neo4jDriver
import networkx 
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

class Neo4jAddNode(AddNode):
    def add_to_graph(self):
        if type(self.id) is not str:
            self.id = str(self.id)
        with self.driver.session() as session:
            session.run(f"CREATE (:{self.label} {{id: $id, name: $name, value: $value, grad: $grad}})",
                        id=self.id, name=self.name, value=self.value, grad=self.grad)


class NetworkXAddNode(AddNode):
    def add_to_graph(self):
        self.driver.add_node(self.id, label=self.label, name=self.name, value=self.value, grad=self.grad)


def node(driver, id=None, label=None, name=None, value=None, grad=None):
    if isinstance(driver, networkx.Graph):
        return NetworkXAddNode(driver, id, label, name, value, grad)
    elif isinstance(driver, Neo4jDriver):
        return Neo4jAddNode(driver, id, label, name, value, grad)
    else:
        raise ValueError('Invalid driver type')


