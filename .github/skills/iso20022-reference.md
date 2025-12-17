# ISO 20022 Payment Messages Reference Guide

## Overview

ISO 20022 is the international standard for electronic data interchange between financial institutions. It uses XML-based messages with rich, structured data.

## Message Naming Convention

ISO 20022 messages follow the pattern: `xxxx.yyy.yyy.zz`

- **xxxx**: Business area (4 letters)
  - `pain`: Payment Initiation
  - `pacs`: Payment Clearing and Settlement
  - `camt`: Cash Management
  - `head`: Business Application Header
  
- **yyy.yyy**: Message functionality (6 digits)
  - First 3 digits: Message type
  - Last 3 digits: Variant
  
- **zz**: Version (2 digits)
  - e.g., `09` = version 9

**Example**: `pain.001.001.09`
- Business Area: Payment Initiation (pain)
- Message Type: Customer Credit Transfer Initiation (001)
- Variant: 001
- Version: 09

## Payment Initiation Messages (pain)

### pain.001 - Customer Credit Transfer Initiation
**Purpose**: Customer instructs bank to transfer funds to a creditor

**Key Mandatory Fields**:
```
Document/CstmrCdtTrfInitn/
  ├─ GrpHdr/                          [1..1] Group Header
  │  ├─ MsgId                         [1..1] Unique message ID
  │  ├─ CreDtTm                       [1..1] Creation date/time
  │  ├─ NbOfTxs                       [1..1] Number of transactions
  │  ├─ CtrlSum                       [0..1] Total amount (optional)
  │  └─ InitgPty                      [1..1] Initiating party
  └─ PmtInf/                          [1..n] Payment Information
     ├─ PmtInfId                      [1..1] Payment info ID
     ├─ PmtMtd                        [1..1] Payment method (e.g., TRF)
     ├─ ReqdExctnDt                   [1..1] Requested execution date
     ├─ Dbtr                          [1..1] Debtor
     ├─ DbtrAcct                      [1..1] Debtor account
     ├─ DbtrAgt                       [1..1] Debtor agent (bank)
     └─ CdtTrfTxInf/                  [1..n] Credit transfer transaction
        ├─ PmtId                      [1..1] Payment identification
        ├─ Amt                        [1..1] Amount
        ├─ CdtrAgt                    [0..1] Creditor agent
        ├─ Cdtr                       [1..1] Creditor
        └─ CdtrAcct                   [1..1] Creditor account
```

**Common Use Cases**:
- Salary payments
- Supplier payments
- Bill payments
- Interbank transfers

### pain.002 - Customer Payment Status Report
**Purpose**: Bank reports status of customer's payment instruction

**Key Mandatory Fields**:
```
Document/CstmrPmtStsRpt/
  ├─ GrpHdr/                          [1..1] Group Header
  │  ├─ MsgId                         [1..1] Message ID
  │  └─ CreDtTm                       [1..1] Creation date/time
  └─ OrgnlGrpInfAndSts/               [0..1] Original group info & status
     ├─ OrgnlMsgId                    [1..1] Original message ID
     ├─ OrgnlMsgNmId                  [1..1] Original message name ID
     └─ GrpSts                        [0..1] Group status (ACCP, RJCT, etc.)
```

**Status Codes**:
- `ACCP`: Accepted Customer Profile
- `ACSC`: Accepted Settlement Completed
- `ACSP`: Accepted Settlement in Process
- `RJCT`: Rejected
- `PDNG`: Pending
- `PART`: Partially Accepted

### pain.008 - Customer Direct Debit Initiation
**Purpose**: Customer instructs bank to collect funds from debtor

