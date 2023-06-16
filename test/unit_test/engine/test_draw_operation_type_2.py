import unittest
import networkx as nx
import sys
sys.path.append('trengx/engine')
from draw_operation_type_2 import DrawOperationType2 

class TestDrawOperationType2(unittest.TestCase):
    
    def setUp(self):
        self.graph = nx.DiGraph()
        self.draw_op_2 = DrawOperationType2(self.graph, operand1_name='operand1', operand1_value=5, operator_name='add', 
                                            operand2_name='operand2', operand2_value=6, output_name='output', output_value=11)
        self.operand1_id, self.operand2_id, self.operator_id, self.output_id = self.draw_op_2.draw_graph()

    def test_nodes(self):
        self.assertIn(self.operand1_id, self.graph.nodes)
        self.assertIn(self.operand2_id, self.graph.nodes)
        self.assertIn(self.operator_id, self.graph.nodes)
        self.assertIn(self.output_id, self.graph.nodes)

    def test_edges(self):
        self.assertIn((self.operand1_id, self.operator_id), self.graph.edges)
        self.assertIn((self.operand2_id, self.operator_id), self.graph.edges)
        self.assertIn((self.operator_id, self.output_id), self.graph.edges)

    def test_node_values(self):
        self.assertEqual(self.graph.nodes[self.operand1_id]['value'], 5)
        self.assertEqual(self.graph.nodes[self.operand2_id]['value'], 6)
        self.assertEqual(self.graph.nodes[self.output_id]['value'], 11)

    def test_operation_name(self):
        self.assertEqual(self.graph.nodes[self.operator_id]['name'], 'add')

if __name__ == '__main__':
    unittest.main()
