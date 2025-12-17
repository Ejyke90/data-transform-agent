# AVRO Schema Support Guide

## Overview

The ISO 20022 Schema Agent now supports both **XSD** and **AVRO** schema formats. This allows you to work with AVRO-based message definitions while maintaining the same field extraction capabilities.

## Quick Comparison

| Feature | XSD Format | AVRO Format |
|---------|------------|-------------|
| File Extensions | `.xsd` | `.avsc`, `.avro` |
| Path Separator | `/` (slash) | `.` (dot) |
| Type System | XML Schema types | JSON types + logical types |
| Namespace Support | Yes | Yes |
| Code Lists | `xs:enumeration` | `enum` type |
| Complex Types | `xs:complexType` | `record` type |
| Arrays | `maxOccurs="unbounded"` | `array` type |
| Optional Fields | `minOccurs="0"` | Union with `null` |

## Using AVRO Schemas

### CLI Usage

```bash
# Analyze AVRO schema
iso20022-agent analyze schemas/pain.001.001.12.avsc -o output/fields.csv

# With detailed breakdown
iso20022-agent analyze schemas/pain.001.001.12.avsc -o output/fields.csv --detailed

# Export to JSON
iso20022-agent analyze schemas/pain.001.001.12.avsc -o output/fields.json -f json
```

### Python API Usage

```python
from iso20022_agent import ISO20022SchemaAgent

# Works the same way - format auto-detected from extension
agent = ISO20022SchemaAgent()
agent.load_schema('schemas/pain.001.001.12.avsc')  # AVRO format
fields = agent.extract_fields()

# Export to CSV with dot notation paths
agent.export_csv('output/avro_fields.csv')

# Get statistics
stats = agent.get_statistics()
print(f"Total fields: {stats['totalFields']}")
print(f"Mandatory: {stats['mandatoryCount']}")
print(f"Optional: {stats['optionalCount']}")
```

### Web UI Usage

1. Start the web server: `python app.py`
2. Upload `.avsc` or `.avro` file
3. Analyze and download results
4. Paths will use dot notation automatically

## Path Notation

### XSD (Slash Notation)
```
Document/Document/CstmrCdtTrfInitn/GrpHdr/MsgId
Document/Document/CstmrCdtTrfInitn/GrpHdr/CreDtTm
```

### AVRO (Dot Notation)
```
Document.Document.CstmrCdtTrfInitn.GrpHdr.MsgId
Document.Document.CstmrCdtTrfInitn.GrpHdr.CreDtTm
```

## AVRO Schema Structure

### Basic Field Types

```json
{
  "type": "record",
  "name": "Payment",
  "fields": [
    {"name": "msgId", "type": "string"},
    {"name": "amount", "type": "double"},
    {"name": "date", "type": {"type": "long", "logicalType": "timestamp-millis"}}
  ]
}
```

**Extracted Fields:**
- `msgId` - `Payment.msgId` - `1..1` - Mandatory
- `amount` - `Payment.amount` - `1..1` - Mandatory
- `date` - `Payment.date` - `1..1` - Mandatory (with logicalType: timestamp-millis)

### Optional Fields (Union with null)

```json
{
  "name": "optionalField",
  "type": ["null", "string"],
  "default": null
}
```

**Extracted:**
- `optionalField` - `Record.optionalField` - `0..1` - Optional

### Arrays

```json
{
  "name": "transactions",
  "type": {
    "type": "array",
    "items": "string"
  }
}
```

**Extracted:**
- `transactions` - `Record.transactions` - `1..unbounded` - Mandatory array

### Enumerations (Code Lists)

```json
{
  "name": "status",
  "type": {
    "type": "enum",
    "name": "StatusCode",
    "symbols": ["PENDING", "COMPLETED", "FAILED"]
  }
}
```

**Extracted:**
- `status` - `Record.status` - `1..1` - Codes: PENDING, COMPLETED, FAILED

### Nested Records

```json
{
  "type": "record",
  "name": "Payment",
  "fields": [
    {
      "name": "header",
      "type": {
        "type": "record",
        "name": "Header",
        "fields": [
          {"name": "msgId", "type": "string"},
          {"name": "createdDate", "type": "long"}
        ]
      }
    }
  ]
}
```

**Extracted Fields:**
- `header` - `Payment.header` - `1..1`
- `msgId` - `Payment.header.msgId` - `1..1`
- `createdDate` - `Payment.header.createdDate` - `1..1`

## Converting XSD to AVRO

We provide a converter script to transform XSD schemas to AVRO format:

```bash
python scripts/convert_xsd_to_avro.py
```

This script:
- Loads the pain.001.001.12 XSD schema
- Converts all 1,673 fields to AVRO format
- Preserves field structure and constraints
- Generates `schemas/pain.001.001.12.avsc`

## CSV Output Format (AVRO)

Same 5-column format as XSD, but with dot notation paths:

```csv
FieldName,Path,Multiplicity,Constraints,Definition
Document,Document,1..1,Type: Document,
Document,Document.Document,1..1,Type: Document,
CstmrCdtTrfInitn,Document.Document.CstmrCdtTrfInitn,1..1,Type: CstmrCdtTrfInitn,
MsgId,Document.Document.CstmrCdtTrfInitn.GrpHdr.MsgId,1..1,Type: string,
CreDtTm,Document.Document.CstmrCdtTrfInitn.GrpHdr.CreDtTm,1..1,Type: long,
```

## Type Mapping

