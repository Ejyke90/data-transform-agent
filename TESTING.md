# Testing the AI Agent

## Quick Test (No Setup Required)

Run basic tests without AI:

```bash
python test_ai_agent.py --test 1  # Test initialization
python test_ai_agent.py --test 2  # Test schema loading
```

## Full Test Suite

### Option 1: Free Local Testing (Ollama)

**1. Install Ollama:**
```bash
# macOS
brew install ollama

# or download from https://ollama.ai
```

**2. Start Ollama and pull a model:**
```bash
ollama pull llama3.2
```

**3. Configure environment:**
```bash
echo "LLM_PROVIDER=ollama" > .env
echo "OLLAMA_MODEL=llama3.2" >> .env
```

**4. Run all tests:**
```bash
python test_ai_agent.py
```

### Option 2: Using OpenAI/Anthropic (Paid)

**1. Get API key:**
- OpenAI: https://platform.openai.com/api-keys
- Anthropic: https://console.anthropic.com/

**2. Configure:**
```bash
# For OpenAI
echo "LLM_PROVIDER=openai" > .env
echo "OPENAI_API_KEY=sk-your-key" >> .env

# OR for Anthropic
echo "LLM_PROVIDER=anthropic" > .env
echo "ANTHROPIC_API_KEY=sk-ant-your-key" >> .env
```

**3. Run tests:**
```bash
python test_ai_agent.py
```

## Individual Tests

Run specific tests:

```bash
python test_ai_agent.py --test 1  # Agent Initialization
python test_ai_agent.py --test 2  # Schema Loading
python test_ai_agent.py --test 3  # Chat Interface
python test_ai_agent.py --test 4  # Schema Queries
python test_ai_agent.py --test 5  # Semantic Matching
python test_ai_agent.py --test 6  # Field Mapping Suggestions
python test_ai_agent.py --test 7  # Documentation Generation
```

## Manual Testing via Web UI

### 1. Start the server:
```bash
python app.py
```

### 2. Open browser:
```
http://localhost:5001
```

### 3. Test each feature:

**📊 Analyze Tab:**
- Upload or select a schema (XSD/AVRO)
- Click "Analyze Schema"
- Download CSV report

**🔄 Compare Tab:**
- Select both XSD and AVRO schemas
- ✅ Enable "Use AI Semantic Matching" (requires LLM)
- Click "Compare Schemas"
- View matched/unmatched fields
- Download comparison CSV

**💬 AI Chat Tab:**
- Ask: "What does MsgId mean?"
- Ask: "Show me all mandatory fields"
- Ask: "Explain the payment initiation structure"

## API Testing

### Test Chat Endpoint:
```bash
curl -X POST http://localhost:5001/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is ISO 20022?", "history": []}'
```

### Test Schema Query:
```bash
curl -X POST http://localhost:5001/ai/query-schema \
  -H "Content-Type: application/json" \
  -d '{
    "schema_path": "schemas/pain.001.001.12.xsd",
    "query": "How many mandatory fields?"
  }'
```

### Test Mapping Suggestions:
```bash
curl -X POST http://localhost:5001/ai/suggest-mappings \
  -H "Content-Type: application/json" \
  -d '{
    "xsd_path": "schemas/pain.001.001.12.xsd",
    "avro_path": "schemas/pain.001.001.12.avsc"
  }'
```

### Test Documentation Generation:
```bash
curl -X POST http://localhost:5001/ai/generate-docs \
  -H "Content-Type: application/json" \
  -d '{
    "schema_path": "schemas/pain.001.001.12.xsd",
    "schema_name": "Pain.001"
  }'
```

## Expected Results

### ✅ Success Indicators:

1. **Agent Initialization:**
   - "✓ Initialized with model: llama3.2" (or your chosen model)

2. **Schema Loading:**
   - "✓ Loaded 1673 fields" (for pain.001.001.12.xsd)
   - "✓ Loaded 1128 fields" (for pain.001.001.12.avsc)

3. **Chat Interface:**
   - Receives contextual responses about ISO 20022

4. **Semantic Matching:**
   - "✓ Found N semantic matches"
   - Shows confidence scores (0.7-1.0)

5. **Field Mappings:**
   - Returns JSON with XSD→AVRO mappings
   - Includes confidence and reasoning

6. **Documentation:**
   - Generates markdown with field descriptions

### ⚠️ Common Issues:

**"OPENAI_API_KEY not found"**
- Solution: Create `.env` file with API key OR use Ollama (free)

**"Ollama not running"**
- Solution: `ollama pull llama3.2` and ensure Ollama is started

**"No matches found"**
- Check if schemas have overlapping fields
- Try disabling semantic matching (uses fuzzy fallback)

**Slow responses**
- Local models (Ollama): First request takes ~5-10s
- Paid APIs: Usually <2s
- Large schemas: Use smaller samples for testing

## Performance Testing

Test with different model sizes:

```bash
# Fast, less accurate
ollama pull llama3.2:1b
echo "OLLAMA_MODEL=llama3.2:1b" >> .env

# Balanced (recommended)
ollama pull llama3.2
echo "OLLAMA_MODEL=llama3.2" >> .env

# Slower, more accurate
ollama pull llama3.1:8b
echo "OLLAMA_MODEL=llama3.1:8b" >> .env
```

## Debugging

Enable verbose output:

```bash
# Add to .env
DEBUG=True

# Run with Python debug mode
python -u test_ai_agent.py
```

View logs:
```bash
tail -f app.log  # If logging is enabled
```

## Next Steps

After successful testing:

1. **Deploy to production** with proper API keys
2. **Add more schemas** to schemas/ folder
3. **Customize prompts** in `src/iso20022_agent/ai_agent.py`
4. **Tune batch sizes** for better performance
5. **Add authentication** for production use

## Support

- Issues: https://github.com/Ejyke90/data-transform-agent/issues
- Setup Guide: `AI_AGENT_GUIDE.md`
- Demo: `DEMO_GUIDE.md`
