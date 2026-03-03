# AI Agent Prompts — Spec-Driven Development

Prompt files and workflows for Windsurf (Cascade) and VS Code (Copilot) to perform
spec-driven, iterative code review and implementation from Jira tickets.

---

## Directory Structure

```
ai-agent-prompts/
├── .windsurf/
│   └── workflows/
│       ├── jira-spec-review.md              ← Generic Jira → code review → commit plan
│       └── knowledge-assistant-pvc-sync.md  ← Specific: PVC embedding sync from S3
│
├── .vscode/
│   └── prompts/
│       ├── jira-spec-review.md              ← Same workflow, formatted for Copilot Chat
│       └── knowledge-assistant-pvc-sync.md  ← PVC sync prompts for Copilot Chat
│
├── clarifying-questions.md                  ← Questions to ask team lead before coding
├── research-openshift-pvc-knowledge-assistant.md  ← Architecture research & best practices
└── README.md
```

---

## How to Use

### Windsurf (Cascade)
Workflows in `.windsurf/workflows/` are available as slash commands in Cascade.
- `/jira-spec-review` — triggers the generic review + commit plan workflow
- `/knowledge-assistant-pvc-sync` — triggers the PVC sync specific workflow

Steps marked `// turbo` above them will auto-run without manual approval.

### VS Code (GitHub Copilot Chat)
1. Open `.vscode/prompts/jira-spec-review.md` or `knowledge-assistant-pvc-sync.md`
2. Copy the relevant `PROMPT — PART N` block
3. Paste into Copilot Chat (`Ctrl+Shift+I` / `Cmd+Shift+I`)
4. Run parts sequentially: Review → Spec → Plan → Execute one commit at a time

---

## Workflow Philosophy

1. **Review first** — AI reads existing code before suggesting changes
2. **Spec before code** — OpenAPI / config contract defined before implementation
3. **Atomic commits** — each commit ≤ 250 lines, maps to one AC item
4. **Tests alongside** — not after
5. **Deployable at every step** — no broken intermediate states

---

## Files Reference

| File | Purpose |
|---|---|
| `clarifying-questions.md` | Ask team lead BEFORE coding to avoid rework |
| `research-openshift-pvc-knowledge-assistant.md` | Architecture patterns, PVC design, Slack/email ingestion, observability |
