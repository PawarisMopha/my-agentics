#!/usr/bin/env python3
import pathlib, re, sys

MAX_LEN = 80
WORKFLOW_DIR = pathlib.Path('.github/workflows')

def fix_file(p: pathlib.Path):
    text = p.read_text(encoding='utf-8')
    lines = text.splitlines()
    # Ensure document start
    if not lines or not lines[0].strip().startswith('---'):
        lines.insert(0, '---')
    new_lines = []
    for line in lines:
        # Fix quoted true/false
        line = re.sub(r"'true'", 'true', line)
        line = re.sub(r'"true"', 'true', line)
        line = re.sub(r"'false'", 'false', line)
        line = re.sub(r'"false"', 'false', line)
        # Ensure comment has two spaces before '#'
        if '#' in line:
            parts = line.split('#', 1)
            before = parts[0].rstrip()
            comment = parts[1].lstrip()
            line = f"{before}  # {comment}" if before else f"# {comment}"
        # Break long lines
        while len(line) > MAX_LEN:
            # Find split point before MAX_LEN
            split_at = line.rfind(' ', 0, MAX_LEN)
            if split_at == -1:
                split_at = MAX_LEN
            # Insert backslash for continuation if it's a bash command (contains = or &&)
            continuation = '\\'
            new_lines.append(line[:split_at] + continuation)
            line = line[split_at:].lstrip()
        new_lines.append(line)
    p.write_text('\n'.join(new_lines) + '\n', encoding='utf-8')
    print(f'Fixed {p}')

for wf in WORKFLOW_DIR.glob('*.yml'):
    fix_file(wf)
