from .add_node import AddNode

class Neo4jAddNode(AddNode):
    def __init__(self, driver, node):
        super().__init__(driver, node)
        self.node_created = False
        self.node_properties = {}
        self.execute()
        
    def execute(self):
        with self.driver.session() as session:
            response = session.run(
                f"CREATE (n:{self.label} {{id: $id, name: $name, value: $value, grad: $grad}}) RETURN n",
                id=self.id, 
                name=self.name, 
                value=self.value, 
                grad=self.grad
            ).single()
            
        if response:
            self.node_created = True
            node = response['n']
            self.node_properties = dict(node.items())
        
    def get_node_properties(self):
        return self.node_properties
    
    def __str__(self):
        if self.node_created:
            return str(self.get_node_properties())
        else:
            return "Node not created."
