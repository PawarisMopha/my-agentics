#!/usr/bin/env python3
import pathlib, sys, re

WORKFLOW_DIR = pathlib.Path('.github/workflows')
for path in WORKFLOW_DIR.glob('*.yml'):
    text = path.read_text(encoding='utf-8')
    lines = text.splitlines()
    # Ensure document start
    if not lines or not lines[0].strip().startswith('---'):
        lines.insert(0, '---')
    # Replace truthy values like "true" or "false" quoted with proper boolean
    # Not strict, just ensure no quoted true/false
    new_lines = []
    for line in lines:
        # simple replace quoted true/false with bare
        line = re.sub(r"'true'", 'true', line)
        line = re.sub(r'"true"', 'true', line)
        line = re.sub(r"'false'", 'false', line)
        line = re.sub(r'"false"', 'false', line)
        new_lines.append(line)
    new_text = '\n'.join(new_lines) + '\n'
    path.write_text(new_text, encoding='utf-8')
print('Fixed document start and truthy values.')