**Key Mandatory Fields**:
```
Document/CstmrDrctDbtInitn/
  ├─ GrpHdr/                          [1..1] Group Header
  └─ PmtInf/                          [1..n] Payment Information
     ├─ PmtTpInf/                     [0..1] Payment type info
     │  └─ SeqTp                      [1..1] Sequence type (FRST, RCUR, etc.)
     ├─ Cdtr                          [1..1] Creditor
     ├─ CdtrAcct                      [1..1] Creditor account
     └─ DrctDbtTxInf/                 [1..n] Direct debit transaction
        ├─ MndtRltdInf                [1..1] Mandate related info
        ├─ DbtrAgt                    [1..1] Debtor agent
        ├─ Dbtr                       [1..1] Debtor
        └─ DbtrAcct                   [1..1] Debtor account
```

**Sequence Types**:
- `FRST`: First collection
- `RCUR`: Recurring collection
- `FNAL`: Final collection
- `OOFF`: One-off collection

## Payment Clearing and Settlement Messages (pacs)

### pacs.008 - FI to FI Customer Credit Transfer
**Purpose**: Financial institution transfers customer payment to another FI

**Key Mandatory Fields**:
```
Document/FIToFICstmrCdtTrf/
  ├─ GrpHdr/                          [1..1] Group Header
  │  ├─ MsgId                         [1..1] Message ID
  │  ├─ CreDtTm                       [1..1] Creation date/time
  │  ├─ NbOfTxs                       [1..1] Number of transactions
  │  ├─ SttlmInf/                     [1..1] Settlement info
  │  │  └─ SttlmMtd                   [1..1] Settlement method
  │  ├─ InstgAgt                      [0..1] Instructing agent
  │  └─ InstdAgt                      [0..1] Instructed agent
  └─ CdtTrfTxInf/                     [1..n] Credit transfer transaction
     ├─ PmtId                         [1..1] Payment identification
     ├─ IntrBkSttlmAmt                [1..1] Interbank settlement amount
     ├─ IntrBkSttlmDt                 [0..1] Interbank settlement date
     ├─ InstgAgt                      [1..1] Instructing agent
     ├─ InstdAgt                      [1..1] Instructed agent
     ├─ Dbtr                          [1..1] Debtor
     ├─ DbtrAcct                      [0..1] Debtor account
     ├─ CdtrAgt                       [1..1] Creditor agent
     ├─ Cdtr                          [1..1] Creditor
     └─ CdtrAcct                      [0..1] Creditor account
```

**Settlement Methods**:
- `INDA`: Instructed Agent
- `INGA`: Instructing Agent
- `COVE`: Cover Method
- `CLRG`: Clearing System

### pacs.002 - FI to FI Payment Status Report
**Purpose**: Report status of payment between financial institutions

**Key Mandatory Fields**:
```
Document/FIToFIPmtStsRpt/
  ├─ GrpHdr/                          [1..1] Group Header
  │  ├─ MsgId                         [1..1] Message ID
  │  └─ CreDtTm                       [1..1] Creation date/time
  └─ TxInfAndSts/                     [1..n] Transaction info & status
     ├─ StsId                         [0..1] Status ID
     ├─ OrgnlInstrId                  [0..1] Original instruction ID
     ├─ OrgnlEndToEndId               [0..1] Original end-to-end ID
     ├─ TxSts                         [0..1] Transaction status
     └─ StsRsnInf                     [0..n] Status reason info
```

### pacs.004 - Payment Return
**Purpose**: Return a payment to the originating FI

**Key Mandatory Fields**:
```
Document/PmtRtr/
  ├─ GrpHdr/                          [1..1] Group Header
  └─ TxInf/                           [1..n] Transaction information
     ├─ RtrId                         [1..1] Return ID
     ├─ OrgnlInstrId                  [0..1] Original instruction ID
     ├─ OrgnlEndToEndId               [1..1] Original end-to-end ID
     ├─ RtrdIntrBkSttlmAmt            [1..1] Returned interbank amount
     └─ RtrRsnInf                     [0..n] Return reason info
```

