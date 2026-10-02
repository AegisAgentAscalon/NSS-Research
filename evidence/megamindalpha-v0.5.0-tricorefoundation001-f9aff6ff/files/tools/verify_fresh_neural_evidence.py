#!/usr/bin/env python3
"""Strict replay of an explicitly supplied NEW numerical-contract report.

Artifact/history inspection, not renewed data-use permission or qualification.
No tolerance fallback, report rewriting or automatic retraining is performed.
"""
from pathlib import Path
import argparse,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from nss_base.neural_backend import environment
from nss_base.neural_contracts import encoded,read_document
from nss_base.neuralprobe001 import implementation,verify_numerics
from nss_base.neural_records import validate_plan
from nss_base.runtime import ContractError,fail

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);args=p.parse_args()
 try:
  s=read_document(args.report);plan=validate_plan(s['plan'])
  if plan['schema_version']!=2:fail('INCOMPATIBLE_CONFIGURATION','Legacy plans are not new numerical-contract evidence')
  if plan['environment']!=environment() or plan['code_sha256']!=implementation()['sha256']:
   fail('INCOMPATIBLE_CONFIGURATION','Different bound implementation/numerical environment; fresh run required')
  result=verify_numerics(s,None,current=False)
  result.update(scope='EXACT_ARTIFACT_REPLAY_ONLY_NOT_CURRENT_DATA_PERMISSION',plan_schema=2,tolerance_fallback=False)
  print(encoded(result).decode());return 0
 except (KeyError,TypeError):
  print(encoded({'status':'VALIDATION_FAILED','authority':'NONE'}).decode());return 1
 except ContractError as e:
  print(encoded({'status':e.code,'detail':str(e),'authority':'NONE'}).decode());return 1
if __name__=='__main__':raise SystemExit(main())
