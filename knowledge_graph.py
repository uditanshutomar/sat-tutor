from neo4j import GraphDatabase
from tqdm import tqdm

class KnowledgeGraphBuilder:
    def __init__(self, uri, username, password):
        """Initialize Neo4j connection"""
        self.driver = GraphDatabase.driver(uri, auth=(username, password))
        
    def close(self):
        """Close the Neo4j connection"""
        self.driver.close()
        
    def create_schema(self):
        """Create constraints and indexes for the knowledge graph"""
        with self.driver.session() as session:
            # Create constraints for unique nodes
            session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (q:Question) REQUIRE q.id IS UNIQUE")
            session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (c:Concept) REQUIRE c.name IS UNIQUE")
            
    def build_graph(self, data):
        """Build the knowledge graph from processed data"""
        with self.driver.session() as session:
            for item in tqdm(data, desc="Building Knowledge Graph"):
                # Create question node
                session.run("""
                    MERGE (q:Question {id: $question_id})
                    SET q.text = $question_text,
                        q.difficulty = $difficulty
                """, item)
                
                # Create concept node and relationship
                session.run("""
                    MERGE (c:Concept {name: $concept})
                    MERGE (q:Question {id: $question_id})
                    MERGE (q)-[:BELONGS_TO]->(c)
                """, item)
                
                # Create correct answer node and relationship
                session.run("""
                    MERGE (q:Question {id: $question_id})
                    MERGE (a:Answer {text: $correct_answer})
                    MERGE (q)-[:HAS_CORRECT_ANSWER]->(a)
                """, item)
                
                # Create explanation node and relationship
                if item["explanation"]:
                    session.run("""
                        MERGE (q:Question {id: $question_id})
                        MERGE (e:Explanation {text: $explanation})
                        MERGE (q)-[:HAS_EXPLANATION]->(e)
                    """, item)
                
                # Create answer choice nodes and relationships
                for i, choice in enumerate(item["answer_choices"]):
                    if choice:
                        is_correct = choice == item["correct_answer"]
                        rel_type = "HAS_CORRECT_ANSWER" if is_correct else "HAS_WRONG_ANSWER"
                        
                        session.run(f"""
                            MERGE (q:Question {{id: $question_id}})
                            MERGE (a:Answer {{text: $choice}})
                            MERGE (q)-[:{rel_type}]->(a)
                        """, {"question_id": item["question_id"], "choice": choice})
    
    def get_related_questions(self, concept, limit=5):
        """Get questions related to a specific concept"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (q:Question)-[:BELONGS_TO]->(c:Concept {name: $concept})
                RETURN q.id as id, q.text as text
                LIMIT $limit
            """, {"concept": concept, "limit": limit})
            return [dict(record) for record in result]
    
    def get_question_context(self, question_id):
        """Get full context for a specific question"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (q:Question {id: $question_id})
                OPTIONAL MATCH (q)-[:BELONGS_TO]->(c:Concept)
                OPTIONAL MATCH (q)-[:HAS_CORRECT_ANSWER]->(ca:Answer)
                OPTIONAL MATCH (q)-[:HAS_WRONG_ANSWER]->(wa:Answer)
                OPTIONAL MATCH (q)-[:HAS_EXPLANATION]->(e:Explanation)
                RETURN q, c, ca, COLLECT(wa) as wrong_answers, e
            """, {"question_id": question_id})
            return result.single() 