**Common Return Reasons**:
- `AC01`: Incorrect account number
- `AC04`: Closed account
- `AC06`: Blocked account
- `AG01`: Transaction forbidden
- `AM05`: Duplication
- `NARR`: Narrative (with text explanation)

### pacs.007 - FI to FI Payment Reversal
**Purpose**: Reverse a previously sent payment instruction

**Key Mandatory Fields**:
```
Document/FIToFIPmtRvsl/
  ├─ GrpHdr/                          [1..1] Group Header
  └─ TxInf/                           [1..n] Transaction information
     ├─ RvslId                        [1..1] Reversal ID
     ├─ OrgnlInstrId                  [0..1] Original instruction ID
     ├─ OrgnlEndToEndId               [0..1] Original end-to-end ID
     └─ RvslRsnInf                    [0..n] Reversal reason info
```

## Cash Management Messages (camt)

### camt.052 - Bank to Customer Account Report
**Purpose**: Intraday account activity report

**Key Mandatory Fields**:
```
Document/BkToCstmrAcctRpt/
  ├─ GrpHdr/                          [1..1] Group Header
  │  ├─ MsgId                         [1..1] Message ID
  │  └─ CreDtTm                       [1..1] Creation date/time
  └─ Rpt/                             [1..n] Report
     ├─ Id                            [1..1] Report ID
     ├─ CreDtTm                       [1..1] Creation date/time
     ├─ Acct                          [1..1] Account
     └─ Ntry/                         [0..n] Entry
        ├─ Amt                        [1..1] Amount
        ├─ CdtDbtInd                  [1..1] Credit/Debit indicator
        ├─ Sts                        [1..1] Status (BOOK, PDNG, INFO)
        └─ BkTxCd                     [1..1] Bank transaction code
```

**Status Values**:
- `BOOK`: Booked
- `PDNG`: Pending
- `INFO`: Information only

### camt.053 - Bank to Customer Statement
**Purpose**: End-of-day account statement

**Key Mandatory Fields**:
```
Document/BkToCstmrStmt/
  ├─ GrpHdr/                          [1..1] Group Header
  └─ Stmt/                            [1..n] Statement
     ├─ Id                            [1..1] Statement ID
     ├─ CreDtTm                       [1..1] Creation date/time
     ├─ Acct                          [1..1] Account
     ├─ Bal/                          [1..n] Balance
     │  ├─ Tp                         [1..1] Type (OPBD, CLBD, etc.)
     │  ├─ Amt                        [1..1] Amount
     │  └─ CdtDbtInd                  [1..1] Credit/Debit indicator
     └─ Ntry/                         [0..n] Entry
        └─ NtryDtls                   [0..n] Entry details
```

**Balance Types**:
- `OPBD`: Opening Booked
- `CLBD`: Closing Booked
- `ITBD`: Interim Booked
- `OPAV`: Opening Available
- `CLAV`: Closing Available

### camt.054 - Bank to Customer Debit Credit Notification
**Purpose**: Real-time notification of account debits/credits

**Key Mandatory Fields**:
```
Document/BkToCstmrDbtCdtNtfctn/
  ├─ GrpHdr/                          [1..1] Group Header
  └─ Ntfctn/                          [1..n] Notification
     ├─ Id                            [1..1] Notification ID
     ├─ CreDtTm                       [1..1] Creation date/time
     ├─ Acct                          [1..1] Account
     └─ Ntry/                         [1..n] Entry
        ├─ Amt                        [1..1] Amount
        ├─ CdtDbtInd                  [1..1] Credit/Debit indicator
        └─ Sts                        [1..1] Status
```

### camt.056 - FI to FI Payment Cancellation Request
**Purpose**: Request cancellation of a previously sent payment

