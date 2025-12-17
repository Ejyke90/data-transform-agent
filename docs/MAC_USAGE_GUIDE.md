# Mac User Guide for ISO 20022 Schema Agent

This guide is specifically designed for macOS users to help you get the most out of the ISO 20022 Schema Agent.

## Table of Contents
1. [Understanding macOS Python](#understanding-macos-python)
2. [Installation Guide](#installation-guide)
3. [Daily Usage Workflow](#daily-usage-workflow)
4. [Common Mac Commands](#common-mac-commands)
5. [Troubleshooting](#troubleshooting)
6. [Tips & Tricks](#tips--tricks)

## Understanding macOS Python

### Why Virtual Environments?

Modern macOS (Monterey and later) implements **PEP 668** protection, which prevents installing packages directly to the system Python. This is why you'll see errors like:

```
error: externally-managed-environment
```

**Solution:** Always use virtual environments. They're isolated, safe, and won't affect your system Python.

### Python Commands on Mac

| Command | What It Does |
|---------|--------------|
| `python3` | Runs Python 3 (correct for Mac) |
| `pip3` | Installs packages for Python 3 |
| `python` | Often points to Python 2 (deprecated) |
| `pip` | May not work without venv |

**Always use `python3` and `pip3` on macOS!**

## Installation Guide

### One-Time Setup

Open Terminal (`Applications` → `Utilities` → `Terminal`) and run:

```bash
# 1. Navigate to your workspace
cd ~/Documents  # or your preferred location

# 2. Clone or navigate to project
cd data-transform-agent

# 3. Create virtual environment
python3 -m venv venv

# 4. Activate virtual environment
source venv/bin/activate

# 5. Install dependencies
pip install -r requirements.txt

# 6. Install the agent
pip install -e .

# 7. Verify installation
iso20022-agent --help
```

### What Each Step Does

1. **`cd ~/Documents`** - Navigate to your Documents folder
2. **`cd data-transform-agent`** - Enter the project directory
3. **`python3 -m venv venv`** - Creates a folder called `venv` with isolated Python
4. **`source venv/bin/activate`** - Activates the environment (you'll see `(venv)` in prompt)
5. **`pip install -r requirements.txt`** - Installs lxml and pandas
6. **`pip install -e .`** - Installs the agent in "editable" mode
7. **`iso20022-agent --help`** - Tests that everything works

## Daily Usage Workflow

Every time you open a **new** Terminal window, you need to activate the virtual environment:

```bash
# Navigate to project
cd ~/Documents/data-transform-agent

# Activate venv
source venv/bin/activate

# Now you can use the agent!
iso20022-agent analyze schemas/pain.001.001.12.xsd -o output/fields.csv
```

### Complete Analysis Example

```bash
# 1. Open Terminal

# 2. Activate environment
cd ~/Documents/data-transform-agent
source venv/bin/activate

# 3. Analyze schema
iso20022-agent analyze schemas/pain.001.001.12.xsd -o output/pain001_fields.csv

# 4. Get detailed breakdown (recommended for accuracy verification)
iso20022-agent analyze schemas/pain.001.001.12.xsd -o output/fields.csv --detailed

# 5. View results in default app (Numbers/Excel)
open output/pain001_fields.csv

# 6. Or view in terminal
cat output/pain001_fields.csv

# 6. Export to other formats
iso20022-agent analyze schemas/pain.001.001.12.xsd -o output/fields.json -f json
iso20022-agent analyze schemas/pain.001.001.12.xsd -o output/fields.md -f markdown
```

## Common Mac Commands

### File Management

```bash
# List files in current directory
ls

# List files including hidden ones (like .venv)
ls -la

# View current directory path
pwd

# Open current directory in Finder
open .

# Open specific file in default app
open output/pain001_fields.csv

# View file contents in terminal
cat output/pain001_fields.csv

# View large file with pagination
less output/pain001_fields.csv  # Press 'q' to quit

# Copy file
cp source.xsd destination.xsd

# Move/rename file
mv old_name.xsd new_name.xsd

# Create directory
mkdir new_folder

# Remove file
rm filename.csv
```

### Schema Management

```bash
# Download schema to Downloads folder, then move it
mv ~/Downloads/pain.001.001.12.xsd schemas/

# Check what schemas you have
ls schemas/

# Analyze all schemas in directory
for schema in schemas/*.xsd; do
  iso20022-agent analyze "$schema" -o "output/$(basename $schema .xsd)_fields.csv"
done
```

### Virtual Environment Commands

```bash
# Activate venv
source venv/bin/activate

# Deactivate venv (go back to system Python)
deactivate

# Check if venv is active (you'll see (venv) in prompt)
which python  # Should show path with 'venv' in it

# Recreate venv if corrupted
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Troubleshooting

### Problem: "command not found: pip"

**Solution:** Use `pip3` instead:
```bash
pip3 --version
```

### Problem: "externally-managed-environment"

**Solution:** You're not in a virtual environment. Activate it:
```bash
cd /path/to/data-transform-agent
source venv/bin/activate
```

### Problem: "No such file or directory: schemas/pain.001.001.12.xsd"

**Solution:** Make sure the XSD file is in the schemas directory:
```bash
# Check if file exists
ls schemas/

# If not there, download or move it
mv ~/Downloads/pain.001.001.12.xsd schemas/
```

### Problem: "iso20022-agent: command not found"

**Solution:** Either venv is not activated or agent not installed:
```bash
# Activate venv
source venv/bin/activate

# Reinstall agent
pip install -e .
```

### Problem: Can't see .venv or hidden files in Finder

**Solution:** Press `Command + Shift + .` (dot) to toggle hidden files

### Problem: Permission denied

**Solution:** Don't use `sudo` with pip! Use virtual environment instead:
```bash
# WRONG: sudo pip install ...
# RIGHT:
source venv/bin/activate
pip install ...
```

## Tips & Tricks

### 1. Create a Startup Script

Create a file called `start.sh` in your project root:

```bash
#!/bin/bash
cd ~/Documents/data-transform-agent
source venv/bin/activate
echo "✓ Virtual environment activated"
echo "Ready to analyze ISO 20022 schemas!"
```

Make it executable:
```bash
chmod +x start.sh
```

Use it:
```bash
./start.sh
```

### 2. Add Alias to Your Shell

Add to `~/.zshrc`:
```bash
alias iso20022="cd ~/Documents/data-transform-agent && source venv/bin/activate"
```

Then reload:
```bash
source ~/.zshrc
```

Now just type:
```bash
iso20022
```

### 3. Use Tab Completion

Start typing and press `Tab`:
```bash
iso20022-agent ana<TAB>  # Completes to "analyze"
```

### 4. View Multiple Files at Once

```bash
# Open all CSV files in output directory
open output/*.csv

# View first 10 lines of each CSV
for csv in output/*.csv; do
  echo "=== $csv ==="
  head -10 "$csv"
done
```

### 5. Compare Outputs

```bash
# Compare two CSV files
diff output/pain001_v11_fields.csv output/pain001_v12_fields.csv

# Or use built-in compare command
iso20022-agent compare schemas/pain.001.001.11.xsd schemas/pain.001.001.12.xsd
```

### 6. Quick Field Search

```bash
# Search for specific field in CSV
grep "MsgId" output/pain001_fields.csv

# Case-insensitive search
grep -i "message" output/pain001_fields.csv

# Count mandatory fields
grep "1..1" output/pain001_fields.csv | wc -l
```

### 7. Keep Terminal Open with venv Active

Instead of deactivating and reactivating, just minimize the Terminal window and come back to it later. The venv stays active!

### 8. Using Numbers (Apple's Excel)

```bash
# Open CSV in Numbers
open -a Numbers output/pain001_fields.csv

# Or just double-click in Finder (defaults to Numbers if installed)
open output/pain001_fields.csv
```

### 9. Batch Processing

```bash
# Analyze all pain schemas
for schema in schemas/pain.*.xsd; do
  name=$(basename "$schema" .xsd)
  iso20022-agent analyze "$schema" -o "output/${name}_fields.csv"
  echo "✓ Processed $name"
done
```

### 10. Check Python Details

```bash
# Python version
python3 --version

# Python location
which python3

# Installed packages
pip list

# Package details
pip show lxml
```

## Environment Variables

Add these to `~/.zshrc` for convenience:

```bash
# Project directory
export ISO20022_HOME="$HOME/Documents/data-transform-agent"

# Quick navigate
alias cdiso="cd $ISO20022_HOME"

# Activate environment
alias isoenv="cd $ISO20022_HOME && source venv/bin/activate"
```

Reload:
```bash
source ~/.zshrc
```

## Performance Tips

1. **SSD matters**: Parsing large XSD files is I/O intensive
2. **Use latest Python**: Python 3.11+ is significantly faster
3. **Increase memory** for large schemas: Close other apps
4. **Use JSON for speed**: CSV formatting is slower for huge datasets

## Getting Help

- **Agent help**: `iso20022-agent --help`
- **Command help**: `iso20022-agent analyze --help`
- **Python help**: `python3 -c "from iso20022_agent import ISO20022SchemaAgent; help(ISO20022SchemaAgent)"`
- **Check logs**: Look for error messages in terminal output

## Resources

- **ISO 20022 Official**: https://www.iso20022.org/
- **Python Docs**: https://docs.python.org/3/
- **macOS Terminal Guide**: https://support.apple.com/guide/terminal/
- **Zsh Documentation**: https://zsh.sourceforge.io/Doc/

---

**Pro Tip:** Bookmark this guide and keep your Terminal window open with venv activated for faster workflow! 🚀
