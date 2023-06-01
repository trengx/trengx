# Graph class
import uuid
from typing import Optional, List, Dict, Union
from neo4j import GraphDatabase as graphdb

class Graph:
    """
    This class acts as an interface for executing and managing basic graph operations
    on a Neo4j graph database.

    Attributes:
        driver : A driver object that maintains the connection to the database.
    """
    def __init__(self, uri: str, user: str, password: str):
        """
        Initializes the Graph object with a connection to the database.

        Args:
            uri (str): The connection string for the database.
            user (str): The username for the database.
            password (str): The password for the database.
        """
        try:
            self.driver = graphdb.driver(uri, auth=(user, password))
        except Exception as e:
            raise Exception(f"Failed to create driver: {e}")

    def close(self) -> None:
        """
        Closes the connection to the database.
        """
        try:
            self.driver.close()
        except Exception as e:
            raise Exception(f"Failed to close driver: {e}")

    def run_query(self, query: str, parameters: Optional[Dict[str, Union[str, int]]] = None) -> List[Dict[str, Union[str, int]]]:
        """
        Runs an arbitrary Cypher query on the database.

        Args:
            query (str): The Cypher query to run.
            parameters (dict, optional): The parameters for the query. Keys are parameter names,
                and values are parameter values.

        Returns:
            list[dict]: A list of dictionaries representing the records returned by the query.
        """
        if parameters is not None and not isinstance(parameters, dict):
            raise TypeError(f"Expected dict for parameters, got {type(parameters)}")

        try:
            with self.driver.session() as session:
                result = session.run(query, parameters)
                return [record.data() for record in result]
        except Exception as e:
            raise Exception(f"Failed to run query: {e}")

    def __del__(self):
        """
        Destructor method to ensure the connection gets closed when the object is deleted.
        """
        self.close()

    # Add node   
    @staticmethod
    def _add_node_tx(tx, node_label: str, properties: dict):
        """
        Private helper function to create a node within a transaction.

        Args:
            tx: Transaction object.
            node_label (str): The label to assign to the node.
            properties (dict): Additional properties to assign to the node.

        Returns:
            dict: A dictionary representing the newly created node.
        """
        properties['uuid'] = str(uuid.uuid4())
        query = f"CREATE (n:{node_label} $properties) RETURN n"
        result = tx.run(query, properties=properties).single()
        node = result['n']
        node_properties = dict(node.items())
        del node_properties['uuid']
        return {'id': node['uuid'], 'label': list(node.labels), 'properties': node_properties}

    def add_node(self, node_label: str, properties: dict = None):
        """
        Public function to add a node in a Neo4j graph database.

        This function creates a new session and transaction with the graph database,
        and calls the helper function `_create_node_tx` to add the node.

        Args:
            node_label (str): The label to assign to the node.
            properties (dict, optional): Additional properties to assign to the node.

        Returns:
            dict: A dictionary representing the newly created node.
        """
        if not isinstance(node_label, str):
            raise TypeError("node_label must be a string")
        if not isinstance(properties, dict):
            raise TypeError("properties must be a dictionary")
        with self.driver.session() as session:
            try:
                node = session.write_transaction(self._add_node_tx, node_label, properties)
                return node
            except Exception as e:
                raise Exception(f"Failed to add node: {e}")
            
    # Get node by id
    @staticmethod
    def _get_node_tx(tx, node_id: str):
        """
        Private helper function to retrieve a node within a transaction.

        Args:
            tx: Transaction object.
            node_id (str): The UUID of the node to retrieve.

        Returns:
            dict: A dictionary representing the retrieved node.
        """
    
        query = "MATCH (n) WHERE n.uuid = $node_id RETURN n"
        result = tx.run(query, node_id=node_id).single()
        if result is None:
            return f"No node found with node_id: {node_id}"
        else:
            node = result['n']
            if node:
                node_properties = dict(node.items())
                del node_properties['uuid']
                return {'id': node['uuid'], 'label': list(node.labels), 'properties': node_properties}

    def get_node (self, node_id: str):
        """
        Public function to retrieve a node from the graph database based on its UUID.

        This function creates a new session and transaction with the graph database,
        and calls the helper function `_get_node_tx` to retrieve the node.

        Args:
            node_id (str): The ID of the node (UUID) to retrieve.

        Returns:
            dict: A dictionary representing the retrieved node, or None if no node is found.
        """        
        if not isinstance(node_id, str):
            raise TypeError("node_id must be a string")
        with self.driver.session() as session:
            try:
                return session.read_transaction(self._get_node_tx, node_id)
            except Exception as e:
                raise Exception(f"Failed to retrieve node: {e}")


    # Update node properties
    @staticmethod
    def _update_node_properties_tx(tx, node_id: str, properties: dict):
        """
        Private helper function to update node properties within a transaction.

        Args:
            tx: Transaction object.
            node_id (str): The ID of the node to update.
            properties (dict): The updated properties to assign to the node.

        Returns:
            dict: A dictionary representing the updated node.

        Raises:
            Exception: If no node is found.
        """
        query = "MATCH (n) WHERE n.uuid = $node_id SET n += $properties RETURN n"
        result = tx.run(query, node_id=node_id, properties=properties).single()
        if result is None:
            raise Exception(f"No node found with node_id: {node_id}")
        else:
            node = result['n']
            node_properties = dict(node.items())
            del node_properties['uuid']
            return {'id': node['uuid'], 'label': list(node.labels), 'properties': node_properties}


    def update_node_properties(self, node_id: str, properties: dict):
        """
        Public function to update the properties of a node in the graph database.

        This function creates a new session and transaction with the graph database,
        and calls the helper function `_update_node_properties_tx` to update the node.

        Args:
            node_id (str): The ID of the node to update.
            properties (dict): The updated properties to assign to the node.

        Returns:
            dict: A dictionary representing the updated node, or None if no node is found.
        """
        if not isinstance(node_id, str):
            raise TypeError("node_id must be a string")
        if not isinstance(properties, dict):
            raise TypeError("properties must be a dictionary")
        with self.driver.session() as session:
            try:
                return session.write_transaction(self._update_node_properties_tx, node_id, properties)
            except Exception as e:
                raise Exception(f"Failed to update node properties: {e}")

    # Delete node
    @staticmethod
    def _delete_node_tx(tx, node_id: str, detach: bool = False):
        """
        Private helper function to delete a node within a transaction.

        Args:
            tx: Transaction object.
            node_id (str): The ID of the node to delete.
            detach (bool, optional): Flag indicating whether to delete the node with or without detaching relationships.

        Returns:
            bool: True if the node was deleted, False otherwise.
        """
        try:
            query = "MATCH (n) WHERE n.uuid = $node_id"
            
            if detach:
                query += " DETACH DELETE n"
            else:
                query += " DELETE n"
            
            query += " RETURN count(n) as deleted_count"
            
            result = tx.run(query, node_id=node_id).single()
            deleted_count = result["deleted_count"]
            
            if deleted_count == 0:
                return False
            return True
        except Exception as e:
            raise Exception(f"Failed to delete node: {e}")


    def delete_node(self, node_id: str, detach: bool = False):
        """
        Public function to delete a node from the graph database based on its ID.

        This function creates a new session and transaction with the graph database,
        and calls the helper function `_delete_node_tx` to delete the node.

        Args:
            node_id (str): The ID of the node to delete.
            detach (bool, optional): Flag indicating whether to delete the node with or without detaching relationships.

        Returns:
            bool: True if the node was deleted, False otherwise.
        """
        if not isinstance(node_id, str):
            raise TypeError("node_id must be a string")
        if not isinstance(detach, bool):
            raise TypeError("detach must be a boolean")

        with self.driver.session() as session:
            try:
                return session.write_transaction(self._delete_node_tx, node_id, detach)
            except Exception as e:
                raise Exception(f"Failed to delete node: {e}")



    #Set node value
    @staticmethod
    def _set_node_value_tx(tx, node_id:str, value):
        """
        1. MATCH path = (in1)-[r:num2op|op2num*0..]->() WHERE id(in1) = $node_id AND all(rel IN relationships(path) WHERE rel.trigger = true):
        Find a path that begins from a node (in1) which has the ID specified by the parameter node_id. 
        The path can include any number of num2op or op2num relationships (from none at all, up to an infinite number, 
        denoted by *0..). The num2op relationship likely signifies the operation to perform on a number 
        and the op2num relationship likely represents the number to perform the operation on. 
        The WHERE clause ensures all relationships in this path have a trigger property that is true.

        2. WITH path ORDER BY length(path) DESC LIMIT 1 WITH nodes(path) AS nodes:
        This statement orders all found paths by their length in descending order and limits the result to the longest path. 
        Then, the nodes of this longest path are collected into a list called nodes.

        3. UNWIND range(0, size(nodes)-2, 2) AS i WITH nodes[i] AS in1, nodes[i+1] AS op, nodes[i+2] AS out:
        The UNWIND statement creates a new row for each value in the range from 0 to the size of nodes - 2, stepping by 2. 
        This is used to group the nodes into triples (in1, op, out).

        4. MATCH (in1)-[:num2op]->(op)-[:op2num]->(out) OPTIONAL MATCH (in2)-[:num2op]->(op) WHERE id(in2) <> id(in1):
        The script then matches these triples to actual paths in the graph. It also optionally matches another node in2 that connects 
        to op with a num2op relationship, provided in2 is not the same as in1.

        5. WITH in1, op, out, in2 SET out.value = CASE ... END:
        Depending on the op.name (the name of the operation), this part updates out.value (the result of the operation). 
        For subtraction and division, it also considers a reverse property on the operation node to decide the order of the operands. 
        If op.name is none of the given, it leaves out.value as it was.
        """

        try:
            query = """
                MATCH (in1)
                WHERE in1.uuid = $node_id
                SET in1.value = $value
                WITH in1
                MATCH path = (in1)-[r:num2op|op2num*0..]->()
                WHERE all(rel IN relationships(path) WHERE rel.trigger = true)
                WITH path
                ORDER BY length(path) DESC
                LIMIT 1
                WITH nodes(path) AS nodes
                UNWIND range(0, size(nodes)-2, 2) AS i
                WITH nodes[i] AS in1, nodes[i+1] AS op, nodes[i+2] AS out
                MATCH (in1)-[:num2op]->(op)-[:op2num]->(out)
                OPTIONAL MATCH (in2)-[:num2op]->(op)
                WHERE in1.uuid  <> in2.uuid   
                WITH in1, op, out, in2
                SET out.value = 
                CASE 
                    WHEN op.name = '+' THEN in1.value + in2.value
                    WHEN op.name = '-' AND op.reverse = false THEN in1.value - in2.value
                    WHEN op.name = '-' AND op.reverse = true THEN in2.value - in1.value
                    WHEN op.name = '*' THEN in1.value * in2.value
                    WHEN op.name = '/' AND op.reverse = false THEN in1.value / in2.value
                    WHEN op.name = '/' AND op.reverse = true THEN in2.value / in1.value
                    WHEN op.name = 'round' THEN round(in1.value)
                    WHEN op.name = 'sqrt' THEN sqrt(in1.value)
                    WHEN op.name = 'abs' THEN abs(in1.value)
                    WHEN op.name = 'exp' THEN exp(in1.value)
                    WHEN op.name = 'log10' THEN log10(in1.value)
                    WHEN op.name = 'log' THEN log(in1.value)
                    WHEN op.name = 'sin' THEN sin(in1.value)
                    WHEN op.name = 'cos' THEN cos(in1.value)
                    WHEN op.name = 'tan' THEN tan(in1.value)
                    WHEN op.name = 'ceil' THEN ceil(in1.value)
                    WHEN op.name = 'floor' THEN floor(in1.value)
                    WHEN op.name = 'round' THEN round(in1.value)
                    WHEN op.name = 'sign' THEN sign(in1.value)
                    WHEN op.name = 'store' THEN in1.value
                    ELSE out.value
                END
            """
            tx.run(query, node_id=node_id, value=value)
            return True
        except Exception as e:
            print(f"Error occurred: {e}")
            return False

    def set_node_value(self, node_id:str, value):
        if not isinstance(node_id, str):
            raise TypeError("node_id must be a string")
        with self.driver.session() as session:
            return session.execute_write(self._set_node_value_tx, node_id, value)
        
    @staticmethod
    def _get_node_value_tx(tx, node_id: str):
        """
        Private helper function to retrieve the 'value' property of a node within a transaction.

        Args:
            tx: Transaction object.
            node_id (str): The ID of the node.

        Returns:
            Any: The value of the 'value' property, or None if the property does not exist.
        """
        key = 'value'  # The key we're interested in is 'value'
        query = """
            MATCH (n) 
            WHERE n.uuid = $node_id
            RETURN apoc.map.values(n, [$key])[0] as value
        """
        result = tx.run(query, node_id=node_id, key=key)
        record = result.single()
        return record['value']

    def get_node_value(self, node_id: str):
        """
        Public function to retrieve the 'value' property of a node from the graph database.

        This function creates a new session and transaction with the graph database,
        and calls the helper function `_get_node_value_tx` to retrieve the 'value' property.

        Args:
            node_id (str): The ID of the node.

        Returns:
            Any: The value of the 'value' property, or None if the property does not exist.
        """
        if not isinstance(node_id, str):
            raise TypeError("node_id must be a string")
        with self.driver.session() as session:
            try:
                return session.read_transaction(self._get_node_value_tx, node_id)
            except Exception as e:
                raise Exception(f"Failed to retrieve node 'value' property: {e}")


    @staticmethod
    def _get_node_property_tx(tx, node_id: str, key: str):
        """
        Private helper function to retrieve a specific property of a node within a transaction.

        Args:
            tx: Transaction object.
            node_id (str): The ID of the node.
            key (str): The property key.

        Returns:
            Any: The value of the specified property, or None if the property does not exist.
        """
        query = """
            MATCH (n) 
            WHERE n.uuid = $node_id
            RETURN apoc.map.values(n, [$key])[0] as value
        """
        result = tx.run(query, node_id=node_id, key=key)
        record = result.single()
        return record['value']

    def get_node_property(self, node_id: str, key: str):
        """
        Public function to retrieve a specific property of a node from the graph database.

        This function creates a new session and transaction with the graph database,
        and calls the helper function `_get_node_property_tx` to retrieve the property.

        Args:
            node_id (str): The ID of the node.
            key (str): The property key.

        Returns:
            Any: The value of the specified property, or None if the property does not exist.
        """
        if not isinstance(node_id, str):
            raise TypeError("node_id must be a string")
        if not isinstance(key, str):
            raise TypeError("key must be a string")
        with self.driver.session() as session:
            try:
                return session.read_transaction(self._get_node_property_tx, node_id, key)
            except Exception as e:
                raise Exception(f"Failed to retrieve node property: {e}")

    # Add edge
    @staticmethod
    def _add_edge_tx(tx, label:str, out_id:str, in_id:str, properties:dict=None, merge:bool=False):
        """
        Private helper function to add an edge between two nodes within a transaction.

        Args:
            tx: Transaction object.
            label (str): The label of the edge.
            out_id (str): The ID of the outgoing node.
            in_id (str): The ID of the incoming node.
            properties (dict, optional): The properties of the edge.
            merge (bool, optional): A flag indicating whether to merge the edge if it already exists.

        Returns:
            list: A list containing dictionaries with details of the created or merged edge.
        """
        if merge:
            add_clause = "MERGE"
        else:
            add_clause = "CREATE"
        
        edge_id = str(uuid.uuid4())
        
        query = f"MATCH (n) WHERE n.uuid = $out_id MATCH (m) WHERE m.uuid = $in_id {add_clause} (n)-[r:{label}{{uuid: $edge_id}}]->(m)"
        if properties:
            query += " SET r += $properties"
        query += " RETURN r.uuid AS id, type(r) AS label, n.uuid AS out_id, m.uuid AS in_id, properties(r) AS properties"
        
        try:
            result = tx.run(query, out_id=out_id, in_id=in_id, edge_id=edge_id, properties=properties).data()
            edge = result[0]
            # Remove the 'edge_id' key from properties
            edge['properties'].pop('uuid', None)
        except Exception as e:
            raise Exception(f"Failed to add edge: {e}")
        
        return edge

    def add_edge(self, label:str, out_id:str, in_id:str, properties:dict=None, merge:bool=False):
        """
        Public function to add an edge between two nodes in the graph database.

        This function creates a new session and transaction with the graph database,
        and calls the helper function `_add_edge_tx` to add the edge.

        Args:
            label (str): The label of the edge.
            out_id (str): The ID of the outgoing node.
            in_id (str): The ID of the incoming node.
            properties (dict, optional): The properties of the edge.
            merge (bool, optional): A flag indicating whether to merge the edge if it already exists.

        Returns:
            list: A list containing dictionaries with details of the created or merged edge.
        """
        if not isinstance(label, str):
            raise TypeError("edge_label must be a string")
        if not isinstance(out_id, str):
            raise TypeError("out_id must be a string")
        if not isinstance(in_id, str):
            raise TypeError("in_id must be a string")
        if properties and not isinstance(properties, dict):
            raise TypeError("properties must be a dictionary")
        if not isinstance(merge, bool):
            raise TypeError("merge must be a boolean")
        
        with self.driver.session() as session:
            try:
                edge = session.write_transaction(self._add_edge_tx, label, out_id, in_id, properties, merge)
                return edge
            except Exception as e:
                raise Exception(f"Failed to add edge: {e}")

    # Get edge
    @staticmethod
    def _get_edge_tx(tx, id: str):
        """
        Private helper function to retrieve an edge by its ID within a transaction.

        Args:
            tx: Transaction object.
            id (str): The ID of the edge to retrieve.

        Returns:
            dict: A dictionary representing the retrieved edge.
        """
        try:
            query = "MATCH ()-[r]-() WHERE r.uuid = $id RETURN r.uuid AS id, type(r) AS label, startNode(r).uuid AS out_id, endNode(r).uuid AS in_id, properties(r) AS properties"
            result = tx.run(query, id=id).data()
            edge = result[0]
            # Remove the 'edge_id' key from properties
            edge['properties'].pop('uuid', None)
        except Exception as e:
            raise Exception(f"Failed to retrieve edge: {e}")
        
        return edge


    def get_edge(self, id: str):
        """
        Public function to retrieve an edge by its ID.

        This function creates a new session and transaction with the graph database,
        and calls the helper function `_get_edge_tx` to retrieve the edge.

        Args:
            id (str): The ID of the edge to retrieve.

        Returns:
            dict: A dictionary representing the retrieved edge, or None if no edge is found.
        """
        if not isinstance(id, str):
            raise TypeError("id must be a string")

        with self.driver.session() as session:
            try:
                return session.read_transaction(self._get_edge_tx, id)
            except Exception as e:
                raise Exception(f"Failed to retrieve edge: {e}")


    # Update edge properties
    @staticmethod
    def _update_edge_properties_tx(tx, id: str, properties: dict):
        """
        Private helper function to update edge properties by ID within a transaction.

        Args:
            tx: Transaction object.
            id (str): The ID of the edge to update.
            properties (dict): The new properties for the edge.

        Returns:
            bool: True if the update operation was successful, False otherwise.
        """
        query = """
            MATCH ()-[r]-()
            WHERE r.uuid = $id
            SET r += $properties
            RETURN r.uuid AS edge_id
        """

        result = tx.run(query, id=id, properties=properties)
        return result is not None


    def update_edge_properties(self, id: str, properties: dict):
        """
        Public function to update edge properties by ID in the graph database.

        Args:
            id (str): The ID of the edge to update.
            properties (dict): The new properties for the edge.

        Returns:
            bool: True if the update operation was successful, False otherwise.
        """
        if not isinstance(id, str):
            raise TypeError("id must be a string")

        if not isinstance(properties, dict):
            raise TypeError("properties must be a dictionary")

        try:
            with self.driver.session() as session:
                return session.write_transaction(self._update_edge_properties_tx, id, properties)
        except Exception as e:
            raise Exception(f"Failed to update edge properties: {e}")


    # Delete edge
    @staticmethod
    def _delete_edge_tx(tx, id: str):
        """
        Private helper function to delete an edge by its ID within a transaction.

        Args:
            tx: Transaction object.
            id (str): The ID of the edge to delete.

        Returns:
            bool: True if at least one edge was deleted, False otherwise.
        """
        try:
            query = "MATCH ()-[r]-() WHERE r.uuid = $id DELETE r RETURN count(r) as deleted_count"
            result = tx.run(query, id=id).single()
            deleted_count = result["deleted_count"]

            return deleted_count > 0
        except Exception as e:
            raise Exception(f"Failed to delete edge: {e}")


    def delete_edge(self, id: str):
        """
        Public function to delete an edge by its ID.

        This function creates a new session and transaction with the graph database,
        and calls the helper function `_delete_edge_tx` to delete the edge.

        Args:
            id (str): The ID of the edge to delete.

        Returns:
            bool: True if at least one edge was deleted, False otherwise.
        """
        if not isinstance(id, str):
            raise TypeError("id must be a string")

        with self.driver.session() as session:
            try:
                return session.write_transaction(self._delete_edge_tx, id)
            except Exception as e:
                raise Exception(f"Failed to delete edge: {e}")


    # Delete all
    @staticmethod
    def _delete_all_tx(tx):
        """
        Private helper function to delete all nodes and relationships within a transaction.

        Args:
            tx: Transaction object.

        Returns:
            bool: True if the deletion operation was successful, False otherwise.
        """
        query = """
            MATCH (n)
            OPTIONAL MATCH (n)-[r]-()
            DELETE n, r
            RETURN count(n) as deleted_nodes, count(r) as deleted_edges
        """
        result = tx.run(query).single()

        return result is not None

    def delete_all(self):
        """
        Public function to delete all nodes and relationships in the graph database.

        Returns:
            bool: True if the deletion operation was successful, False otherwise.
        """
        try:
            with self.driver.session() as session:
                return session.write_transaction(self._delete_all_tx)
        except Exception as e:
            raise Exception(f"Failed to delete all nodes and relationships: {e}")

