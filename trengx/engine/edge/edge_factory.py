# NetworkX
import networkx
from .networkx_edge import NetworkXEdge
from .add_edge.networkx_add_edge import NetworkXAddEdge

#Neo4j
from neo4j import Driver as Neo4jDriver
from .neo4j_edge import Neo4jEdge
from .add_edge.neo4j_add_edge import Neo4jAddEdge

def edge(driver):
    if isinstance(driver, networkx.Graph):
        return NetworkXEdge
    elif isinstance(driver, Neo4jDriver):
        return Neo4jEdge
    else:
        raise ValueError('Invalid driver type')

def add_edge(driver, edge):
    if isinstance(driver, networkx.Graph):
        return NetworkXAddEdge(driver)
    elif isinstance(driver, Neo4jDriver):  
        return Neo4jAddEdge(driver)
    else:
        raise ValueError('Invalid driver type')
    