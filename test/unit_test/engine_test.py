import unittest
import networkx as nx
import sys
sys.path.append('trengx')
from engine import op1, op2, forward_propagate, backward_propagate, Neuron

class TestEngine(unittest.TestCase):

    def setUp(self):
        self.G = nx.DiGraph()  # create a new graph for each test

    def test_op1(self):
        in_id, op_id, out_id = op1(self.G, in_name='in', in_value=1.0, op_name='sin', out_name='out')
        self.assertEqual(self.G.nodes[in_id]['value'], 1.0)
        self.assertEqual(self.G.nodes[op_id]['name'], 'sin')
        self.assertEqual(self.G.nodes[out_id]['name'], 'out')

    def test_forward_propagate(self):
        in_id, op_id, out_id = op1(self.G, in_name='in', in_value=1.0, op_name='sin', out_name='out')
        forward_propagate(self.G, in_id, 2.0)
        self.assertAlmostEqual(self.G.nodes[out_id]['value'], 0.9092974268)

    # similarly, you can write other test methods

    def test_neuron(self):
        neuron = Neuron(self.G)
        inlet, b, v, outlet = neuron.get_nodes()
        self.assertEqual(self.G.nodes[inlet]['name'], 'inlet')
        self.assertEqual(self.G.nodes[b]['name'], 'b')
        self.assertEqual(self.G.nodes[v]['name'], 'v')
        self.assertEqual(self.G.nodes[outlet]['name'], 'outlet')

if __name__ == '__main__':
    unittest.main()
