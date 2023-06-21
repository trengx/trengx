from .edge import Edge

class NetworkXEdge(Edge):
    '''
    The minimum argument requirement for creating an edge in NetworkX is the source and target attributes.
    Source and target attributes represent the nodes between which the edge is connected.
    Other attributes such as id and label are optional and can be provided based on your specific needs.
    '''
    def __init__(self, edge):
        super().__init__(edge)
        if self.source is None or self.target is None:
            raise ValueError("Both 'source' and 'target' attributes are required for creating a NetworkX edge.")
        
        self._validate_type(self.id, str, 'id')
        self._validate_type(self.label, str, 'label')
        self._validate_type(self.source, str, 'source')
        self._validate_type(self.target, str, 'target')
        self._validate_type(self.name, str, 'name')
        self._validate_type(self.second_operand, bool, 'second_operand')


    def _validate_type(self, value, expected_types, attribute_name):
        if value is not None and not isinstance(value, expected_types):
            expected_type_names = ', '.join([t.__name__ for t in expected_types])
            raise TypeError(f"Expected type(s) '{expected_type_names}' for attribute '{attribute_name}', but got '{type(value).__name__}'")
        

