from .edge import Edge

class Neo4jEdge(Edge):
    '''
    When creating an edge in Neo4j, it is enforced to specify the `source` and `target` attributes,
    even though it may not be a strict requirement imposed by Neo4j.
    These attributes indicate the nodes between which the edge is connected.
    Optionally, you can provide additional attributes such as `id`, `label`, and `second_operand` to suit your specific needs.
    '''
    def __init__(self, edge):
        super().__init__(edge)
        if self.source is None or self.target is None:
            raise ValueError("Both 'source' and 'target' attributes are required for creating a Neo4j edge.")
        
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
        
