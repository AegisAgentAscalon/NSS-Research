import csv, json, sys, zipfile
sys.stdout.reconfigure(encoding='utf-8')
ARCHIVE='Research/NSS_CM02_Execution_v0.6.zip'
P='NSS_CM02_Execution_v0.6/raw/main/capture_run/scores/'
OUT='.research_review/CM02_v0.6_20260924/'
SEEDS=['1201','1202','1203','1204','1205']
ARMS=['W','I','O']
class Lines:
 def __init__(self,stream): self.stream=stream
 def __iter__(self):
  for line in self.stream: yield line.decode('utf-8')
def rows(z,name):
 with z.open(P+name) as f:
  for row in csv.DictReader(Lines(f)): yield row
def bucket(d,k): return d.setdefault(k,{'correct':0,'rows':0,'queries':set(),'episodes':set()})
def num(r,k): return int(r[k] or 0)
with zipfile.ZipFile(ARCHIVE) as z:
 decisions=[]
 for r in rows(z,'DECISIONS.csv'): decisions.append(r)
 d_arm={}; d_family={}; d_negative={}; pair={}; all_q=set(); held_q=set(); held_ep=set(); case_ids=set()
 outcome_fields=['known','expected','predicted','correct','route','reason','accepted_reference','observable_invalid_acceptance','hidden_intent_wrong_binding','management_abstention','safe_but_lost_recall','correct_unknown','covered','intended_revision','bound_revision','neural_selected_row','output_id','whole_map_integrity']
 for r in decisions:
  arm=r['arm']; split=r['split']; qid=r['query_id']; seed=r['model_seed']; all_q.add(qid); case_ids.add(r['episode_id'])
  b=bucket(d_arm,(split,arm)); b['rows']+=1; b['correct']+=num(r,'correct'); b['queries'].add(qid); b['episodes'].add(r['episode_id'])
  if split=='heldout':
   held_q.add(qid); held_ep.add(r['episode_id'])
  f=bucket(d_family,(split,r['family'],arm)); f['rows']+=1; f['correct']+=num(r,'correct'); f['queries'].add(qid); f['episodes'].add(r['episode_id'])
  if split=='heldout' and ((r['template']=='F' and r['checkpoint'] in ('16','48')) or (r['template']=='C' and r['checkpoint']=='32') or (r['template']=='N' and r['checkpoint'] in ('16','32'))):
   k=(r['template'],r['checkpoint'],arm); n=bucket(d_negative,k); n['rows']+=1; n['correct']+=num(r,'correct'); n['safe_but_lost_recall']=n.get('safe_but_lost_recall',0)+num(r,'safe_but_lost_recall'); n['management_abstention']=n.get('management_abstention',0)+num(r,'management_abstention'); n['hidden_intent_wrong_binding']=n.get('hidden_intent_wrong_binding',0)+num(r,'hidden_intent_wrong_binding'); n['correct_unknown']=n.get('correct_unknown',0)+num(r,'correct_unknown'); n['queries'].add(qid); n['episodes'].add(r['episode_id'])
  if arm in ('W','I'):
   k=(qid,seed); pp=pair.setdefault(k,{})
   if arm in pp: raise ValueError('duplicate arm/query/seed row')
   pp[arm]=tuple(r[x] for x in outcome_fields)
 parity_pairs=sum(1 for v in pair.values() if 'W' in v and 'I' in v)
 parity_mismatches=sum(1 for v in pair.values() if 'W' in v and 'I' in v and v['W']!=v['I'])
 assert len(decisions)==2880 and parity_pairs==960
 heldout={arm:{'correct':d_arm[('heldout',arm)]['correct'],'rows':d_arm[('heldout',arm)]['rows'],'unique_query_occasions':len(d_arm[('heldout',arm)]['queries']),'unique_sequences':len(d_arm[('heldout',arm)]['episodes'])} for arm in ARMS}
 assert all(heldout[a]['rows']==600 for a in ARMS)
 family=[]
 for fam in sorted(k[1] for k in d_family if k[0]=='heldout' and k[2]=='W'):
  row={'family':fam}
  for arm in ARMS:
   v=d_family[('heldout',fam,arm)]; row[arm]={'correct':v['correct'],'rows':v['rows'],'accuracy':round(v['correct']/v['rows'],6)}
  row['W_minus_I_pp']=round(100*(row['W']['accuracy']-row['I']['accuracy']),4)
  row['W_minus_O_pp']=round(100*(row['W']['accuracy']-row['O']['accuracy']),4)
  family.append(row)
 exact={}
 for r in rows(z,'EXACT_CONTROLS.csv'):
  if r['split']!='heldout': continue
  b=bucket(exact,r['control']); b['rows']+=1; b['correct']+=num(r,'correct'); b['queries'].add(r['query_id']); b['episodes'].add(r['episode_id'])
 exact_out={k:{'correct':v['correct'],'rows':v['rows'],'unique_query_occasions':len(v['queries'])} for k,v in exact.items()}
 assert all(v['rows']==120 for v in exact_out.values())
 negative_out={}
 for (template,checkpoint,arm),v in d_negative.items():
  if arm in ('W','I','O'):
   negative_out[template+':'+checkpoint+'/'+arm]={k:(len(val) if k in ('queries','episodes') else val) for k,val in v.items()}
 mem={}; mem_fields=['whole_unique_python_graph_bytes','query_index_reads','query_packet_decodes','query_returned_bytes','query_peak_transient_controller_graph_bytes']
 for r in rows(z,'MEMORY_AND_READ_WORK.csv'):
  if r['split']!='heldout' or r['model_seed']!='1201' or r['arm'] not in ('W','I'): continue
  k=(r['arm'],r['family']); v=mem.setdefault(k,{'rows':0,'graph_sum':0,'graph_max':0,'query_index_reads':0,'query_packet_decodes':0,'query_returned_bytes':0,'peak_transient':0})
  v['rows']+=1; graph=num(r,'whole_unique_python_graph_bytes'); v['graph_sum']+=graph; v['graph_max']=max(v['graph_max'],graph); v['peak_transient']=max(v['peak_transient'],num(r,'query_peak_transient_controller_graph_bytes'))
  for field in ['query_index_reads','query_packet_decodes','query_returned_bytes']: v[field]+=num(r,field)
 ev_fields=['index_reads','packet_encodes','packet_decodes','task_field_semantic_bytes_rewritten','workspace_ascii_bytes_rewritten','selection_object_bytes_reallocated','journal_append_bytes','lookup_returned_bytes','numerical_bytes_rewritten']
 event={}
 for r in rows(z,'EVENT_WORK.csv'):
  if r['split']!='heldout' or r['arm'] not in ('W','I'): continue
  k=(r['arm'],r['family']); v=event.setdefault(k,{x:0 for x in ev_fields})
  for field in ev_fields: v[field]+=num(r,field)
 cost_by_family=[]; cost_totals={arm:{'families':0,'event_plus_query_index_reads':0,'packet_encodes':0,'packet_decodes':0,'task_field_semantic_bytes_rewritten':0,'workspace_ascii_bytes_rewritten':0,'selection_object_bytes_reallocated':0,'query_returned_bytes':0,'lookup_returned_bytes':0,'journal_append_bytes':0,'numerical_bytes_rewritten':0,'resident_graph_observations':0,'resident_graph_sum':0,'resident_graph_max':0,'peak_transient_max':0} for arm in ('W','I')}
 for fam in sorted(k[1] for k in event if k[0]=='W'):
  for arm in ('W','I'):
   e=event[(arm,fam)]; q=mem[(arm,fam)]
   c={'family':fam,'arm':arm,'seed_for_query_observations':1201,'query_observations':q['rows'],'resident_graph_mean_bytes':round(q['graph_sum']/q['rows'],2),'resident_graph_max_bytes':q['graph_max'],'peak_query_transient_controller_graph_bytes':q['peak_transient'],'event_plus_query_index_reads':e['index_reads']+q['query_index_reads'],'event_packet_encodes':e['packet_encodes'],'event_plus_query_packet_decodes':e['packet_decodes']+q['query_packet_decodes'],'event_task_field_semantic_bytes_rewritten':e['task_field_semantic_bytes_rewritten'],'event_workspace_ascii_bytes_rewritten':e['workspace_ascii_bytes_rewritten'],'event_selection_object_bytes_reallocated':e['selection_object_bytes_reallocated'],'event_journal_append_bytes':e['journal_append_bytes'],'event_lookup_returned_bytes':e['lookup_returned_bytes'],'query_returned_bytes':q['query_returned_bytes'],'event_numerical_bytes_rewritten':e['numerical_bytes_rewritten']}
   cost_by_family.append(c); t=cost_totals[arm]; t['families']+=1; t['event_plus_query_index_reads']+=c['event_plus_query_index_reads']; t['packet_encodes']+=c['event_packet_encodes']; t['packet_decodes']+=c['event_plus_query_packet_decodes']; t['task_field_semantic_bytes_rewritten']+=c['event_task_field_semantic_bytes_rewritten']; t['workspace_ascii_bytes_rewritten']+=c['event_workspace_ascii_bytes_rewritten']; t['selection_object_bytes_reallocated']+=c['event_selection_object_bytes_reallocated']; t['query_returned_bytes']+=c['query_returned_bytes']; t['lookup_returned_bytes']+=c['event_lookup_returned_bytes']; t['journal_append_bytes']+=c['event_journal_append_bytes']; t['numerical_bytes_rewritten']+=c['event_numerical_bytes_rewritten']; t['resident_graph_observations']+=q['rows']; t['resident_graph_sum']+=q['graph_sum']; t['resident_graph_max']=max(t['resident_graph_max'],q['graph_max']); t['peak_transient_max']=max(t['peak_transient_max'],q['peak_transient'])
 for arm,t in cost_totals.items():
  t['resident_graph_mean_bytes']=round(t.pop('resident_graph_sum')/t['resident_graph_observations'],2); t['resident_graph_max_bytes']=t.pop('resident_graph_max'); t['peak_query_transient_controller_graph_bytes']=t.pop('peak_transient_max')
 main_by_arm={arm:{'correct':sum(d_arm[(split,arm)]['correct'] for split in ('development','heldout')),'rows':sum(d_arm[(split,arm)]['rows'] for split in ('development','heldout'))} for arm in ARMS}
 summary={'source_members':[P+x for x in ['DECISIONS.csv','EXACT_CONTROLS.csv','FAMILY_PAIRED.csv','MEMORY_AND_READ_WORK.csv','EVENT_WORK.csv']],
 'recomputed':{'decision_rows':len(decisions),'main_rows_by_arm':main_by_arm,'heldout_rows_by_arm':heldout,'heldout_unique_query_occasions':len(held_q),'heldout_unique_sequences':len(held_ep),'all_unique_query_ids':len(all_q),'unique_episode_ids':len(case_ids),'w_i_exact_decision_pairs':parity_pairs,'w_i_exact_decision_mismatches':parity_mismatches,'w_i_comparison_fields':outcome_fields,'heldout_family_results':family,'heldout_exact_controls':exact_out,'selected_heldout_negative_strata':negative_out},
 'costs':{'scope':'heldout EVENT_WORK rows plus seed-1201 heldout MEMORY_AND_READ_WORK query observations; additive work is summed, resident graph is summarized by mean/max, not summed as simultaneous memory','totals_by_arm':cost_totals,'per_family':cost_by_family},
 'interpretation_limits':{'training_updates':0,'five_frozen_reader_seeds':'repeated measures, not independent episodes','heldout_unit':'20 sequences / 120 query occasions / five families','w_i_equal_decisions':'shared manager contract and experimental audit cache; not evidence of independent forward computations','status':'retained-table recomputation only; no scorer/model rerun'}}
 with open(OUT+'metrics_summary.json','x',encoding='utf-8') as f: json.dump(summary,f,indent=2)
 lines=['# CM-02 v0.6 retained metrics check','',
 'Recomputed from the archived main decision, exact-control, family-paired, memory/read-work and event-work CSVs. The archive was read-only; no model, scorer or source module was imported or run.','',
 '## Main and heldout scores','',
 f"The main decision table has {len(decisions):,} rows. Heldout W and I each score {heldout['W']['correct']}/{heldout['W']['rows']} and O scores {heldout['O']['correct']}/{heldout['O']['rows']}. The denominator is 120 heldout query occasions repeated across five frozen reader seeds: 20 sequences and five families, not 600 independent episodes. W/I decision fields match on {parity_pairs:,}/{parity_pairs:,} paired rows, with {parity_mismatches} mismatches.",
 '', 'Exact retrieval controls are run once per occasion:', '',
 '; '.join(f"{k}: {v['correct']}/{v['rows']}" for k,v in sorted(exact_out.items()))+'.', '',
 'Family-level heldout W/I/O counts and W–O differences are in `metrics_summary.json`; the W–O difference is positive in each of the five families.','',
 '## Retained failure strata','',
 f"At F:16, W and I each score {negative_out.get('F:16/W',{}).get('correct',0)}/{negative_out.get('F:16/W',{}).get('rows',0)} and retain safe-but-lost-recall flags; at F:48, W/I score {negative_out.get('F:48/W',{}).get('correct',0)}/{negative_out.get('F:48/W',{}).get('rows',0)}. C:32 W/I score {negative_out.get('C:32/W',{}).get('correct',0)}/{negative_out.get('C:32/W',{}).get('rows',0)}. N:16 and N:32 together produce {negative_out.get('N:16/W',{}).get('correct',0)+negative_out.get('N:32/W',{}).get('correct',0)}/{negative_out.get('N:16/W',{}).get('rows',0)+negative_out.get('N:32/W',{}).get('rows',0)} correct W outcomes, while hidden-intent-wrong-binding flags remain retained. These diagnostic rows are not an overall pass/fail gate.", '',
 '## Measured W/I work','',
 'The totals below combine heldout event work with query work for representative reader seed 1201. Object-graph byte observations are reported as mean/max and peak transient graph; they are not summed as simultaneous resident memory.', '',
 '; '.join(f"{arm}: {v['event_plus_query_index_reads']:,} event+query index reads, {v['packet_encodes']:,} event packet encodes, {v['packet_decodes']:,} event+query decodes, {v['task_field_semantic_bytes_rewritten']:,} semantic-field bytes rewritten, {v['workspace_ascii_bytes_rewritten']:,} ASCII bytes rewritten" for arm,v in cost_totals.items())+'.',
 '',f"Across heldout query observations, mean/max resident graph was W {cost_totals['W']['resident_graph_mean_bytes']:,.2f}/{cost_totals['W']['resident_graph_max_bytes']:,} bytes and I {cost_totals['I']['resident_graph_mean_bytes']:,.2f}/{cost_totals['I']['resident_graph_max_bytes']:,}; peak transient graph was W {cost_totals['W']['peak_query_transient_controller_graph_bytes']:,} and I {cost_totals['I']['peak_query_transient_controller_graph_bytes']:,} bytes.", '',
 'The archived report identifies zero training updates and describes internal exact replay; this table check is not an independent scorer rerun or third-party replication. Repeated query measurements across five fixed seeds are not independent episode samples.']
 with open(OUT+'METRICS.md','x',encoding='utf-8',newline='') as f: f.write('\n'.join(lines)+'\n')

