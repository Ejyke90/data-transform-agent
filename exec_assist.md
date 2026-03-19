# Business Executive Assistant Setup - Part 2
## Continuation of CEO/COO Workspace Setup

This is Part 2 of the Business Executive Assistant setup. Complete Part 1 first (directory structure and Core Identity).

---

## Step 3: Create Workflows

### Create `/start` workflow

```bash
cat > .agent/workflows/start.md << 'ENDOFFILE'
---
description: Boot CEO/COO strategic assistant with business context
---

# /start — Executive Session Initialization

## Phase 1: Load Executive Identity

- [ ] Read `.framework/modules/Core_Identity.md`
- [ ] Confirm business leadership principles loaded
- [ ] Activate executive decision framework

## Phase 2: Recall Business Context

- [ ] Find the latest session log in `.context/memories/session_logs/`
- [ ] Display executive summary:
  - Strategic priorities and progress
  - Key business metrics and trends
  - Critical decisions pending
  - Board and investor commitments

## Phase 3: Create New Session

- [ ] Run `python .agent/scripts/create_session.py`
- [ ] Session file format: `YYYY-MM-DD-session-XX.md`
- [ ] Initialize executive session metadata

## Phase 4: Ready Confirmation

- [ ] Output: "⚡ Ready. Session XX started. Business context loaded."
- [ ] Highlight any urgent items requiring executive attention

## Autonomic Behaviors (Active Throughout Session)

| Behavior | Trigger | Action |
|----------|---------|--------|
| **Strategic Logging** | After major decisions | Document decision, rationale, and impact |
| **Quicksave** | After every response | `python .agent/scripts/quicksave.py "<summary>"` |
| **Stakeholder Tracking** | Commitments made | Add to stakeholder log (board, investors, customers) |
| **Metric Monitoring** | Financial/growth metrics discussed | Track trends and flag anomalies |

---

## Quick Reference

- `/start` - Boot executive session
- `/end` - Close session and prepare executive summary
- `/strategy` - Deep strategic planning mode
- `/board-prep` - Prepare for board meeting
- `/okr-review` - Review OKRs and progress
- `/decision` - Executive decision framework
- `/fundraise` - Fundraising preparation

---

*Vision. Execution. Results.*
ENDOFFILE
```

### Create `/strategy` workflow

