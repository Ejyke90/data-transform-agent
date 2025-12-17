# ISO 20022 Payment Schema AI Agent

An intelligent AI agent designed to ingest, analyze, and validate ISO 20022 payment message schemas. Supports both **XSD** and **AVRO** schema formats with comprehensive field extraction.

## Overview

The ISO 20022 Payment Schema Agent provides automated analysis of payment message schemas across three key payment domains:

- **Payment Initiation (pain)** - Customer-to-bank payment instructions
- **Payments Clearing and Settlement (pacs)** - Financial institution-to-financial institution payments
- **Cash Management (camt)** - Account statements, notifications, and reporting
- **Business Application Header (head)** - Message envelope and routing information

## Features

### Core Capabilities

✅ **Dual Format Support**
- Parse ISO 20022 XML Schema Definition (XSD) files (.xsd)
- Parse AVRO schemas (.avsc, .avro) - NEW!
- Auto-detect format from file extension
- Consistent output regardless of input format

✅ **Schema Ingestion**
- Support multiple message versions (e.g., pain.001.001.09, pain.001.001.12)
- Extract complete message structure hierarchies
- Handle nested complex types and arrays

✅ **Field Classification**
- Identify mandatory fields (multiplicity 1..1, 1..n)
- Identify optional fields (multiplicity 0..1, 0..n)
- Detect conditional field requirements
- Extract field metadata (type, length, patterns, code lists)

✅ **ISO 20022 Compliance Validation**
- Validate against official ISO 20022 standards
- Check data type conformance
- Verify code set usage
- Validate business rules and constraints

✅ **Comprehensive Documentation**
- Generate field-level documentation
- Provide usage guidelines and examples
- Create validation rule summaries
- Export structured field reports (JSON, CSV, Markdown)

## Supported Message Types

### Payment Initiation (pain.xxx.xxx.xx)
| Message | Name | Purpose |
|---------|------|---------|
| pain.001 | CustomerCreditTransferInitiation | Initiate credit transfers |
| pain.002 | CustomerPaymentStatusReport | Report payment status |
| pain.007 | CustomerPaymentReversal | Reverse previous payment |
| pain.008 | CustomerDirectDebitInitiation | Initiate direct debits |
| pain.013 | CreditorPaymentActivationRequest | Request payment activation |
| pain.014 | CreditorPaymentActivationRequestStatusReport | Status of activation request |

### Payments Clearing and Settlement (pacs.xxx.xxx.xx)
| Message | Name | Purpose |
|---------|------|---------|
| pacs.002 | FIToFIPaymentStatusReport | Payment status between FIs |
| pacs.003 | FIToFICustomerDirectDebit | Direct debit between FIs |
| pacs.004 | PaymentReturn | Return payment to originator |
| pacs.007 | FIToFIPaymentReversal | Reverse payment instruction |
| pacs.008 | FIToFICustomerCreditTransfer | Credit transfer between FIs |
| pacs.009 | FinancialInstitutionCreditTransfer | Bank-to-bank transfer |
| pacs.010 | FinancialInstitutionDirectDebit | Bank-to-bank direct debit |
| pacs.028 | FIToFIPaymentStatusRequest | Request payment status |

### Cash Management (camt.xxx.xxx.xx)
| Message | Name | Purpose |
|---------|------|---------|
| camt.052 | BankToCustomerAccountReport | Intraday account reporting |
| camt.053 | BankToCustomerStatement | Account statement |
| camt.054 | BankToCustomerDebitCreditNotification | Transaction notifications |
| camt.055 | CustomerPaymentCancellationRequest | Customer cancellation request |
| camt.056 | FIToFIPaymentCancellationRequest | FI cancellation request |
| camt.057 | NotificationToReceive | Expected payment notification |
| camt.060 | AccountReportingRequest | Request account report |

### Business Application Header (head.001.001.xx)
Essential metadata wrapper for all ISO 20022 business messages containing routing, identification, and control information.

## Quick Start

> 📚 **New to the project?** Start with the [Getting Started Guide](GETTING_STARTED.md)  
> 🍎 **Mac User?** See the [Complete Mac Usage Guide](docs/MAC_USAGE_GUIDE.md)  
> ✅ **See Test Results:** [pain.001.001.12 Analysis Results](TEST_RESULTS.md)  
> 🔍 **Verify Accuracy:** [How to Confirm Numbers are Correct](docs/ACCURACY_VERIFICATION.md)  
> 🔷 **AVRO Support:** [Using AVRO Schemas](docs/AVRO_SUPPORT.md) - NEW!

## Installation

### For Mac Users (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/data-transform-agent.git
cd data-transform-agent

