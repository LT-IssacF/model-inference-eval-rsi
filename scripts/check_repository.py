#!/usr/bin/env python3
"""Check RSI records and archived evidence using the Python standard library."""

import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
STATUSES = {'validated_in_scope', 'rejected', 'partial', 'proposed'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(',', ':'), allow_nan=False).encode('utf-8')


def sha256(value):
    return hashlib.sha256(value).hexdigest()


def relative_file(root, name):
    relative = Path(name)
    require(not relative.is_absolute() and '..' not in relative.parts,
            f'invalid relative path: {name}')
    path = (root / relative).resolve()
    require(path.is_relative_to(root.resolve()) and path.is_file(),
            f'missing or external file: {name}')
    return path


def pointer(value, path):
    require(isinstance(path, str) and path.startswith('/'), f'invalid pointer: {path}')
    for part in path.split('/')[1:]:
        part = part.replace('~1', '/').replace('~0', '~')
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def observed(evidence, path):
    values = evidence['values']
    prefixes = [key for key in values if path == key or path.startswith(key + '/')]
    require(bool(prefixes), f'pointer not captured: {path}')
    prefix = max(prefixes, key=len)
    value = values[prefix]
    return pointer(value, path[len(prefix):]) if path != prefix else value


def check_claim(actual, operator, expected):
    if operator == 'eq':
        return canonical(actual) == canonical(expected)
    if operator == 'length':
        return isinstance(actual, (dict, list, str)) and len(actual) == expected
    if operator == 'contains':
        return isinstance(actual, str) and isinstance(expected, str) and expected in actual
    require(operator in {'lt', 'gt'}, f'unknown assertion operator: {operator}')
    require(type(actual) in (int, float) and type(expected) in (int, float)
            and math.isfinite(actual) and math.isfinite(expected), 'non-finite numeric assertion')
    return actual < expected if operator == 'lt' else actual > expected


def check_graph(episodes):
    visiting, visited = set(), set()

    def visit(identity):
        require(identity in episodes, f'unknown parent: {identity}')
        require(identity not in visiting, f'cyclic lineage at {identity}')
        if identity in visited:
            return
        visiting.add(identity)
        for parent in episodes[identity]['parents']:
            visit(parent)
        visiting.remove(identity)
        visited.add(identity)

    for identity in episodes:
        visit(identity)


def check_links(project_root):
    internal, external = 0, 0
    for path in sorted(ROOT.rglob('*.md')):
        content = path.read_text(encoding='utf-8')
        require('**' not in content and '__' not in content, f'bold marker in {path.name}')
        for link in re.findall(r'\]\(([^)]+)\)', content):
            if '://' in link or link.startswith('#'):
                continue
            target = (path.parent / link.split('#')[0]).resolve()
            if target.is_relative_to(ROOT):
                require(target.exists(), f'broken local link: {path.name} -> {link}')
                internal += 1
            else:
                if project_root is not None:
                    # Repository links to ProteinArena are relative to the workspace root.
                    default_project = ROOT.parents[1]
                    require(target.is_relative_to(default_project), f'link escapes project: {link}')
                    relocated = project_root / target.relative_to(default_project)
                    require(relocated.exists(), f'broken project link: {link}')
                external += 1
    return {'local': internal, 'project': external}


def check_release_language(registry):
    if registry.get('release', {}).get('language') != 'en':
        return None
    for path in sorted(ROOT.rglob('*')):
        if '.git' in path.relative_to(ROOT).parts or path.suffix not in {'.md', '.json', '.py'}:
            continue
        require(re.search(r'[\u3400-\u9fff]', path.read_text(encoding='utf-8')) is None,
                f'non-English release content: {path.relative_to(ROOT)}')
    return 'en'


