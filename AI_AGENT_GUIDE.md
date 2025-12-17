# AI Agent Setup Guide

## 🤖 AI Agent Features

This tool now includes **LLM-powered AI agent capabilities** for intelligent schema analysis:

### Features
- **💬 Conversational Chat**: Ask questions about schemas in natural language
- **🔍 Schema Queries**: "Show me all mandatory payment fields"
- **🧠 Intelligent Field Mapping**: AI suggests XSD → AVRO field mappings
- **📝 Auto Documentation**: Generate human-readable docs from schemas
- **💡 Field Explanations**: Understand what fields mean in business terms

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Choose Your LLM Provider

#### 🆓 **FREE OPTIONS (Recommended for Testing)**

##### **Option A: Ollama (Local - Completely Free!)**

1. Install Ollama: https://ollama.ai
2. Pull a model:
   ```bash
   ollama pull llama3.2
   # or try: llama3.1, mistral, codellama
   ```
3. Create `.env`:
   ```env
   LLM_PROVIDER=ollama
   OLLAMA_MODEL=llama3.2
   OLLAMA_BASE_URL=http://localhost:11434
   ```

**Pros:** 
- ✅ 100% free, runs locally
- ✅ No API keys needed
- ✅ Private (data stays on your machine)
- ✅ Fast responses

**Cons:** 
- ⚠️ Requires ~4GB RAM
- ⚠️ Quality varies by model

##### **Option B: OpenRouter (Free Tier)**

1. Get API key: https://openrouter.ai/keys
2. Create `.env`:
   ```env
   LLM_PROVIDER=openrouter
   OPENROUTER_API_KEY=sk-or-your-key-here
   OPENROUTER_MODEL=meta-llama/llama-3.2-3b-instruct:free
   ```

**Free models available:**
- `meta-llama/llama-3.2-3b-instruct:free`
- `google/gemma-2-9b-it:free`
- `mistralai/mistral-7b-instruct:free`

##### **Option C: HuggingFace (Free API)**

1. Get token: https://huggingface.co/settings/tokens
2. Create `.env`:
   ```env
   LLM_PROVIDER=huggingface
   HUGGINGFACE_API_KEY=hf_your-token-here
   HUGGINGFACE_MODEL=meta-llama/Meta-Llama-3-8B-Instruct
   ```

#### 💳 **PAID OPTIONS (Better Quality)**

##### **OpenAI (GPT-4)**
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o
```
Cost: ~$0.01-0.03 per request

##### **Anthropic (Claude)**
```env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-your-key-here
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```
Cost: ~$0.01-0.03 per request

### 3. Start the Server
```bash
python app.py
```

Visit: http://localhost:5001

## Quick Start (Free & Local)

**Fastest way to get started with zero cost:**

```bash
# 1. Install Ollama
brew install ollama  # macOS
# or download from https://ollama.ai

# 2. Pull a model
ollama pull llama3.2

# 3. Create .env file
echo "LLM_PROVIDER=ollama" > .env
echo "OLLAMA_MODEL=llama3.2" >> .env

# 4. Start the server
python app.py
```

That's it! No API keys, no costs, runs completely locally.

## Usage

### Chat Interface (Web UI)
1. Click the **💬 AI Chat** tab
2. Ask questions like:
   - "What does MsgId field mean?"
   - "Show me all mandatory fields"
   - "Explain the payment initiation structure"

### API Endpoints

#### Chat
```bash
POST /chat
{
  "message": "What is MsgId?",
  "history": []
}
```

#### Query Schema
```bash
POST /ai/query-schema
{
  "schema_path": "schemas/pain.001.001.12.xsd",
  "query": "What are the mandatory fields?"
}
```

#### Suggest Field Mappings
```bash
POST /ai/suggest-mappings
{
  "xsd_path": "schemas/pain.001.001.12.xsd",
  "avro_path": "schemas/pain.001.001.12.avsc"
}
```

#### Generate Documentation
```bash
POST /ai/generate-docs
{
  "schema_path": "schemas/pain.001.001.12.xsd",
  "schema_name": "Pain.001.001.12"
}
```

## Python API

```python
from iso20022_agent.ai_agent import SchemaAIAgent
from iso20022_agent import ISO20022SchemaAgent

# === FREE: Use Ollama (Local) ===
ai_agent = SchemaAIAgent(provider='ollama')

# === PAID: Use OpenAI or Anthropic ===
# ai_agent = SchemaAIAgent(provider='openai')
# ai_agent = SchemaAIAgent(provider='anthropic')

# === FREE: Use OpenRouter or HuggingFace ===
# ai_agent = SchemaAIAgent(provider='openrouter')
# ai_agent = SchemaAIAgent(provider='huggingface')

# Load schema
agent = ISO20022SchemaAgent()
agent.load_schema('schemas/pain.001.001.12.xsd')
fields = agent.extract_fields()

# Query
answer = ai_agent.query_schema(fields, "What does MsgId mean?")
print(answer)

# Generate docs
docs = ai_agent.generate_documentation(fields, "Pain.001")
print(docs)

# Suggest mappings
avro_agent = ISO20022SchemaAgent()
avro_agent.load_schema('schemas/pain.001.001.12.avsc')
avro_fields = avro_agent.extract_fields()

mappings = ai_agent.suggest_field_mappings(fields, avro_fields)
for mapping in mappings:
    print(f"{mapping['xsd_field']} → {mapping['avro_field']}")
    print(f"Confidence: {mapping['confidence']}")
    print(f"Reasoning: {mapping['reasoning']}\n")
```

## Provider Comparison

| Provider | Cost | Speed | Quality | Privacy | Setup |
|----------|------|-------|---------|---------|-------|
| **Ollama** | 🆓 Free | ⚡ Fast | ⭐⭐⭐ Good | 🔒 100% Private | Easy |
| **OpenRouter** | 🆓 Free tier | ⚡ Fast | ⭐⭐⭐⭐ Very Good | ☁️ Cloud | Easy |
| **HuggingFace** | 🆓 Free | 🐌 Slow | ⭐⭐⭐ Good | ☁️ Cloud | Easy |
| **OpenAI** | 💳 ~$0.03/req | ⚡⚡ Very Fast | ⭐⭐⭐⭐⭐ Best | ☁️ Cloud | Easy |
| **Anthropic** | 💳 ~$0.03/req | ⚡⚡ Very Fast | ⭐⭐⭐⭐⭐ Best | ☁️ Cloud | Easy |

**Recommendation:**
- **Development/Testing**: Use Ollama (free, fast, private)
- **Production**: Use OpenAI or Anthropic (best quality)
- **Budget-conscious**: Use OpenRouter free tier

## Troubleshooting

**Error: "OPENAI_API_KEY not found"**
- Make sure `.env` file exists with valid API key
- Or switch to free option: `LLM_PROVIDER=ollama`
- Restart the server after adding keys

**Error: "Ollama not running"**
- Install Ollama: https://ollama.ai
- Start Ollama and pull a model: `ollama pull llama3.2`
- Verify it's running: `ollama list`

**Error: Rate limit exceeded**
- Switch to Ollama (no rate limits)
- Or wait a few seconds between requests
- Consider using a higher tier API plan

**Slow responses with HuggingFace?**
- First request is slow (model cold start)
- Subsequent requests are faster
- Or switch to Ollama for consistent speed

**Model not found?**
- For Ollama: `ollama pull <model-name>`
- Available models: `ollama list`
- See https://ollama.ai/library for all models
