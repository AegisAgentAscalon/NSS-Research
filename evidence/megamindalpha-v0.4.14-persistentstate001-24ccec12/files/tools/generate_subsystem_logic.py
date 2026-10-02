#!/usr/bin/env python3
"""One data-driven renderer replaces five copy-pasted subsystem scripts.

The validated JSON Atlas remains canonical. Historical Word reports are not rewritten.
"""
import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from nss_base.logic_atlas import load_atlas
from logic_views import entry, dot


def main(argv=None):
    views = json.loads((ROOT/'spec/logic_documents.json').read_text())['views']
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--view', choices=[v['id'] for v in views]); p.add_argument('--render', action='store_true')
    a = p.parse_args(argv)
    selected = [v for v in views if a.view is None or v['id'] == a.view]
    atlas = load_atlas(); doc = ROOT/'docs/PSEUDOCODE_FLOWCHART_ATLAS.md'; text = doc.read_text()
    parents = {fid for v in selected for fid in v['parents']}
    for i, f in enumerate(atlas['flows'], 1):
        if f['id'] not in parents: continue
        heading = f'## {i:02d}. {f["title"]}'
        text, n = re.subn(re.escape(heading)+r'\n.*?(?=\n## |\Z)', lambda _: entry(f, heading), text, count=1, flags=re.S)
        if n != 1: raise SystemExit('Missing exact parent section: '+heading)
    doc.write_text(text)
    for v in selected:
        content = v['heading']+'\n\n'+v['introduction']+'\n'
        for f in load_atlas(ROOT/v['spec'])['flows']:
            content += '\n'+entry(f, '## '+f['title'])
            path = ROOT/'docs/logic_flowcharts'/(f['id']+'.dot'); path.write_text(dot(f))
            if a.render:
                if not shutil.which('dot'): raise SystemExit('Graphviz required only for --render')
                for ext in ('svg','png'):
                    subprocess.run(['dot','-T'+ext,str(path),'-o',str(path.with_suffix('.'+ext))], check=True)
        (ROOT/v['output']).write_text(content)
    print('Regenerated:', ', '.join(v['id'] for v in selected))
    return 0


if __name__ == '__main__': raise SystemExit(main())