```bash
cat > .agent/workflows/strategy.md << 'ENDOFFILE'
---
description: Deep strategic business planning and analysis
---

# /strategy — Strategic Business Planning

> **Use when**: Annual planning, market expansion, strategic pivots, M&A

## Phase 1: Strategic Context

### Current State
- [ ] Where are we today? (market position, financials, team)
- [ ] What's working? What's not?
- [ ] What are our core strengths?
- [ ] What are our key constraints?

### Market Analysis
- [ ] Market size and growth rate (TAM, SAM, SOM)
- [ ] Competitive landscape and positioning
- [ ] Customer trends and needs
- [ ] Regulatory or macro trends

### Strategic Intent
- [ ] Where do we want to be in 3 years?
- [ ] What does success look like?
- [ ] What's our sustainable competitive advantage?
- [ ] What are we willing to bet on?

## Phase 2: Strategic Options

Generate at least 3 strategic paths:

### Option A: [Name - e.g., "Double Down on Core"]
- **Description**: What is this strategy?
- **Market Opportunity**: What market are we targeting?
- **Competitive Positioning**: How do we win?
- **Revenue Model**: How do we make money?
- **Investment Required**: Time, money, resources
- **Key Risks**: What could derail this?
- **3-Year Outcome**: Where does this take us?

### Option B: [Name - e.g., "Expand to Adjacent Market"]
- **Description**: What is this strategy?
- **Market Opportunity**: What market are we targeting?
- **Competitive Positioning**: How do we win?
- **Revenue Model**: How do we make money?
- **Investment Required**: Time, money, resources
- **Key Risks**: What could derail this?
- **3-Year Outcome**: Where does this take us?

### Option C: [Name - e.g., "Transform Business Model"]
- **Description**: What is this strategy?
- **Market Opportunity**: What market are we targeting?
- **Competitive Positioning**: How do we win?
- **Revenue Model**: How do we make money?
- **Investment Required**: Time, money, resources
- **Key Risks**: What could derail this?
- **3-Year Outcome**: Where does this take us?

## Phase 3: Strategic Evaluation

| Criterion | Option A | Option B | Option C |
|-----------|----------|----------|----------|
| **Market Size** | $X | $X | $X |
| **Time to Revenue** | X months | X months | X months |
| **Investment Required** | $X | $X | $X |
| **Probability of Success** | X% | X% | X% |
| **Competitive Intensity** | High/Med/Low | High/Med/Low | High/Med/Low |
| **Execution Complexity** | High/Med/Low | High/Med/Low | High/Med/Low |
| **Strategic Fit** | High/Med/Low | High/Med/Low | High/Med/Low |
| **Exit Potential** | High/Med/Low | High/Med/Low | High/Med/Low |

## Phase 4: Strategic Choice & Roadmap

### Recommended Strategy
- [ ] **Choice**: Which path and why?
- [ ] **Key Bets**: What are we betting on?
- [ ] **Success Metrics**: How we'll measure progress
- [ ] **Risk Mitigation**: How we'll manage key risks
- [ ] **What We're NOT Doing**: Explicit choices to say no

### 3-Year Strategic Roadmap

**Year 1: Foundation**
- [ ] Key milestones and metrics
- [ ] Team and organizational changes
- [ ] Product/market initiatives
- [ ] Financial targets

**Year 2: Scale**
- [ ] Key milestones and metrics
- [ ] Team and organizational changes
- [ ] Product/market initiatives
- [ ] Financial targets

**Year 3: Optimize**
- [ ] Key milestones and metrics
- [ ] Team and organizational changes
- [ ] Product/market initiatives
- [ ] Financial targets

### Resource Allocation
- [ ] **Budget**: Annual investment by category
- [ ] **Headcount**: Hiring plan by function
- [ ] **Capital**: Fundraising needs and timing
- [ ] **Partnerships**: Strategic alliances needed

## Phase 5: Stakeholder Alignment

### Board Approval
- [ ] Strategic narrative and business case
- [ ] Financial projections and ROI
- [ ] Risk assessment and mitigation
- [ ] Resource requirements and asks

### Leadership Team Alignment
- [ ] Functional implications (Product, Eng, Sales, Marketing)
- [ ] OKRs cascade from strategy
- [ ] Resource allocation by team
- [ ] Success metrics and accountability

### Company Communication
- [ ] Vision and strategy narrative
- [ ] How this affects each team
- [ ] What stays the same, what changes
- [ ] How we'll measure success

## Phase 6: Execution Framework

### Quarterly OKRs
- [ ] Q1 objectives and key results
- [ ] Q2 objectives and key results
- [ ] Q3 objectives and key results
- [ ] Q4 objectives and key results

### Decision Gates
- [ ] **End of Q1**: Validate assumptions, adjust course
- [ ] **End of Q2**: Scale or pivot decision
- [ ] **End of Q3**: Optimization and refinement
- [ ] **End of Q4**: Annual review and next year planning

---

*Strategy is about making choices. Choose wisely. Execute relentlessly.*
ENDOFFILE
```

### Create `/board-prep` workflow

