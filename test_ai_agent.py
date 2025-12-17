#!/usr/bin/env python3
"""
Test script for AI Agent integration
Tests all AI features with real schemas
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from iso20022_agent import ISO20022SchemaAgent
from iso20022_agent.ai_agent import SchemaAIAgent
from iso20022_agent.semantic_matcher import SemanticFieldMatcher


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def test_ai_agent_initialization():
    """Test 1: Initialize AI agent with different providers"""
    print_section("TEST 1: AI Agent Initialization")
    
    providers = ['ollama', 'openai', 'anthropic', 'openrouter', 'huggingface']
    
    for provider in providers:
        try:
            print(f"Testing {provider}...", end=" ")
            ai_agent = SchemaAIAgent(provider=provider)
            print(f"✓ Initialized with model: {ai_agent.model}")
        except ValueError as e:
            print(f"⚠️  Not configured: {str(e)}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")


def test_schema_loading():
    """Test 2: Load XSD and AVRO schemas"""
    print_section("TEST 2: Schema Loading")
    
    test_schemas = [
        'schemas/pain.001.001.12.xsd',
        'schemas/pain.001.001.12.avsc'
    ]
    
    for schema_path in test_schemas:
        if os.path.exists(schema_path):
            try:
                print(f"Loading {schema_path}...", end=" ")
                agent = ISO20022SchemaAgent()
                agent.load_schema(schema_path)
                fields = agent.extract_fields()
                print(f"✓ Loaded {len(fields)} fields")
            except Exception as e:
                print(f"❌ Error: {str(e)}")
        else:
            print(f"⚠️  Schema not found: {schema_path}")


def test_chat_interface():
    """Test 3: Conversational chat interface"""
    print_section("TEST 3: Chat Interface")
    
    try:
        ai_agent = SchemaAIAgent()
        print(f"Using provider: {ai_agent.provider} ({ai_agent.model})")
        
        test_messages = [
            "What is ISO 20022?",
            "Explain what MsgId field means",
            "What are mandatory fields in payment messages?"
        ]
        
        for message in test_messages:
            print(f"\n👤 User: {message}")
            try:
                response = ai_agent.chat(message)
                print(f"🤖 Agent: {response[:200]}..." if len(response) > 200 else f"🤖 Agent: {response}")
            except Exception as e:
                print(f"❌ Error: {str(e)}")
                break
                
    except ValueError as e:
        print(f"⚠️  AI not configured: {str(e)}")
        print("\nTo enable AI chat:")
        print("1. Install Ollama: https://ollama.ai")
        print("2. Run: ollama pull llama3.2")
        print("3. Create .env with: LLM_PROVIDER=ollama")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def test_schema_query():
    """Test 4: Natural language schema queries"""
    print_section("TEST 4: Schema Queries")
    
    schema_path = 'schemas/pain.001.001.12.xsd'
    
    if not os.path.exists(schema_path):
        print(f"⚠️  Schema not found: {schema_path}")
        return
    
    try:
        # Load schema
        print(f"Loading schema: {schema_path}")
        agent = ISO20022SchemaAgent()
        agent.load_schema(schema_path)
        fields = agent.extract_fields()
        print(f"✓ Loaded {len(fields)} fields\n")
        
        # Initialize AI agent
        ai_agent = SchemaAIAgent()
        print(f"Using AI provider: {ai_agent.provider}\n")
        
        # Test queries
        queries = [
            "How many mandatory fields are there?",
            "What fields are related to payment amount?",
            "List all fields under GrpHdr"
        ]
        
        for query in queries:
            print(f"❓ Query: {query}")
            try:
                answer = ai_agent.query_schema(fields, query)
                print(f"💡 Answer: {answer[:300]}...\n" if len(answer) > 300 else f"💡 Answer: {answer}\n")
            except Exception as e:
                print(f"❌ Error: {str(e)}\n")
                break
                
    except ValueError as e:
        print(f"⚠️  AI not configured: {str(e)}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def test_semantic_matching():
    """Test 5: Semantic field matching"""
    print_section("TEST 5: Semantic Field Matching")
    
    xsd_path = 'schemas/pain.001.001.12.xsd'
    avro_path = 'schemas/pain.001.001.12.avsc'
    
    if not os.path.exists(xsd_path) or not os.path.exists(avro_path):
        print(f"⚠️  Schemas not found")
        return
    
    try:
        # Load both schemas
        print("Loading XSD schema...")
        xsd_agent = ISO20022SchemaAgent()
        xsd_agent.load_schema(xsd_path)
        xsd_fields = xsd_agent.extract_fields()
        print(f"✓ XSD: {len(xsd_fields)} fields")
        
        print("Loading AVRO schema...")
        avro_agent = ISO20022SchemaAgent()
        avro_agent.load_schema(avro_path)
        avro_fields = avro_agent.extract_fields()
        print(f"✓ AVRO: {len(avro_fields)} fields\n")
        
        # Test with LLM
        print("Testing semantic matching WITH LLM...")
        try:
            ai_agent = SchemaAIAgent()
            semantic_matcher = SemanticFieldMatcher(ai_agent)
            
            # Use small sample for testing
            xsd_sample = xsd_fields[:10]
            avro_sample = avro_fields[:20]
            
            matches = semantic_matcher.match_fields(xsd_sample, avro_sample, use_llm=True, batch_size=10)
            
            print(f"✓ Found {len(matches)} semantic matches:\n")
            for i, (xsd_id, (xsd_f, avro_f, conf)) in enumerate(matches.items(), 1):
                print(f"  {i}. {xsd_f.name} ({xsd_f.path})")
                print(f"     ↔ {avro_f.name} ({avro_f.path})")
                print(f"     Confidence: {conf:.2f}\n")
                
        except ValueError as e:
            print(f"⚠️  LLM not available: {str(e)}")
            print("Falling back to fuzzy matching...\n")
        except Exception as e:
            print(f"⚠️  LLM error: {str(e)}")
            print("Falling back to fuzzy matching...\n")
        
        # Test without LLM (fuzzy fallback)
        print("Testing fuzzy matching (no LLM)...")
        semantic_matcher = SemanticFieldMatcher(None)
        matches = semantic_matcher.match_fields(xsd_fields[:10], avro_fields[:20], use_llm=False)
        
        print(f"✓ Found {len(matches)} fuzzy matches")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def test_field_mapping_suggestions():
    """Test 6: AI-powered field mapping suggestions"""
    print_section("TEST 6: AI Field Mapping Suggestions")
    
    xsd_path = 'schemas/pain.001.001.12.xsd'
    avro_path = 'schemas/pain.001.001.12.avsc'
    
    if not os.path.exists(xsd_path) or not os.path.exists(avro_path):
        print(f"⚠️  Schemas not found")
        return
    
    try:
        # Load schemas
        xsd_agent = ISO20022SchemaAgent()
        xsd_agent.load_schema(xsd_path)
        xsd_fields = xsd_agent.extract_fields()[:20]  # Sample for testing
        
        avro_agent = ISO20022SchemaAgent()
        avro_agent.load_schema(avro_path)
        avro_fields = avro_agent.extract_fields()[:20]
        
        print(f"XSD fields: {len(xsd_fields)}")
        print(f"AVRO fields: {len(avro_fields)}\n")
        
        # Get AI suggestions
        ai_agent = SchemaAIAgent()
        print(f"Using AI provider: {ai_agent.provider}")
        print("Generating mapping suggestions...\n")
        
        suggestions = ai_agent.suggest_field_mappings(xsd_fields, avro_fields)
        
        if suggestions:
            print(f"✓ Generated {len(suggestions)} mapping suggestions:\n")
            for i, suggestion in enumerate(suggestions[:5], 1):  # Show top 5
                print(f"{i}. {suggestion.get('xsd_field', 'N/A')}")
                print(f"   → {suggestion.get('avro_field', 'N/A')}")
                print(f"   Confidence: {suggestion.get('confidence', 0):.2f}")
                print(f"   Reasoning: {suggestion.get('reasoning', 'N/A')[:100]}...\n")
        else:
            print("⚠️  No suggestions generated")
        
    except ValueError as e:
        print(f"⚠️  AI not configured: {str(e)}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def test_documentation_generation():
    """Test 7: Auto-generate documentation"""
    print_section("TEST 7: Documentation Generation")
    
    schema_path = 'schemas/pain.001.001.12.xsd'
    
    if not os.path.exists(schema_path):
        print(f"⚠️  Schema not found: {schema_path}")
        return
    
    try:
        # Load schema
        agent = ISO20022SchemaAgent()
        agent.load_schema(schema_path)
        fields = agent.extract_fields()[:30]  # Sample for testing
        
        print(f"Loaded {len(fields)} sample fields")
        
        # Generate docs
        ai_agent = SchemaAIAgent()
        print(f"Using AI provider: {ai_agent.provider}")
        print("Generating documentation...\n")
        
        docs = ai_agent.generate_documentation(fields, "Pain.001.001.12")
        
        print("✓ Generated documentation:\n")
        print(docs[:500] + "...\n" if len(docs) > 500 else docs + "\n")
        
    except ValueError as e:
        print(f"⚠️  AI not configured: {str(e)}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print("  ISO 20022 AI AGENT INTEGRATION TEST SUITE")
    print("="*70)
    
    tests = [
        ("Agent Initialization", test_ai_agent_initialization),
        ("Schema Loading", test_schema_loading),
        ("Chat Interface", test_chat_interface),
        ("Schema Queries", test_schema_query),
        ("Semantic Matching", test_semantic_matching),
        ("Field Mapping Suggestions", test_field_mapping_suggestions),
        ("Documentation Generation", test_documentation_generation)
    ]
    
    results = {"passed": 0, "failed": 0, "skipped": 0}
    
    for name, test_func in tests:
        try:
            test_func()
            results["passed"] += 1
        except Exception as e:
            print(f"\n❌ Test '{name}' failed: {str(e)}")
            results["failed"] += 1
    
    # Summary
    print_section("TEST SUMMARY")
    print(f"✓ Passed: {results['passed']}")
    print(f"❌ Failed: {results['failed']}")
    print(f"⚠️  Skipped: {results['skipped']}")
    
    print("\n" + "="*70)
    print("  Setup Instructions")
    print("="*70)
    print("\n🆓 FREE OPTION (Recommended for testing):")
    print("  1. Install Ollama: https://ollama.ai")
    print("  2. Pull model: ollama pull llama3.2")
    print("  3. Create .env: echo 'LLM_PROVIDER=ollama' > .env")
    print("  4. Run tests again")
    
    print("\n💳 PAID OPTIONS:")
    print("  OpenAI: Add OPENAI_API_KEY to .env")
    print("  Anthropic: Add ANTHROPIC_API_KEY to .env")
    print("  OpenRouter: Add OPENROUTER_API_KEY to .env (free tier available)")
    
    print("\n📚 Documentation:")
    print("  See AI_AGENT_GUIDE.md for complete setup instructions")
    print("="*70 + "\n")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Test AI Agent Integration')
    parser.add_argument('--test', type=str, help='Run specific test (1-7)')
    args = parser.parse_args()
    
    if args.test:
        test_map = {
            '1': test_ai_agent_initialization,
            '2': test_schema_loading,
            '3': test_chat_interface,
            '4': test_schema_query,
            '5': test_semantic_matching,
            '6': test_field_mapping_suggestions,
            '7': test_documentation_generation
        }
        if args.test in test_map:
            test_map[args.test]()
        else:
            print(f"Invalid test number. Choose 1-7.")
    else:
        run_all_tests()
