import networkx as nx

class AddEdge:
    def __init__(self, graph, source, target, weight=None):
        """
        Initialize an AddEdge object.
        
        Parameters:
        - graph: An instance of networkx.Graph representing the graph.
        - source: The source node of the edge.
        - target: The target node of the edge.
        - weight: Optional. The weight of the edge.
        """
        if not isinstance(graph, nx.Graph):
            raise ValueError("Graph must be an instance of networkx.Graph.")
        
        self.graph = graph
        self.source = source
        self.target = target
        self.weight = weight

    def add_to_graph(self):
        """
        Add the edge to the graph.
        
        Returns:
        - The source node, target node, and the created edge object as a tuple.
        """
        self.graph.add_edge(self.source, self.target, weight=self.weight)
        created_edge = self.graph.edges[self.source, self.target]
        return self.source, self.target, created_edge
    
def main():
    # Create a networkx.Graph object
    graph = nx.Graph()

    # Create an instance of AddEdge
    edge = AddEdge(graph, source="Node 1", target="Node 2", weight=0.5)

    # Add the edge to the graph and print the result
    source_node, target_node, created_edge = edge.add_to_graph()
    print(f"Source Node: {source_node}")
    print(f"Target Node: {target_node}")
    print(f"Created Edge: {created_edge}")

if __name__ == "__main__":
    main()
