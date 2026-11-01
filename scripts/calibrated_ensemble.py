"""Development-only ensemble diagnostic; never claims independent test performance."""
import sys
from pathlib import Path
from itertools import product

import numpy as np
from scipy.optimize import minimize_scalar
from sklearn.metrics import f1_score, log_loss
from sklearn.model_selection import train_test_split

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from sentiment_research.common import ROOT, read_csv, sha256, write_json
from sentiment_research.evaluation import evaluate
from sentiment_research import LABEL2ID, LABELS


def temperature_scale(probabilities, temperature):
    logits = np.log(np.clip(probabilities, 1e-12, 1.)) / temperature
    logits -= logits.max(axis=1, keepdims=True)
    scaled = np.exp(logits)
    return scaled / scaled.sum(axis=1, keepdims=True)


def load_aligned(files):
    reference, arrays = None, []
    for file in files:
        rows = read_csv(file)
        identity = [(r['tweet_id'], r['group_id'], r['text'], r['true_label']) for r in rows]
        if reference is not None and identity != reference:
            raise ValueError('Prediction identities/order/labels differ')
        reference = identity
        p = np.array([[float(r[f'p_{label}']) for label in LABELS] for r in rows])
        if not np.isfinite(p).all() or (p < 0).any() or not np.allclose(p.sum(1), 1., atol=1e-5):
            raise ValueError('Invalid probabilities')
        arrays.append(p / p.sum(axis=1, keepdims=True))
    return rows, np.array(arrays)


def main():
    folder = ROOT / 'outputs/automated_v3/calibrated_ensemble'
    if folder.exists():
        raise FileExistsError(folder)
    names = ['hingbert', 'hingroberta', 'hingroberta_focal', 'muril']
    files = [ROOT / f'outputs/sentimix_development_v2/{m}/seed_42/validation_predictions.csv' for m in names]
    rows, probabilities = load_aligned(files)
    y = np.array([LABEL2ID[r['true_label']] for r in rows])
    calibration, remainder = train_test_split(np.arange(len(y)), train_size=.4, stratify=y, random_state=42)
    tuning, diagnostic = train_test_split(remainder, test_size=.5, stratify=y[remainder], random_state=43)
    temperatures, calibrated = [], []
    for p in probabilities:
        fit = minimize_scalar(lambda t: log_loss(y[calibration], temperature_scale(p[calibration], t), labels=[0,1,2]),
                              bounds=(.25, 4.), method='bounded')
        if not fit.success:
            raise RuntimeError('Temperature fit failed')
        temperatures.append(float(fit.x))
        calibrated.append(temperature_scale(p, fit.x))
    calibrated = np.array(calibrated)
    best_score, weights = -1., None
    for a, b, c in product(range(11), repeat=3):
        d = 10-a-b-c
        if d < 0:
            continue
        w = np.array([a,b,c,d]) / 10
        pred = np.tensordot(w, calibrated[:, tuning], axes=1).argmax(1)
        score = f1_score(y[tuning], pred, average='macro', labels=[0,1,2], zero_division=0)
        if score > best_score:
            best_score, weights = score, w
    result = np.tensordot(weights, calibrated[:, diagnostic], axes=1)
    evidence = [{**rows[i], 'label': rows[i]['true_label'], 'label_id': int(y[i])} for i in diagnostic]
    diagnostic_metrics = evaluate(folder, evidence, result.argmax(1), result, 'development_diagnostic', 0)
    equal = probabilities[:, diagnostic].mean(0)
    evaluate(folder, evidence, equal.argmax(1), equal, 'equal_uncalibrated_diagnostic', 0)
    write_json(folder / 'selection.json', {
        'models': names, 'temperatures': temperatures, 'weights': weights.tolist(),
        'calibration_ids': [rows[i]['tweet_id'] for i in calibration],
        'tuning_ids': [rows[i]['tweet_id'] for i in tuning],
        'diagnostic_ids': [rows[i]['tweet_id'] for i in diagnostic],
        'input_sha256': {str(f.relative_to(ROOT)): sha256(f) for f in files},
        'diagnostic_metrics': diagnostic_metrics,
        'limitation': 'Base checkpoints selected on the entire validation set. These are conditional development diagnostics, not fresh test estimates or training out-of-fold predictions.'})
    print(diagnostic_metrics)


if __name__ == '__main__':
    main()
