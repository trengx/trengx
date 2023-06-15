import uuid
import networkx as nx
from operation_1 import Operation_1

class Operation_2(Operation_1):
    def __init__(self, graph, input1_id=None, input1_name=None, input1_value=None, input1_grad=0, operation_name=None, 
                 input2_id=None, input2_name=None, input2_value=None, input2_grad=0, 
                 output_id=None, output_name=None, output_value=None, output_grad=0):
        
        super().__init__(graph, input_id=input1_id, input_name=input1_name, input_value=input1_value, 
                         input_grad=input1_grad, operation_name=operation_name, 
                         output_id=output_id, output_name=output_name, output_value=output_value, 
                         output_grad=output_grad)
        
        self.input2_id = str(uuid.uuid4()) if input2_id is None else input2_id
        self.input2_name = input2_name
        self.input2_value = input2_value
        self.input2_grad = input2_grad

    def create_graph(self):
        super().create_graph()
        self.graph.add_node(self.input2_id, name=self.input2_name, value=self.input2_value, grad=self.input2_grad)
        self.graph.add_edge(self.input2_id, self.operation_id)
        return self.input_id, self.input2_id, self.operation_id, self.output_id

