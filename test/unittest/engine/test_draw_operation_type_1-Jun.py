import unittest
import networkx as nx
import sys
sys.path.append('trengx/engine')
from draw_operation_type_1 import DrawOperationType1 

class TestDrawOperationType1(unittest.TestCase):
    
    def setUp(self):
        self.graph = nx.DiGraph()
        self.draw_op_1 = DrawOperationType1(self.graph, operand_name='in', operand_value=2, operator_name='op',
                                     output_name='out', output_value=3)

    def test_init(self):
        self.assertEqual(self.draw_op_1.operand_name, 'in')
        self.assertEqual(self.draw_op_1.operand_value, 2)
        self.assertEqual(self.draw_op_1.operator_name, 'op')
        self.assertEqual(self.draw_op_1.output_name, 'out')
        self.assertEqual(self.draw_op_1.output_value, 3)
        
    def test_draw_graph(self):
        self.draw_op_1.draw_graph()
        self.assertTrue(self.draw_op_1.operand_id in self.graph.nodes)
        self.assertTrue(self.draw_op_1.operator_id in self.graph.nodes)
        self.assertTrue(self.draw_op_1.output_id in self.graph.nodes)

# Run the tests
if __name__ == '__main__':
    unittest.main()
