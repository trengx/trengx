
import uuid
import networkx as nx

class ForwardPropagation:
    def __init__(self, graph, operand1_id=None, operand1_value=None, updated_nodes=None):
        self.graph = graph
        self.operand1_id = operand1_id
        self.operand1_value = operand1_value
        self.updated_nodes = updated_nodes
        
        # Initialize the set of updated nodes if it's None
        if self.updated_nodes is None:
            self.updated_nodes = set()
        
        prev_in1_value = self.graph.nodes[self.operand1_id]['value'] 
        self.graph.nodes[self.operand1_id]['value'] =self.operand1_value
        updated_nodes.add(operand1_id)  # Mark the current node as updated
        for _, operator in self.graph.out_edges(self.operand1_id):
            operator_name = self.graph.nodes[operator]['name']
            second_operand = self.graph[self.operand1_id][operator].get('second_operand', False)

            # Handle the optional second operand
            in2 = next((node for node in G.predecessors(op) if node != in1), None)
            in2_value = G.nodes[in2]['value'] if in2 else None

            out = next(G.successors(op), None)

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
                out_value = in1_value * (in2_value if in2_value is not None else 1)
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
            elif op_name == 'sqr':
                out_value = in1_value**2
            elif op_name == 'sqrt':
                if in1_value >= 0:
                    out_value = np.sqrt(in1_value)
                else:
                    print(f"Error: sqrt of negative number {in1_value}")
                    return
            elif op_name == 'store':
                if out not in updated_nodes:  # Only update 'out' if it hasn't been updated yet
                    forward_propagate(G, out, prev_in1_value, updated_nodes)
                G.nodes[in1]['value'] = in1_value
                continue

            # Store the output value back into the graph
            if out not in updated_nodes:  # Only update 'out' if it hasn't been updated yet
                G.nodes[out]['value'] = out_value

            # Now recursively forward propagate the new value to the next nodes
            forward_propagate(G, out, out_value, updated_nodes)

    # Backward propagation function
    def backward_propagate(G, node_id, lr):
        if G.nodes[node_id]['name'][0] in {'w', 'b'}:  # variable names start with 'w' or 'b'
                G.nodes[node_id]['value'] -= lr * G.nodes[node_id]['grad']
                G.nodes[node_id]['grad'] = 0 # reset the gradient to zero 
        else:
            grad = G.nodes[node_id]['grad']
            if G.nodes[node_id]['name'] == 'e2':
                G.nodes[node_id]['grad'] = 1
            else:
                G.nodes[node_id]['grad'] = 0 # reset the gradient to zero       
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
                elif op_name == 'sqr':
                    G.nodes[in1]['grad'] += grad * 2 * in1_value
                elif op_name == 'sqrt':
                    if in1_value > 0:
                        G.nodes[in1]['grad'] += grad / (2 * np.sqrt(in1_value))
                    else:
                        raise ValueError(f"Error: gradient through sqrt of negative number {in1_value}")

                for in_node, _ in G.in_edges(op):
                    backward_propagate(G, in_node, lr)

class Neuron:
    def __init__(self, G):
        self.G = G
        self.create()

    def create(self):
        self.inlet, self.b, _, self.v = op2(self.G, in1_name = 'inlet', in2_name = 'b', op_name='+', out_name = 'v')
        _, _, self.outlet = op1(self.G, in_id=self.v, op_name='ReLU', out_name = 'outlet')

    def get_nodes(self):
        return self.inlet, self.b, self.v, self.outlet
