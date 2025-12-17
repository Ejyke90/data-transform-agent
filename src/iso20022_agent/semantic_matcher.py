"""
Semantic Field Matcher using LLM
Intelligent field matching based on semantic meaning, not just names
"""
from typing import List, Dict, Any, Tuple, Optional
import json
import re


class SemanticFieldMatcher:
    """LLM-powered semantic field matching"""
    
    def __init__(self, ai_agent=None):
        """
        Initialize semantic matcher
        
        Args:
            ai_agent: SchemaAIAgent instance (optional, will create if not provided)
        """
        self.ai_agent = ai_agent
        
    def match_fields(self, xsd_fields: List[Any], avro_fields: List[Any], 
                     use_llm: bool = True, batch_size: int = 20) -> Dict[int, Tuple[Any, Any, float]]:
        """
        Match XSD and AVRO fields using semantic understanding
        
        Args:
            xsd_fields: List of XSD field objects
            avro_fields: List of AVRO field objects
            use_llm: If True, use LLM for semantic matching (default). If False, use fuzzy only.
            batch_size: Number of fields to match per LLM call
            
        Returns:
            Dict mapping xsd_field_id -> (xsd_field, avro_field, confidence_score)
        """
        if use_llm and self.ai_agent:
            return self._semantic_match_with_llm(xsd_fields, avro_fields, batch_size)
        else:
            return self._fuzzy_match(xsd_fields, avro_fields)
    
    def _semantic_match_with_llm(self, xsd_fields: List[Any], avro_fields: List[Any], 
                                  batch_size: int) -> Dict[int, Tuple[Any, Any, float]]:
        """Use LLM to understand semantic meaning and match fields"""
        matched_pairs = {}
        xsd_matched = set()
        avro_matched = set()
        
        # Process in batches to avoid token limits
        for i in range(0, len(xsd_fields), batch_size):
            xsd_batch = xsd_fields[i:i+batch_size]
            
            # Build context for LLM
            xsd_context = self._build_field_context(xsd_batch, "XSD")
            avro_context = self._build_field_context(avro_fields, "AVRO")
            
            system_prompt = """You are an expert in ISO 20022 payment schemas and data mapping.
Your task is to match XSD fields to AVRO fields based on SEMANTIC MEANING, not just name similarity.

Consider:
1. Business meaning (e.g., "MsgId" and "message_identification" mean the same)
2. Data purpose (payment amount, debtor info, etc.)
3. Field hierarchy and context
4. ISO 20022 standard definitions

Return ONLY valid JSON array with high-confidence matches:
[
  {
    "xsd_field": "field_name",
    "xsd_path": "full/path",
    "avro_field": "field_name", 
    "avro_path": "full.path",
    "confidence": 0.95,
    "reasoning": "Both represent message identification"
  }
]

Only include matches with confidence >= 0.7. Return empty array [] if no good matches."""

            user_prompt = f"""Match these XSD fields to AVRO fields:

{xsd_context}

Available AVRO fields:
{avro_context}

Return JSON array of matches."""

            try:
                response = self.ai_agent._call_llm(system_prompt, user_prompt)
                
                # Parse JSON response
                matches = self._parse_llm_response(response)
                
                # Convert to matched pairs
                for match in matches:
                    if match['confidence'] >= 0.7:
                        xsd_field = self._find_field_by_path(xsd_batch, match['xsd_path'])
                        avro_field = self._find_field_by_path(avro_fields, match['avro_path'])
                        
                        if xsd_field and avro_field:
                            xsd_id = id(xsd_field)
                            avro_id = id(avro_field)
                            
                            if xsd_id not in xsd_matched and avro_id not in avro_matched:
                                matched_pairs[xsd_id] = (xsd_field, avro_field, match['confidence'])
                                xsd_matched.add(xsd_id)
                                avro_matched.add(avro_id)
                
            except Exception as e:
                print(f"LLM matching error (falling back to fuzzy): {e}")
                # Fall back to fuzzy for this batch
                fuzzy_matches = self._fuzzy_match(xsd_batch, avro_fields)
                for xsd_id, (xsd_f, avro_f, conf) in fuzzy_matches.items():
                    if xsd_id not in xsd_matched and id(avro_f) not in avro_matched:
                        matched_pairs[xsd_id] = (xsd_f, avro_f, conf)
                        xsd_matched.add(xsd_id)
                        avro_matched.add(id(avro_f))
        
        # Fill remaining with fuzzy matching
        unmatched_xsd = [f for f in xsd_fields if id(f) not in xsd_matched]
        unmatched_avro = [f for f in avro_fields if id(f) not in avro_matched]
        
        if unmatched_xsd and unmatched_avro:
            fuzzy_matches = self._fuzzy_match(unmatched_xsd, unmatched_avro)
            for xsd_id, (xsd_f, avro_f, conf) in fuzzy_matches.items():
                if id(avro_f) not in avro_matched:
                    matched_pairs[xsd_id] = (xsd_f, avro_f, conf)
                    avro_matched.add(id(avro_f))
        
        return matched_pairs
    
    def _fuzzy_match(self, xsd_fields: List[Any], avro_fields: List[Any]) -> Dict[int, Tuple[Any, Any, float]]:
        """Fallback fuzzy matching using string similarity"""
        matched_pairs = {}
        avro_matched = set()
        
        def normalize(name):
            return name.lower().replace('_', '').replace('-', '')
        
        def get_path_components(path):
            return [p for p in re.split(r'[/.]', path) if p]
        
        # Build index for quick lookup
        avro_index = {}
        for avro_f in avro_fields:
            components = get_path_components(avro_f.path)
            
            # Index by field name
            if components:
                norm_name = normalize(components[-1])
                if norm_name not in avro_index:
                    avro_index[norm_name] = []
                avro_index[norm_name].append(avro_f)
            
            # Index by full path
            full_path = '.'.join(components)
            if full_path not in avro_index:
                avro_index[full_path] = []
            avro_index[full_path].append(avro_f)
        
        # Match XSD fields
        for xsd_f in xsd_fields:
            xsd_components = get_path_components(xsd_f.path)
            xsd_id = id(xsd_f)
            
            # Try exact path match first
            xsd_path = '.'.join(xsd_components)
            if xsd_path in avro_index:
                for avro_f in avro_index[xsd_path]:
                    if id(avro_f) not in avro_matched:
                        matched_pairs[xsd_id] = (xsd_f, avro_f, 1.0)
                        avro_matched.add(id(avro_f))
                        break
                continue
            
            # Try field name match
            if xsd_components:
                norm_name = normalize(xsd_components[-1])
                if norm_name in avro_index:
                    for avro_f in avro_index[norm_name]:
                        if id(avro_f) not in avro_matched:
                            matched_pairs[xsd_id] = (xsd_f, avro_f, 0.8)
                            avro_matched.add(id(avro_f))
                            break
        
        return matched_pairs
    
    def _build_field_context(self, fields: List[Any], schema_type: str) -> str:
        """Build concise context string for LLM"""
        context = f"{schema_type} Fields:\n"
        for field in fields[:50]:  # Limit for token efficiency
            context += f"- {field.name} | Path: {field.path} | Type: {field.requirement.value}\n"
        if len(fields) > 50:
            context += f"... and {len(fields) - 50} more fields\n"
        return context
    
    def _parse_llm_response(self, response: str) -> List[Dict]:
        """Parse LLM JSON response"""
        try:
            # Extract JSON from response
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                response = response.split("```")[1].split("```")[0]
            
            response = response.strip()
            
            # Handle array or single object
            matches = json.loads(response)
            if isinstance(matches, dict):
                matches = [matches]
            
            return matches
        except:
            return []
    
    def _find_field_by_path(self, fields: List[Any], path: str) -> Optional[Any]:
        """Find field object by path"""
        # Normalize path separators
        path_normalized = path.replace('/', '.').replace('\\', '.')
        
        for field in fields:
            field_path_normalized = field.path.replace('/', '.').replace('\\', '.')
            if field_path_normalized == path_normalized or field.path == path:
                return field
            
            # Also try matching by name if full path doesn't match
            if field.name == path or field.name in path:
                return field
        
        return None
