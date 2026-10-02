#!/usr/bin/env python3
from pathlib import Path
import json, subprocess, shutil, sys, argparse
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from nss_base.logic_atlas import load_atlas

ROOT=Path(__file__).resolve().parents[1]
SPEC=ROOT/'spec'/'logic_atlas.json'
OUT=ROOT/'docs'/'logic_flowcharts'
OUT.mkdir(parents=True, exist_ok=True)

def q(s):
    return s.replace('\\','\\\\').replace('"','\\"').replace('\n','\\n')

def wrap(text, width=24):
    words=text.split()
    lines=[]; line=''
    for w in words:
        test=(line+' '+w).strip()
        if len(test)>width and line:
            lines.append(line); line=w
        else: line=test
    if line: lines.append(line)
    return '\n'.join(lines)

parser=argparse.ArgumentParser()
parser.add_argument('--flow',help='Regenerate only one reviewed flow ID')
parser.add_argument('--node')
parser.add_argument('--node-modules')
args=parser.parse_args()
atlas=load_atlas(SPEC)
selected=[f for f in atlas['flows'] if args.flow is None or f['id']==args.flow]
if not selected: raise SystemExit('Unknown flow ID')
if shutil.which('dot') is None and not (args.node and args.node_modules):
    raise SystemExit('Install Graphviz or supply --node and --node-modules with @viz-js/viz and sharp')
for flow in selected:
    fid=flow['id']
    rank = 'TB' if fid in ('master','experience') else 'LR'
    dot=['digraph G {',f'rankdir={rank};','graph [bgcolor="white", pad="0.15", nodesep="0.25", ranksep="0.35"];',
         'node [shape=box, style="rounded,filled", fillcolor="#F7F8FA", color="#475569", fontname="DejaVu Sans", fontsize=10, margin="0.08,0.05"];',
         'edge [color="#64748B", fontcolor="#475569", fontname="DejaVu Sans", fontsize=8, arrowsize=0.7];']
    for n in flow['nodes']:
        attrs=[]
        if n['kind']=='decision': attrs += ['shape=diamond','style="filled"','fillcolor="#FFF7E6"','color="#A16207"']
        elif n['kind']=='success': attrs += ['shape=oval','fillcolor="#ECFDF5"','color="#047857"']
        elif n['kind']=='failure': attrs += ['shape=oval','fillcolor="#FEF2F2"','color="#B91C1C"']
        elif n['kind']=='start': attrs += ['fillcolor="#EFF6FF"','color="#1D4ED8"']
        dot.append(f'"{q(n["id"])}" [label="{q(wrap(n["label"]))}"{"," if attrs else ""}{",".join(attrs)}];')
    for e in flow['transitions']:
        lab='' if e['when']=='always' else f' [label="{q(wrap(e["when"],18))}"]'
        dot.append(f'"{q(e["from"])}" -> "{q(e["to"])}"{lab};')
    dot.append('}')
    dot_path=OUT/f'{fid}.dot'; png_path=OUT/f'{fid}.png'
    dot_path.write_text('\n'.join(dot),encoding='utf-8')
    if shutil.which('dot'):
        subprocess.run(['dot','-Tpng','-Gdpi=170',str(dot_path),'-o',str(png_path)],check=True)
        subprocess.run(['dot','-Tsvg',str(dot_path),'-o',str(OUT/f'{fid}.svg')],check=True)
print(f'rendered {len(selected)} flowcharts to {OUT}')

if shutil.which('dot') is None:
    subprocess.run([args.node, str(ROOT/'tools/render_dot.cjs'), args.node_modules, str(OUT)], check=True)
