"""Explicit cross-corpus evaluation of a frozen checkpoint; validation by default."""
import argparse
import sys
from pathlib import Path
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from sentiment_research.common import read_json, load_splits, write_json, sha256
from sentiment_research.evaluation import evaluate


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--checkpoint', type=Path, required=True)
    p.add_argument('--config', type=Path, required=True, help='Target dataset config')
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--split', choices=['validation', 'test'], default='validation')
    p.add_argument('--allow-test', action='store_true', help='Explicitly release final evaluation labels')
    args = p.parse_args()
    if args.split == 'test' and not args.allow_test:
        p.error('Final test evaluation requires --allow-test after protocol freeze')
    if args.output.exists():
        raise FileExistsError(args.output)
    config = read_json(args.config)
    splits, audit = load_splits(config, [args.split])
    training = read_json(args.checkpoint.parent / 'config.json')
    expected = training.get('preprocessing_version', 'v1')
    if expected != config.get('preprocessing_version', 'v1'):
        p.error('Source checkpoint and target preprocessing versions must match')
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    tokenizer = AutoTokenizer.from_pretrained(args.checkpoint, local_files_only=True)
    model = AutoModelForSequenceClassification.from_pretrained(args.checkpoint, local_files_only=True).to(device).eval()
    rows, probabilities = splits[args.split], []
    with torch.inference_mode():
        for start in range(0, len(rows), 8):
            inputs = tokenizer([r['text'] for r in rows[start:start+8]], padding=True, truncation=True,
                               max_length=training['transformer']['max_length'], return_tensors='pt').to(device)
            probabilities.append(model(**inputs).logits.float().softmax(-1).cpu().numpy())
    probs = np.concatenate(probabilities)
    result = evaluate(args.output, rows, probs.argmax(1), probs, args.split, 0)
    write_json(args.output / 'transfer.json', {'checkpoint': str(args.checkpoint.resolve()),
               'source_config_sha256': sha256(args.checkpoint.parent / 'config.json'),
               'target_audit': audit, 'split': args.split, 'metrics': result})


if __name__ == '__main__':
    main()
