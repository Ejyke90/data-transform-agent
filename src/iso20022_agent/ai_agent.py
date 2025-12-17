"""
AI Agent Module for ISO 20022 Schema Analysis
Provides LLM-powered capabilities for intelligent schema understanding
"""
import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

class SchemaAIAgent:
    """AI Agent for intelligent schema analysis and field mapping"""
    
    def __init__(self, provider: str = None):
        """
        Initialize AI agent with specified LLM provider
        
        Args:
            provider: 'openai' or 'anthropic' (defaults to env var LLM_PROVIDER)
        """
        self.provider = provider or os.getenv('LLM_PROVIDER', 'openai')
        self.client = None
        self._initialize_client()
        
    def _initialize_client(self):
        """Initialize the LLM client based on provider"""
        if self.provider == 'openai':
            import openai
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in environment")
            self.client = openai.OpenAI(api_key=api_key)
            self.model = os.getenv('OPENAI_MODEL', 'gpt-4o')
            
        elif self.provider == 'anthropic':
            import anthropic
            api_key = os.getenv('ANTHROPIC_API_KEY')
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not found in environment")
            self.client = anthropic.Anthropic(api_key=api_key)
            self.model = os.getenv('ANTHROPIC_MODEL', 'claude-3-5-sonnet-20241022')
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def _build_schema_context(self, fields: List[Any]) -> str:
        """Build context string from schema fields for LLM"""
        context = "Schema Fields:\n"
        for field in fields[:100]:  # Limit to first 100 fields for context
            context += f"- {field.name} ({field.path}): {field.requirement.value}, {field.multiplicity}\n"
        if len(fields) > 100:
            context += f"... and {len(fields) - 100} more fields\n"
        return context
    
    def _call_llm(self, system_prompt: str, user_prompt: str) -> str:
        """Generic LLM call wrapper"""
        if self.provider == 'openai':
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content
            
        elif self.provider == 'anthropic':
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response.content[0].text
    
    def query_schema(self, fields: List[Any], query: str) -> str:
        """
        Natural language query against schema
        
        Args:
            fields: List of field objects from schema
            query: Natural language question about the schema
            
        Returns:
            AI-generated answer
        """
        system_prompt = """You are an expert in ISO 20022 payment messaging standards.
        You help users understand schema structures, field meanings, and relationships.
        Provide clear, accurate answers based on the schema data provided."""
        
        context = self._build_schema_context(fields)
        user_prompt = f"{context}\n\nQuestion: {query}"
        
        return self._call_llm(system_prompt, user_prompt)
    
    def suggest_field_mappings(self, xsd_fields: List[Any], avro_fields: List[Any]) -> List[Dict[str, Any]]:
        """
        AI-powered field mapping suggestions between XSD and AVRO schemas
        
        Args:
            xsd_fields: List of XSD field objects
            avro_fields: List of AVRO field objects
            
        Returns:
            List of suggested mappings with confidence scores
        """
        system_prompt = """You are an expert in schema mapping and data transformation.
        Analyze the provided XSD and AVRO schemas and suggest intelligent field mappings.
        Consider semantic meaning, not just name similarity. Return JSON format:
        [{"xsd_field": "path", "avro_field": "path", "confidence": 0.95, "reasoning": "why"}]"""
        
        xsd_context = "XSD Schema:\n" + "\n".join([f"{f.name}: {f.path}" for f in xsd_fields[:50]])
        avro_context = "AVRO Schema:\n" + "\n".join([f"{f.name}: {f.path}" for f in avro_fields[:50]])
        
        user_prompt = f"{xsd_context}\n\n{avro_context}\n\nSuggest top 10 field mappings in JSON format."
        
        response = self._call_llm(system_prompt, user_prompt)
        
        try:
            # Extract JSON from response
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                response = response.split("```")[1].split("```")[0]
            return json.loads(response.strip())
        except:
            return []
    
    def generate_documentation(self, fields: List[Any], schema_name: str) -> str:
        """
        Generate human-readable documentation for schema
        
        Args:
            fields: List of field objects
            schema_name: Name of the schema
            
        Returns:
            Markdown-formatted documentation
        """
        system_prompt = """You are a technical writer specializing in payment systems.
        Generate comprehensive, well-structured documentation for ISO 20022 schemas.
        Include overview, field descriptions, mandatory vs optional fields, and usage examples.
        Format output in Markdown."""
        
        context = self._build_schema_context(fields)
        user_prompt = f"Schema: {schema_name}\n\n{context}\n\nGenerate complete documentation."
        
        return self._call_llm(system_prompt, user_prompt)
    
    def explain_field(self, field: Any) -> str:
        """
        Explain what a specific field means in business context
        
        Args:
            field: Field object to explain
            
        Returns:
            Human-readable explanation
        """
        system_prompt = """You are an ISO 20022 expert. Explain payment message fields
        in simple business terms that non-technical users can understand."""
        
        user_prompt = f"""Explain this field:
        Name: {field.name}
        Path: {field.path}
        Type: {field.requirement.value}
        Multiplicity: {field.multiplicity}
        
        What does this field mean? When is it used? What kind of data goes here?"""
        
        return self._call_llm(system_prompt, user_prompt)
    
    def chat(self, message: str, conversation_history: List[Dict[str, str]] = None) -> str:
        """
        Conversational interface for schema exploration
        
        Args:
            message: User's message
            conversation_history: Previous messages [{"role": "user/assistant", "content": "..."}]
            
        Returns:
            Agent's response
        """
        system_prompt = """You are a helpful AI assistant specialized in ISO 20022 schemas.
        Help users understand, analyze, and work with payment message schemas.
        Be conversational, clear, and practical."""
        
        if self.provider == 'openai':
            messages = [{"role": "system", "content": system_prompt}]
            if conversation_history:
                messages.extend(conversation_history)
            messages.append({"role": "user", "content": message})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.8
            )
            return response.choices[0].message.content
            
        elif self.provider == 'anthropic':
            # Anthropic doesn't use system role in messages array
            user_messages = []
            if conversation_history:
                user_messages.extend(conversation_history)
            user_messages.append({"role": "user", "content": message})
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=system_prompt,
                messages=user_messages
            )
            return response.content[0].text
