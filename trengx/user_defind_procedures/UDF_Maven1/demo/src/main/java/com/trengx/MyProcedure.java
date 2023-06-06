// User Defined Function for Neo4j
package com.trengx;

import org.neo4j.graphdb.GraphDatabaseService;
import org.neo4j.graphdb.Result;
import org.neo4j.graphdb.Transaction;
import org.neo4j.procedure.Context;
import org.neo4j.procedure.Description;
import org.neo4j.procedure.Name;
import org.neo4j.procedure.UserFunction;

import java.util.HashMap;
import java.util.Map;

public class MyProcedure {

    @Context
    public GraphDatabaseService db;

    @UserFunction
    @Description("com.trengx.getNameByUuid(uuid) - Get node name by uuid.")
    public String getNameByUuid(@Name("uuid") String uuid) {
        Map<String, Object> params = new HashMap<>();
        params.put("uuid", uuid);

        try (Transaction tx = db.beginTx()) {
            Result result = tx.execute("MATCH (n) WHERE n.uuid = $uuid RETURN n.name as name", params);

            if (result.hasNext()) {
                String name = (String) result.next().get("name");
                return name;
            } else {
                return null;
            }
        }
    }
}