# Create virtual environment (required on modern macOS)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install the agent
pip install -e .
```

**Important for Mac Users:**
- Use `python3` and `pip3` (not `python` or `pip`)
- Always activate the virtual environment before running commands: `source venv/bin/activate`
- macOS requires virtual environments due to PEP 668 protection

### For Other Systems

```bash
# Clone the repository
git clone https://github.com/yourusername/data-transform-agent.git
cd data-transform-agent

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the agent
pip install -e .
```

> 📖 For detailed installation instructions, see [INSTALL.md](INSTALL.md)

### Mac Users - Complete Workflow

```bash
# 1. Activate virtual environment (do this every time you open a new terminal)
source venv/bin/activate

# 2. Place your XSD schema in the schemas/ directory
# Download from https://www.iso20022.org/

# 3. Run analysis using CLI
iso20022-agent analyze schemas/pain.001.001.12.xsd -o output/pain001_fields.csv

# 4. For detailed breakdown with samples and statistics
iso20022-agent analyze schemas/pain.001.001.12.xsd -o output/fields.csv --detailed

# 5. View results
open output/pain001_fields.csv  # Opens in default app (Excel/Numbers)
# or
cat output/pain001_fields.csv   # View in terminal

# 6. For JSON or Markdown output
iso20022-agent analyze schemas/pain.001.001.12.xsd -o output/fields.json -f json
iso20022-agent analyze schemas/pain.001.001.12.xsd -o output/fields.md -f markdown
```

**Mac Tips:**
- Keep your terminal open with venv activated for multiple operations
- Use `Command+Shift+.` in Finder to see hidden files like `.venv`
- Use `open .` to view current directory in Finder

### Python API Usage

```python
from iso20022_agent import ISO20022SchemaAgent

# Initialize the agent
agent = ISO20022SchemaAgent()

# Load and analyze a schema
agent.load_schema('schemas/pain.001.001.12.xsd')
fields = agent.extract_fields()

# Get mandatory and optional fields
mandatory = agent.get_mandatory_fields()
optional = agent.get_optional_fields()
print(f"Found {len(mandatory)} mandatory and {len(optional)} optional fields")

# Export to CSV (primary format for easy testing)
agent.export_csv('output/pain001_fields.csv')

# Also available: JSON and Markdown formats
agent.export_json('output/pain001_fields.json')
agent.export_markdown('output/pain001_fields.md')

# Print summary (standard)
agent.print_summary()

# Print detailed summary with breakdown
agent.print_summary(detailed=True)

# CSV Output Format:
# FieldName, Path, Multiplicity, Constraints, Definition
# Easy to open in Excel, import to databases, or use in testing tools
```

## Project Structure

```
data-transform-agent/
├── .github/
│   ├── prompts/
│   │   └── agent-instructions.md    # AI agent instructions
│   └── skills/
│       └── data-transformation.md   # Transformation skills & patterns
├── src/
│   ├── agents/
│   │   └── schema_agent.py          # Main agent implementation
│   ├── parsers/
│   │   └── xsd_parser.py            # XSD schema parser
│   ├── validators/
│   │   └── iso20022_validator.py   # ISO 20022 validation
│   └── exporters/
│       └── report_exporter.py       # Report generation
├── schemas/                          # Sample ISO 20022 schemas
├── tests/                           # Unit and integration tests
├── docs/                            # Documentation and examples
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## Key ISO 20022 Concepts

### Message Structure
Every ISO 20022 payment message follows a consistent structure:
```xml
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:pain.001.001.09">
  <CstmrCdtTrfInitn>
    <GrpHdr>                        <!-- Group Header (Mandatory) -->
      <MsgId>MSG-001</MsgId>        <!-- Message ID (Mandatory) -->
      <CreDtTm>2025-12-16T...</CreDtTm>  <!-- Creation DateTime (Mandatory) -->
    </GrpHdr>
    <PmtInf>                        <!-- Payment Information (Mandatory) -->
      <!-- Payment details -->
    </PmtInf>
  </CstmrCdtTrfInitn>
</Document>
```

### Multiplicity Rules
- **1..1**: Mandatory, exactly one occurrence
- **1..n**: Mandatory, one or more occurrences
- **0..1**: Optional, zero or one occurrence
- **0..n**: Optional, zero or more occurrences

### Common Mandatory Elements
Across most payment messages:
- **Group Header (GrpHdr)**: Message-level information
- **Message Identification (MsgId)**: Unique message reference
- **Creation Date Time (CreDtTm)**: Message creation timestamp
- **Initiating Party (InitgPty)** or **Instructing Agent (InstgAgt)**: Sender identification
- **Payment Information (PmtInf)** or **Transaction Information**: Core payment details

