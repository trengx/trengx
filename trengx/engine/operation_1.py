import uuid
import networkx as nx

class Operation_1:
    def __init__(self, graph, input_id=None, input_name=None, input_value=None, input_grad=0, 
                 operation_name=None, output_id=None, output_name=None, output_value=None, output_grad=0):
        
        # Check if the graph is a valid instance of networkx.Graph
        if not isinstance(graph, nx.Graph):
            raise ValueError("Graph must be an instance of networkx.Graph.")
        
        self.graph = graph
        self.input_id = str(uuid.uuid4()) if input_id is None else input_id
        self.input_name = input_name
        self.input_value = input_value
        self.input_grad = input_grad

        self.operation_id = str(uuid.uuid4())
        self.operation_name = operation_name

        self.output_id = str(uuid.uuid4()) if output_id is None else output_id
        self.output_name = output_name
        self.output_value = output_value
        self.output_grad = output_grad

    def create_graph(self):
        self.graph.add_node(self.input_id, name=self.input_name, value=self.input_value, grad=self.input_grad)
        self.graph.add_node(self.operation_id, name=self.operation_name)
        self.graph.add_node(self.output_id, name=self.output_name, value=self.output_value, grad=self.output_grad)
        self.graph.add_edge(self.input_id, self.operation_id)
        self.graph.add_edge(self.operation_id, self.output_id)
        return self.input_id, self.operation_id, self.output_id