**Key Mandatory Fields**:
```
Document/FIToFIPmtCxlReq/
  ├─ Assgnmt/                         [1..1] Assignment
  │  ├─ Id                            [1..1] Assignment ID
  │  ├─ Assgnr                        [1..1] Assigner
  │  └─ Assgne                        [1..1] Assignee
  └─ Undrlyg/                         [1..n] Underlying
     └─ TxInf/                        [0..1] Transaction info
        ├─ CxlId                      [0..1] Cancellation ID
        ├─ OrgnlInstrId               [0..1] Original instruction ID
        └─ OrgnlEndToEndId            [0..1] Original end-to-end ID
```

## Business Application Header (head.001.001.xx)

### Purpose
The Business Application Header (BAH) is a standardized wrapper that accompanies ISO 20022 business messages, providing:
- Message routing information
- Sender and receiver identification
- Message metadata
- Duplicate detection
- Priority indication

### Key Mandatory Fields
```
AppHdr/
  ├─ Fr/                              [1..1] From (sender)
  │  └─ FIId/                         [0..1] Financial Institution ID
  │     └─ FinInstnId                 [1..1] Financial Institution
  ├─ To/                              [1..1] To (receiver)
  │  └─ FIId/                         [0..1] Financial Institution ID
  │     └─ FinInstnId                 [1..1] Financial Institution
  ├─ BizMsgIdr                        [1..1] Business message ID
  ├─ MsgDefIdr                        [1..1] Message definition ID
  ├─ CreDt                            [1..1] Creation date
  └─ BizSvc                           [0..1] Business service
```

### Optional but Important Fields
```
AppHdr/
  ├─ CpyDplct                         [0..1] Copy/Duplicate indicator
  ├─ PssblDplct                       [0..1] Possible duplicate flag
  ├─ Prty                             [0..1] Priority (HIGH, NORM)
  ├─ Sgntr                            [0..1] Digital signature
  └─ Rltd/                            [0..1] Related reference
     ├─ Fr                            [0..1] From
     ├─ To                            [0..1] To
     ├─ BizMsgIdr                     [0..1] Related message ID
     └─ CreDt                         [0..1] Creation date
```

### Example BAH Usage
```xml
<AppHdr xmlns="urn:iso:std:iso:20022:tech:xsd:head.001.001.02">
  <Fr>
    <FIId>
      <FinInstnId>
        <BICFI>BANKUSXXXXX</BICFI>
      </FinInstnId>
    </FIId>
  </Fr>
  <To>
    <FIId>
      <FinInstnId>
        <BICFI>BANKGBXXXXX</BICFI>
      </FinInstnId>
    </FIId>
  </To>
  <BizMsgIdr>MSGID-2025-001</BizMsgIdr>
  <MsgDefIdr>pacs.008.001.08</MsgDefIdr>
  <CreDt>2025-12-16T10:30:00Z</CreDt>
</AppHdr>
```

## Common Data Types

### Simple Types

| Type | Description | Example |
|------|-------------|---------|
| Max3Text | Up to 3 characters | "USD" |
| Max35Text | Up to 35 characters | Message IDs |
| Max140Text | Up to 140 characters | Descriptions |
| Max350Text | Up to 350 characters | Long text |
| ISODate | Date (YYYY-MM-DD) | "2025-12-16" |
| ISODateTime | Date and time | "2025-12-16T10:30:00" |
| IBAN2007Identifier | IBAN format | "GB82WEST12345698765432" |
| BICFIDec2014Identifier | BIC code | "BANKGB22XXX" |
| ActiveOrHistoricCurrencyCode | ISO 4217 currency | "USD", "EUR" |
| LEIIdentifier | Legal Entity Identifier | 20-character code |

### Complex Types

#### PartyIdentification
```
Nm                     [0..1] Name
PstlAdr/               [0..1] Postal Address
  ├─ StrtNm            [0..1] Street name
  ├─ BldgNb            [0..1] Building number
  ├─ PstCd             [0..1] Postal code
  ├─ TwnNm             [0..1] Town name
  └─ Ctry              [0..1] Country (ISO 3166)
Id/                    [0..1] Identification
  ├─ OrgId             [0..1] Organization ID
  └─ PrvtId            [0..1] Private ID
```

