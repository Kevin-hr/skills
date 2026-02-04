# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a collection of **Claude Agent Skills** - modular packages that extend Claude's capabilities. The repository contains:

- **Document Skills** (`skills/pdf`, `skills/docx`, `skills/pptx`, `skills/xlsx`): Source-available skills powering Claude's native document capabilities
- **Example Skills** (`skills/` subdirectories): Open-source (Apache 2.0) examples demonstrating skill patterns
- **Specification** (`spec/`): Agent Skills specification (redirects to [agentskills.io/specification](https://agentskills.io/specification))
- **Template** (`template/`): Starting point for creating new skills

## Skill Anatomy

Each skill is a folder containing:
- `SKILL.md` (required): YAML frontmatter + Markdown instructions
- `scripts/` (optional): Executable code (Python/Bash) bundled with the skill
- `references/` (optional): Documentation loaded as needed
- `assets/` (optional): Templates and other resource files

**SKILL.md Frontmatter Required Fields:**
```yaml
---
name: skill-name        # lowercase, hyphens for spaces
description: Clear description of what the skill does and when to use it
---
```

## Helper Scripts

Scripts for skill development are planned but not yet implemented.

## Key Design Principles

- **Progressive Disclosure**: Skills load in tiers - metadata always in context, full instructions when triggered, bundled resources as needed. Keep `SKILL.md` lean (under 500 lines).
- **Concise is Key**: Skills share context window; be economical with instructions.
- **Self-Contained**: Each skill should work independently with all necessary resources bundled.

## Installing Skills in Claude Code

```bash
/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills
/plugin install example-skills@anthropic-agent-skills
```

After installation, use skills by mentioning them: "Use the PDF skill to extract form fields from..."
