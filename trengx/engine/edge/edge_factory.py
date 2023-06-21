# Standard library imports
import networkx

# Third-party imports
from neo4j import Driver as Neo4jDriver

# Local application imports
from .add_edge.networkx_add_edge import NetworkXAddEdge
from .add_edge.neo4j_add_edge import Neo4jAddEdge

# Registry mapping driver classes to corresponding edge classes
driver_to_edge_class_registry = {
    networkx.Graph: NetworkXAddEdge,
    Neo4jDriver: Neo4jAddEdge
}

def add_edge(driver, edge):
    """
    Factory function acting as the 'Factory Method' in the Factory Method Pattern.

    This function returns a new edge object of the appropriate type, based on the type
    of the provided driver. The function uses a registry to map driver types to edge
    classes, making it easy to extend the function to support new types of drivers and edges.

    Args:
    driver: A driver object. The type of this object determines the type of edge created.
    edge: The data for the edge to be added.

    Returns:
    An instance of an edge class. The exact type depends on the type of the driver.

    Raises:
    ValueError: If the type of the driver is not supported (i.e., not present in the registry).
    """
    for driver_class, edge_class in driver_to_edge_class_registry.items():
        if isinstance(driver, driver_class):
            return edge_class(driver, edge)

    raise ValueError(f'Invalid driver type: {type(driver)}. Supported driver types are: {list(driver_to_edge_class_registry.keys())}')

    