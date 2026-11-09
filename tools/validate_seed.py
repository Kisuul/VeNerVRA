#!/usr/bin/env python3
"""Read-only structural validator for the VeNerVRA 2.0 repository seed.

Validates required files, local Markdown links, research record envelopes,
scopes, stable unique IDs, date ordering and index coverage.
This does NOT validate research truth, privacy safety or agent behavior.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

REQUIRED_FILES = (
    'README.md', 'AGENTS.md', 'VEN.md',
    'ven/MEMORY_PROTOCOL.md', 'ven/RESEARCH_PROTOCOL.md',
    'ven/STATE_PROTOCOL.md', 'ven/PERMISSIONS.md', 'ven/VERIFICATION.md',
    'research/INDEX.md', 'research/templates/INDEX.md',
    'evaluations/SCENARIOS.md', 'evaluations/SCORECARD.md',
    'docs/source/VeNerVRA-1.1.txt',
    'integration/kestrel/README.md',
    'integration/kestrel/candidates/INDEX.md',
)
REQUIRED_KEYS = {
    'schema', 'id', 'kind', 'scope', 'status', 'epistemic_status',
    'confidence', 'evidence', 'sensitivity', 'author', 'created', 'updated', 'sources',
}
KINDS = {'question', 'claim', 'source', 'hypothesis', 'journal', 'experiment', 'handoff'}
STATUS = {'draft', 'active', 'disputed', 'superseded', 'archived'}
EPISTEMIC = {'proposed', 'investigating', 'supported', 'disputed', 'refuted', 'superseded', 'not-applicable'}
CONFIDENCE = {'unresolved', 'low', 'moderate', 'high'}
EVIDENCE = {'observed', 'supported', 'inferred', 'hypothesis', 'user-stated', 'unverified'}
SENSITIVITY = {'public', 'internal', 'restricted'}
LINK_RE = re.compile(r'(?<!!)\[[^]\n]+\]\(([^)\n]+)\)')
ID_RE = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')


def parse_frontmatter(content: str) -> Tuple[Dict[str, str], List[str]]:
    """Parse a deliberately limited flat scalar frontmatter schema."""
    lines = content.splitlines()
    if not lines or lines[0] != '---':
        return {}, ['missing opening --- frontmatter delimiter']
    try:
        ending = lines.index('---', 1)
    except ValueError:
        return {}, ['missing closing --- frontmatter delimiter']
    fields: Dict[str, str] = {}
    problems: List[str] = []
    for line in lines[1:ending]:
        if not line or line.isspace():
            continue
        if ':' not in line or line[0].isspace():
            problems.append(f'invalid flat metadata: {line!r}')
            continue
        key, value = line.split(':', 1)
        key, value = key.strip(), value.strip()
        if not re.fullmatch(r'[a-z][a-z0-9_]*', key):
            problems.append(f'invalid metadata key: {key!r}')
            continue
        if key in fields:
            problems.append(f'duplicate metadata key: {key}')
            continue
        if not value or value in ('null', 'None') or value.startswith(('[', '{', '|', '>')):
            problems.append(f'missing or non-scalar value for {key}')
        if value.startswith('"'):
            try:
                value = json.loads(value)
                if not isinstance(value, str):
                    problems.append(f'nonstring scalar for {key}')
            except json.JSONDecodeError:
                problems.append(f'invalid quoted string for {key}')
        elif value.startswith("'"):
            problems.append(f'use JSON-style double-quoted strings for {key}')
        fields[key] = str(value)
    return fields, problems


def resolve_local_link(source: Path, target: str, root: Path) -> Optional[str]:
    """Return an error for a non-resolving local markdown link, else None."""
    target = target.strip().split(' ', 1)[0].strip('<>')
    if target.startswith(('http:', 'https:', 'mailto:', 'data:', '#')):
        return None
    target = target.split('#', 1)[0].split('?', 1)[0]
    if not target:
        return None
    actual = ((root / target.lstrip('/')) if target.startswith('/') else source.parent / target).resolve()
    if not actual.is_relative_to(root.resolve()):
        return f'link escapes repository: {target}'
    if not actual.exists():
        return f'broken link: {target}'
    return None


def visible_markdown_lines(content: str):
    """Yield prose/links outside fenced or indented code and HTML comments.

    Deliberately supports a narrow journal/index grammar, not full CommonMark.
    """
    fence_char = None
    fence_width = 0
    in_comment = False
    for line in content.splitlines():
        if in_comment:
            if '-->' in line:
                in_comment = False
            continue
        if '<!--' in line:
            in_comment = '-->' not in line.split('<!--', 1)[1]
            continue
        if fence_char is not None:
            end = r'^ {0,3}' + re.escape(fence_char) + '{' + str(fence_width) + r',}\s*$'
            if re.match(end, line):
                fence_char = None
            continue
        start = re.match(r'^ {0,3}([`~])\1{2,}', line)
        if start:
            fence_char = start.group(1)
            fence_width = len(start.group(0).lstrip())
            continue
        if line.startswith(('    ', '\t')):
            continue
        yield line


def markdown_sections(content: str) -> Dict[str, str]:
    """Parse strict level-two headings, ignoring untrusted examples in code."""
    result: Dict[str, str] = {}
    heading: Optional[str] = None
    body: List[str] = []
    for line in visible_markdown_lines(content):
        if line.startswith('## '):
            if heading is not None:
                result[heading] = '\n'.join(body).strip()
            heading, body = line[3:].rstrip(), []
        elif heading is not None:
            body.append(line)
    if heading is not None:
        result[heading] = '\n'.join(body).strip()
    return result


def index_links_to(index: Path, target: Path, root: Path) -> bool:
    """Check an actual resolving local Markdown link, never a bare mention."""
    if not index.is_file():
        return False
    canonical_root = root.resolve()
    canonical_target = target.resolve()
    if not canonical_target.is_relative_to(canonical_root):
        return False
    for line in visible_markdown_lines(index.read_text(encoding='utf-8')):
        line = re.sub(r'(`+).*?\1', '', line)  # inline code is not an index link
        for match in LINK_RE.finditer(line):
            raw = match.group(1).strip().split(' ', 1)[0].strip('<>')
            if raw.startswith(('http:', 'https:', 'mailto:', 'data:', '#')):
                continue
            raw = raw.split('#', 1)[0].split('?', 1)[0]
            if not raw:
                continue
            dest = ((canonical_root / raw.lstrip('/'))
                    if raw.startswith('/') else index.parent / raw).resolve()
            if dest == canonical_target and dest.is_relative_to(canonical_root):
                return True
    return False

def validate_record(path: Path, slug: str) -> List[str]:
    txt = path.read_text(encoding='utf-8')
    fields, problems = parse_frontmatter(txt)
    problems.extend(f'missing required key: {key}' for key in sorted(REQUIRED_KEYS - fields.keys()))
    if fields.get('schema') != '1':
        problems.append('schema must be 1')
    for key, allowed in [('kind', KINDS), ('status', STATUS), ('epistemic_status', EPISTEMIC),
                         ('confidence', CONFIDENCE), ('evidence', EVIDENCE), ('sensitivity', SENSITIVITY)]:
        if key in fields and fields[key] not in allowed:
            problems.append(f'unsupported {key}: {fields[key]}')
    if fields.get('scope') != f'research:{slug}':
        problems.append(f'scope must be research:{slug}')
    if not ID_RE.fullmatch(fields.get('id', '')):
        problems.append('id must use lowercase letters, numbers and hyphens')
    for date_key in ('created', 'updated'):
        if date_key in fields:
            try:
                dt.date.fromisoformat(fields[date_key])
            except ValueError:
                problems.append(f'invalid {date_key} ISO date')
    if fields.get('created') and fields.get('updated'):
        try:
            if dt.date.fromisoformat(fields['updated']) < dt.date.fromisoformat(fields['created']):
                problems.append('updated is earlier than created')
        except ValueError:
            pass
    parsed_sections = markdown_sections(txt)
    for heading in ('Summary', 'Evidence', 'Revisit when'):
        if heading not in parsed_sections:
            problems.append(f'missing ## {heading} section')
    if fields.get('status') == 'superseded' and '## Superseded by' not in txt:
        problems.append('superseded record missing ## Superseded by link')
    if fields.get('kind') in {'claim', 'hypothesis'} and fields.get('epistemic_status') == 'not-applicable':
        problems.append('claim or hypothesis cannot have not-applicable epistemic status')
    if fields.get('kind') not in {'claim', 'hypothesis'} and fields.get('epistemic_status') != 'not-applicable':
        problems.append('non-proposition record must have not-applicable epistemic status')
    return problems


def investigation_dirs(root: Path) -> List[Path]:
    research = root / 'research'
    if not research.exists():
        return []
    result = []
    for index in research.rglob('INDEX.md'):
        parent = index.parent
        if parent == research or parent == research / 'templates' or parent == research / 'examples':
            continue
        if 'templates' in parent.relative_to(research).parts:
            continue
        result.append(parent)
    return sorted(result)


def validate_repo(root: Path) -> List[str]:
    errors: List[str] = []
    root = root.resolve()
    for needed in REQUIRED_FILES:
        if not (root / needed).is_file():
            errors.append(f'missing required file: {needed}')

    # In template files, placeholder links intentionally do not resolve.
    for source in root.rglob('*.md'):
        if 'templates' in source.relative_to(root).parts:
            continue
        for line in visible_markdown_lines(source.read_text(encoding='utf-8')):
            line = re.sub(r'(`+).*?\1', '', line)
            for match in LINK_RE.finditer(line):
                problem = resolve_local_link(source, match.group(1), root)
                if problem:
                    errors.append(f'{source.relative_to(root)}: {problem}')

    master_index = root / 'research' / 'INDEX.md'
    seen: Dict[str, Path] = {}
    for directory in investigation_dirs(root):
        slug = directory.name
        rel_idx = (directory / 'INDEX.md').relative_to(root / 'research').as_posix()
        if not index_links_to(master_index, directory / 'INDEX.md', root):
            errors.append(f'research/INDEX.md does not register {rel_idx}')
        for record in sorted(directory.glob('*.md')):
            if record.name == 'INDEX.md':
                continue
            rel = record.relative_to(root)
            for problem in validate_record(record, slug):
                errors.append(f'{rel}: {problem}')
            fields, _ = parse_frontmatter(record.read_text(encoding='utf-8'))
            key = fields.get('id')
            if key:
                if key in seen:
                    errors.append(f'duplicate id {key} at {rel} and {seen[key].relative_to(root)}')
                else:
                    seen[key] = record
            if not index_links_to(directory / 'INDEX.md', record, root):
                errors.append(f'{rel}: record missing from nearest INDEX.md')
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    issues = validate_repo(args.root)
    if issues:
        print(f'FAIL: {len(issues)} structural issue(s):')
        for issue in issues:
            print(' -', issue)
        return 1
    print('PASS: VeNerVRA seed structural validation (no behavioral or scientific verification)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
