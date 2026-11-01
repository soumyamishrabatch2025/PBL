"""Print the experiment queue by default; --train executes sequentially without overwrites."""
import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from sentiment_research.common import ROOT, read_json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', action='store_true')
    parser.add_argument('--experiments', nargs='+', help='Subset of experiment names')
    parser.add_argument('--seeds', nargs='+', type=int, default=[42])
    args = parser.parse_args()
    plan = read_json(ROOT / 'outputs/automated_v3/experiment_plan.json')
    known = {r['name'] for r in plan}
    if args.experiments and set(args.experiments) - known:
        parser.error('Unknown experiment name')
    for item in plan:
        if args.experiments and item['name'] not in args.experiments:
            continue
        config = read_json(ROOT / item['config'])
        for seed in args.seeds:
            folder = ROOT / config['output_dir'] / config['transformer']['run_name'] / f'seed_{seed}'
            if (folder / 'complete.json').exists():
                print('COMPLETE', item['name'], seed, flush=True)
                continue
            command = [sys.executable, str(ROOT / 'run_research.py'), 'train', '--config',
                       str(ROOT / item['config']), '--seeds', str(seed)]
            print('TRAIN' if args.train else 'PLANNED', item['name'], seed, flush=True)
            if args.train:
                if folder.exists() and any(folder.iterdir()):
                    raise FileExistsError(f'Incomplete run preserved at {folder}; choose a new output directory')
                subprocess.run(command, cwd=ROOT, check=True)


if __name__ == '__main__':
    main()
