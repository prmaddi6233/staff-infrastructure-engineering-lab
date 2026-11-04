"""Check local Markdown file links and selected accidental disclosure patterns.

A lightweight regression check, not a substitute for secret scanning or review.
"""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
errors = []
for path in root.rglob('*'):
    if not path.is_file() or path.suffix not in {'.py', '.md', '.yml'}:
        continue
    text = path.read_text()
    if re.search(r'(?<!\d)\d{12}(?!\d)', text):
        errors.append(f'{path.relative_to(root)}: possible account identifier')
    if path.suffix == '.md':
        for link in re.findall(r'\]\(([^)]+)\)', text):
            if '://' not in link and not link.startswith('#'):
                if not (path.parent / link.split('#')[0]).exists():
                    errors.append(f'{path.relative_to(root)}: missing {link}')
if errors:
    raise SystemExit('\n'.join(errors))
print('Local Markdown links and account-identifier regression check passed.')
