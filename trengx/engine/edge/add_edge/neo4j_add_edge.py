from .add_edge import AddEdge

class Neo4jAddEdge(AddEdge):
    def add_to_graph(self):
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
