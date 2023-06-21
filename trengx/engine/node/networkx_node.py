from .node import Node

class NetworkXNode(Node):
    '''
    The minimum argument requirement for creating a node in NetworkX is the id attribute.
    The id attribute serves as a unique identifier for the node within the graph.
    Other attributes such as label, name, value, and grad are optional and can be provided based on your specific needs.
    '''
    def __init__(self, node):
        super().__init__(node)
        if self.id is None:
            raise ValueError("The 'id' attribute is required for creating a NetworkX node.")
        
        self._validate_type(self.id, str, 'id')
        self._validate_type(self.label, str, 'label')
        self._validate_type(self.name, str, 'name')
        self._validate_type(self.value, (int, float), 'value')
        self._validate_type(self.grad, (int, float), 'grad')

    def _validate_type(self, value, expected_types, attribute_name):
        if value is not None and not isinstance(value, expected_types):
            expected_type_names = ', '.join([t.__name__ for t in expected_types])
            raise TypeError(f"Expected type(s) '{expected_type_names}' for attribute '{attribute_name}', but got '{type(value).__name__}'")
