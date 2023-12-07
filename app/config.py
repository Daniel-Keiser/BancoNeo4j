from neo4j import GraphDatabase

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "12345678"

class Neo4jSession:
    def __init__(self):
        self._driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    def close(self):
        self._driver.close()

    def test_connection(self):
        with self._driver.session() as session:
            result = session.run("RETURN 1 AS value")
            record = result.single()
            if record and record["value"] == 1:
                print("Neo4j connection successful.")
            else:
                print("Neo4j connection failed.")

# Criar uma instância da classe Neo4jSession
neo4j_session = Neo4jSession()

# Testar a conexão e imprimir o resultado
neo4j_session.test_connection()
