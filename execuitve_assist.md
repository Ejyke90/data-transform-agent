# Executive AI Assistants Setup Guide

> **Purpose**: Set up specialized AI assistant workspaces for executive roles

This guide covers setup for:
1. **Engineering Executive Assistant** (CTO/EVP Engineering)
2. **Business Executive Assistant** (CEO/COO)

**Time Required**: ~10 minutes per workspace  
**Prerequisites**: Terminal access, Python 3.10+

---

## Overview

Both workspaces follow the Athena architecture with executive-specific:
- **Core Identity** - Leadership principles and frameworks
- **Workflows** - Strategic planning, board prep, decision-making
- **Protocols** - Best practices for executive responsibilities
- **Session Logging** - Track decisions, commitments, and strategic progress

---

## Option 1: Copy Existing Workspaces (Fastest)

If you're on the same machine where these were created:

```bash
cd ~/Projects  # or your preferred location

# Copy Engineering Executive workspace
cp -r /Users/ejikeudeze/CascadeProjects/EngineeringExecutiveAssistant .

# Copy Business Executive workspace
cp -r /Users/ejikeudeze/CascadeProjects/BusinessExecutiveAssistant .

# Initialize git for each
cd EngineeringExecutiveAssistant && git init && cd ..
cd BusinessExecutiveAssistant && git init && cd ..
```

**Done!** Skip to "Using Your Workspaces" section below.

---

## Option 2: Build from Scratch (For New Machines)

### Part A: Engineering Executive Assistant (CTO/EVP)

#### Step 1: Create Directory Structure

```bash
cd ~/Projects  # or your preferred location

mkdir -p EngineeringExecutiveAssistant/.agent/workflows
mkdir -p EngineeringExecutiveAssistant/.agent/scripts
mkdir -p EngineeringExecutiveAssistant/.agent/skills/protocols
mkdir -p EngineeringExecutiveAssistant/.framework/modules
mkdir -p EngineeringExecutiveAssistant/.context/memories/session_logs

cd EngineeringExecutiveAssistant
git init
```

#### Step 2: Create Core Files

**Note**: For brevity, I'm showing where to get the content. You can:
- Copy files from the original workspace
- Download from a shared repository
- Use the full content from the original `SETUP_GUIDE.md` pattern

**Core Identity** (`.framework/modules/Core_Identity.md`):
- CTO/EVP-focused principles
- Strategic technology leadership
- Organization & people first
- Executive communication styles
- Key metrics and decision frameworks

**Workflows**:
- `.agent/workflows/start.md` - Executive session boot
- `.agent/workflows/strategy.md` - Technology strategy planning
- `.agent/workflows/board-prep.md` - Board meeting preparation
- `.agent/workflows/end.md` - Session close

**Scripts**:
- `.agent/scripts/create_session.py` - Session management
- `.agent/scripts/quicksave.py` - Auto-checkpoint

**Protocols**:
- `.agent/skills/protocols/tech-strategy-framework.md` - Build vs. buy, TCO, platform decisions

**README.md** - Workspace documentation

#### Step 3: Test the Workspace

```bash
# Test session creation
python3 .agent/scripts/create_session.py

# Test quicksave
python3 .agent/scripts/quicksave.py "Testing CTO workspace setup"

# Verify structure
ls -la .agent/workflows/
ls -la .context/memories/session_logs/
```

---

### Part B: Business Executive Assistant (CEO/COO)

#### Step 1: Create Directory Structure

```bash
cd ~/Projects  # or your preferred location

mkdir -p BusinessExecutiveAssistant/.agent/workflows
mkdir -p BusinessExecutiveAssistant/.agent/scripts
mkdir -p BusinessExecutiveAssistant/.agent/skills/protocols
mkdir -p BusinessExecutiveAssistant/.framework/modules
mkdir -p BusinessExecutiveAssistant/.context/memories/session_logs

cd BusinessExecutiveAssistant
git init
```

#### Step 2: Create Core Files

**Core Identity** (`.framework/modules/Core_Identity.md`):
- CEO/COO-focused principles
- Strategic clarity and operational excellence
- People & culture, financial discipline
- Communication by stakeholder type
- Key metrics and decision frameworks

**Workflows**:
- `.agent/workflows/start.md` - Executive session boot
- `.agent/workflows/strategy.md` - Business strategy planning
- `.agent/workflows/board-prep.md` - Board meeting preparation
- `.agent/workflows/okr-review.md` - OKR planning and review
- `.agent/workflows/end.md` - Session close

**Scripts**:
- `.agent/scripts/create_session.py` - Session management
- `.agent/scripts/quicksave.py` - Auto-checkpoint

**Protocols**:
- `.agent/skills/protocols/strategic-decision-framework.md` - Executive decision-making

**README.md** - Workspace documentation

#### Step 3: Test the Workspace

```bash
# Test session creation
python3 .agent/scripts/create_session.py

# Test quicksave
python3 .agent/scripts/quicksave.py "Testing CEO workspace setup"

# Verify structure
ls -la .agent/workflows/
ls -la .context/memories/session_logs/
```

