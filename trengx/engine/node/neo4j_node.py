from .node import Node

class Neo4jNode(Node):
    '''
    The minimum argument requirement for creating a node in Neo4j is no specific attribute.
    Neo4j automatically assigns a unique identifier to each node created within the database.
    Other attributes such as label, name, value, and grad are optional and can be provided based on your specific needs.
    '''
    def __init__(self, label=None, name=None, value=None, grad=None):
        self._validate_type(label, str, 'label')
        self._validate_type(name, str, 'name')
        self._validate_type(value, (int, float), 'value')
        self._validate_type(grad, (int, float), 'grad')

        super().__init__(label=label, name=name, value=value, grad=grad)

    def _validate_type(self, value, expected_types, attribute_name):
        if value is not None and not isinstance(value, expected_types):
            expected_type_names = ', '.join([t.__name__ for t in expected_types])
            raise TypeError(f"Expected type(s) '{expected_type_names}' for attribute '{attribute_name}', but got '{type(value).__name__}'")
