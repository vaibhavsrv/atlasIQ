import os
from neo4j import GraphDatabase

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

class Neo4jClient:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    def close(self):
        self.driver.close()

    def query(self, query: str, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [record for record in result]

    def create_business_node(self, name: str, industry: str):
        query = (
            "MERGE (b:Business {name: $name, industry: $industry}) "
            "RETURN b"
        )
        return self.query(query, parameters={"name": name, "industry": industry})

    def create_location_node(self, city: str):
        query = (
            "MERGE (l:Location {city: $city}) "
            "RETURN l"
        )
        return self.query(query, parameters={"city": city})

def get_neo4j_client():
    return Neo4jClient()
