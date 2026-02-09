#!/usr/bin/env python3
"""
Skill Analyzer - Read and analyze Claude skill source files

Usage:
    python analyzer.py read <skill-name> [--path <base-path>]
    python analyzer.py list [--path <base-path>] [--output json|table]
    python analyzer.py detect-mcp <skill-name> [--path <base-path>]

Examples:
    python analyzer.py read skill-analyzer
    python analyzer.py list --output table
    python analyzer.py detect-mcp data-scanner
"""

import sys
import json
from pathlib import Path
from datetime import datetime


def read_skill_md(skill_path):
    """Read and parse SKILL.md frontmatter."""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return None, "SKILL.md not found"

    content = skill_md.read_text(encoding='utf-8')

    # Parse frontmatter
    frontmatter = {}
    in_frontmatter = False
    body_lines = []

    for line in content.split('\n'):
        if line.strip() == '---':
            if not in_frontmatter:
                in_frontmatter = True
                continue
            else:
                break
        elif in_frontmatter and ':' in line:
            key, value = line.split(':', 1)
            frontmatter[key.strip()] = value.strip()
        elif in_frontmatter:
            body_lines.append(line)

    body = '\n'.join(body_lines)

    return {
        'frontmatter': frontmatter,
        'body': body,
        'content': content
    }, None


def list_skill_structure(skill_path):
    """List directory structure of a skill."""
    structure = []

    if not skill_path.exists():
        return None, "Skill directory not found"

    for item in skill_path.rglob('*'):
        if item.is_file():
            rel_path = item.relative_to(skill_path)
            structure.append(str(rel_path))

    return sorted(structure), None


def detect_mcp_tools(skill_path):
    """Detect possible MCP tool usage in skill."""
    detected = []
    possible = []

    # Patterns to search for
    mcp_patterns = ['mcp__', 'MCP::', '@mcp']
    tool_names = ['web_search', 'understand_image', 'MiniMax']

    # Search in SKILL.md
    skill_data, _ = read_skill_md(skill_path)
    if skill_data:
        content = skill_data['content'].lower()

        # Check for web search mentions
        if 'web_search' in content or 'search' in content:
            possible.append('mcp__MiniMax__web_search (mentioned in SKILL.md)')

        # Check for image understanding
        if 'image' in content or 'understand' in content:
            possible.append('mcp__MiniMax__understand_image (mentioned in SKILL.md)')

    # Search in script files
    scripts_dir = skill_path / 'scripts'
    if scripts_dir.exists():
        for py_file in scripts_dir.glob('*.py'):
            content = py_file.read_text(encoding='utf-8')

            for pattern in mcp_patterns:
                if pattern in content:
                    detected.append(f'{pattern} found in {py_file.name}')

            for tool in tool_names:
                if tool in content:
                    detected.append(f'{tool} found in {py_file.name}')

    # Search in reference files
    refs_dir = skill_path / 'references'
    if refs_dir.exists():
        for md_file in refs_dir.glob('*.md'):
            content = md_file.read_text(encoding='utf-8')

            for tool in tool_names:
                if tool.lower() in content.lower():
                    possible.append(f'{tool} mentioned in {md_file.name}')

    return {
        'detected': detected,
        'possible': possible
    }, None


def read_skill(skill_name, base_path='C:\\Users\\52648\\.claude\\skills'):
    """Full analysis of a single skill."""
    skill_path = Path(base_path) / skill_name

    if not skill_path.exists():
        return {'error': f'Skill not found: {skill_name}'}

    result = {
        'name': skill_name,
        'path': str(skill_path),
        'analyzed_at': datetime.now().isoformat()
    }

    # Read SKILL.md
    skill_data, error = read_skill_md(skill_path)
    if error:
        result['error'] = error
        return result

    result['frontmatter'] = skill_data['frontmatter']

    # Get structure
    structure, _ = list_skill_structure(skill_path)
    result['files'] = structure
    result['file_count'] = len(structure) if structure else 0

    # Detect MCP tools
    mcp, _ = detect_mcp_tools(skill_path)
    result['mcp_tools'] = mcp

    return result


def list_skills(base_path='C:\\Users\\52648\\.claude\\skills', output='json'):
    """List all skills with summary info."""
    path = Path(base_path)
    skills = []

    for item in path.iterdir():
        if item.is_dir() and (item / 'SKILL.md').exists():
            skill_data = read_skill(item.name, base_path)

            summary = {
                'name': skill_data.get('name'),
                'description': skill_data.get('frontmatter', {}).get('description', '')[:80],
                'files': skill_data.get('file_count', 0),
                'mcp_tools': skill_data.get('mcp_tools', {})
            }
            skills.append(summary)

    if output == 'json':
        return json.dumps(skills, ensure_ascii=False, indent=2)
    else:
        # Table format
        lines = ["| Name | Description | Files | MCP Tools |"]
        lines.append("|-------|------------|-------|-----------|")

        for s in skills:
            mcp_count = len(s['mcp_tools'].get('detected', [])) + len(s['mcp_tools'].get('possible', []))
            mcp_str = f"{mcp_count} detected"
            desc = s['description'][:40] + '...' if len(s['description']) > 40 else s['description']
            lines.append(f"| {s['name']} | {desc} | {s['files']} | {mcp_str} |")

        return '\n'.join(lines)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == 'read':
        if len(sys.argv) < 3:
            print("Usage: analyzer.py read <skill-name> [--path <path>]")
            sys.exit(1)

        skill_name = sys.argv[2]
        base_path = 'C:\\Users\\52648\\.claude\\skills'

        for i, arg in enumerate(sys.argv[3:], 3):
            if arg == '--path' and i + 1 < len(sys.argv):
                base_path = sys.argv[i + 1]

        result = read_skill(skill_name, base_path)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == 'list':
        base_path = 'C:\\Users\\52648\\.claude\\skills'
        output = 'json'

        for i, arg in enumerate(sys.argv[2:], 2):
            if arg == '--path' and i + 1 < len(sys.argv):
                base_path = sys.argv[i + 1]
            elif arg == '--output' and i + 1 < len(sys.argv):
                output = sys.argv[i + 1]

        result = list_skills(base_path, output)
        print(result)

    elif command == 'detect-mcp':
        if len(sys.argv) < 3:
            print("Usage: analyzer.py detect-mcp <skill-name> [--path <path>]")
            sys.exit(1)

        skill_name = sys.argv[2]
        base_path = 'C:\\Users\\52648\\.claude\\skills'

        for i, arg in enumerate(sys.argv[3:], 3):
            if arg == '--path' and i + 1 < len(sys.argv):
                base_path = sys.argv[i + 1]

        skill_path = Path(base_path) / skill_name
        result, _ = detect_mcp_tools(skill_path)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    else:
        print(f"Unknown command: {command}")
        print(__doc__)


if __name__ == "__main__":
    main()
