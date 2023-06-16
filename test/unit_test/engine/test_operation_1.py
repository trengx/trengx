import unittest
import networkx as nx
import sys
sys.path.append('trengx/engine')
from operation_1 import Operation_1 

class TestOperation_1(unittest.TestCase):
    
    def setUp(self):
        self.graph = nx.DiGraph()
        self.operation = Operation_1(self.graph, input_name='in', input_value=2, operation_name='op',
                                     output_name='out', output_value=3)

    def test_init(self):
        self.assertEqual(self.operation.input_name, 'in')
        self.assertEqual(self.operation.input_value, 2)
        self.assertEqual(self.operation.operation_name, 'op')
        self.assertEqual(self.operation.output_name, 'out')
        self.assertEqual(self.operation.output_value, 3)
        
    def test_create_graph(self):
        self.operation.create_graph()
        self.assertTrue(self.operation.input_id in self.graph.nodes)
        self.assertTrue(self.operation.operation_id in self.graph.nodes)
        self.assertTrue(self.operation.output_id in self.graph.nodes)

# Run the tests
if __name__ == '__main__':
    unittest.main()