---
description: Spec-driven code review and iterative implementation plan from a Jira ticket
---

# Jira Spec-Driven Code Review Workflow

## Instructions
Fill in the variables in [BRACKETS] before running. Cascade will then:
1. Review the codebase end-to-end against the ACs
2. Draft/update an OpenAPI spec before any code changes
3. Produce an atomic, iterative commit plan

---

## Step 1: Load Ticket Context

```
Jira Ticket: [TICKET-ID]
Title: [Ticket Title]
Epic: [Epic Name or ID]

User Story:
As a [user type], I want [goal], so that [reason].

Acceptance Criteria:
- [AC-1]
- [AC-2]
- [AC-3]

Out of Scope:
- [anything explicitly excluded]
```

---

## Step 2: Codebase Review (run this prompt in Cascade)

```
You are a senior software engineer. I have a Jira ticket with the acceptance criteria listed below.

Review the existing codebase with these objectives:
1. Identify ALL files and components in scope (entry points, services, data layer, config, tests)
2. Trace the current data flow end-to-end relevant to this ticket
3. For each AC item, identify the exact file(s) and line(s) that must change
4. Flag upstream/downstream dependencies that will be impacted
5. Identify gaps: missing logic, incorrect behavior, or tech debt relevant to this ticket
6. Surface any ambiguity in the ACs that I should clarify with the team lead BEFORE coding

Output as a table:
| File | Current Behavior | Required Change | AC Coverage | Risk (L/M/H) |

Acceptance Criteria:
[PASTE ACs HERE]
```

---

## Step 3: OpenAPI Spec First (spec-driven development)

```
Before writing any implementation code, draft or update the OpenAPI 3.0 spec for this ticket.

For each affected endpoint:
- Show the full YAML block (path, method, request body, response schema, error codes)
- If no HTTP endpoints are affected, document any internal config schema or data contract changes
- Mark new fields vs modified fields with a comment

Output: complete openapi.yaml snippet(s) only. No implementation code yet.
```

---

## Step 4: Iterative Commit Plan

```
Break the implementation into small, atomic commits. Rules:
- Each commit must be independently deployable (no broken intermediate states)
- Each commit maps to exactly one AC item or one logical unit of change
- No single commit should exceed ~250 lines of change
- Commit messages must follow Conventional Commits format
- Tests must be written alongside (not after) each commit

For each commit output:
---
Commit [N]: <type>(<scope>): <short description>
Files changed: <list>
What changes: <specific description>
AC satisfied: <AC-N>
Tests to add: <unit / integration / e2e>
---
```

---

## Step 5: Execute Commits (one at a time)

// turbo
For each commit in the plan:
1. Implement only that commit's changes
2. Run existing tests to confirm no regression
3. Confirm the AC item is satisfied
4. Stage, commit, and push
5. Move to the next commit only after the previous is green