#### FinancialInstitutionIdentification
```
BICFI                  [0..1] BIC code
ClrSysMmbId/           [0..1] Clearing system member ID
  ├─ ClrSysId          [1..1] Clearing system
  └─ MmbId             [1..1] Member ID
LEI                    [0..1] Legal Entity Identifier
Nm                     [0..1] Name
PstlAdr                [0..1] Postal Address
Othr/                  [0..1] Other identification
  ├─ Id                [1..1] Identification
  └─ SchmeNm           [0..1] Scheme name
```

#### AccountIdentification
```
IBAN                   [0..1] IBAN
Othr/                  [0..1] Other
  ├─ Id                [1..1] Identification
  └─ SchmeNm           [0..1] Scheme name
```

## Validation Rules

### Standard Checks
1. **XML Well-formedness**: Valid XML structure
2. **Schema Compliance**: Validates against XSD
3. **Namespace**: Correct ISO 20022 namespace URI
4. **Message Type**: Valid message identifier

### Business Rules
1. **ControlSum**: Sum of transaction amounts = control sum (if present)
2. **NumberOfTransactions**: Count of transactions matches declared number
3. **Date Logic**: Settlement date >= creation date
4. **Currency Consistency**: Same currency within payment instruction
5. **Account Format**: IBAN checksum validation
6. **BIC Format**: 8 or 11 character BIC validation

### Cross-Field Validation
1. **Debtor Agent Required**: For credit transfers, debtor agent mandatory
2. **Creditor Agent Required**: For direct debits, creditor agent mandatory
3. **Mandate Info**: Required for direct debits (first/recurring)
4. **Settlement Info**: Required for FI-to-FI messages
5. **Status Reason**: Required when status is RJCT

## Regional Implementations

### SEPA (Single Euro Payments Area)
- **Scheme**: European Union payment scheme
- **Currency**: EUR only
- **Account**: IBAN mandatory
- **Additional Rules**: SEPA specific rulebooks apply
- **Messages**: pain.001, pain.008, pacs.008, camt.053

### SWIFT gpi (Global Payments Innovation)
- **Tracking**: End-to-end payment tracking
- **Speed**: Same-day use of funds
- **Transparency**: Fee transparency
- **Messages**: Enhanced pacs.008 with gpi extensions

### US Fedwire
- **Network**: Federal Reserve payment system
- **Currency**: USD only
- **Real-time**: Immediate settlement
- **Messages**: Mapped to ISO 20022 equivalents

### UK Faster Payments
- **Speed**: Near real-time clearing
- **Limit**: Transaction limits apply
- **Currency**: GBP only
- **Messages**: pain.001, pacs.008, camt.054

## Best Practices

### Message Design
1. Use structured remittance info for reconciliation
2. Include end-to-end references for tracking
3. Populate optional fields when beneficial
4. Use clear, descriptive message IDs
5. Include contact information for queries

### Error Handling
1. Validate before sending
2. Handle rejection codes appropriately
3. Implement retry logic for temporary failures
4. Log all messages for audit
5. Provide clear error messages to users

### Performance
1. Batch transactions when possible
2. Cache schema validations
3. Use incremental processing for large files
4. Implement parallel processing where appropriate
5. Monitor message processing times

### Security
1. Encrypt sensitive data
2. Use digital signatures (BAH)
3. Validate sender/receiver identity
4. Implement non-repudiation
5. Audit all transactions

## Resources

- **ISO 20022 Website**: https://www.iso20022.org/
- **Message Catalogue**: https://www.iso20022.org/iso-20022-message-definitions
- **External Code Lists**: https://www.iso20022.org/external_code_list.page
- **SWIFT Standards**: https://www.swift.com/standards/iso-20022
- **MyStandards**: SWIFT's implementation tool
