import re
import json
from groq import Groq
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

class SemanticAugmenter:
    def __init__(self, use_groq=False, api_key=None, model_name="TheBloke/Llama-2-13B-GGUF"):
        """Initialize the semantic augmenter with either Groq or local model"""
        self.use_groq = use_groq
        if use_groq:
            self.client = Groq(api_key=api_key)
            self.model_name = model_name
        else:
            # Load local quantized model optimized for AMD
            print("Initializing local model for semantic augmentation...")
            self.model_name = model_name
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                device_map="cpu",
                low_cpu_mem_usage=True,
                torch_dtype=torch.float16
            )
            # Move to ROCm if available
            if torch.backends.mps.is_available():
                self.model = self.model.to('mps')
                print("Using AMD GPU acceleration for semantic augmentation!")
            
            self.pipe = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                max_new_tokens=500,
                do_sample=True,
                temperature=0.7,
                top_p=0.95,
                batch_size=1
            )
            print("Local model for semantic augmentation initialized!")
    
    def extract_entities_and_relations(self, text):
        """Extract semantic entities and relationships from text"""
        prompt = f"""
        Extract key entities and their relationships from the following educational text:
        
        {text}
        
        Return the result as a JSON with the following structure:
        {{
            "entities": [
                {{"name": "entity_name", "type": "concept/person/event/term"}}
            ],
            "relationships": [
                {{"source": "entity1", "relation": "supports/contradicts/explains/relates_to", "target": "entity2"}}
            ]
        }}
        """
        
        if self.use_groq:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=1000
            )
            result = response.choices[0].message.content
        else:
            outputs = self.pipe(prompt, max_new_tokens=1000, temperature=0.2)
            result = outputs[0]["generated_text"]
        
        # Extract JSON from response
        try:
            json_match = re.search(r'({.*})', result, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))
            return {"entities": [], "relationships": []}
        except:
            return {"entities": [], "relationships": []}
    
    def generate_explanation(self, question, correct_answer, wrong_answers):
        """Generate detailed explanation for a question"""
        prompt = f"""
        Generate a detailed explanation for the following SAT question:
        
        Question: {question}
        Correct Answer: {correct_answer}
        Wrong Answers: {', '.join(wrong_answers)}
        
        Provide:
        1. Why the correct answer is right
        2. Why each wrong answer is incorrect
        3. Key concepts being tested
        4. Tips for similar questions
        """
        
        if self.use_groq:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        else:
            outputs = self.pipe(prompt, max_new_tokens=1000, temperature=0.7)
            return outputs[0]["generated_text"]
    
    def extract_concepts(self, text):
        """Extract key concepts from text"""
        prompt = f"""
        Extract key historical concepts from the following text:
        
        {text}
        
        Return the result as a JSON array of concept objects:
        [
            {{"name": "concept_name", "description": "brief_description"}}
        ]
        """
        
        if self.use_groq:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=500
            )
            result = response.choices[0].message.content
        else:
            outputs = self.pipe(prompt, max_new_tokens=500, temperature=0.2)
            result = outputs[0]["generated_text"]
        
        try:
            json_match = re.search(r'(\[.*\])', result, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))
            return []
        except:
            return [] 
    def augment(self, text):
        """Augment the given text using the semantic augmenter"""
        if self.use_groq:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": text}],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        else:
            outputs = self.pipe(text, max_new_tokens=500, temperature=0.7)
            return outputs[0]["generated_text"]