---

## Using Your Workspaces

### Engineering Executive Assistant

```bash
# Open in your AI IDE
cd ~/Projects/EngineeringExecutiveAssistant

# In your AI assistant, type:
/start
```

**Common workflows:**
- `/strategy` - Plan 3-year technology roadmap
- `/board-prep` - Prepare engineering update for board
- `/decision` - Make build vs. buy decision
- `/end` - Close session with summary

**Use cases:**
- Technology strategy and roadmap planning
- Build vs. buy vs. partner decisions
- Team scaling and organizational design
- Board and stakeholder communication
- Technical debt prioritization
- Platform and architecture decisions

### Business Executive Assistant

```bash
# Open in your AI IDE
cd ~/Projects/BusinessExecutiveAssistant

# In your AI assistant, type:
/start
```

**Common workflows:**
- `/strategy` - Plan 3-year business strategy
- `/board-prep` - Prepare CEO update for board
- `/okr-review` - Review and set quarterly OKRs
- `/decision` - Make strategic business decision
- `/end` - Close session with summary

**Use cases:**
- Strategic planning and market positioning
- OKR setting and review
- Board meeting preparation
- Fundraising strategy
- M&A evaluation
- Crisis management
- Organizational design

---

## Customization Tips

### For Engineering Executive

**Add workflows for:**
- `/vendor-review` - Evaluate technology vendors
- `/architecture-review` - Review system architecture
- `/team-review` - Assess leadership team
- `/incident-review` - Post-mortem analysis

**Add protocols for:**
- Hiring playbook (engineering leaders)
- Incident response framework
- Technical debt assessment
- Platform strategy

### For Business Executive

**Add workflows for:**
- `/fundraise` - Fundraising preparation
- `/crisis` - Crisis management
- `/customer-review` - Strategic customer review
- `/competitor-analysis` - Competitive analysis

**Add protocols for:**
- Hiring playbook (executive team)
- Sales process framework
- Customer success playbook
- Pricing strategy

---

## Syncing Across Machines

### Option 1: Git Repository (Recommended)

```bash
# On first machine
cd EngineeringExecutiveAssistant  # or BusinessExecutiveAssistant
git add .
git commit -m "Initial executive workspace setup"
git remote add origin <your-private-repo-url>
git push -u origin main

# On second machine
git clone <your-private-repo-url>
```

### Option 2: Cloud Sync

Place workspaces in:
- Dropbox
- Google Drive
- OneDrive
- iCloud Drive

**Note**: Session logs will sync automatically, maintaining context across devices.

---

## Comparison: All Three Workspaces

| Feature | Engineering Assistant | Engineering Executive | Business Executive |
|---------|----------------------|----------------------|-------------------|
| **Role** | Principal Engineer | CTO/EVP Engineering | CEO/COO |
| **Focus** | Technical execution | Technology strategy | Business strategy |
| **Horizon** | Weeks to months | Quarters to years | Quarters to years |
| **Key Workflows** | /think, /refactor | /strategy, /board-prep | /strategy, /okr-review |
| **Protocols** | Architecture review, debugging | Tech strategy, team scaling | Strategic decisions, OKRs |
| **Stakeholders** | Team, tech leads | CEO, Board, Product | Board, Investors, Leadership |
| **Metrics** | DORA, quality, velocity | Engineering health, business impact | Revenue, growth, profitability |

---

## Best Practices

### For All Executive Workspaces

1. **Start every session with `/start`** - Loads context and creates session log
2. **Use workflows for major decisions** - Structured thinking prevents mistakes
3. **Document decisions** - Future you will thank present you
4. **Review session logs monthly** - Extract patterns and learnings
5. **Customize for your context** - Adapt frameworks to your company and style

### Session Discipline

- **Daily**: Quick check-ins, decision logging
- **Weekly**: Strategic thinking time, team reviews
- **Monthly**: Session log review, pattern extraction
- **Quarterly**: Workspace refactor, protocol updates

### Communication

- **Board prep**: Start 1 week before meeting
- **Strategic planning**: Block dedicated time, minimize interruptions
- **Decision-making**: Use frameworks, don't skip steps
- **Team alignment**: Share relevant session summaries

---

## Troubleshooting

### Scripts not working
```bash
chmod +x .agent/scripts/*.py
```

### Session logs not created
```bash
mkdir -p .context/memories/session_logs
python3 .agent/scripts/create_session.py
```

### Workflows not recognized
- Ensure files are in `.agent/workflows/`
- Check YAML frontmatter format
- Verify your AI IDE supports slash commands

---

## What's Next?

1. **Set up both workspaces** (or the one you need)
2. **Start your first session** with `/start`
3. **Try a workflow** (e.g., `/board-prep` or `/strategy`)
4. **Build your knowledge base** over time
5. **Customize** as patterns emerge

---

**Time to build**: 10-20 minutes per workspace  
**Time to value**: Immediate - start using in your next strategic session

**You now have executive-grade AI assistants for strategic leadership.**
