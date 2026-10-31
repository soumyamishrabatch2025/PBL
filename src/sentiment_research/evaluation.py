"""Common evaluation for every model, with prediction-level evidence."""
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.metrics import (accuracy_score, balanced_accuracy_score, classification_report,
                             cohen_kappa_score, confusion_matrix, ConfusionMatrixDisplay,
                             f1_score, log_loss, matthews_corrcoef, precision_recall_fscore_support,
                             roc_auc_score)

from . import LABELS
from .common import write_csv, write_json


def metrics(y_true, y_pred, probabilities=None):
    result = {"n_examples": len(y_true), "accuracy": float(accuracy_score(y_true, y_pred)),
              "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
              "matthews_correlation": float(matthews_corrcoef(y_true, y_pred)),
              "cohen_kappa": float(cohen_kappa_score(y_true, y_pred))}
    for average in ("macro", "weighted", "micro"):
        precision, recall, f1, _ = precision_recall_fscore_support(
            y_true, y_pred, labels=list(range(3)), average=average, zero_division=0)
        result.update({f"{average}_precision": float(precision), f"{average}_recall": float(recall),
                       f"{average}_f1": float(f1)})
    if probabilities is not None:
        result["log_loss"] = float(log_loss(y_true, probabilities, labels=list(range(3))))
        if len(set(y_true)) == 3:
            result["macro_roc_auc_ovr"] = float(roc_auc_score(y_true, probabilities, multi_class="ovr", average="macro"))
    return result


def bootstrap_intervals(y_true, y_pred, n_samples=1000, seed=42):
    """Stratified paired resampling; conditional on this test set and trained model."""
    y_true, y_pred = np.asarray(y_true), np.asarray(y_pred)
    rng = np.random.default_rng(seed)
    groups = [np.flatnonzero(y_true == label) for label in range(3)]
    estimates = {"accuracy": [], "macro_f1": [], "weighted_f1": []}
    for _ in range(n_samples):
        index = np.concatenate([rng.choice(group, len(group), replace=True) for group in groups if len(group)])
        estimates["accuracy"].append(float(np.mean(y_true[index] == y_pred[index])))
        for average in ("macro", "weighted"):
            estimates[f"{average}_f1"].append(float(f1_score(y_true[index], y_pred[index], labels=[0, 1, 2], average=average, zero_division=0)))
    return {"method": "Stratified test-example bootstrap; excludes training-seed/split uncertainty",
            "n_resamples": n_samples, "seed": seed,
            "95_percent_intervals": {key: np.quantile(values, [0.025, 0.975]).tolist() for key, values in estimates.items()}}


def evaluate(folder, rows, y_pred, probabilities=None, split="test", bootstrap_samples=1000):
    y_true = np.array([int(row["label_id"]) for row in rows])
    y_pred = np.asarray(y_pred, dtype=int)
    if len(y_true) != len(y_pred) or not len(rows):
        raise ValueError("Nonempty aligned labels and predictions are required")
    result = metrics(y_true, y_pred, probabilities)
    write_json(folder / f"{split}_metrics.json", result)
    report = classification_report(y_true, y_pred, labels=[0, 1, 2], target_names=LABELS, output_dict=True, zero_division=0)
    write_json(folder / f"{split}_classification_report.json", report)
    write_csv(folder / f"{split}_per_class.csv", [{"label": label, **report[label]} for label in LABELS])
    predictions = []
    for index, (row, predicted) in enumerate(zip(rows, y_pred)):
        entry = {"tweet_id": row["tweet_id"], "group_id": row["group_id"], "text": row["text"],
                 "true_label": row["label"], "predicted_label": LABELS[predicted],
                 "correct": bool(int(row["label_id"]) == predicted)}
        if probabilities is not None:
            entry.update({f"p_{label}": float(probabilities[index, label_id]) for label_id, label in enumerate(LABELS)})
        predictions.append(entry)
    write_csv(folder / f"{split}_predictions.csv", predictions)
    write_csv(folder / f"{split}_errors.csv", [row for row in predictions if not row["correct"]], list(predictions[0]))
    matrix = confusion_matrix(y_true, y_pred, labels=[0, 1, 2])
    write_csv(folder / f"{split}_confusion_matrix.csv", [{"actual": label, **dict(zip(LABELS, map(int, matrix[i])))} for i, label in enumerate(LABELS)])
    for mode in (None, "true"):
        display = ConfusionMatrixDisplay.from_predictions(y_true, y_pred, labels=[0, 1, 2], display_labels=LABELS,
                                                          normalize=mode, cmap="Blues", colorbar=False,
                                                          values_format=".2f" if mode else "d")
        display.ax_.set_title(f"{folder.parent.name} - {split}" + (" (row normalized)" if mode else ""))
        display.figure_.tight_layout()
        display.figure_.savefig(folder / f"{split}_confusion_matrix{'_normalized' if mode else ''}.png", dpi=220)
        plt.close(display.figure_)
    if bootstrap_samples:
        write_json(folder / f"{split}_bootstrap.json", bootstrap_intervals(y_true, y_pred, bootstrap_samples))
    return result
