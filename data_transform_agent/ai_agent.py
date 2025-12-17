"""
AI Agent Module.

This module provides AI-powered schema transformation capabilities
using LLM to optimize and improve schema conversions.
"""

import os
from typing import Dict, Any, Optional
import json


class AIAgent:
    """AI Agent for intelligent schema transformation."""

    # Default model to use for OpenAI API calls
    DEFAULT_MODEL = "gpt-4"

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize the AI agent.

        Args:
            api_key: OpenAI API key (optional, can use OPENAI_API_KEY env var)
            model: OpenAI model to use (default: gpt-4)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model or os.getenv("OPENAI_MODEL", self.DEFAULT_MODEL)
        self.client = None

        # Only initialize OpenAI client if API key is available
        if self.api_key:
            try:
                from openai import OpenAI

                self.client = OpenAI(api_key=self.api_key)
            except ImportError:
                print(
                    "Warning: OpenAI library not available. AI features will be disabled."
                )

    def enhance_schema_conversion(
        self,
        xsd_info: Dict[str, Any],
        target_format: str,
        converted_schema: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Use AI to enhance and optimize schema conversion.

        Args:
            xsd_info: Original XSD schema information
            target_format: Target format ('json' or 'avro')
            converted_schema: Initially converted schema

        Returns:
            Enhanced schema
        """
        if not self.client:
            # Return original schema if AI is not available
            return converted_schema

        try:
            prompt = self._build_enhancement_prompt(xsd_info, target_format, converted_schema)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert in schema design and data transformation. "
                        "Your task is to review and enhance schema conversions.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
            )

            enhanced_schema_str = response.choices[0].message.content
            # Try to extract JSON from the response
            enhanced_schema = self._extract_json_from_response(enhanced_schema_str)

            return enhanced_schema if enhanced_schema else converted_schema

        except Exception as e:
            print(f"Warning: AI enhancement failed: {e}")
            return converted_schema

    def suggest_improvements(
        self, xsd_info: Dict[str, Any], target_format: str
    ) -> Dict[str, Any]:
        """
        Get AI suggestions for schema conversion.

        Args:
            xsd_info: Original XSD schema information
            target_format: Target format ('json' or 'avro')

        Returns:
            Dictionary with suggestions
        """
        if not self.client:
            return {"suggestions": ["AI enhancement not available - API key not configured"]}

        try:
            prompt = f"""
Analyze the following XSD schema and provide suggestions for converting it to {target_format.upper()} format:

XSD Schema Info:
{json.dumps(xsd_info, indent=2)}

Please provide:
1. Key considerations for the conversion
2. Potential issues or edge cases
3. Best practices to follow
4. Recommendations for field naming and structure
"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert in schema design and data transformation.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.5,
            )

            suggestions_text = response.choices[0].message.content
            return {"suggestions": suggestions_text.split("\n")}

        except Exception as e:
            return {"suggestions": [f"Failed to get AI suggestions: {e}"]}

    def _build_enhancement_prompt(
        self, xsd_info: Dict[str, Any], target_format: str, converted_schema: Dict[str, Any]
    ) -> str:
        """Build prompt for schema enhancement."""
        return f"""
Review and enhance the following schema conversion from XSD to {target_format.upper()}:

Original XSD Schema Info:
{json.dumps(xsd_info, indent=2)}

Converted {target_format.upper()} Schema:
{json.dumps(converted_schema, indent=2)}

Please review the conversion and provide an enhanced version that:
1. Follows {target_format.upper()} best practices
2. Uses appropriate type mappings
3. Includes helpful descriptions where applicable
4. Optimizes the structure for common use cases

Return ONLY the enhanced schema in valid JSON format, without any explanation.
"""

    def _extract_json_from_response(self, response: str) -> Optional[Dict[str, Any]]:
        """Extract JSON object from AI response."""
        try:
            # Try to parse the entire response as JSON
            return json.loads(response)
        except json.JSONDecodeError:
            # Try to find JSON block in markdown code block
            if "```json" in response:
                start = response.find("```json") + 7
                end = response.find("```", start)
                if end > start:
                    try:
                        return json.loads(response[start:end].strip())
                    except json.JSONDecodeError:
                        pass
            # Try to find any JSON object
            start = response.find("{")
            end = response.rfind("}") + 1
            if start >= 0 and end > start:
                try:
                    return json.loads(response[start:end])
                except json.JSONDecodeError:
                    pass
        return None

    def is_available(self) -> bool:
        """Check if AI agent is available."""
        return self.client is not None
