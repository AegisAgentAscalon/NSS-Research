from pathlib import Path
import shutil,json,hashlib,datetime
B=Path('/mnt/data/_nss_pass61_work/reconciled'); R=Path('/mnt/data/NSS_LB03_LEARNABILITY_v0.1'); S=B/'NSS_NBR02_LB02_MASTER16_Execution_v0.1'; Q=B/'NSS_NBR02_LB02_Q2_TRAIN_Execution_v0.1'
for d in ('bin','inputs/parents','inputs/replay','inputs/prior_fixtures'): (R/d).mkdir(parents=True,exist_ok=True)
for src,dst in [('experiment.py','inherited_engine.py'),('master16.c','master16.c'),('inherited_kernels.c','kernels.c'),('task.py','task.py')]:shutil.copyfile(S/'source'/src,R/'source'/dst)
# All copied original checkpoints remain unchanged. Selection is stage-based, never score-based.
links=[]
for seed in range(4101,4105):
 for step in (0,1024):
  src=Q/f'checkpoints/{seed}_Q2_M8/step{step:04d}.pt';dst=R/f'inputs/parents/{seed}_s{step:04d}.pt';shutil.copyfile(src,dst)
  links.append(dict(pass_number=57,archive='NSS_NBR02_LB02_Q2_TRAIN_Execution_v0.1.zip',member=str(src.relative_to(B)),copied_to=str(dst.relative_to(R)),sha256=hashlib.sha256(dst.read_bytes()).hexdigest()))
 shutil.copyfile(Q/f'inputs/replay/{seed}.npz',R/f'inputs/replay/{seed}.npz')
# Materialized older panels permit an exact-window exclusion against available data.
for num,tag in [(56,'LB01_TERNARY'),(57,'LB02_Q2_TRAIN'),(58,'LB02_MASTER16'),(59,'LB01_T3_TARGET')]:
 root=B/f'NSS_NBR02_{tag}_Execution_v0.1'
 for f in sorted((root/'fixtures').glob('*.npz')):shutil.copyfile(f,R/f'inputs/prior_fixtures/p{num}_{f.name}')
(R/'provenance/SELECTED_STARTS.json').write_text(json.dumps(links,indent=2))
C=dict(study='LB03-LEARNABILITY',version='0.1',pass_number=61,parents=[4101,4102,4103,4104],modes=['M32','M16_NEAREST','M16_STOCHASTIC'],regimes=['EARLY','NEW'],updates_per_branch=512,total_main_updates=12288,main_extra_update_allowance=0,preflight_update_cap=96,benchmark_update_cap=144,audit_update_cap=48,total_actual_update_cap=12576,branch_wall_limit_seconds=90,total_training_core_limit_seconds=900,max_rss_bytes=2147483648,evidence_bytes=268435456,branch_checkpoint_steps=[0,64,128,256,512],dev_steps=[0,64,128,256,512],confirmation_steps=[0,512],lr_start=.003,lr_end=.0003,clip_norm=1.0,betas=[.9,.999],epsilon=1e-8,optimizer='inherited_M8_custom_SQ8_reset_for_every_branch',new_cue_indices=[2,5],old_B=[0,1,0,1,0,1,0,1],new_B=[0,1,1,1,0,0,0,1],selection='Both candidate modes mandatory; no winner or endpoint selection from development or confirmation.',fixture_seed=161202610,round_seed_base=61002026,benchmark_seed=161991,fixture_counts={'development':16,'confirmation':256,'stress':32},prefix={'development':24,'confirmation':24,'stress':64},length={'development':56,'confirmation':56,'stress':192},numerical={'fp64_atol':1e-9,'fp64_rtol':1e-8,'fp32_grad_atol':2e-6,'fp32_grad_rtol':2e-4},gates={'same_task_event_floor':.98,'same_task_whole_floor':.90,'early_net_error_reduction_floor':.90,'new_B_probability_floor':.80,'event_loss_vs_control_max':.005,'whole_loss_vs_control_max':.02,'extra_false_done_vs_control_max':1,'retained_event_loss_vs_start_max':.01,'retained_whole_loss_vs_start_max':.02,'new_false_done_vs_start_max':1,'learning_array_saving_min':.15,'training_time_ratio_max':1.25,'required_parent_count':3},semantic_review_indices=[0,64,128,192],no_post_learning_repair=True,no_model_adoption=True,no_pretrained_download=True)
(R/'protocol/CONFIG.json').write_text(json.dumps(C,indent=2)+'\n')
(R/'protocol/PLAN_RECEIPT.json').write_text(json.dumps(dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='DESIGN_BEFORE_PREFLIGHT_AND_MAIN',config_sha256=hashlib.sha256((R/'protocol/CONFIG.json').read_bytes()).hexdigest(),no_main_results_examined=True),indent=2))
print('setup copied',len(links),'exact checkpoints')
