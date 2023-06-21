# Standard library imports
import networkx

# Third-party imports
from neo4j import Driver as Neo4jDriver

# Local application imports
from .add_node.networkx_add_node import NetworkXAddNode
from .add_node.neo4j_add_node import Neo4jAddNode

# Registry mapping driver classes to corresponding node classes
driver_to_node_class_registry = {
    networkx.Graph: NetworkXAddNode,
    Neo4jDriver: Neo4jAddNode
}

def add_node(driver, node):
    """
    Factory function acting as the 'Factory Method' in the Factory Method Pattern.

    This function returns a new node object of the appropriate type, based on the type
    of the provided driver. The function uses a registry to map driver types to node
    classes, making it easy to extend the function to support new types of drivers and nodes.

    Args:
    driver: A driver object. The type of this object determines the type of node created.
    node: The data for the node to be added.

    Returns:
    An instance of a node class. The exact type depends on the type of the driver.

    Raises:
    ValueError: If the type of the driver is not supported (i.e., not present in the registry).
    """
    for driver_class, edge_class in driver_to_node_class_registry.items():
        if isinstance(driver, driver_class):
            return edge_class(driver, node)

    raise ValueError(f'Invalid driver type: {type(driver)}. Supported driver types are: {list(driver_to_node_class_registry.keys())}')

    
