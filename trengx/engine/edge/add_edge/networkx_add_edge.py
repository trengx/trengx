from .add_edge import AddEdge

class NetworkXAddEdge(AddEdge):
    def __init__(self, driver, edge):
        super().__init__(driver, edge)
        self.edge_created = False
        self.execute()
        
    def execute(self):
        "The first argument is the source node and the second argument is the target node."
        self.driver.add_edge(self.source, self.target, id=self.id, label=self.label, name=self.name, second_operand=self.second_operand)
        self.edge_created = True
        
    def __str__(self):
        if self.edge_created:
            return str(self.edge)
        else:
            return "Edge not created."
