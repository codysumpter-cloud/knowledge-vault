---
name: codebase-inspection
description: "Inspect codebases w/ pygount: LOC, languages, ratios."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [LOC, Code Analysis, pygount, Codebase, Metrics, Repository]
    related_skills: [github-repo-management]
prerequisites:
  commands: [pygount]
---
# Codebase Inspection with Extended Documentation Analysis

This skill now covers **systematic repository analysis** including:
- Reading documentation files (README, ARCHITECTURE, RUNBOOK, SOUL, etc.)
- Understanding project structure and conventions
- Extracting key operational principles and boundaries
- Summarizing governance models (councils, roles, responsibilities)

## Process for Documentation Analysis

1. **Read first-contact files in order:**
   - README.md (project overview)
   - ARCHITECTURE.md / SYSTEM.md (high-level design)
   - RUNBOOK.md / OPERATIONS.md (operational procedures)
   - SOUL.md / IDENTITY.md (governance and values)
   - MEMORY.md / CONTEXT.md (persistent state and lessons)

2. **Extract key facts:**
   - Ownership boundaries (what the repo does/doesn't own)
   - Startup sequences and cold-start entry points
   - Council/roles structure and decision-making processes
   - Security boundaries and approval requirements
   - Integration points with other systems

3. **Document findings in a structured summary** with:
   - Purpose and scope
   - Key files and their relationships
   - Operating principles and constraints
   - Integration points
   - Security considerations

## Examples from Recent Analysis

**buddy-brain (BeMore-stack):**
- Operator stack for BMO with Adventure Time council
- Cold-start sequence: AGENTS.md → soul.md → memory.md → routines.md
- Explicit boundaries: `openclaw` owns Telegram runtime, `prismtek-site` owns public web
- Council: 12-seat Adventure Time council, Huntress Wizard and Ice King as reserves

**hermes-agent:**
- Self-improving AI agent with learning loop
- Supports 200+ models via multiple providers
- Security: approval system, output redaction, credential isolation
- Features: MCP, cron scheduling, parallel subagents, trajectory generation
