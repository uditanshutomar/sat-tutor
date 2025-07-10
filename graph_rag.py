from sentence_transformers import SentenceTransformer
import numpy as np

class GraphRAGQueryEngine:
    def __init__(self, neo4j_driver, llm_client, embedding_model="all-MiniLM-L6-v2"):
        """Initialize the Graph RAG Query Engine"""
        self.driver = neo4j_driver
        self.llm_client = llm_client
        self.embedding_model = SentenceTransformer(embedding_model)
    
    def embed_query(self, query):
        """Embed the query using sentence transformer"""
        return self.embedding_model.encode(query)
    
    def retrieve_relevant_subgraph(self, query, top_k=3):
        """Find relevant questions based on semantic similarity"""
        query_embedding = self.embed_query(query)
        
        with self.driver.session() as session:
            # Get all questions
            questions = session.run("""
                MATCH (q:Question)
                RETURN q.id, q.text
            """).data()
            
            # Calculate similarity scores
            similarities = []
            for q in questions:
                if q["q.text"]:
                    q_embedding = self.embedding_model.encode(q["q.text"])
                    similarity = np.dot(query_embedding, q_embedding) / (
                        np.linalg.norm(query_embedding) * np.linalg.norm(q_embedding)
                    )
                    similarities.append((q["q.id"], similarity))
            
            # Get top-k most similar questions
            top_questions = sorted(similarities, key=lambda x: x[1], reverse=True)[:top_k]
            
            # Retrieve subgraph for each question
            subgraphs = []
            for q_id, _ in top_questions:
                subgraph = session.run("""
                    MATCH (q:Question {id: $q_id})
                    OPTIONAL MATCH (q)-[:BELONGS_TO]->(c:Concept)
                    OPTIONAL MATCH (q)-[:HAS_CORRECT_ANSWER]->(ca:Answer)
                    OPTIONAL MATCH (q)-[:HAS_WRONG_ANSWER]->(wa:Answer)
                    OPTIONAL MATCH (q)-[:HAS_EXPLANATION]->(e:Explanation)
                    RETURN q, c, ca, COLLECT(wa) as wrong_answers, e
                """, {"q_id": q_id}).data()
                subgraphs.extend(subgraph)
            
            return subgraphs
    
    def format_context(self, subgraphs):
        """Format retrieved subgraphs into context for the LLM"""
        context = "Relevant information:\n\n"
        
        for item in subgraphs:
            if 'q' in item and item['q']:
                context += f"Question: {item['q'].get('text', '')}\n"
            
            if 'c' in item and item['c']:
                context += f"Concept: {item['c'].get('name', '')}\n"
            
            if 'ca' in item and item['ca']:
                context += f"Correct Answer: {item['ca'].get('text', '')}\n"
            
            if 'wrong_answers' in item:
                context += "Wrong Answers:\n"
                for wa in item['wrong_answers']:
                    if wa:
                        context += f"- {wa.get('text', '')}\n"
            
            if 'e' in item and item['e']:
                context += f"Explanation: {item['e'].get('text', '')}\n\n"
        
        return context
    
    def generate_response(self, query):
        """Generate a response using GraphRAG"""
        # Retrieve relevant subgraph
        subgraphs = self.retrieve_relevant_subgraph(query)
        
        # Format context from subgraph
        context = self.format_context(subgraphs)
        
        # Generate response using LLM
        prompt = f"""
        You are an expert SAT history tutor. Use the following relevant information to answer the student's question.
        Provide a comprehensive, diverse, and empowering response that helps the student understand the concept deeply.
        
        {context}
        
        Student Question: {query}
        
        Response:
        """
        
        if hasattr(self.llm_client, 'chat'):
            # Using Groq
            response = self.llm_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        else:
            # Using local model
            outputs = self.llm_client(prompt, max_new_tokens=1000, temperature=0.7)
            return outputs[0]["generated_text"] 