def check(project_root):
    registry = read(ROOT / 'registry.json')
    require(registry['name'] == ROOT.name, 'registry and directory names differ')
    require(registry['method_effectiveness']['status'] == 'not_run'
            and registry['method_effectiveness']['held_out_evaluation'] == 'not_run',
            'this release has no recorded agent-comparison or held-out results')
    evidence = read(ROOT / 'evaluations/evidence.json')['evidence']
    for identity, record in evidence.items():
        require(sha256(canonical(record['values'])) == record['values_sha256'],
                f'evidence snapshot hash mismatch: {identity}')
        require(re.fullmatch(r'[0-9a-f]{64}', record['source_sha256']) is not None,
                f'invalid source hash: {identity}')
        if project_root is not None:
            source = relative_file(project_root, record['source'])
            raw = source.read_bytes()
            require(sha256(raw) == record['source_sha256'], f'source hash mismatch: {identity}')
            source_format = record.get('source_format', 'json')
            if source_format == 'text':
                value = {'text': raw.decode('utf-8')}
            elif source_format == 'text_lines':
                value = {'lines': raw.decode('utf-8').splitlines()}
            else:
                require(source_format == 'json', f'unknown source format: {source_format}')
                value = json.loads(raw)
            for key, expected in record['values'].items():
                require(canonical(pointer(value, key)) == canonical(expected),
                        f'source extraction mismatch: {identity} {key}')

    episodes = {}
    require(len(registry['cases']) == len(set(registry['cases'])), 'duplicate case path')
    for name in registry['cases']:
        case = read(relative_file(ROOT, name))
        for episode in case['episodes']:
            identity = episode['id']
            require(identity not in episodes, f'duplicate episode: {identity}')
            require(episode['status'] in STATUSES, f'invalid episode status: {identity}')
            for field in ('problem', 'observation', 'validation', 'adoption'):
                require(isinstance(episode[field], str) and bool(episode[field].strip()),
                        f'missing {field}: {identity}')
            require(bool(episode['artifact_change']['description']) and bool(episode['limits']),
                    f'missing change or applicability: {identity}')
            require(bool(episode['evidence']) and all(key in evidence for key in episode['evidence']),
                    f'unknown or missing evidence: {identity}')
            require(isinstance(episode['parents'], list)
                    and len(episode['parents']) == len(set(episode['parents'])),
                    f'invalid parents: {identity}')
            if project_root is not None:
                for artifact in episode['artifact_change']['project_paths']:
                    relative_file(project_root, artifact)
            episodes[identity] = episode
    check_graph(episodes)

    checked, covered = set(), set()
    for claim in read(ROOT / 'evaluations/checks.json')['checks']:
        require(claim['id'] not in checked, f'duplicate assertion: {claim["id"]}')
        require(claim['episode'] in episodes, f'unknown assertion episode: {claim["id"]}')
        require(claim['evidence'] in episodes[claim['episode']]['evidence'],
                f'assertion outside episode evidence: {claim["id"]}')
        actual = observed(evidence[claim['evidence']], claim['pointer'])
        require(check_claim(actual, claim['operator'], claim['expected']),
                f'failed evidence assertion: {claim["id"]}')
        checked.add(claim['id'])
        covered.add(claim['episode'])
    require(covered == set(episodes), 'some episodes have no evidence assertions')

    suite = read(ROOT / 'evaluations/tasks.json')
    tasks = suite['tasks']
    task_ids = {task['id'] for task in tasks}
    require(suite['status'] == 'not_run' and len(task_ids) == len(tasks), 'invalid development suite')
    rubrics = read(ROOT / 'evaluations/rubric.json')['rubrics']
    require(len(rubrics) == len(tasks) and {row['task'] for row in rubrics} == task_ids,
            'task and rubric coverage differ')
    for task in tasks:
        require(bool(task['evidence']) and all(key in evidence for key in task['evidence']),
                f'unknown task evidence: {task["id"]}')
        require(bool(task['prompt']) and bool(task['output']), f'empty task: {task["id"]}')
    return {'passed': True, 'version': registry['version'], 'scope': 'archived_evidence_consistency',
            'cases': len(registry['cases']), 'episodes': len(episodes), 'evidence_snapshots': len(evidence),
            'evidence_assertions': len(checked), 'development_tasks': len(tasks),
            'links': check_links(project_root), 'project_sources_verified': project_root is not None,
            'release_language': check_release_language(registry),
            'method_effectiveness': 'not_run', 'held_out_evaluation': 'not_run'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project-root', type=Path, help='Verify original evidence files in this workspace')
    parser.add_argument('--output', type=Path, help='Write the check result to a JSON file')
    args = parser.parse_args()
    try:
        result = check(args.project_root.resolve() if args.project_root else None)
    except (ValueError, OSError, KeyError, TypeError, IndexError, RecursionError) as error:
        result = {'passed': False, 'scope': 'archived_evidence_consistency', 'error': str(error)}
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        args.output.write_text(rendered, encoding='utf-8')
    print(rendered, end='')
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