## Use Cases

### 1. Schema Documentation
Automatically generate comprehensive documentation for any ISO 20022 payment schema, including all fields, their requirements, data types, and business meanings.

### 2. Message Validation
Validate payment message instances against their schemas to ensure compliance with ISO 20022 standards and identify missing mandatory fields.

### 3. Implementation Planning
Analyze schemas to understand implementation requirements, identify required vs. optional fields for specific use cases, and plan system integrations.

### 4. Migration Analysis
Compare different schema versions to identify changes, new fields, deprecated elements, and plan migration strategies.

### 5. Training & Onboarding
Generate clear documentation and field catalogs to help teams understand ISO 20022 message structures and requirements.

## Advanced Features

### Conditional Field Detection
The agent identifies fields that are optional in the schema but become mandatory under specific business conditions:

```python
conditional_fields = analysis.get_conditional_fields()
for field in conditional_fields:
    print(f"{field.path}: {field.condition}")
```

### Cross-Version Comparison
Compare the same message type across different versions:

```python
comparison = agent.compare_versions(
    "schemas/pain.001.001.09.xsd",
    "schemas/pain.001.001.11.xsd"
)
print(comparison.added_fields)
print(comparison.removed_fields)
print(comparison.modified_fields)
```

### Custom Validation Rules
Extend the agent with custom business rules:

```python
agent.add_validation_rule(
    name="sepa_iban_required",
    condition=lambda msg: msg.payment_method == "SEPA",
    check=lambda msg: msg.debtor_account.id.startswith("IBAN"),
    message="SEPA payments require IBAN account numbers"
)
```

## Configuration

Configure the agent behavior via `config.yaml`:

```yaml
iso20022_agent:
  schema_validation:
    strict_mode: true
    validate_code_lists: true
    check_deprecated_fields: true
  
  field_extraction:
    include_annotations: true
    extract_examples: true
    generate_patterns: true
  
  output_formats:
    default: csv  # CSV is the primary format
    available:
      - csv        # Recommended for testing and validation
      - json       # For programmatic use
      - markdown   # For documentation
  
  supported_versions:
    pain: ["09", "10", "11"]
    pacs: ["08", "09", "10"]
    camt: ["08", "09", "10"]
```

## Resources

### ISO 20022 Official Resources
- [ISO 20022 Website](https://www.iso20022.org/)
- [Message Definitions Catalogue](https://www.iso20022.org/iso-20022-message-definitions)
- [Payment Domain Messages](https://www.iso20022.org/iso-20022-message-definitions?business-domain%5B0%5D=1)
- [Business Application Header](https://www.iso20022.org/catalogue-messages/additional-content-messages/business-application-header-bah)

### Documentation
- [Agent Instructions](.github/prompts/agent-instructions.md) - Detailed AI agent behavior
- [Transformation Skills](.github/skills/data-transformation.md) - Data transformation patterns
- [ISO 20022 Reference](.github/skills/iso20022-reference.md) - Complete message reference
- [Quick Start Guide](.github/prompts/quick-start.md) - Get started quickly
- [CSV Testing Guide](docs/csv-testing-guide.md) - Using CSV output for testing and validation
- [Sample CSV Output](examples/pain001_fields_sample.csv) - Example field extraction

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run linters
flake8 src/
black src/
mypy src/
```

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## Roadmap

### Phase 1: Core Schema Analysis (Current)
- ✅ XSD parsing and field extraction
- ✅ Mandatory/optional field classification
- ✅ Basic validation rules
- ✅ Documentation generation

### Phase 2: Advanced Validation
- ⏳ Business rule validation
- ⏳ Cross-field constraint checking
- ⏳ Code list validation
- ⏳ Market practice guide support (SEPA, SWIFT)

### Phase 3: Message Instance Processing
- 📋 XML message parsing
- 📋 Real-time validation
- 📋 Message transformation
- 📋 Format conversion (XML, JSON, CSV)

### Phase 4: Integration & Automation
- 📋 API endpoints
- 📋 CI/CD pipeline integration
- 📋 Monitoring and alerting
- 📋 Performance optimization

## Support

- **Issues**: [GitHub Issues](https://github.com/Ejyke90/data-transform-agent/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Ejyke90/data-transform-agent/discussions)
- **Email**: support@example.com

## Acknowledgments

This project leverages the ISO 20022 Universal Financial Industry Message Scheme, maintained by the ISO 20022 Registration Authority.

---

**Built with ❤️ for the financial messaging community**