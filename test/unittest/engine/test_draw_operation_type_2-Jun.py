import unittest
import networkx as nx
import sys
sys.path.append('trengx/engine')
from draw_operation_type_2 import DrawOperationType2 

class TestDrawOperationType2(unittest.TestCase):
    
    def setUp(self):
        self.graph = nx.DiGraph()
        self.draw_op_2 = DrawOperationType2(self.graph, operand1_name='in1', operand1_value=2, operator_name='op',
                                            operand2_name='in2', operand2_value=3,
                                            output_name='out', output_value=5)
        self.draw_op_2_minus = DrawOperationType2(self.graph, operand1_name='in1', operand1_value=2, operator_name='-',
                                                  operand2_name='in2', operand2_value=3,
                                                  output_name='out', output_value=-1)
        self.draw_op_2_divide = DrawOperationType2(self.graph, operand1_name='in1', operand1_value=2, operator_name='/',
                                                   operand2_name='in2', operand2_value=2,
                                                   output_name='out', output_value=1)

    def test_init(self):
        self.assertEqual(self.draw_op_2.operand1_name, 'in1')
        self.assertEqual(self.draw_op_2.operand1_value, 2)
        self.assertEqual(self.draw_op_2.operator_name, 'op')
        self.assertEqual(self.draw_op_2.operand2_name, 'in2')
        self.assertEqual(self.draw_op_2.operand2_value, 3)
        self.assertEqual(self.draw_op_2.output_name, 'out')
        self.assertEqual(self.draw_op_2.output_value, 5)
        
    def test_draw_graph(self):
        self.draw_op_2.draw_graph()
        self.draw_op_2_minus.draw_graph()
        self.draw_op_2_divide.draw_graph()

        self.assertTrue(self.draw_op_2.operand_id in self.graph.nodes)
        self.assertTrue(self.draw_op_2.operator_id in self.graph.nodes)
        self.assertTrue(self.draw_op_2.output_id in self.graph.nodes)
        self.assertTrue(self.draw_op_2.operand2_id in self.graph.nodes)
        self.assertTrue((self.draw_op_2.operand_id, self.draw_op_2.operator_id) in self.graph.edges)
        self.assertTrue((self.draw_op_2.operand2_id, self.draw_op_2.operator_id) in self.graph.edges)
        self.assertTrue((self.draw_op_2.operator_id, self.draw_op_2.output_id) in self.graph.edges)

        # Verify if 'second_operand' is present for '-' operator
        edge_data_minus = self.graph.get_edge_data(self.draw_op_2_minus.operand2_id, self.draw_op_2_minus.operator_id)
        self.assertEqual(edge_data_minus['second_operand'], True)

        # Verify if 'second_operand' is present for '/' operator
        edge_data_divide = self.graph.get_edge_data(self.draw_op_2_divide.operand2_id, self.draw_op_2_divide.operator_id)
        self.assertEqual(edge_data_divide['second_operand'], True)

if __name__ == '__main__':
    unittest.main()
