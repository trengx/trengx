from .add_edge import AddEdge

class NetworkXAddEdge(AddEdge):
    def add_to_graph(self):
        # the add_edge method in networkx takes the form of G.add_edge(n1, n2, **attr)
        if not isinstance(self.node1, str):
            raise TypeError('node1 must be a string')
        if not isinstance(self.node2, str):
            raise TypeError('node2 must be a string')
        if not isinstance(self.id, str):
            raise TypeError('id must be a string')
        if not isinstance(self.label, str):
            raise TypeError('label must be a string')
        if not isinstance(self.second_operand, bool):
            raise TypeError('second_operand must be a boolean')
        self.driver.add_edge(self.node1, self.node2, id=self.id, label=self.label, second_operand=self.second_operand)
