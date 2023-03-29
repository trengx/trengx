# Graph class
"""Module providing basic graph queries (Neo4j Cypher)"""

class Graph:
    """Class for providing basic graph queries (Neo4j Cypher)"""
    # Initialize graph database class
    def __init__(self, graphdb, uri, user, password):
        self.driver = graphdb.driver(uri, auth=(user, password))

    # Close session
    def close(self)-> None:
        """Function for session closing"""
        self.driver.close()

    # Add node
    @staticmethod
    def _add_node_tx(tx, node_label, key, value):
        query = "MERGE (n:" + node_label + "{ " + key + ": $value })" \
                " RETURN n{.*}"
        result = tx.run(query, value = value)
        return result.single()[0]

    def add_node(self, node_label, key, value):
        """Function for adding node"""
        with self.driver.session() as session:
            result = session.execute_write(self._add_node_tx, node_label, key, value)
            return result

    # Delete node
    @staticmethod
    def _delete_node_tx(tx, node_label, key, value):
        query = "MATCH (n:" + node_label + "{ " + key + ": $value })" \
                " DELETE n"
        result = tx.run(query, value = value)
        return result

    def delete_node(self, node_label, key, value):
        """Function for deleting node"""
        with self.driver.session() as session:
            result = session.execute_write(self._delete_node_tx, node_label, key, value)
            return result
    
    # perform math operation
    @staticmethod    
    def _do_math_tx(tx, id_key, id_value):
        query = "MATCH (in1:num {"+ id_key + ": $id_value})-[:num2op]->(o:op)<-[:num2op]-(in2:num)" \
            " MATCH (o)-[:op2num]->(out:num)" \
            " WITH in1, in2, out, o.name AS opName" \
            " SET out.value = CASE opName" \
            "    WHEN '+' THEN in1.value + in2.value" \
            "    WHEN '-' THEN in1.value - in2.value" \
            "    WHEN '*' THEN in1.value * in2.value" \
            "    WHEN '/' THEN in1.value / in2.value" \
            "    ELSE out.value" \
            " END" \
            " RETURN out.name, out.value"
        result = tx.run(query, id_key = id_key, id_value = id_value) # e.g., <Record out.name='z' out.value=10.4>
        for record in result:
            name = record['out.name']
            value = record['out.value']
            print (name)
            print (value)
        return name, value
    
    def do_math(self, id_key, id_value):
        """Function for doing math"""
        with self.driver.session() as session:
            result = session.execute_write(self._do_math_tx, id_key, id_value)
            self.set_node_prop('name', result[0], 'value', result[1], True)
            return result

    # check the presence of outgoing edge
    @staticmethod
    def _check_outgoing_edge_tx(tx, id_key, id_value):
        query = "MATCH (n:num {"+ id_key + ": $id_value})-[label:num2op]->()" \
                " RETURN COUNT(label) > 0 as has_outgoing_label" 
        result = tx.run(query, id_value = id_value)
        result = result.single()[0]
        return result  # True or False
    
    def check_outgoing_edge(self, id_key, id_value):
        """Function for checking the presence of outgoing edge"""
        with self.driver.session() as session:
            result = session.execute_write(self._check_outgoing_edge_tx, id_key, id_value)
            return result      
    
    # set node property value
    @staticmethod
    def _set_node_prop_tx(tx, id_key, id_value, key, value):
        query = "MATCH (n) WHERE n." + id_key + " = $id_value" \
                " SET n." + key + " = $value" \
                " RETURN n." + key 
        result = tx.run(query, id_value = id_value, value = value)
        return [id_key, id_value, key, result.single()[0]]
    
    def set_node_prop(self, id_key, id_value, key, value, forward):
        """Function for setting node property value"""
        results = []
        with self.driver.session() as session:
            result1 = session.execute_write(self._set_node_prop_tx, id_key, id_value, key, value)
            results.append(result1)
            if forward is True:
                outgoing_edge = self.check_outgoing_edge (id_key, id_value)
                if outgoing_edge is True:
                    result2 = self.do_math (id_key, id_value)
                    results.append(result2)
            return results


    # Get node property value
    @staticmethod
    def _get_node_prop_tx(tx, id_key, id_value, key ):
        query = "MATCH (n) WHERE n." + id_key + " = $id_value" \
                " RETURN n." + key + " as value"
        result = tx.run(query, id_value = id_value)
        return result.single()[0]

    def get_node_prop(self, id_key, id_value, key):
        """Function for getting node property value"""
        with self.driver.session() as session:
            result = session.execute_write(self._get_node_prop_tx, id_key, id_value, key)
            return result
    
    # Remove node property
    @staticmethod
    def _remove_node_prop_tx(tx, id_key, id_value, key ):
        query = "MATCH (n) WHERE n." + id_key + " = $id_value" \
                " REMOVE n." + key
        result = tx.run(query, id_value = id_value)
        return result

    def remove_node_prop(self, id_key, id_value, key):
        """Function for removing node property value"""
        with self.driver.session() as session:
            result = session.execute_write(self._remove_node_prop_tx, id_key, id_value, key)
            return result

    # Add edge
    @staticmethod
    def _add_edge_tx(tx, edge_label:str, out_key:str, out_val, in_key:str, in_val):
        query = "MATCH (n) WHERE n." + out_key + " = $out_val" \
                " MATCH (m) WHERE m." + in_key + " = $in_val" \
                " MERGE (n)-[r:" + edge_label + "]->(m)"
        results = tx.run(query, out_val = out_val, in_val = in_val).data
        return results
    def add_edge(self, edge_label:str, out_key:str, out_val, in_key:str, in_val):
        """Function for adding edge"""
        with self.driver.session() as session:
            results = session.execute_write(self._add_edge_tx, edge_label, out_key, out_val, in_key, in_val)
            return (results)

    # Delete edge
    @staticmethod
    def _delete_edge_tx(tx, edge_label, out_key, out_val, in_key, in_val):
        query = "MATCH (n) WHERE n." + out_key + " = $out_val" \
                " MATCH (m) WHERE m." + in_key + " = $in_val" \
                " MATCH (n)-[r:" + edge_label + "]->(m)" \
                " DELETE r"
        tx.run(query, out_val = out_val, in_val = in_val)
    def delete_edge(self, edge_label, out_key, out_val, in_key, in_val):
        """Function for deleting edge"""
        with self.driver.session() as session:
            session.execute_write(self._delete_edge_tx, edge_label, out_key, out_val, in_key, in_val)
    
    
