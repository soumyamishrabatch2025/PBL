"""Versioned, label-preserving preprocessing and reproducible experiment preparation."""
import copy
import hashlib
import re
from collections import Counter, defaultdict

from .common import ROOT, read_csv, read_json, sha256, write_csv, write_json
from .data import normalize


def normalize_v2(text, lowercase=False):
    # Repair tokenized URLs and anonymized mention suffixes without removing opinions.
    text = re.sub(r"\bhttps?\s*(?::\s*)?/\s*/\s*\S+", " URL ", text, flags=re.I)
    text = re.sub(r"\bUSER\s+_\s*[\w_]+", " USER ", text)
    text = normalize(text, lowercase)
    return re.sub(r"\bUSER\s+_\s*[\w_]+", "USER", text, flags=re.I)


def key(text):
    return normalize_v2(text).casefold()


def version_rows(rows, source):
    result = []
    for row in rows:
        row = dict(row)
        row['text'] = normalize_v2(row.get('raw_text', row['text']))
        row['group_id'] = hashlib.sha256(key(row['text']).encode()).hexdigest()
        row['corpus'] = source
        result.append(row)
    return result


def save_dataset(folder, splits, sources, exclusions, preprocessing_version='v2'):
    if folder.exists():
        raise FileExistsError(f'Use a new version; dataset exists: {folder}')
    for name, rows in splits.items():
        write_csv(folder / f'{name}.csv', rows)
    write_csv(folder / 'exclusions.csv', exclusions,
              ['corpus', 'split', 'tweet_id', 'group_id', 'reason'])
    write_json(folder / 'audit.json', {
        'lowercase': False, 'split_seed': 42, 'preprocessing_version': preprocessing_version,
        'source_sha256': sources,
        'split_sha256': {s: sha256(folder / f'{s}.csv') for s in splits},
        'split_counts': {s: {'rows': len(r), 'labels': dict(Counter(x['label'] for x in r))}
                         for s, r in splits.items()},
        'protocol': 'Existing split membership retained; no relabeling. Evaluation texts excluded from training.',
        'evaluation_warning': 'SentiMix evaluation previously exposed; SAIL is a derived benchmark, not guaranteed unseen pretraining data.',
    })


def prepare_improvements():
    target = ROOT / 'data/research/automated_v3'
    if target.exists():
        raise FileExistsError(f'{target} exists; refusing to overwrite')
    splits, sources = {}, {}
    for corpus, directory in [('sentimix', 'sentimix_custom_split_v1'), ('sail', 'sail2017_prepared_v1')]:
        for split in ['train', 'validation', 'test']:
            file = ROOT / 'data/research' / directory / f'{split}.csv'
            splits[corpus, split] = version_rows(read_csv(file), corpus)
            sources[f'{corpus}/{split}'] = sha256(file)
    # Test wins over validation; both win over training. Conflicting training groups
    # are excluded rather than assigning a new label. Decisions never use test labels.
    eval_groups = set()
    cleaned, excluded, overlap = {}, [], []
    for split in ['test', 'validation', 'train']:
        groups = defaultdict(list)
        for corpus in ['sentimix', 'sail']:
            for row in splits[corpus, split]:
                groups[row['group_id']].append(row)
        for group_id, rows in groups.items():
            if len(rows) > 1:
                overlap.append({'split': split, 'group_id': group_id, 'count': len(rows),
                                'corpora': sorted({r['corpus'] for r in rows})})
            conflict = split == 'train' and len({r['label'] for r in rows}) > 1
            seen_corpora = set()
            for row in rows:
                reason = ('overlaps_higher_priority_split' if group_id in eval_groups else
                          'conflicting_training_labels' if conflict else
                          'duplicate_within_corpus' if row['corpus'] in seen_corpora else None)
                if reason:
                    excluded.append({k: row[k] for k in ['corpus', 'tweet_id', 'group_id']} |
                                    {'split': split, 'reason': reason})
                else:
                    cleaned.setdefault((row['corpus'], split), []).append(row)
                    seen_corpora.add(row['corpus'])
        if split != 'train':
            eval_groups.update(groups)
    for corpus in ['sentimix', 'sail']:
        save_dataset(target / corpus, {s: cleaned.get((corpus, s), []) for s in ['train', 'validation', 'test']},
                     sources, [r for r in excluded if r['corpus'] == corpus])
    # One row per normalized text in pooled training, including cross-source duplicates.
    pooled_train = {r['group_id']: r for c in ['sentimix', 'sail'] for r in cleaned[c, 'train']}
    save_dataset(target / 'pooled', {'train': list(pooled_train.values()),
                 'validation': cleaned['sentimix', 'validation'], 'test': cleaned['sentimix', 'test']}, sources, excluded)
    write_json(target / 'overlap_audit.json', {'groups': overlap, 'excluded_rows': len(excluded),
               'policy': 'Global test > validation > train, training conflicts excluded; no labels changed.'})
    # A matched preprocessing control uses precisely the same retained rows as v2.
    control = {s: [{**r, 'text': normalize(r['raw_text'])} for r in cleaned['sentimix', s]]
               for s in ['train', 'validation', 'test']}
    save_dataset(target / 'sentimix_control', control, sources,
                 [r for r in excluded if r['corpus'] == 'sentimix'], 'v1')
    make_configs(target)
    return target


def make_configs(target):
    template = read_json(ROOT / 'configs/development_hingroberta_focal.json')
    plan = []
    variants = [('ce', 0., None), ('weighted_ce', 0., [1., 1.25, 1.]),
                ('focal', 2., None), ('weighted_focal', 2., [1., 1.25, 1.])]
    experiments = [(f'loss_{name}', 'sentimix', gamma, weights, 2e-5, False)
                   for name, gamma, weights in variants]
    experiments += [('preprocess_control', 'sentimix_control', 0., None, 2e-5, False)]
    experiments += [(f'lr_{lr:g}', 'sentimix', 0., None, lr, False) for lr in [1e-5, 3e-5]]
    experiments += [(f'corpus_{corpus}', corpus, 0., None, 2e-5, False) for corpus in ['sail', 'pooled']]
    experiments += [('pooled_balanced', 'pooled', 0., None, 2e-5, True)]
    for name, corpus, gamma, weights, lr, balanced in experiments:
        config = copy.deepcopy(template)
        config.update(experiment=f'automated_v3_{name}', prepared_dir=str((target / corpus).relative_to(ROOT)),
                      output_dir=f'outputs/automated_v3/{name}', baseline_output_dir=f'outputs/automated_v3/{name}')
        config['transformer'].update(focal_gamma=gamma, class_weights=weights, learning_rate=lr,
                                     early_stopping_patience=1, dataset_balanced_sampling=balanced)
        config['preprocessing_version'] = 'v1' if corpus == 'sentimix_control' else 'v2'
        config['report_section'] = f'automated_v3_{name}'
        file = ROOT / 'configs/automated_v3' / f'{name}.json'
        write_json(file, config)
        plan.append({'name': name, 'config': str(file.relative_to(ROOT)), 'status': 'ready_not_trained',
                     'seeds': [42], 'dataset': corpus})
    write_json(ROOT / 'outputs/automated_v3/experiment_plan.json', plan)


if __name__ == '__main__':
    print(prepare_improvements())
