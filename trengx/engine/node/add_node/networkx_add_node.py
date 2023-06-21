from .add_node import AddNode

class NetworkXAddNode(AddNode):
    def __init__(self, driver, node):
        super().__init__(driver, node)
        self.node_created = False
        self.execute()
        
    def execute(self):
        '''
        Creates a node in the graph using the properties from the given node object
        by utilizing the networkx 'add_node' method.

        In NetworkX, the 'add_node' method does not return anything. 
        It is used to add a single node to a graph, modifying the graph in place
        by including the specified node in the set of nodes (vertices).

        Args:
            node: The node object containing properties such as id, label, name, value, grad.
        '''
        self.driver.add_node(self.id, label=self.label, name=self.name, value=self.value, grad=self.grad)
        self.node_created = True
        
    def __str__(self):
        if self.node_created:
            return str(self.node)
        else:
            return "Node not created."
