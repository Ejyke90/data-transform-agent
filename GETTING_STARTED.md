# Getting Started with ISO 20022 Schema Agent

Welcome! This guide will help you get up and running with the ISO 20022 Schema Agent in minutes.

## What is This?

The ISO 20022 Schema Agent is an AI-powered tool that:
- 📖 Reads ISO 20022 XSD schemas
- 🔍 Extracts all mandatory and optional fields
- 📊 Exports field information to CSV (perfect for testing!)
- ✅ Validates payment messages
- 📈 Compares schema versions

## Step-by-Step Setup

### For Mac Users

#### Step 1: Open Terminal
- Go to **Applications** → **Utilities** → **Terminal**
- Or press `Command + Space` and type "Terminal"

#### Step 2: Navigate to Project
```bash
cd ~/Documents  # or wherever you cloned/downloaded the project
cd data-transform-agent
```

#### Step 3: Create Virtual Environment (Required on macOS)
```bash
python3 -m venv venv
```
This creates an isolated Python environment.

#### Step 4: Activate Virtual Environment
```bash
source venv/bin/activate
```
You'll see `(venv)` in your prompt. **Do this every time you open a new terminal!**

#### Step 5: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 6: Install the Agent
```bash
pip install -e .
```

#### Step 7: Verify Installation
```bash
iso20022-agent --help
```
You should see the help menu.

### For Windows/Linux Users

```bash
# Navigate to the project directory
cd /path/to/data-transform-agent

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the agent
pip install -e .
```

### Get an ISO 20022 Schema

**Option A: Download from ISO 20022 Website**

1. Go to https://www.iso20022.org/iso-20022-message-definitions
2. Find "Payments Initiation" or your desired message set
3. Click "Download Complete Message Set"
4. Extract the XSD files
5. Copy XSD file (e.g., `pain.001.001.12.xsd`) to the `schemas/` directory

**Option B: Use the Provided Schema**

A `pain.001.001.12.xsd` file is included in the project for testing.

### Run Your First Analysis

#### Mac Users - CLI Method
```bash
# Make sure venv is activated!
source venv/bin/activate

# Analyze the schema (standard summary)
iso20022-agent analyze schemas/pain.001.001.12.xsd -o output/pain001_fields.csv

# Analyze with detailed breakdown (recommended for verification)
iso20022-agent analyze schemas/pain.001.001.12.xsd -o output/fields.csv --detailed

# View the results
open output/pain001_fields.csv  # Opens in Excel/Numbers
# or
cat output/pain001_fields.csv   # View in terminal
```

#### Python API Method
```bash
# Make sure venv is activated!
source venv/bin/activate

# Run the example
python examples/basic_usage.py
```

```bash
# Analyze a schema and export to CSV
iso20022-agent analyze schemas/pain.001.001.09.xsd -o output/pain001_fields.csv
```

### Step 4: View the Results

Open `output/pain001_fields.csv` in:
- Excel or Google Sheets
- Any text editor
- Your test automation tool

The CSV contains exactly what you need:
- FieldName
- Path (XML location)
- Multiplicity (1..1 = mandatory, 0..1 = optional)
- Constraints (validation rules)
- Definition (what the field means)

## Usage Examples

### Example 1: Extract Mandatory Fields

```python
from iso20022_agent import ISO20022SchemaAgent

agent = ISO20022SchemaAgent()
agent.analyze_schema('schemas/pain.001.001.09.xsd')

# Get only mandatory fields
mandatory = agent.get_mandatory_fields()
print(f"Found {len(mandatory)} mandatory fields:")

for field in mandatory[:10]:  # Show first 10
    print(f"  ✓ {field.name} ({field.path})")
```

### Example 2: Export for Testing

```python
from iso20022_agent import ISO20022SchemaAgent

agent = ISO20022SchemaAgent()
agent.analyze_schema('schemas/pain.001.001.09.xsd')

# Export to CSV (best for testing)
agent.export_csv('test_data/pain001_fields.csv')

# Now you can:
# - Import into your test framework
# - Open in Excel to add test cases
# - Use in automated validation
```

### Example 3: Validate a Message

```python
from iso20022_agent import ISO20022SchemaAgent

agent = ISO20022SchemaAgent()
agent.analyze_schema('schemas/pain.001.001.09.xsd')

# Validate a message file
results = agent.validate_message_file('messages/payment.xml')

if results['valid']:
    print("✅ Message is valid!")
else:
    print("❌ Validation errors:")
    for error in results['errors']:
        print(f"  - {error}")
```

### Example 4: Compare Schema Versions

