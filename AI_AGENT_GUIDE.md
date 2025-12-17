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

### 2. Configure API Keys

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and add your API key:

**Option A: Use OpenAI (GPT-4)**
```env
OPENAI_API_KEY=sk-your-key-here
LLM_PROVIDER=openai
OPENAI_MODEL=gpt-4o
```

**Option B: Use Anthropic (Claude)**
```env
ANTHROPIC_API_KEY=sk-ant-your-key-here
LLM_PROVIDER=anthropic
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

### 3. Start the Server
```bash
python app.py
```

Visit: http://localhost:5001

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

# Initialize
ai_agent = SchemaAIAgent(provider='openai')  # or 'anthropic'

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

## Cost Considerations

- **OpenAI GPT-4**: ~$0.01-0.03 per request
- **Anthropic Claude**: ~$0.01-0.03 per request

Use `.env` to switch providers based on your preference and budget.

## Troubleshooting

**Error: "OPENAI_API_KEY not found"**
- Make sure `.env` file exists with valid API key
- Restart the server after adding keys

**Error: Rate limit exceeded**
- Wait a few seconds between requests
- Consider using a higher tier API plan

**No .env file?**
- Copy `.env.example` to `.env`
- Add your API keys
