from abc import ABC, abstractmethod
import uuid
from typing import Any, Dict, Union

class AddNode(ABC):
    """
    Abstract base class for a node in a computational graph.

    The `execute` method must be implemented by any concrete subclass.
    """
    
    def __init__(self, driver: Any, node: Dict[str, Union[str, float]]) -> None:
        """
        Initialize the AddNode.

        If a node dict is not provided or doesn't have the correct types, raises a ValueError.
        """
        
        if node is None:
            raise ValueError("node cannot be None")

        id = node.get('id', str(uuid.uuid1()))
        if not isinstance(id, str):
            raise ValueError("id must be a string")

        label = node.get('label')
        if label is not None and not isinstance(label, str):
            raise ValueError("label must be a string")

        name = node.get('name')
        if name is not None and not isinstance(name, str):
            raise ValueError("name must be a string")

        value = node.get('value')
        if value is not None and not isinstance(value, (int, float)):
            raise ValueError("value must be a number")

        grad = node.get('grad')
        if grad is not None and not isinstance(grad, (int, float)):
            raise ValueError("grad must be a number")
        
        self.driver = driver
        self.node = node
        self.id = id
        self.label = label
        self.name = name
        self.value = value
        self.grad = grad

    @abstractmethod
    def execute(self) -> None:
        """
        Execute the node's operation.

        This method must be implemented by any concrete subclass.
        """
        pass



