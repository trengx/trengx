import uuid
import networkx as nx

class AddNode:
    def __init__(self, graph, id=None, name=None, value=None, grad=None):
        """
        Initialize a Node object.
        
        Parameters:
        - graph: An instance of networkx.Graph representing the graph.
        - id: Optional. A unique identifier for the node. If not provided, a new UUIDv1 will be generated.
        - name: Optional. The name of the node.
        - value: Optional. The value associated with the node.
        - grad: Optional. The gradient value of the node.
        """
        if not isinstance(graph, nx.Graph):
            raise ValueError("Graph must be an instance of networkx.Graph.")
        
        self.graph = graph
        self.id = self._generate_unique_id(id)
        self.name = name
        self.value = value
        self.grad = grad

    def _generate_unique_id(self, id):
        """
        Generate a unique identifier for the node. If the provided ID is None, a new UUIDv1 will be generated. 
        This method can be modified to generate a unique ID.
        
        Parameters:
        - id: Optional. The provided node ID, if any.
        
        Returns:
        - A unique identifier for the node.
        """
        if id is None:
            return str(uuid.uuid1())
        return id

    def add_to_graph(self):
        """
        Add the node to the graph.
        
        Returns:
        - The node ID and the created node object as a tuple.
        """
        self.graph.add_node(self.id, name=self.name, value=self.value, grad=self.grad)
        created_node = self.graph.nodes[self.id]
        return self.id, created_node
    
def main():
    # Create a networkx.Graph object
    graph = nx.Graph()

    # Create an instance of AddNode
    node = AddNode(graph, name="Node 1", value=42, grad=0.5)

    # Add the node to the graph and print the result
    node_id, created_node = node.add_to_graph()
    print(f"Node ID: {node_id}")
    print(f"Created Node: {created_node}")

if __name__ == "__main__":
    main()