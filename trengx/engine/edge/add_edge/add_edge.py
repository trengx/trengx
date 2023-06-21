from abc import ABC, abstractmethod
import uuid
from typing import Any, Dict, Union

class AddEdge(ABC):
    """
    Abstract base class for an edge in a computational graph.

    The `execute` method must be implemented by any concrete subclass.
    """

    def __init__(self, driver: Any, edge: Dict[str, Union[str, bool]]) -> None:
        """
        Initialize the AddEdge.

        If an edge dict is not provided or doesn't have the correct types, raises a ValueError.
        """
        
        if edge is None:
            raise ValueError("edge cannot be None")

        id = edge.get('id', str(uuid.uuid1()))
        if not isinstance(id, str):
            raise ValueError("id must be a string")

        label = edge.get('label')
        if label is not None and not isinstance(label, str):
            raise ValueError("label must be a string")

        source = edge.get('source')
        if source is not None and not isinstance(source, str):
            raise ValueError("source must be a string")

        target = edge.get('target')
        if target is not None and not isinstance(target, str):
            raise ValueError("target must be a string")

        name = edge.get('name')
        if name is not None and not isinstance(name, str):
            raise ValueError("name must be a string")

        second_operand = edge.get('second_operand')
        if second_operand is not None and not isinstance(second_operand, bool):
            raise ValueError("second_operand must be a boolean")
        
        self.driver = driver
        self.edge = edge
        self.id = id
        self.label = label
        self.source = source
        self.target = target
        self.name = name
        self.second_operand = second_operand

    @abstractmethod
    def execute(self) -> None:
        """
        Execute the edge's operation.

        This method must be implemented by any concrete subclass.
        """
        pass

    