#!/usr/bin/env python3
import pathlib, sys
from ruamel.yaml import YAML

yaml = YAML()
yaml.indent(mapping=2, sequence=4, offset=2)
WORKFLOW_DIR = pathlib.Path('.github/workflows')

for wf_path in WORKFLOW_DIR.glob('*.yml'):
    try:
        data = yaml.load(wf_path.read_text(encoding='utf-8'))
    except Exception as e:
        print(f'Failed to parse {wf_path}: {e}', file=sys.stderr)
        continue
    # Write back with yaml.dump which handles booleans, etc.
    with wf_path.open('w', encoding='utf-8') as f:
        yaml.dump(data, f)
    print(f'Formatted {wf_path}')
