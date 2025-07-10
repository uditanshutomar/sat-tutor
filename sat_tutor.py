import os
import pandas as pd
from dotenv import load_dotenv
from groq import Groq
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from neo4j import GraphDatabase
from knowledge_graph import KnowledgeGraphBuilder
from semantic_augmenter import SemanticAugmenter
from graph_rag import GraphRAGQueryEngine
import torch

def load_environment():
    """Load environment variables"""
    load_dotenv()
    return {
        'neo4j_uri': os.getenv('NEO4J_URI'),
        'neo4j_user': os.getenv('NEO4J_USER'),
        'neo4j_password': os.getenv('NEO4J_PASSWORD'),
        'groq_api_key': os.getenv('GROQ_API_KEY')
    }

def preprocess_dataset(df, llm_client=None):
    """Preprocess the SAT dataset"""
    # Handle missing values
    df = df.fillna("")
    
    # Extract concepts, questions, answers, and explanations
    processed_data = []
    
    for _, row in df.iterrows():
        # Extract subject as concept
        concept = row.get("subject", "")
        
        # Create answer choices list
        answer_choices = [
            row.get("A", ""),
            row.get("B", ""),
            row.get("C", ""),
            row.get("D", ""),
            row.get("E", "")
        ]
        
        # Get correct answer - handle both single character and string answers
        answer = row.get("answer", "")
        if answer and len(answer) > 0:
            # If answer is a single character (A, B, C, D, E)
            if len(answer) == 1:
                index = ord(answer) - ord('A')
                if 0 <= index < len(answer_choices):
                    correct_answer = answer_choices[index]
                else:
                    correct_answer = ""
            # If answer is a string (like "A.", "B.", etc.)
            else:
                # Extract the first character and remove any punctuation
                first_char = answer[0].upper()
                if first_char in ['A', 'B', 'C', 'D', 'E']:
                    index = ord(first_char) - ord('A')
                    if 0 <= index < len(answer_choices):
                        correct_answer = answer_choices[index]
                    else:
                        correct_answer = ""
                else:
                    correct_answer = ""
        else:
            correct_answer = ""
        
        # Generate explanation if LLM client is provided
        explanation = ""
        if llm_client:
            explanation = generate_explanation(
                row.get("prompt", ""),
                correct_answer,
                answer_choices,
                llm_client
            )
        
        item = {
            "question_id": str(row.get("id", "")),
            "question_text": row.get("prompt", ""),
            "correct_answer": correct_answer,
            "explanation": explanation,
            "concept": concept,
            "difficulty": "medium",  # Can be enhanced with difficulty detection
            "answer_choices": answer_choices
        }
        processed_data.append(item)
    
    return processed_data

def generate_explanation(question, correct_answer, answer_choices, llm_client):
    """Generate a detailed explanation for a question using the LLM"""
    prompt = f"""
    Generate a detailed explanation for the following SAT question:
    
    Question: {question}
    
    Answer Choices:
    A) {answer_choices[0]}
    B) {answer_choices[1]}
    C) {answer_choices[2]}
    D) {answer_choices[3]}
    E) {answer_choices[4]}
    
    Correct Answer: {correct_answer}
    
    Please provide:
    1. A clear explanation of why the correct answer is right
    2. Brief explanations of why other options are incorrect
    3. Key concepts or skills being tested
    4. Tips for approaching similar questions
    
    Explanation:
    """
    
    if isinstance(llm_client, Groq):
        response = llm_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    else:
        outputs = llm_client.pipe(prompt, max_new_tokens=500, temperature=0.7)
        return outputs[0]["generated_text"]

def initialize_components(env_vars, use_groq=False):
    """Initialize all components of the system"""
    # Initialize LLM client
    if use_groq:
        llm_client = Groq(api_key=env_vars['groq_api_key'])
    else:
        # Initialize local quantized model optimized for AMD GPUs
        print("Initializing local LLaMA model...")
        model_name = "TheBloke/Llama-2-13B-GGUF"  # Using GGUF format which works better with AMD
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="cpu",  # Start with CPU, we'll optimize memory usage
            low_cpu_mem_usage=True,
            torch_dtype=torch.float16
        )
        # Move to ROCm if available
        if torch.backends.mps.is_available():
            model = model.to('mps')
            print("Using AMD GPU acceleration!")
        
        llm_client = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=500,
            do_sample=True,
            temperature=0.7,
            top_p=0.95,
            batch_size=1  # Prevent memory issues
        )
        print("Local model initialized successfully!")
    
    # Initialize Neo4j connection
    print("Connecting to Neo4j...")
    kg_builder = KnowledgeGraphBuilder(
        env_vars['neo4j_uri'],
        env_vars['neo4j_user'],
        env_vars['neo4j_password']
    )
    print("Neo4j connection established!")
    
    # Initialize semantic augmenter
    print("Initializing semantic augmenter...")
    semantic_augmenter = SemanticAugmenter(use_groq=False, api_key=None)
    print("Semantic augmenter initialized!")
    
    # Initialize query engine
    print("Initializing query engine...")
    query_engine = GraphRAGQueryEngine(kg_builder.driver, llm_client)
    print("Query engine initialized!")
    
    return kg_builder, semantic_augmenter, query_engine, llm_client

def main():
    # Load environment variables
    env_vars = load_environment()
    
    # Initialize components
    kg_builder, semantic_augmenter, query_engine, llm_client = initialize_components(env_vars)
    
    try:
        # Load and preprocess dataset
        sat_data_path = "/Users/uditanshutomar/Downloads/sat_world_and_us_history.csv"
        df = pd.read_csv(sat_data_path)
        processed_data = preprocess_dataset(df, llm_client)
        
        # Create knowledge graph schema
        kg_builder.create_schema()
        
        # Build knowledge graph
        kg_builder.build_graph(processed_data)
        
        # Interactive loop
        print("SAT History Tutor initialized! Type 'quit' to exit.")
        while True:
            question = input("\nYour question: ")
            if question.lower() == 'quit':
                break
            
            # Generate response using GraphRAG
            response = query_engine.generate_response(question)
            print("\nTutor's response:")
            print(response)
    
    finally:
        # Clean up
        kg_builder.close()

if __name__ == "__main__":
    main() 