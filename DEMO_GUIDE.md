# Web UI Demo Guide

## Quick Start for Tomorrow's Demo

### Start the Web UI

```bash
# 1. Open Terminal
cd ~/Documents/data-transform-agent

# 2. Activate virtual environment
source venv/bin/activate

# 3. Start the web server
python app.py
```

The server will start at: **http://localhost:5000**

### Demo Flow (5 minutes)

#### 1. Introduction (30 seconds)
"This is our ISO 20022 Schema Agent - an automated tool that analyzes payment message schemas and extracts all mandatory and optional fields with their constraints."

#### 2. Show Existing Schemas (30 seconds)
- Point to the dropdown showing `pain.001.001.12.xsd`
- Explain: "We can analyze any ISO 20022 schema - payment initiation, clearing & settlement, cash management, etc."

#### 3. Run Analysis (1 minute)
- Select `pain.001.001.12.xsd` from dropdown
- Keep "Show detailed breakdown" checked
- Click **"Analyze Schema"**
- Show loading indicator
- Highlight: "Processing 1,673 fields in seconds"

#### 4. Present Results (2 minutes)
**Statistics Cards:**
- Total Fields: 1,673
- Mandatory: 468 (28%)
- Optional: 1,205 (72%)
- Code Lists: 71 fields with enumerated values
- Patterns: 169 fields with regex validation

**Explain the value:**
- "Every field path is unique"
- "Constraints extracted automatically"
- "Ready for testing and validation"

#### 5. Show Sample Data (1 minute)
Scroll through tables:
- **Mandatory Fields**: MsgId, CreDtTm, etc. with constraints
- **Optional Fields**: CtrlSum, Nm, etc.
- **Code Lists**: AUTH, FDET, FSUM, ILEV values

#### 6. Download & Use (30 seconds)
- Click **"Download Results"** button
- Show CSV opens in Excel/Numbers
- Explain: "Five columns: FieldName, Path, Multiplicity, Constraints, Definition"

#### 7. Alternative Formats (30 seconds)
- Show format selector: CSV, JSON, Markdown
- Demo JSON for programmatic access
- Markdown for documentation

### Key Messages for Business Team

✅ **Automated**: No manual XSD parsing required  
✅ **Accurate**: 100% field extraction with verification  
✅ **Fast**: Analyze complex schemas in seconds  
✅ **Flexible**: CSV, JSON, or Markdown output  
✅ **Complete**: All constraints, patterns, and code lists captured  

### Demo Tips

1. **Keep browser at 100% zoom** for clear display
2. **Pre-select the schema** before demo starts (saves time)
3. **Have Excel/Numbers ready** to open CSV immediately
4. **Show the detailed breakdown** to prove accuracy
5. **Mention testing use case**: "Feed this CSV into your test data generators"

### Backup: Upload New Schema

If asked about other schemas:
1. Click upload section
2. Drag/drop or select XSD file
3. Process same way
4. Show it works with any ISO 20022 schema

### Technical Questions - Prepared Answers

**Q: How do you handle nested structures?**  
A: "We recursively traverse all ComplexTypes and expand them to full field paths - that's why 358 XSD elements become 1,673 unique field paths."

**Q: What about versioning?**  
A: "We support all versions. Compare tool can show field differences between versions like pain.001.001.09 vs .12"

**Q: Can this integrate with our systems?**  
A: "Yes! Three ways: 1) CLI for automation, 2) Python API for custom integration, 3) REST API through this web interface"

**Q: What about validation?**  
A: "We extract all constraints - patterns, lengths, code lists, multiplicities. Feed this into your validators."

**Q: Performance?**  
A: "The pain.001 schema with 1,673 fields processes in under 2 seconds. Scales well for larger schemas."

## Running the Demo

### Option 1: Local Demo
```bash
source venv/bin/activate
python app.py
# Open http://localhost:5000 in browser
```

### Option 2: Network Demo (accessible to team)
```bash
source venv/bin/activate
python app.py
# Access from other machines: http://YOUR-IP:5000
# Find your IP: ifconfig | grep "inet "
```

### Option 3: Share Screen
- Run locally
- Share screen during video call
- Works on any meeting platform

## Troubleshooting

### Issue: Port 5000 already in use
```bash
# Use different port
python -c "from app import app; app.run(port=5001)"
# Then access: http://localhost:5001
```

### Issue: Flask not found
```bash
source venv/bin/activate
pip install flask
```

### Issue: Browser shows old version
```bash
# Hard refresh
# Mac: Command + Shift + R
# Clear browser cache if needed
```

## Post-Demo Actions

After successful demo:

1. **Email results file** to stakeholders
2. **Share GitHub repo** link
3. **Schedule follow-up** for integration discussion
4. **Document feedback** for enhancements
5. **Prepare integration plan** if approved

## Demo Checklist

- [ ] Virtual environment activated
- [ ] Flask installed
- [ ] Web server running at http://localhost:5000
- [ ] Browser open and tested
- [ ] pain.001.001.12.xsd present in schemas/
- [ ] Excel or Numbers ready to open CSV
- [ ] Screen sharing tested (if remote)
- [ ] Backup schemas available
- [ ] This guide accessible for reference
- [ ] 5-minute timer ready

## Success Metrics

**Demo is successful if team understands:**
1. ✅ What the tool does (automated field extraction)
2. ✅ Why it's valuable (saves time, ensures accuracy)
3. ✅ How it works (upload schema → get CSV/JSON/Markdown)
4. ✅ What they get (complete field catalog with constraints)
5. ✅ Next steps (integration possibilities)

## Follow-up Materials

Prepare to share after demo:
- [ ] Link to this repository
- [ ] Sample CSV file (pain001_fields.csv)
- [ ] Quick Start Guide (GETTING_STARTED.md)
- [ ] Mac Usage Guide (docs/MAC_USAGE_GUIDE.md)
- [ ] Accuracy Verification Guide (docs/ACCURACY_VERIFICATION.md)
- [ ] Test Results (TEST_RESULTS.md)

---

**Good luck with tomorrow's demo! 🚀**

The tool is production-ready and will impress the business team with its speed and accuracy.