```bash
cat > .agent/workflows/board-prep.md << 'ENDOFFILE'
---
description: Prepare for board meeting - CEO business update
---

# /board-prep — Board Meeting Preparation

> **Use when**: Preparing CEO update for board meeting

## Phase 1: Gather Key Metrics

### Financial Performance
- [ ] Revenue (actual vs. plan, YoY growth)
- [ ] Gross margin, EBITDA, net income
- [ ] Cash position, burn rate, runway
- [ ] ARR/MRR trends

### Growth Metrics
- [ ] New customer acquisition
- [ ] Churn rate and NRR
- [ ] Pipeline and conversion rates
- [ ] Market share and competitive position

### Operational Metrics
- [ ] Key product/service metrics
- [ ] Customer satisfaction (NPS, CSAT)
- [ ] Team size and productivity
- [ ] Operational efficiency

## Phase 2: Craft Executive Narrative

### What We Accomplished (Last Quarter)
- [ ] Strategic milestones achieved
- [ ] Financial targets hit/missed (with context)
- [ ] Major wins (customers, partnerships, product launches)
- [ ] Organizational progress (key hires, culture initiatives)

### Current State of the Business
- [ ] Overall health: Strong/On Track/Challenged
- [ ] Market position and competitive dynamics
- [ ] Customer sentiment and feedback
- [ ] Team morale and capacity

### Strategic Progress
- [ ] Progress on 3-year vision
- [ ] OKR achievement rate
- [ ] Major strategic decisions made
- [ ] Pivots or course corrections

### Challenges & Risks
- [ ] Top 3 risks with mitigation plans
- [ ] Market headwinds or tailwinds
- [ ] Competitive threats
- [ ] Operational challenges

### Looking Ahead (Next Quarter)
- [ ] Strategic priorities
- [ ] Financial targets
- [ ] Key initiatives and expected outcomes
- [ ] Resource needs

## Phase 3: Prepare Board Materials

### Board Deck Structure (15-20 slides)
1. **Executive Summary** (1 slide)
2. **Financial Performance** (2-3 slides)
3. **Business Metrics** (2-3 slides)
4. **Strategic Progress** (2-3 slides)
5. **Product/Market Update** (2-3 slides)
6. **Team & Organization** (1-2 slides)
7. **Challenges & Risks** (1-2 slides)
8. **Next Quarter Plan** (1-2 slides)
9. **Asks** (1 slide)
10. **Appendix** (detailed backup)

### Supporting Documents
- [ ] Detailed financial statements
- [ ] Customer case studies or testimonials
- [ ] Competitive analysis
- [ ] Organizational chart
- [ ] Product roadmap

## Phase 4: Anticipate Board Questions

### Strategy
- [ ] Are we focused on the right things?
- [ ] How do we compare to competitors?
- [ ] What's our sustainable competitive advantage?
- [ ] Should we pivot or stay the course?

### Financial
- [ ] When will we be profitable?
- [ ] What's our path to next funding round?
- [ ] Can we extend runway?
- [ ] What are unit economics trends?

### Growth
- [ ] Can we hit our growth targets?
- [ ] What's limiting growth?
- [ ] Should we expand to new markets/segments?
- [ ] What's our CAC payback period?

### Team & Organization
- [ ] Do we have the right leadership team?
- [ ] Can we scale to meet targets?
- [ ] What's our retention strategy?
- [ ] Are we building the right culture?

### Risk
- [ ] What keeps you up at night?
- [ ] What could derail the plan?
- [ ] Are we compliant with regulations?
- [ ] What's our contingency plan?

## Phase 5: Prepare Your Asks

Be specific and clear:

### Good Asks
- ✅ "Approve $2M for sales expansion - expect 3x ROI in 18 months"
- ✅ "Introduction to [specific person] for partnership discussion"
- ✅ "Guidance on M&A strategy - should we acquire or build?"

### Bad Asks
- ❌ "We need more money"
- ❌ "Can you help with sales?"
- ❌ "What should we do about competition?"

## Phase 6: Practice & Refine

- [ ] Rehearse presentation (aim for 20-30 minutes)
- [ ] Practice answering tough questions
- [ ] Get feedback from leadership team
- [ ] Refine messaging and data

## Output Template

```markdown
## Board Meeting - [Date]

### Executive Summary
[3-4 sentences: State of business, key wins, challenges, outlook]

### Financial Snapshot
| Metric | Actual | Plan | YoY |
|--------|--------|------|-----|
| Revenue | $X | $Y | +Z% |
| Gross Margin | X% | Y% | +Z% |
| Burn Rate | $X/mo | $Y/mo | -Z% |
| Runway | X months | - | - |

### Strategic Highlights
1. [Major achievement with impact]
2. [Major achievement with impact]
3. [Major achievement with impact]

### Key Metrics
- New Customers: X (target: Y)
- Churn: X% (target: Y%)
- NPS: X (target: Y)
- Team Size: X (target: Y)