```python
from iso20022_agent import ISO20022SchemaAgent

# Load version 09
agent_v09 = ISO20022SchemaAgent()
agent_v09.analyze_schema('schemas/pain.001.001.09.xsd')

# Load version 11
agent_v11 = ISO20022SchemaAgent()
agent_v11.analyze_schema('schemas/pain.001.001.11.xsd')

# Compare mandatory fields
fields_v09 = set(f.path for f in agent_v09.get_mandatory_fields())
fields_v11 = set(f.path for f in agent_v11.get_mandatory_fields())

added = fields_v11 - fields_v09
removed = fields_v09 - fields_v11

print(f"Fields added in v11: {len(added)}")
print(f"Fields removed in v11: {len(removed)}")
```

## Using the CLI

The command-line interface is great for quick tasks:

```bash
# Show help
iso20022-agent --help

# Analyze a schema
iso20022-agent analyze schemas/pain.001.001.09.xsd

# Export to different formats
iso20022-agent analyze schemas/pain.001.001.09.xsd -o output/fields.csv -f csv
iso20022-agent analyze schemas/pain.001.001.09.xsd -o output/fields.json -f json
iso20022-agent analyze schemas/pain.001.001.09.xsd -o output/fields.md -f markdown

# Validate a message
iso20022-agent validate schemas/pain.001.001.09.xsd messages/payment.xml

# Compare versions
iso20022-agent compare schemas/pain.001.001.09.xsd schemas/pain.001.001.11.xsd
```

## Understanding the CSV Output

The CSV file has 5 columns:

### 1. FieldName
Human-readable name of the field
```
MessageIdentification
```

### 2. Path
XML path to find the field in messages
```
Document/CstmrCdtTrfInitn/GrpHdr/MsgId
```

### 3. Multiplicity
Shows if field is mandatory or optional:
- `1..1` = Mandatory, exactly once
- `0..1` = Optional, at most once
- `1..n` = Mandatory, one or more times
- `0..n` = Optional, zero or more times

### 4. Constraints
Validation rules:
```
MaxLength: 35; Pattern: [A-Za-z0-9/\-\?:().,'+ ]{1,35}
```

### 5. Definition
Business explanation of the field
```
Point to point reference assigned by the instructing party...
```

## Common Workflows

### For Developers

```bash
# 1. Analyze schema
python -c "
from iso20022_agent import ISO20022SchemaAgent
agent = ISO20022SchemaAgent()
agent.analyze_schema('schemas/pain.001.001.09.xsd')
agent.print_summary()
agent.export_csv('output/fields.csv')
"

# 2. Use CSV in your code
import csv
with open('output/fields.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if not row['FieldName'].startswith('#'):
            print(f"Validate: {row['FieldName']}")
```

### For Testers

1. Run the agent to get CSV
2. Open CSV in Excel
3. Add columns: TestCase1_Value, TestCase1_Expected
4. Fill in test scenarios
5. Import into test framework

### For Business Analysts

1. Run the agent to get Markdown
2. Share the `.md` file with team
3. Use for documentation and training
4. Reference in specifications

## Troubleshooting

### "ModuleNotFoundError: No module named 'iso20022_agent'"

```bash
# Make sure you installed the package
pip install -e .

# Or add to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

### "Schema file not found"

```bash
# Check the file exists
ls -l schemas/pain.001.001.09.xsd

# Use absolute path if needed
python examples/basic_usage.py /full/path/to/schema.xsd
```

### "No fields extracted"

Check that:
- XSD file is valid XML
- File is an ISO 20022 schema (not documentation)
- File has proper namespace declarations

## What's Next?

- Read [CSV Testing Guide](docs/csv-testing-guide.md) for test automation
- Check [ISO 20022 Reference](.github/skills/iso20022-reference.md) for message details
- Review [Agent Instructions](.github/prompts/agent-instructions.md) for advanced usage
- See [INSTALL.md](INSTALL.md) for detailed installation guide

## Quick Reference

```python
# Import
from iso20022_agent import ISO20022SchemaAgent

# Create agent
agent = ISO20022SchemaAgent()

# Load and analyze
agent.analyze_schema('schemas/pain.001.001.09.xsd')

# Get fields
all_fields = agent.fields
mandatory = agent.get_mandatory_fields()
optional = agent.get_optional_fields()

# Export
agent.export_csv('output/fields.csv')
agent.export_json('output/fields.json')
agent.export_markdown('output/fields.md')

# Validate
results = agent.validate_message_file('messages/payment.xml')

# Statistics
stats = agent.get_statistics()
agent.print_summary()
```

## Support

Need help?
- 📖 Check the [documentation](docs/)
- 💬 Open an [issue](https://github.com/Ejyke90/data-transform-agent/issues)
- 🗣️ Start a [discussion](https://github.com/Ejyke90/data-transform-agent/discussions)

Happy analyzing! 🚀
