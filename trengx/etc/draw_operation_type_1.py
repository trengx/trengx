import uuid
import networkx as nx

class DrawOperationType1:
    def __init__(self, graph, operand_id=None, operand_name=None, operand_value=None, operand_grad=0, 
                 operator_name=None, output_id=None, output_name=None, output_value=None, output_grad=0):
        
        # Check if the graph is a valid instance of networkx.Graph
        if not isinstance(graph, nx.Graph):
            raise ValueError("Graph must be an instance of networkx.Graph.")
        
        self.graph = graph
        self.operand_id = str(uuid.uuid4()) if operand_id is None else operand_id
        self.operand_name = operand_name
        self.operand_value = operand_value
        self.operand_grad = operand_grad

        self.operator_id = str(uuid.uuid4())
        self.operator_name = operator_name

        self.output_id = str(uuid.uuid4()) if output_id is None else output_id
        self.output_name = output_name
        self.output_value = output_value
        self.output_grad = output_grad

    def draw_graph(self):
        self.graph.add_node(self.operand_id, name=self.operand_name, value=self.operand_value, grad=self.operand_grad)
        self.graph.add_node(self.operator_id, name=self.operator_name)
        self.graph.add_node(self.output_id, name=self.output_name, value=self.output_value, grad=self.output_grad)
        self.graph.add_edge(self.operand_id, self.operator_id)
        self.graph.add_edge(self.operator_id, self.output_id)
        return self.operand_id, self.operator_id, self.output_id