### Top 3 Priorities Next Quarter
1. [Priority] - [Expected outcome]
2. [Priority] - [Expected outcome]
3. [Priority] - [Expected outcome]

### Risks & Mitigation
1. [Risk] - [Mitigation]
2. [Risk] - [Mitigation]

### Asks
1. [Specific ask with context]
2. [Specific ask with context]
```

---

*Tell the story. Own the narrative. Drive the outcome.*
ENDOFFILE
```

### Create `/okr-review` workflow

```bash
cat > .agent/workflows/okr-review.md << 'ENDOFFILE'
---
description: Review and update OKRs (Objectives and Key Results)
---

# /okr-review — OKR Review & Update

> **Use when**: Quarterly OKR planning, mid-quarter check-ins, annual goal setting

## Phase 1: Review Current OKRs

### Company-Level OKRs
For each objective:
- [ ] **Objective**: [What we want to achieve]
- [ ] **Key Results**: [How we measure success]
- [ ] **Current Status**: On track / At risk / Off track
- [ ] **Progress**: X% complete
- [ ] **Blockers**: What's preventing progress?
- [ ] **Learnings**: What have we learned?

### Functional OKRs (Product, Engineering, Sales, Marketing, etc.)
- [ ] Review alignment with company OKRs
- [ ] Assess progress and blockers
- [ ] Identify dependencies across teams

## Phase 2: OKR Health Assessment

### Red Flags
- [ ] OKRs consistently at 100% (not ambitious enough)
- [ ] OKRs consistently below 30% (unrealistic or blocked)
- [ ] OKRs not aligned across teams
- [ ] Key results are outputs, not outcomes
- [ ] Too many OKRs (lack of focus)

### Good Signs
- [ ] 60-70% achievement rate (right level of ambition)
- [ ] Clear line of sight from individual to company OKRs
- [ ] Teams can explain how their work connects to OKRs
- [ ] Regular progress updates and course corrections

## Phase 3: Next Quarter OKR Planning

### Company Objectives (3-5 max)
For each objective, ask:
- [ ] **Is it ambitious?** Does it stretch the organization?
- [ ] **Is it measurable?** Can we track progress?
- [ ] **Is it aligned?** Does it support our strategy?
- [ ] **Is it achievable?** Can we realistically do this?
- [ ] **Is it inspiring?** Does it motivate the team?

### Key Results (3-5 per objective)
For each key result, ensure:
- [ ] **Outcome-based**: "Increase NPS to 50" not "Launch feature X"
- [ ] **Measurable**: Clear metric with target
- [ ] **Time-bound**: Achievable within the quarter
- [ ] **Owned**: Clear DRI (Directly Responsible Individual)

### Example OKR Structure

**Objective 1: Become the market leader in [segment]**
- KR1: Increase market share from X% to Y%
- KR2: Achieve NPS of 50+ (up from 40)
- KR3: Win 10 enterprise customers (>$100K ARR each)

**Objective 2: Build a world-class team**
- KR1: Hire 20 A-players across Product, Eng, Sales
- KR2: Improve employee engagement score from 7.5 to 8.5
- KR3: Achieve 90%+ retention rate for top performers

**Objective 3: Achieve financial sustainability**
- KR1: Grow ARR from $XM to $YM
- KR2: Improve gross margin from X% to Y%
- KR3: Extend runway to 18+ months

## Phase 4: Cascade & Align

### Leadership Team Alignment
- [ ] Each leader drafts functional OKRs
- [ ] Review for alignment with company OKRs
- [ ] Identify dependencies and conflicts
- [ ] Finalize and commit

### Company-Wide Communication
- [ ] All-hands presentation of company OKRs
- [ ] Each team shares their OKRs
- [ ] Explain how individual work connects to OKRs
- [ ] Set up tracking and review cadence

## Phase 5: Tracking & Accountability

### Weekly Check-ins
- [ ] Leadership team reviews progress
- [ ] Flag at-risk OKRs early
- [ ] Unblock teams and reallocate resources

### Monthly Reviews
- [ ] Update OKR progress in company meeting
- [ ] Celebrate wins and learn from misses
- [ ] Adjust tactics (not OKRs) as needed

### End of Quarter
- [ ] Score all OKRs (0.0 to 1.0 scale)
- [ ] Conduct retrospective
- [ ] Document learnings
- [ ] Plan next quarter

## Common OKR Mistakes to Avoid

❌ **Too many OKRs** - Focus on 3-5 company objectives max
❌ **Sandbagging** - Setting easy targets to hit 100%
❌ **Activity-based KRs** - "Launch feature X" vs. "Increase engagement by Y%"
❌ **No ownership** - Every KR needs a DRI
❌ **Set and forget** - OKRs need weekly review and updates
❌ **Misalignment** - Team OKRs don't ladder up to company OKRs
❌ **Lack of ambition** - OKRs should stretch the organization

## OKR Grading Scale

- **0.0 - 0.3**: We failed or made little progress
- **0.4 - 0.6**: We made progress but fell short (this is okay!)
- **0.7 - 1.0**: We hit or exceeded the target (might be too easy)

**Target**: Average 0.6-0.7 across all OKRs

---

*Focus. Measure. Achieve.*
ENDOFFILE
```

