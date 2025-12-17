# Quick Start Guide: ISO 20022 Payment Schema Agent

## Purpose

This AI agent helps you:
1. **Ingest** ISO 20022 payment schemas (XSD files)
2. **Extract** mandatory and optional fields
3. **Classify** fields by requirement level
4. **Validate** payment messages against schemas
5. **Generate** comprehensive documentation

## Supported Message Types

### Payment Initiation (pain)
- `pain.001` - Customer Credit Transfer
- `pain.002` - Payment Status Report
- `pain.007` - Payment Reversal
- `pain.008` - Direct Debit Initiation

### Payments Clearing & Settlement (pacs)
- `pacs.002` - FI Payment Status Report
- `pacs.003` - FI Direct Debit
- `pacs.004` - Payment Return
- `pacs.007` - FI Payment Reversal
- `pacs.008` - FI Customer Credit Transfer

### Cash Management (camt)
- `camt.052` - Account Report (intraday)
- `camt.053` - Account Statement
- `camt.054` - Debit/Credit Notification
- `camt.056` - Payment Cancellation Request

### Business Application Header (head)
- `head.001` - Message envelope/wrapper

## Agent Capabilities

### 1. Schema Analysis
The agent can:
- Parse ISO 20022 XSD schema files
- Extract complete message structure hierarchies
- Identify all defined fields with metadata
- Build field catalogs with full documentation

### 2. Field Classification
For each field, the agent identifies:
- **Path**: Full XML path (e.g., `Document/CstmrCdtTrfInitn/GrpHdr/MsgId`)
- **Name**: Business name
- **Type**: ISO 20022 data type
- **Multiplicity**: Min..Max occurrences (e.g., 1..1, 0..1, 1..n)
- **Requirement**: MANDATORY, OPTIONAL, or CONDITIONAL
- **Definition**: Business meaning
- **Constraints**: Length, pattern, code lists

### 3. Mandatory Field Extraction
Fields are marked MANDATORY when:
- `minOccurs >= 1` in the XSD schema
- Required by ISO 20022 standard
- Essential for message processing

**Example Mandatory Fields** (pain.001):
```
✓ Message Identification (MsgId)
✓ Creation Date Time (CreDtTm)
✓ Initiating Party (InitgPty)
✓ Payment Information (PmtInf)
✓ Debtor (Dbtr)
✓ Debtor Account (DbtrAcct)
✓ Creditor (Cdtr)
✓ Creditor Account (CdtrAcct)
✓ Amount (Amt)
```

### 4. Optional Field Extraction
Fields are marked OPTIONAL when:
- `minOccurs = 0` in the XSD schema
- Provide additional information
- May become mandatory in specific contexts

**Example Optional Fields** (pain.001):
```
○ Control Sum (CtrlSum)
○ Ultimate Debtor (UltmtDbtr)
○ Ultimate Creditor (UltmtCdtr)
○ Creditor Agent (CdtrAgt)
○ Purpose (Purp)
○ Regulatory Reporting (RgltryRptg)
○ Remittance Information (RmtInf)
```

### 5. Validation
The agent validates:
- Schema compliance
- Mandatory field presence
- Data type correctness
- Length constraints
- Pattern matching (regex)
- Code list values
- Business rules

## How to Use the Agent

### Request Schema Analysis

**Example Prompts**:

```
"Analyze the pain.001.001.09 schema and extract all mandatory fields"

"What are the optional fields in pacs.008.001.08?"

"Compare mandatory fields between pain.001 version 09 and version 11"

"Generate documentation for camt.053.001.08 with all field definitions"

"Validate this payment message against pain.001.001.09 schema"
```

### Expected Output Format

The agent provides output in **CSV format** by default, making it easy to:
- Import into Excel or Google Sheets
- Use in automated testing tools
- Load into databases
- Process with scripts
- Share with non-technical stakeholders

**CSV Structure:**
```csv
FieldName,Path,Multiplicity,Constraints,Definition
MessageIdentification,Document/CstmrCdtTrfInitn/GrpHdr/MsgId,1..1,"MaxLength: 35","Point to point reference assigned by the instructing party and sent to the next party in the chain to unambiguously identify the message."
CreationDateTime,Document/CstmrCdtTrfInitn/GrpHdr/CreDtTm,1..1,"Format: ISODateTime","Date and time at which the message was created."
NumberOfTransactions,Document/CstmrCdtTrfInitn/GrpHdr/NbOfTxs,1..1,"MaxLength: 15; Pattern: [0-9]{1,15}","Number of individual transactions contained in the message."
ControlSum,Document/CstmrCdtTrfInitn/GrpHdr/CtrlSum,0..1,"TotalDigits: 18; FractionDigits: 5","Total of all individual amounts included in the message."
```

**File includes header comments with metadata:**
```csv
# Message Type: pain.001.001.09
# Total Fields: 87
# Mandatory Fields: 23
# Optional Fields: 64
# Extraction Date: 2025-12-16
#
FieldName,Path,Multiplicity,Constraints,Definition
...
```

**Alternative formats available:**
- **JSON**: For programmatic processing
- **Markdown**: For documentation and wikis

## Common Questions

