"""Read-only checks and reproducibility entry point. No downloads or deployment."""
from pathlib import Path
import argparse, datetime, json, os, shutil, subprocess, sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'scripts'))
from integrity import verify


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('integrity', 'checks', 'rescore', 'resume', 'replay'))
    parser.add_argument('--pair', type=int, choices=range(1, 6), default=1)
    parser.add_argument('--output', type=Path,
                        help='New run directory outside this release; defaults to a sibling output folder.')
    args = parser.parse_args()
    print(json.dumps(verify(), indent=2), flush=True)
    if args.action == 'integrity':
        return
    env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', 'OMP_NUM_THREADS': '1',
           'MKL_NUM_THREADS': '1', 'OPENBLAS_NUM_THREADS': '1'}
    if args.action == 'checks':
        subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-v'],
                       cwd=ROOT, env=env, check=True)
    else:
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        out = (args.output or ROOT.parent / 'NSS_Run_Output' / ('IdentityBinding009_' + args.action + '_' + stamp)).resolve()
        if out == ROOT or ROOT in out.parents:
            raise SystemExit('Output must be outside the immutable release directory.')
        if out.exists():
            raise SystemExit('Choose a new output directory; existing runs are not overwritten.')
        if args.action == 'replay' and sys.platform == 'win32':
            raise SystemExit('Full replay currently requires Unix resource telemetry. Windows replay is NOT_SUPPORTED in this release.')
        out.mkdir(parents=True)
        if args.action == 'rescore':
            command = ['scripts/rescore.py', '--receipt', str(out / 'RESCORE.json')]
        elif args.action == 'resume':
            target = out / 'fixtures'
            shutil.copytree(ROOT / 'evidence/verification/continuations', target)
            command = ['scripts/continuations.py', '--folder', str(target), '--verify-only']
        else:
            command = ['scripts/replay.py', '--pair', str(args.pair), '--out', str(out)]
        subprocess.run([sys.executable, '-B', *command], cwd=ROOT, env=env, check=True)
        print('Run output:', out, flush=True)
    print(json.dumps(verify(), indent=2), flush=True)


if __name__ == '__main__':
    main()
