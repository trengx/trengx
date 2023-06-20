from .add_edge import AddEdge

class Neo4jAddEdge(AddEdge):
    def add_to_graph(self):
        if not isinstance(self.node1, str):
            raise TypeError('node1 must be a string')
        if not isinstance(self.node2, str):
            raise TypeError('node2 must be a string')
        if not isinstance(self.id, str):
            raise TypeError('id must be a string')
        if not isinstance(self.label, str):
            raise TypeError('label must be a string')
        if not isinstance(self.second_operand, bool):
            raise TypeError('second_operand must be a boolean')
        
        # Construct the Cypher query
        query = f"""
                 MATCH (a),(b) 
                 WHERE a.id = $node1_id AND b.id = $node2_id
                 CREATE (a)-[r:{self.label} {{id: $id, second_operand: $second_operand}}]->(b)
                 RETURN r
                 """

        # Use a Neo4j session to run the constructed query
        with self.driver.session() as session:
            session.run(query, node1_id=self.node1, node2_id=self.node2, id=self.id, second_operand=self.second_operand)
