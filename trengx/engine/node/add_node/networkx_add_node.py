from .add_node import AddNode

class NetworkXAddNode(AddNode):
    def execute(self, node):
        '''
        Creates a node in the graph using the properties from the given node object
        by utilizing the networkx 'add_node' method.

        In NetworkX, the 'add_node' method does not return anything. 
        It is used to add a single node to a graph, modifying the graph in place
        by including the specified node in the set of nodes (vertices).

        Args:
            node: The node object containing properties such as id, label, name, value, grad.

        Returns:
            The same node object that was added to the graph.
        '''
        
        self.driver.add_node(node.id, label=node.label, name=node.name, value=node.value, grad=node.grad)
        return node
