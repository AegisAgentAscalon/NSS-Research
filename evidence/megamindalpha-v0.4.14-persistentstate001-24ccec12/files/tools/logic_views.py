"""Shared pure Markdown/Mermaid/DOT rendering, with no write-on-import behavior."""
from nss_base.logic_atlas import flow_metrics

def mermaid(flow):
    lines=['```mermaid','flowchart TD']
    shapes={'start':('[',']'),'process':('[',']'),'decision':('{','}'),'success':('([','])'),'failure':('([','])')}
    def esc(s):return s.replace('"','#quot;').replace('|','#124;').replace('\n',' ')
    for n in flow['nodes']:
        a,b=shapes[n['kind']];lines.append(f'  n_{n["id"]}{a}"{esc(n["label"])}"{b}')
    for e in flow['transitions']:
        label='' if e['when']=='always' else '|"'+esc(e['when'])+'"|'
        lines.append(f'  n_{e["from"]} -->{label} n_{e["to"]}')
    return '\n'.join(lines+['```'])


def entry(flow,heading):
    m=flow_metrics(flow)
    sections=[heading,'',f'**ID:** `{flow["id"]}`  ',f'**Owner:** {flow["owner"]}  ',
        f'**Status:** {flow["status"]}; implementation: `{flow["implementation"]}`  ',
        f'**Purpose:** {flow["purpose"]}','',
        '**Inputs:** '+'; '.join(flow['inputs']),'**Outputs:** '+'; '.join(flow['outputs']),
        f'**Structural metrics:** {m.nodes} nodes; {m.transitions} transitions; normalized complexity {m.cyclomatic_complexity}. Not runtime proof.','',
        '### Flowchart','',mermaid(flow),'','### Pseudocode','','```text',*flow['pseudocode'],'```']
    for title,key in [('Invariants','invariants'),('Typed failures','failure_codes'),('Forbidden edges','forbidden_edges'),('Optimization notes','optimization_notes')]:
        sections+=['','### '+title,'']+['- '+v for v in flow[key]]
    return '\n'.join(sections)+'\n'


def dot(flow):
    def q(s):return s.replace('\\','\\\\').replace('"','\\"').replace('\n','\\n')
    def wrap(s,w=31):
        words=s.split();lines=[];line=''
        for word in words:
            if line and len(line)+len(word)+1>w:lines.append(line);line=word
            else:line=(line+' '+word).strip()
        return '\n'.join(lines+[line])
    lines=['digraph G {','rankdir=TB;',
        'graph [bgcolor="white", pad="0.2", nodesep="0.35", ranksep="0.5"];',
        'node [shape=box, style="rounded", fontname="DejaVu Sans", fontsize=11];',
        'edge [fontname="DejaVu Sans", fontsize=9];']
    for n in flow['nodes']:
        shape='diamond' if n['kind']=='decision' else ('oval' if n['kind'] in ('start','success','failure') else 'box')
        lines.append(f'{n["id"]} [shape={shape},label="{q(wrap(n["label"]))}"];')
    for e in flow['transitions']:
        label='' if e['when']=='always' else e['when']
        lines.append(f'{e["from"]} -> {e["to"]} [label="{q(wrap(label,23))}"];')
    return '\n'.join(lines+['}'])+'\n'