### Q: What does "1..1" multiplicity mean?
**A:** The field is mandatory and must appear exactly once.

### Q: What does "0..1" multiplicity mean?
**A:** The field is optional and can appear zero or one time.

### Q: What does "1..n" multiplicity mean?
**A:** The field is mandatory and must appear one or more times.

### Q: What does "0..n" multiplicity mean?
**A:** The field is optional and can appear zero or more times.

### Q: How do I know if a field is mandatory?
**A:** Check the multiplicity. If `minOccurs >= 1`, it's mandatory.

### Q: What are conditional fields?
**A:** Fields that are optional in the schema but become mandatory based on business rules or specific contexts.

**Example**: `CdtrAgt` (Creditor Agent) is optional in pain.001 schema, but mandatory for cross-border payments.

### Q: What's the difference between pain, pacs, and camt?
**A:** 
- **pain**: Customer-to-bank messages (payment initiation)
- **pacs**: Bank-to-bank messages (clearing & settlement)
- **camt**: Bank-to-customer messages (statements, reports)

### Q: What is the Business Application Header (BAH)?
**A:** A standardized message wrapper containing routing and control information that wraps around the business message.

### Q: How do I validate an actual payment message?
**A:** Provide the XML message and schema. The agent will:
1. Check mandatory fields are present
2. Validate data types and formats
3. Check constraints (length, patterns)
4. Verify code list values
5. Apply business rules

### Q: Can the agent compare different schema versions?
**A:** Yes! The agent can identify fields that were added, removed, or modified between versions.

### Q: What output formats are supported?
**A:** 
- **CSV** (default and recommended) - Easy to use with Excel, testing tools, and databases
- **JSON** - For programmatic processing and API integration
- **Markdown** - For documentation, wikis, and human-readable reports

CSV is recommended because it's:
- ✅ Easy to open in Excel/Sheets
- ✅ Simple to import into test frameworks
- ✅ Compatible with most tools
- ✅ Easy to diff and version control
- ✅ Accessible to non-technical users

## Key ISO 20022 Concepts

### Message Structure
Every ISO 20022 payment message has:
1. **Document Root**: Top-level element
2. **Message Type Element**: e.g., `CstmrCdtTrfInitn`
3. **Group Header**: Message-level information
4. **Transaction/Report Data**: Core business content

### Common Mandatory Elements
Almost all payment messages require:
- **Message ID**: Unique identifier
- **Creation Date/Time**: When message was created
- **Sender/Initiator**: Who is sending
- **Number of Transactions**: Transaction count
- **Transaction Details**: Core payment information

### Data Types
- **Text Types**: Max35Text, Max140Text (character limits)
- **Amount Types**: DecimalNumber with currency
- **Date Types**: ISODate (YYYY-MM-DD), ISODateTime
- **Code Types**: Predefined enumerations
- **Identifier Types**: IBAN, BIC, LEI

### Validation Levels
1. **Syntax**: Valid XML structure
2. **Schema**: Conforms to XSD
3. **Business**: Follows ISO 20022 rules
4. **Implementation**: Meets local/network requirements

## Next Steps

### For Schema Analysis:
1. Provide the schema file (XSD) or message type
2. Specify what you need (mandatory fields, full documentation, etc.)
3. Review the extracted information
4. Request additional analysis as needed

### For Message Validation:
1. Provide the payment message (XML)
2. Specify the schema/message type
3. Review validation results
4. Address any errors identified

### For Documentation:
1. Specify message type and version
2. Choose output format (JSON, Markdown, CSV)
3. Indicate level of detail needed
4. Request specific field information

## Example Workflow

### Scenario: Implementing SEPA Credit Transfer

**Step 1**: Analyze Schema
```
"Extract mandatory fields from pain.001.001.03 for SEPA credit transfers"
```

**Step 2**: Review Requirements
```
Agent provides:
- 23 mandatory fields
- Field paths and definitions
- IBAN and BIC requirements
- SEPA-specific rules
```

**Step 3**: Validate Implementation
```
"Validate my pain.001 message against the schema"
```

**Step 4**: Generate Documentation
```
"Generate Markdown documentation for pain.001.001.03 mandatory fields"
```

## Troubleshooting

### "Schema not found"
- Verify schema file path or message type
- Check version number format (e.g., 09 not 9)

### "Validation failed"
- Review mandatory fields list
- Check field data types
- Verify format patterns (IBAN, BIC, dates)
- Ensure all parent elements are present

### "Field not recognized"
- Verify field path syntax
- Check schema version compatibility
- Ensure correct namespace

## Resources

- **ISO 20022 Official Site**: https://www.iso20022.org/
- **Message Catalogue**: https://www.iso20022.org/iso-20022-message-definitions
- **Agent Instructions**: See `.github/prompts/agent-instructions.md`
- **Full Reference**: See `.github/skills/iso20022-reference.md`

## Support

For specific questions about:
- **Message types**: Reference the ISO 20022 catalogue
- **Agent capabilities**: Review agent-instructions.md
- **Field details**: Check iso20022-reference.md
- **Implementation**: Consult market practice guides (SEPA, SWIFT gpi)

---

**Ready to start?** Just ask the agent to analyze a schema or validate a message!
