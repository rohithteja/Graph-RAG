"""
Simple Neo4j Knowledge Graph for Superhero Demo
"""
from neo4j import GraphDatabase
import json

class SuperheroGraph:
    def __init__(self, uri=None, user=None, password=None):
        import os
        # Use environment variables if available, otherwise defaults
        uri = uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
        user = user or os.getenv("NEO4J_USER", "neo4j")
        password = password or os.getenv("NEO4J_PASSWORD", "password")
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        self.driver.close()
    
    def clear_graph(self):
        """Clear all nodes and relationships"""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
    
    def create_superhero_graph(self):
        """Create the superhero knowledge graph"""
        with self.driver.session() as session:
            # Create heroes
            heroes = [
                {
                    "name": "Superman",
                    "real_name": "Clark Kent",
                    "powers": ["super strength", "flight", "invulnerability", "heat vision"],
                    "origin": "Krypton",
                    "team": "Justice League"
                },
                {
                    "name": "Batman", 
                    "real_name": "Bruce Wayne",
                    "powers": ["intelligence", "martial arts", "technology"],
                    "origin": "Gotham City",
                    "team": "Justice League"
                },
                {
                    "name": "Wonder Woman",
                    "real_name": "Diana Prince", 
                    "powers": ["super strength", "lasso of truth", "combat skills"],
                    "origin": "Themyscira",
                    "team": "Justice League"
                },
                {
                    "name": "Flash",
                    "real_name": "Barry Allen",
                    "powers": ["super speed", "time travel"],
                    "origin": "Central City", 
                    "team": "Justice League"
                }
            ]
            
            # Create hero nodes
            for hero in heroes:
                session.run("""
                    CREATE (h:Hero {
                        name: $name,
                        real_name: $real_name,
                        powers: $powers,
                        origin: $origin,
                        team: $team
                    })
                """, **hero)
            
            # Create Justice League team node
            session.run("""
                CREATE (t:Team {
                    name: "Justice League",
                    type: "superhero team",
                    founded: "1960"
                })
            """)
            
            # Create relationships
            relationships = [
                ("Superman", "Batman", "TEAMMATE"),
                ("Superman", "Wonder Woman", "TEAMMATE"), 
                ("Superman", "Flash", "TEAMMATE"),
                ("Batman", "Wonder Woman", "TEAMMATE"),
                ("Batman", "Flash", "TEAMMATE"),
                ("Wonder Woman", "Flash", "TEAMMATE"),
                ("Superman", "Batman", "ALLY"),
                ("Superman", "Wonder Woman", "ALLY"),
                ("Superman", "Flash", "ALLY")
            ]
            
            # Create TEAMMATE relationships
            for hero1, hero2, rel_type in relationships:
                session.run("""
                    MATCH (h1:Hero {name: $hero1})
                    MATCH (h2:Hero {name: $hero2})
                    CREATE (h1)-[:""" + rel_type + """]->(h2)
                """, hero1=hero1, hero2=hero2)
            
            # Create MEMBER_OF relationships with Justice League
            for hero in heroes:
                session.run("""
                    MATCH (h:Hero {name: $name})
                    MATCH (t:Team {name: "Justice League"})
                    CREATE (h)-[:MEMBER_OF]->(t)
                """, name=hero["name"])
            
            print("✅ Superhero knowledge graph created!")
    
    def query_graph(self, query_type, entity=None):
        """Query the graph for different types of information"""
        with self.driver.session() as session:
            
            if query_type == "all_heroes":
                result = session.run("""
                    MATCH (h:Hero)
                    RETURN h.name as name, h.real_name as real_name, h.powers as powers, h.origin as origin, h.team as team, h.description as description
                """)
                return [dict(record) for record in result]
            
            elif query_type == "hero_relationships" and entity:
                result = session.run("""
                    MATCH (h:Hero {name: $entity})-[r]-(connected)
                    RETURN h.name as hero, type(r) as relationship, connected.name as connected_to, labels(connected) as connected_type
                """, entity=entity)
                return [dict(record) for record in result]
            
            elif query_type == "teammates" and entity:
                result = session.run("""
                    MATCH (h:Hero {name: $entity})-[:TEAMMATE]-(teammate:Hero)
                    RETURN teammate.name as teammate, teammate.real_name as real_name
                """, entity=entity)
                return [dict(record) for record in result]
            
            elif query_type == "team_members":
                result = session.run("""
                    MATCH (h:Hero)-[:MEMBER_OF]->(t:Team {name: "Justice League"})
                    RETURN h.name as hero, h.powers as powers
                """)
                return [dict(record) for record in result]
            
            elif query_type == "hero_details" and entity:
                result = session.run("""
                    MATCH (h:Hero {name: $entity})
                    RETURN h.name as name, h.real_name as real_name, h.powers as powers, 
                           h.origin as origin, h.team as team, h.description as description
                """, entity=entity)
                return [dict(record) for record in result]
            
            return []
    
    def visualize_graph(self):
        """Get graph data for visualization"""
        with self.driver.session() as session:
            # Get all nodes
            nodes_result = session.run("""
                MATCH (n) 
                RETURN id(n) as id, labels(n) as labels, properties(n) as props
            """)
            nodes = []
            for record in nodes_result:
                node = {
                    "id": record["id"],
                    "labels": record["labels"],
                    "properties": dict(record["props"])
                }
                nodes.append(node)
            
            # Get all relationships  
            rels_result = session.run("""
                MATCH (a)-[r]->(b)
                RETURN id(a) as source, id(b) as target, type(r) as type, properties(r) as props
            """)
            relationships = []
            for record in rels_result:
                rel = {
                    "source": record["source"],
                    "target": record["target"], 
                    "type": record["type"],
                    "properties": dict(record["props"])
                }
                relationships.append(rel)
            
            return {"nodes": nodes, "relationships": relationships}

if __name__ == "__main__":
    # Test the graph
    graph = SuperheroGraph()
    try:
        graph.clear_graph()
        graph.create_superhero_graph()
        
        # Test queries
        print("\n🦸‍♂️ All Heroes:")
        heroes = graph.query_graph("all_heroes")
        for hero in heroes:
            print(f"- {hero['name']} ({hero['real_name']})")
        
        print(f"\n🤝 Superman's Relationships:")
        relationships = graph.query_graph("hero_relationships", "Superman")
        for rel in relationships:
            print(f"- {rel['relationship']} with {rel['connected_to']}")
            
    finally:
        graph.close()
