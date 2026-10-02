#!/usr/bin/env python3
"""Static Python import-boundary checks, not a runtime sandbox or authority proof."""
import ast
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]


def check(root=ROOT):
    root=Path(root)
    rules=json.loads((root/'spec/python_dependencies.json').read_text())['modules']
    paths={str(p.relative_to(root/'nss_base').with_suffix('')).replace('/','.'):p
           for p in (root/'nss_base').rglob('*.py')}
    errors=[]; graph={name:set() for name in paths}
    if set(paths)!=set(rules):
        errors.append('Module inventory differs from reviewed allowlist')
    for name,path in paths.items():
        for node in ast.walk(ast.parse(path.read_text(),filename=str(path))):
            targets=[]
            if isinstance(node,ast.ImportFrom):
                if node.level:
                    targets=[node.module] if node.module else [a.name for a in node.names]
                    if node.level!=1:errors.append(f'{name}: unreviewed relative import depth')
                elif node.module and node.module.startswith('nss_base.'):
                    targets=[node.module[len('nss_base.'):]]
                elif node.module=='nss_base':targets=[a.name for a in node.names]
            elif isinstance(node,ast.Import):
                targets=[a.name[len('nss_base.'):] for a in node.names if a.name.startswith('nss_base.')]
            elif isinstance(node,ast.Call):
                fun=node.func
                if (isinstance(fun,ast.Name) and fun.id=='__import__') or (isinstance(fun,ast.Attribute) and fun.attr=='import_module'):
                    errors.append(f'{name}: dynamic imports are unreviewed')
            for target in targets:
                graph[name].add(target)
                if target not in rules.get(name,[]):
                    errors.append(f'{name} -> {target}: forbidden/unreviewed import')
                if target not in paths:errors.append(f'{name}: missing module {target}')
    visiting=set();visited=set()
    def visit(node):
        if node in visiting:
            errors.append(f'Circular dependency through {node}');return
        if node in visited:return
        visiting.add(node)
        for target in graph.get(node,()):visit(target)
        visiting.remove(node);visited.add(node)
    for node in graph:visit(node)
    return sorted(set(errors))


if __name__=='__main__':
    issues=check()
    print('\n'.join(issues) if issues else 'PASS: reviewed local Python import edges; no cycles detected.')
    raise SystemExit(bool(issues))
