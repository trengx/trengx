import uuid
import numpy as np

# Type 1 elementary operation unit
def op1 (G, in_id=None, in_name=None, in_value=None, in_grad=0, op_name=None, out_id=None, out_name=None, out_value=None, out_grad=0):
    # Generate a new UUID if no id is provided for in
    if in_id == None:
        in_id = str(uuid.uuid4())
        G.add_node(in_id, label = 'num', name=in_name, value=in_value, grad=in_grad)
    if out_id == None:
        out_id = str(uuid.uuid4())
        G.add_node(out_id, label = 'num', name=out_name, value=out_value, grad=out_grad)
    op_id = str(uuid.uuid4())
    G.add_node(op_id, label = 'op', name=op_name)
    # Create edges
    G.add_edge(in_id, op_id, label='num2op')
    G.add_edge(op_id, out_id, label='op2num')
    return in_id, op_id, out_id

# Type 2 elementary operation unit
def op2 (G, in1_id=None, in1_name=None, in1_value=None, in1_grad=0, in2_id=None, in2_name=None, in2_value=None, in2_grad=0, op_name=None, out_id=None, out_name=None, out_value=None, out_grad=0):
    # Generate a new UUID if no id is provided 
    if in1_id == None:
        in1_id = str(uuid.uuid4())
        G.add_node(in1_id, label = 'num', name=in1_name, value=in1_value, grad=in1_grad)
    if in2_id == None:
        in2_id = str(uuid.uuid4())
        G.add_node(in2_id, label = 'num', name=in2_name, value=in2_value, grad=in2_grad)
    if out_id == None:
        out_id = str(uuid.uuid4())
        G.add_node(out_id, label = 'num', name=out_name, value=out_value, grad=out_grad)
    op_id = str(uuid.uuid4())
    G.add_node(op_id, label = 'op', name=op_name)
    # Create edges
    G.add_edge(in1_id, op_id, label='num2op')
    G.add_edge(in2_id, op_id, label='num2op', reverse=True)
    G.add_edge(op_id, out_id, label='op2num')
    return in1_id, in2_id, op_id, out_id


# Forward propagation function
# Forward propagation function
def forward_propagate(G, in1, in1_value):
    G.nodes[in1]['value'] = in1_value
    for _, op in G.out_edges(in1):
        op_name = G.nodes[op]['name']
        reverse = G[in1][op].get('reverse', False)

        # Handle the optional second operand
        in2 = next((node for node in G.predecessors(op) if node != in1), None)
        in2_value = G.nodes[in2]['value'] if in2 else None
        
        out = next(G.successors(op), None)
        out_value = G.nodes[out]['value'] if out else None

        # Calculate the output value based on the operation
        if op_name == '+':
            out_value = in1_value + (in2_value if in2_value is not None else 0)
        elif op_name == '-':
            if in2_value is not None:
                if reverse:
                    out_value = in2_value - in1_value
                else:
                    out_value = in1_value - in2_value
            else:
                out_value = in1_value
        elif op_name == '*':
            out_value = (out_value if out_value is not None else 0) + in1_value * (in2_value if in2_value is not None else 1)
        elif op_name == 'log':
            if in1_value > 0:
                out_value = np.log(in1_value)
            else:
                print(f"Error: Log of non-positive number {in1_value}")
                return
        elif op_name == 'sin':
            out_value = np.sin(in1_value)
        
        elif op_name == 'ReLU':
            if in1_value > 0:
                out_value = in1_value
            else:
                out_value = 0

        for _, out in G.out_edges(op):
            forward_propagate(G, out, out_value)


# Backward propagation function
def backward_propagate(G, node_id):
    grad = G.nodes[node_id]['grad']
    for op, _ in G.in_edges(node_id):
        op_name = G.nodes[op]['name']

        in1 = next((node for node in G.predecessors(op)), None)
        in1_value = G.nodes[in1]['value'] if in1 else None

        in2 = next((node for node in G.predecessors(op) if node != in1), None)
        in2_value = G.nodes[in2]['value'] if in2 else None
        reverse = G[in2][op].get('reverse', False) if in2 else False

        if op_name == '+':
            G.nodes[in1]['grad'] += grad
            G.nodes[in2]['grad'] += grad
        elif op_name == '-':
            G.nodes[in1]['grad'] += grad 
            G.nodes[in2]['grad'] += -grad if reverse else grad
        elif op_name == '*':
            G.nodes[in1]['grad'] += grad * in2_value
            G.nodes[in2]['grad'] += grad * in1_value
        elif op_name == 'log':
            G.nodes[in1]['grad'] += grad / in1_value
        elif op_name == 'sin':
            G.nodes[in1]['grad']  += grad * np.cos(in1_value)
        elif op_name == 'ReLU':
            G.nodes[in1]['grad'] += grad if in1_value > 0 else 0

        for in_node, _ in G.in_edges(op):
            backward_propagate(G, in_node)
            
class Neuron:
    def __init__(self, G):
        self.G = G
        self.create()

    def create(self):
        self.input, self.b, _, self.v = op2(self.G, in1_name = 'in', in2_name = 'b', op_name='+', out_name = 'v')
        _, _, self.output = op1(self.G, in_id=self.v, op_name='ReLU', out_name = 'out')

    def get_nodes(self):
        return self.input, self.b, self.v, self.output



        