### Create `/end` workflow

```bash
cat > .agent/workflows/end.md << 'ENDOFFILE'
---
description: Close session and synthesize learnings
---

# /end — Session Close

## Phase 1: Review Session Checkpoints

- [ ] Read all `### ⚡ Checkpoint` entries from current session log
- [ ] Identify key themes and patterns

## Phase 2: Synthesize Session

Update the current session log with:

### Key Topics
- [ ] List main business areas discussed
- [ ] Note any strategic decisions made
- [ ] Highlight important discoveries or insights

### Decisions Made
- [ ] Document business decisions with rationale
- [ ] Include trade-offs considered
- [ ] Note any assumptions or constraints

### Action Items
- [ ] Create/update action items table:

| Action | Owner | Priority | Status |
|--------|-------|----------|--------|
| ... | ... | High/Med/Low | Pending/In Progress/Done |

### Learnings & Patterns
- [ ] New patterns discovered
- [ ] Mistakes to avoid
- [ ] Useful techniques or approaches

## Phase 3: Commit to Memory

- [ ] Save and close the session log
- [ ] Mark session status as "Closed"
- [ ] Add timestamp for session end

## Phase 4: Confirm

- [ ] Output: "✅ Session XX closed. [Brief summary of key outcomes]"
- [ ] Highlight any urgent action items

---

*Clean closure. Clear outcomes. Ready for next session.*
ENDOFFILE
```

---

## Step 4: Create Automation Scripts

### Copy scripts from Engineering Executive workspace

```bash
# Copy the scripts (they're identical)
cp ../EngineeringExecutiveAssistant/.agent/scripts/create_session.py .agent/scripts/
cp ../EngineeringExecutiveAssistant/.agent/scripts/quicksave.py .agent/scripts/

