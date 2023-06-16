import uuid
import networkx as nx
from draw_operation_type_1 import DrawOperationType1

class DrawOperationType2(DrawOperationType1):
    def __init__(self, graph, operand1_id=None, operand1_name=None, operand1_value=None, operand1_grad=0, 
                 operator_name=None, operand2_id=None, operand2_name=None, operand2_value=None, 
                 operand2_grad=0, output_id=None, output_name=None, output_value=None, output_grad=0):
        
        super().__init__(graph, operand_id=operand1_id, operand_name=operand1_name, operand_value=operand1_value, 
                         operand_grad=operand1_grad, operator_name=operator_name, 
                         output_id=output_id, output_name=output_name, output_value=output_value, 
                         output_grad=output_grad)
        
        self.operand2_id = str(uuid.uuid4()) if operand2_id is None else operand2_id
        self.operand2_name = operand2_name
        self.operand2_value = operand2_value
        self.operand2_grad = operand2_grad

    def draw_graph(self):
        super().draw_graph()
        self.graph.add_node(self.operand2_id, name=self.operand2_name, value=self.operand2_value, grad=self.operand2_grad)
        self.graph.add_edge(self.operand2_id, self.operator_id)
        return self.operand_id, self.operand2_id, self.operator_id, self.output_id

