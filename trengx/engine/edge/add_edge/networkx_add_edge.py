from .add_edge import AddEdge

class NetworkXAddEdge(AddEdge):
    def execute(self, edge):
        """
        Adds an edge between the source node and the target node in the graph.

        Args:
            source_node: The source node object.
            target_node: The target node object.
            label (optional): The label of the edge.

        Returns:
            The source node object.
        """
        self.driver.add_edge(edge.source, edge.target, id = edge.id, label=edge.label, name=edge.name, second_operand=edge.second_operand)
        return edge