chmod +x .agent/scripts/*.py
```

**OR create them manually** (same content as Engineering Executive):

```bash
cat > .agent/scripts/create_session.py << 'ENDOFFILE'
#!/usr/bin/env python3
"""Create a new session log file for engineering sessions."""

from datetime import datetime
from pathlib import Path

def create_session():
    log_dir = Path(".context/memories/session_logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Find existing sessions for today
    existing = list(log_dir.glob(f"{today}-session-*.md"))
    session_num = len(existing) + 1
    
    filename = f"{today}-session-{session_num:02d}.md"
    filepath = log_dir / filename
    
    template = f"""# Engineering Session Log: {today} (Session {session_num})

**Date**: {today}
**Time**: {datetime.now().strftime("%H:%M")} - ...
**Focus**: [Technical area or project]

---

## Session Context

**Current Sprint/Milestone**: ...
**Technical Stack**: ...
**Team Members Involved**: ...

---

## Key Topics

- ...

---

## Technical Decisions Made

| Decision | Rationale | Trade-offs | Reversible? |
|----------|-----------|------------|-------------|
| ... | ... | ... | Yes/No |

---

## Architecture Discussions

- ...

---

## Code Reviews / PRs

- ...

---

## Action Items

| Action | Owner | Priority | Status | Due Date |
|--------|-------|----------|--------|----------|
| ... | ... | High/Med/Low | Pending | YYYY-MM-DD |

---

## Learnings & Patterns

### What Worked
- ...

### What Didn't Work
- ...

### New Patterns Discovered
- ...

---

## References

- Links to PRs, docs, tickets, etc.

---

## Session Closed

**Status**: Open
**End Time**: ...
**Summary**: ...
"""
    
    filepath.write_text(template)
    print(f"✅ Created: {filepath}")
    print(f"   Session: {today}-session-{session_num:02d}")
    return str(filepath)

if __name__ == "__main__":
    create_session()
ENDOFFILE

chmod +x .agent/scripts/create_session.py
```

```bash
cat > .agent/scripts/quicksave.py << 'ENDOFFILE'
#!/usr/bin/env python3
"""Append a checkpoint to the current session log."""

import sys
from datetime import datetime
from pathlib import Path

def quicksave(summary: str):
    log_dir = Path(".context/memories/session_logs")
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Find today's session logs
    logs = sorted(log_dir.glob(f"{today}-session-*.md"))
    if not logs:
        print(f"⚠️ No session log found for {today}")
        print(f"💡 Run: python .agent/scripts/create_session.py")
        return
    
    current_log = logs[-1]  # Most recent
    timestamp = datetime.now().strftime("%H:%M")
    
    checkpoint = f"\n### ⚡ Checkpoint [{timestamp}]\n{summary}\n"
    
    with open(current_log, "a") as f:
        f.write(checkpoint)
    
    print(f"✅ Quicksave [{timestamp}] → {current_log.name}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        quicksave(" ".join(sys.argv[1:]))
    else:
        print("Usage: python quicksave.py <summary>")
        print("Example: python quicksave.py 'Discussed Q1 OKRs and strategic priorities'")
ENDOFFILE

chmod +x .agent/scripts/quicksave.py
```

---

## Step 5: Create Protocol

```bash
cat > .agent/skills/protocols/strategic-decision-framework.md << 'ENDOFFILE'
# Protocol: Strategic Decision Framework

> **Use when**: Major business decisions, strategic pivots, resource allocation, M&A

## The Executive Decision Framework

### 1. Frame the Decision

**What are we deciding?**
- [ ] State the decision clearly and specifically
- [ ] Define the scope and boundaries
- [ ] Identify the decision maker (you, board, team)
- [ ] Set the decision deadline

**Why does this matter?**
- [ ] Business impact (revenue, cost, risk)
- [ ] Strategic implications (market position, competitive advantage)
- [ ] Stakeholder impact (customers, employees, investors)
- [ ] Opportunity cost (what we're NOT doing)

### 2. Gather Information

**Quantitative Data:**
- [ ] Financial projections and models
- [ ] Market size and growth rates
- [ ] Customer data and metrics
- [ ] Competitive benchmarks

**Qualitative Insights:**
- [ ] Customer feedback and needs
- [ ] Team capabilities and morale
- [ ] Market trends and dynamics
- [ ] Expert opinions and advice

**Avoid:**
- ❌ Analysis paralysis (perfect information doesn't exist)
- ❌ Confirmation bias (seeking data that supports your view)
- ❌ Recency bias (overweighting recent events)

### 3. Generate Options

Create at least 3 distinct options:

**Option A: [Bold/Aggressive]**
- High risk, high reward
- Requires significant investment
- Potential for market leadership

**Option B: [Balanced/Pragmatic]**
- Moderate risk, moderate reward
- Reasonable investment
- Steady progress

**Option C: [Conservative/Safe]**
- Low risk, lower reward
- Minimal investment
- Maintain status quo or incremental improvement

**Option D: [Creative/Unconventional]**
- Different approach entirely
- May challenge assumptions
- Could be a game-changer

### 4. Evaluate Options

| Criterion | Weight | Option A | Option B | Option C | Option D |
|-----------|--------|----------|----------|----------|----------|
| **Strategic Fit** | 25% | Score 1-10 | Score 1-10 | Score 1-10 | Score 1-10 |
| **Financial Return** | 25% | Score 1-10 | Score 1-10 | Score 1-10 | Score 1-10 |
| **Execution Risk** | 20% | Score 1-10 | Score 1-10 | Score 1-10 | Score 1-10 |
| **Time to Value** | 15% | Score 1-10 | Score 1-10 | Score 1-10 | Score 1-10 |
| **Team Capability** | 15% | Score 1-10 | Score 1-10 | Score 1-10 | Score 1-10 |
| **Total** | 100% | Weighted | Weighted | Weighted | Weighted |

### 5. Test Your Thinking

**Pre-Mortem Exercise:**
"It's 12 months from now. We made this decision and it failed spectacularly. Why?"
- [ ] What went wrong?
- [ ] What did we miss?
- [ ] What assumptions were incorrect?

**Second-Order Thinking:**
- [ ] What happens next? (First-order effect)
- [ ] Then what? (Second-order effect)
- [ ] And then? (Third-order effect)

**Regret Minimization:**
"Will I regret NOT doing this in 5 years?"
- [ ] If yes → Bias toward action
- [ ] If no → Bias toward caution

### 6. Seek Diverse Perspectives

**Internal Stakeholders:**
- [ ] Leadership team input
- [ ] Board member perspectives
- [ ] Employee feedback (where appropriate)

**External Advisors:**
- [ ] Industry experts
- [ ] Investors or mentors
- [ ] Customers or partners

**Devil's Advocate:**
- [ ] Assign someone to argue against the decision
- [ ] Challenge assumptions
- [ ] Stress-test the logic

### 7. Make the Decision

**Decision Criteria:**
- [ ] Does this align with our strategy?
- [ ] Can we afford it (time, money, focus)?
- [ ] Can we execute it with our current team?
- [ ] Is the risk acceptable?
- [ ] Is now the right time?

**Decision Types:**

**Type 1 (Irreversible):**
- High stakes, hard to undo
- Requires deep analysis and consensus
- Examples: M&A, major pivots, key hires

**Type 2 (Reversible):**
- Lower stakes, easy to undo
- Move fast, gather data, adjust
- Examples: Marketing campaigns, feature experiments

**Make Type 2 decisions quickly. Take time on Type 1.**

### 8. Communicate the Decision

**To the Board:**
- [ ] Decision and rationale
- [ ] Expected outcomes and metrics
- [ ] Risks and mitigation plans
- [ ] Resource requirements

**To the Team:**
- [ ] Why we're doing this
- [ ] What it means for them
- [ ] How we'll measure success
- [ ] How they can contribute

**To Customers/Partners:**
- [ ] What's changing
- [ ] Why it's good for them
- [ ] Timeline and next steps

### 9. Execute with Discipline

**Set Clear Milestones:**
- [ ] 30-day checkpoint
- [ ] 90-day review
- [ ] 6-month assessment

**Define Success Metrics:**
- [ ] Leading indicators (early signals)
- [ ] Lagging indicators (final outcomes)
- [ ] Thresholds for go/no-go decisions

**Assign Ownership:**
- [ ] DRI (Directly Responsible Individual)
- [ ] Supporting team members
- [ ] Escalation path

### 10. Learn and Iterate

**Regular Reviews:**
- [ ] Are we seeing expected results?
- [ ] What's working? What's not?
- [ ] Do we need to adjust course?

**Decision Journal:**
Document:
- [ ] What we decided and why
- [ ] What we expected to happen
- [ ] What actually happened
- [ ] What we learned

**Improve Decision-Making:**
- [ ] Which decisions worked well?
- [ ] Which decisions didn't?
- [ ] What patterns emerge?
- [ ] How can we decide better next time?

## Common Decision-Making Traps

❌ **Sunk Cost Fallacy** - "We've invested so much, we can't stop now"
✅ **Better**: Evaluate based on future value, not past investment

❌ **Groupthink** - Everyone agrees too quickly
✅ **Better**: Actively seek dissenting opinions

❌ **Analysis Paralysis** - Waiting for perfect information
✅ **Better**: Set decision deadline, decide with available data

❌ **Overconfidence** - "I'm sure this will work"
✅ **Better**: Probabilistic thinking, plan for multiple scenarios

❌ **Availability Bias** - Recent events overly influence thinking
✅ **Better**: Look at longer-term data and trends

❌ **Anchoring** - First number or idea overly influences thinking
✅ **Better**: Generate options independently before comparing

## Decision Documentation Template

```markdown
## Strategic Decision: [Name]

**Date**: YYYY-MM-DD
**Decision Maker**: CEO / Board / Leadership Team
**Status**: Proposed / Approved / In Progress / Complete

### Decision
[Clear, specific statement of what we're deciding]

### Context
[Why are we making this decision? What's the business context?]

### Options Considered
1. [Option A] - [Brief description]
2. [Option B] - [Brief description]
3. [Option C] - [Brief description]

### Recommendation
[Which option and why?]

### Expected Outcomes
- [Outcome 1]: [Metric and target]
- [Outcome 2]: [Metric and target]

### Investment Required
- Budget: $X
- Headcount: X people
- Timeline: X months

### Risks & Mitigation
1. [Risk]: [Mitigation plan]
2. [Risk]: [Mitigation plan]

### Stakeholder Impact
- Customers: [Impact]
- Employees: [Impact]
- Investors: [Impact]

### Success Metrics
- [Metric 1]: Baseline → Target
- [Metric 2]: Baseline → Target

### Review Schedule
- 30-day checkpoint: [Date]
- 90-day review: [Date]
- 6-month assessment: [Date]

### Reversibility
[Can we undo this? How hard? What's the cost?]
```

---

#protocol #strategic-decisions #executive-framework #ceo
ENDOFFILE
```

---

## Step 6: Create README

```bash
cat > README.md << 'ENDOFFILE'
# Business Executive Assistant (CEO/COO)

A strategic AI assistant workspace designed for CEOs, COOs, and business executives. Navigate the complexities of running and scaling a business with frameworks for strategic planning, operational excellence, and stakeholder management.

## Quick Start

### 1. Open this directory in your AI IDE
```bash
cd ~/Projects/BusinessExecutiveAssistant  # adjust path as needed
```

### 2. Start a session
Type `/start` in your AI assistant

### 3. Use executive workflows
- `/strategy` - Deep strategic business planning
- `/board-prep` - Prepare CEO update for board
- `/okr-review` - Review and update OKRs
- `/decision` - Executive decision framework

## Core Features

- 🎯 **Executive-Level Focus** - Strategic planning, OKR management, board communication
- 📊 **Key Responsibilities** - Strategic, operational, organizational, external leadership
- 🛠️ **Executive Workflows** - `/start`, `/strategy`, `/board-prep`, `/okr-review`, `/end`
- 📝 **Protocols** - Strategic decision framework, OKR best practices

## Directory Structure

```
BusinessExecutiveAssistant/
├── .framework/modules/
│   └── Core_Identity.md          # CEO/COO principles
├── .agent/
│   ├── workflows/                # Executive workflows
│   ├── scripts/                  # Automation
│   └── skills/protocols/         # Best practices
└── .context/memories/
    └── session_logs/             # All sessions
```

---

**You're not just running a company—you're building something that outlasts you.**
ENDOFFILE
```

---

## Step 7: Test the Setup

```bash
# Test session creation
python3 .agent/scripts/create_session.py

# Test quicksave
python3 .agent/scripts/quicksave.py "Testing CEO workspace setup"

# Verify structure
ls -la .agent/workflows/
ls -la .context/memories/session_logs/
```

**Expected output:**
- ✅ Session created
- ✅ Quicksave checkpoint added
- ✅ All files present

---

# Setup Complete!

You now have both executive workspaces fully configured:

1. **Engineering Executive Assistant** (CTO/EVP)
2. **Business Executive Assistant** (CEO/COO)

## Next Steps

1. Open each workspace in your AI IDE
2. Type `/start` to begin your first session
3. Try the workflows (`/strategy`, `/board-prep`, `/okr-review`)
4. Build your knowledge base over time

---

**Both workspaces are production-ready and tested.**
