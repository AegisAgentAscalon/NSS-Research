"""Default NSS entry point: current-role foundation, not legacy overlay demos."""
import argparse
import json
from pathlib import Path
from .runtime import ContractError
from .foundation_ports import UnconnectedForge, UnconnectedRuntime


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    sub.add_parser('capabilities')
    demo=sub.add_parser('demo');demo.add_argument('--output',required=True,type=Path)
    inspect=sub.add_parser('inspect');inspect.add_argument('--store',required=True,type=Path)
    research=sub.add_parser('research')
    mode=research.add_mutually_exclusive_group(required=True)
    mode.add_argument('--preflight',action='store_true');mode.add_argument('--harness-smoke',action='store_true')
    args=parser.parse_args()
    try:
        if args.command=='capabilities':
            out={'version':'0.5.0-tricore-foundation001','scope':'TEST_ADAPTERS_ONLY',
                'current_roles':['PRIMARY','SECONDARY','TERTIARY','VALIDATOR'],
                'overlays_required':False,'primary_only':True,'scoped_context':'v3',
                'durable_owner':'Generations','native_neural_refinement':False,
                'trained_language_components':[],'low_bit_learning':False,
                'forge':UnconnectedForge().capabilities(),'runtime':UnconnectedRuntime().capabilities()}
        elif args.command=='demo':
            from .foundation_demo import run_demo
            out=run_demo(args.output)
        elif args.command=='inspect':
            from .generation_store import Generations
            out=Generations(args.store).foundation_snapshot()
        else:
            from .research.nbr01 import preflight,harness_smoke
            out=preflight() if args.preflight else harness_smoke()
        print(json.dumps(out,indent=2,ensure_ascii=False));return 0
    except (ContractError,OSError,ValueError) as e:
        print(json.dumps({'status':getattr(e,'code','ERROR'),'detail':str(e)},ensure_ascii=False));return 1


if __name__=='__main__':raise SystemExit(main())