| XSD Type | AVRO Type |
|----------|-----------|
| xs:string | string |
| xs:boolean | boolean |
| xs:int | int |
| xs:long | long |
| xs:float | float |
| xs:double | double |
| xs:decimal | string (with note) |
| xs:date | int (logicalType: date) |
| xs:dateTime | long (logicalType: timestamp-millis) |
| xs:complexType | record |
| xs:enumeration | enum |

## Multiplicity Rules

### Mandatory (1..1)
```json
{"name": "field", "type": "string"}
```

### Optional (0..1)
```json
{"name": "field", "type": ["null", "string"]}
```

### Mandatory Array (1..unbounded)
```json
{"name": "field", "type": {"type": "array", "items": "string"}}
```

### Optional Array (0..unbounded)
```json
{"name": "field", "type": ["null", {"type": "array", "items": "string"}]}
```

## Example: Full AVRO Schema

```json
{
  "type": "record",
  "name": "CustomerCreditTransfer",
  "namespace": "org.iso20022.pain",
  "doc": "Customer Credit Transfer Initiation",
  "fields": [
    {
      "name": "groupHeader",
      "type": {
        "type": "record",
        "name": "GroupHeader",
        "fields": [
          {"name": "messageId", "type": "string"},
          {
            "name": "creationDateTime",
            "type": {"type": "long", "logicalType": "timestamp-millis"}
          },
          {"name": "numberOfTransactions", "type": "int"},
          {"name": "controlSum", "type": ["null", "double"], "default": null}
        ]
      }
    },
    {
      "name": "paymentInfo",
      "type": {
        "type": "array",
        "items": {
          "type": "record",
          "name": "PaymentInfo",
          "fields": [
            {"name": "paymentId", "type": "string"},
            {"name": "amount", "type": "double"}
          ]
        }
      }
    }
  ]
}
```

**Extracted Fields (10 fields):**
1. `groupHeader` - `CustomerCreditTransfer.groupHeader` - `1..1`
2. `messageId` - `CustomerCreditTransfer.groupHeader.messageId` - `1..1`
3. `creationDateTime` - `CustomerCreditTransfer.groupHeader.creationDateTime` - `1..1`
4. `numberOfTransactions` - `CustomerCreditTransfer.groupHeader.numberOfTransactions` - `1..1`
5. `controlSum` - `CustomerCreditTransfer.groupHeader.controlSum` - `0..1` (Optional)
6. `paymentInfo` - `CustomerCreditTransfer.paymentInfo` - `1..unbounded` (Array)
7. `paymentId` - `CustomerCreditTransfer.paymentInfo.paymentId` - `1..1`
8. `amount` - `CustomerCreditTransfer.paymentInfo.amount` - `1..1`

## Testing AVRO Support

```bash
# 1. Convert XSD to AVRO
python scripts/convert_xsd_to_avro.py

# 2. Analyze AVRO schema
iso20022-agent analyze schemas/pain.001.001.12.avsc -o output/avro_test.csv --detailed

# 3. Compare with XSD results
iso20022-agent analyze schemas/pain.001.001.12.xsd -o output/xsd_test.csv --detailed

# 4. Check field counts match (same structure, different notation)
wc -l output/avro_test.csv output/xsd_test.csv
```

## Benefits of AVRO Support

1. **Modern Format**: AVRO is widely used in big data ecosystems (Kafka, Hadoop)
2. **Compact**: Binary format more efficient than XML
3. **Schema Evolution**: Built-in support for versioning
4. **Language Agnostic**: Works with Python, Java, C++, etc.
5. **Interoperability**: Easier integration with streaming platforms

## Use Cases

### 1. Kafka Integration
```python
# Extract fields from AVRO schema used in Kafka
agent = ISO20022SchemaAgent()
agent.load_schema('kafka/payment-topic.avsc')
fields = agent.extract_fields()
agent.export_csv('docs/kafka_payment_fields.csv')
```

### 2. Schema Registry
```python
# Analyze schemas from Confluent Schema Registry
agent = ISO20022SchemaAgent()
agent.load_schema('registry/schemas/payment-v1.avsc')
agent.print_summary(detailed=True)
```

### 3. Data Pipeline Documentation
```bash
# Generate field documentation for data engineers
iso20022-agent analyze pipeline/payment.avsc -o docs/pipeline_fields.md -f markdown
```

## Limitations

- **Logical Types**: Some AVRO logical types may not have exact XSD equivalents
- **Custom Properties**: AVRO allows arbitrary properties that may not map to XSD constraints
- **Complex Unions**: Multi-type unions (beyond null) are simplified
- **Recursive Types**: Self-referencing schemas may have limited depth

## FAQ

**Q: Can I use both XSD and AVRO in the same project?**  
A: Yes! The agent auto-detects format from file extension.

**Q: Will paths be the same between XSD and AVRO?**  
A: No. XSD uses `/` (slash), AVRO uses `.` (dot). Structure is the same.

**Q: Do code lists work the same way?**  
A: Yes. Both `xs:enumeration` (XSD) and `enum` type (AVRO) are extracted as code lists.

**Q: What about performance?**  
A: AVRO parsing is typically faster than XSD parsing due to simpler JSON structure.

**Q: Can I convert AVRO back to XSD?**  
A: Not currently supported, but you can use the CSV output to generate either format.

## Next Steps

- Test with your AVRO schemas
- Use in Kafka/streaming projects
- Integrate with Schema Registry
- Share feedback for improvements

---

**AVRO support is production-ready! 🚀**
