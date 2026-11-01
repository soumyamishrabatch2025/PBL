"""Check new dataset hashes/disjointness and tokenizer lengths without model training."""
import sys
from pathlib import Path
from collections import Counter
import numpy as np
from transformers import AutoTokenizer

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from sentiment_research.common import ROOT, read_json, load_splits, write_json
from sentiment_research.improvements import key


def main():
    metadata = read_json(ROOT / 'outputs/sentimix_development_v2/hingroberta/seed_42/training_metadata.json')
    tokenizer = AutoTokenizer.from_pretrained(metadata['resolved_snapshot'], local_files_only=True)
    results = {}
    for corpus in ['sentimix', 'sentimix_control', 'sail', 'pooled']:
        config = {'prepared_dir': f'data/research/automated_v3/{corpus}', 'lowercase': False, 'split_seed': 42}
        splits, _ = load_splits(config)
        text_sets = {s: {key(r['text']) for r in rows} for s, rows in splits.items()}
        for a, b in [('train','validation'), ('train','test'), ('validation','test')]:
            if text_sets[a] & text_sets[b]:
                raise ValueError(f'{corpus}: leakage {a}/{b}')
        for split, rows in splits.items():
            if len(text_sets[split]) != len(rows):
                raise ValueError(f'{corpus}/{split}: duplicate text')
        # No tokenizer diagnostics on test; lengths cannot influence final evaluation.
        stats = {}
        for split in ['train', 'validation']:
            rows = splits[split]
            lengths = np.array([len(ids) for ids in tokenizer([r['text'] for r in rows],
                                truncation=False, verbose=False)['input_ids']])
            stats[split] = {'rows': len(rows), 'p95_tokens': float(np.quantile(lengths,.95)),
                            'over_128': int((lengths>128).sum()), 'over_256': int((lengths>256).sum()),
                            'corpora': dict(Counter(r['corpus'] for r in rows))}
        results[corpus] = stats
    write_json(ROOT / 'outputs/automated_v3/data_checks.json', {'status': 'passed', 'details': results,
               'checks': 'Recorded hashes verified, casefolded v2 texts unique and disjoint within all datasets.'})
    print(results)


if __name__ == '__main__':
    main()
