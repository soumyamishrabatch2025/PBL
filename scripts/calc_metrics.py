"""Calculate comprehensive metrics for all trained models."""
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from sklearn.metrics import (
    classification_report, f1_score, accuracy_score,
    matthews_corrcoef, cohen_kappa_score, roc_auc_score
)
from sklearn.preprocessing import label_binarize
from sentiment_research.common import read_csv

LABEL2ID = {'negative': 0, 'neutral': 1, 'positive': 2}

root = Path('outputs/sentimix_development_v2')
models = ['hingbert', 'hingroberta', 'hingroberta_focal', 'muril']
preds = {}

for m in models:
    p = root / m / 'seed_42/validation_predictions.csv'
    if p.exists():
        rows = read_csv(p)
        preds[m] = np.array([[float(r['p_negative']), float(r['p_neutral']), float(r['p_positive'])] for r in rows])
        print(f'Loaded {m}: {len(rows)} rows')
    else:
        print(f'MISSING: {p}')

y_true_rows = read_csv(root / 'hingbert/seed_42/validation_predictions.csv')
y_true = np.array([LABEL2ID[r['true_label']] for r in y_true_rows])
y_true_bin = label_binarize(y_true, classes=[0, 1, 2])

print()
print('='*70)
print('INDIVIDUAL MODEL METRICS (Validation Set, Seed 42)')
print('='*70)

for name, prob in preds.items():
    yp = prob.argmax(1)
    auc = roc_auc_score(y_true_bin, prob, multi_class='ovr', average='macro')
    print(f'\n--- {name} ---')
    print(f'Accuracy:    {accuracy_score(y_true, yp):.4f}')
    print(f'Macro F1:    {f1_score(y_true, yp, average="macro"):.4f}')
    print(f'Weighted F1: {f1_score(y_true, yp, average="weighted"):.4f}')
    print(f'MCC:         {matthews_corrcoef(y_true, yp):.4f}')
    print(f'Kappa:       {cohen_kappa_score(y_true, yp):.4f}')
    print(f'Macro AUC:   {auc:.4f}')
    print(classification_report(y_true, yp, target_names=['negative', 'neutral', 'positive'], digits=4))

# ─── Ensembles ────────────────────────────────────────────────────────────────
print()
print('='*70)
print('ENSEMBLE METRICS')
print('='*70)

def eval_ensemble(name, weights):
    """Weighted soft-vote ensemble."""
    probs = np.zeros((len(y_true), 3))
    for model_name, w in weights.items():
        probs += w * preds[model_name]
    yp = probs.argmax(1)
    auc = roc_auc_score(y_true_bin, probs, multi_class='ovr', average='macro')
    print(f'\n--- {name} ---')
    print(f'Weights: {weights}')
    print(f'Accuracy:    {accuracy_score(y_true, yp):.4f}')
    print(f'Macro F1:    {f1_score(y_true, yp, average="macro"):.4f}')
    print(f'Weighted F1: {f1_score(y_true, yp, average="weighted"):.4f}')
    print(f'MCC:         {matthews_corrcoef(y_true, yp):.4f}')
    print(f'Kappa:       {cohen_kappa_score(y_true, yp):.4f}')
    print(f'Macro AUC:   {auc:.4f}')
    print(classification_report(y_true, yp, target_names=['negative', 'neutral', 'positive'], digits=4))
    return f1_score(y_true, yp, average='weighted'), f1_score(y_true, yp, average='macro')

# Tri-model equal weights
eval_ensemble('Tri-Equal (HingBERT + RoBERTa CE + Focal)', {
    'hingbert': 1/3, 'hingroberta': 1/3, 'hingroberta_focal': 1/3
})

# Quad equal
eval_ensemble('Quad-Equal (all four)', {
    'hingbert': 0.25, 'hingroberta': 0.25, 'hingroberta_focal': 0.25, 'muril': 0.25
})

# Best previous tuned
eval_ensemble('Quad-Tuned (0.35/0.25/0.30/0.10)', {
    'hingbert': 0.35, 'hingroberta': 0.25, 'hingroberta_focal': 0.30, 'muril': 0.10
})

# Focal-heavy
eval_ensemble('Focal-Heavy (0.40/0.20/0.35/0.05)', {
    'hingbert': 0.40, 'hingroberta': 0.20, 'hingroberta_focal': 0.35, 'muril': 0.05
})

# Grid search for best weighted F1
print()
print('='*70)
print('GRID SEARCH: Best Ensemble Weights (Macro F1)')
print('='*70)

best_wf1, best_mf1, best_cfg = 0, 0, None
step = 0.05
grid_results = []
for w1 in np.arange(0, 1.05, step):
    for w2 in np.arange(0, 1.05 - w1, step):
        for w3 in np.arange(0, 1.05 - w1 - w2, step):
            w4 = round(1 - w1 - w2 - w3, 10)
            if w4 < -1e-9:
                continue
            w4 = max(0, w4)
            probs = (w1 * preds['hingbert'] + w2 * preds['hingroberta'] +
                     w3 * preds['hingroberta_focal'] + w4 * preds['muril'])
            yp = probs.argmax(1)
            mf1 = f1_score(y_true, yp, average='macro')
            wf1 = f1_score(y_true, yp, average='weighted')
            grid_results.append((mf1, wf1, w1, w2, w3, w4))
            if mf1 > best_mf1:
                best_mf1 = mf1
                best_wf1 = wf1
                best_cfg = (w1, w2, w3, w4)

grid_results.sort(reverse=True)
print(f'\nTop 10 configurations (sorted by Macro F1):')
print(f'{"HingBERT":>10} {"RoBERTa":>10} {"Focal":>10} {"MuRIL":>10} {"MacroF1":>10} {"WeightF1":>10}')
for mf1, wf1, w1, w2, w3, w4 in grid_results[:10]:
    print(f'{w1:>10.2f} {w2:>10.2f} {w3:>10.2f} {w4:>10.2f} {mf1:>10.4f} {wf1:>10.4f}')

print(f'\nBEST: HingBERT={best_cfg[0]:.2f}, RoBERTa={best_cfg[1]:.2f}, Focal={best_cfg[2]:.2f}, MuRIL={best_cfg[3]:.2f}')
print(f'Best Macro F1: {best_mf1:.4f}  |  Best Weighted F1: {best_wf1:.4f}')

# Evaluate the grid-search winner in detail
print()
eval_ensemble('Grid-Search Best', {
    'hingbert': best_cfg[0], 'hingroberta': best_cfg[1],
    'hingroberta_focal': best_cfg[2], 'muril': best_cfg[3]
})
