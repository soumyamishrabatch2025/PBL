import json
import itertools

import numpy as np
from sklearn.metrics import f1_score

from . import LABEL2ID, LABELS
from .common import ROOT, path, read_csv, read_json, write_csv, write_json


FIELDS = ["accuracy", "weighted_precision", "weighted_recall", "weighted_f1", "macro_precision", "macro_recall", "macro_f1", "balanced_accuracy", "matthews_correlation", "cohen_kappa"]


def write_metrics_markdown(config, runs, summary, comparisons):
    """Human-readable root report generated exclusively from measured artifacts."""
    from datetime import datetime
    from zoneinfo import ZoneInfo

    def number(value):
        if value is None:
            return "Not available"
        return f"{value:.10f}" if isinstance(value, float) else str(value)

    def link(file):
        try:
            return file.relative_to(ROOT).as_posix()
        except ValueError:
            return file.as_posix()

    root = path(config["output_dir"])
    audit = read_json(path(config["prepared_dir"]) / "audit.json")
    lines = ["# All model metrics", "",
             "Generated: " + datetime.now(ZoneInfo("Asia/Kolkata")).isoformat(timespec="seconds"), "",
             "Experiment: `" + config["experiment"] + "`. Only measured results from completed runs are reported.",
             "Scores are on a 0-1 scale unless stated otherwise; MCC and kappa range from -1 to 1. Counts and seconds are explicit.",
             "Values are rounded to 10 decimal places here; linked JSON artifacts retain full numerical precision.", "",
             "## Dataset and evaluation protocol", "",
             "Custom deduplicated split of the SentiMix training/development sources, not the paper's exact Hinglish-24k or official benchmark test set.", "",
             "| Split | Examples | Negative | Neutral | Positive |", "|---|---:|---:|---:|---:|"]
    for split, counts in audit["split_counts"].items():
        lines.append("| " + " | ".join([split, str(counts["rows"])] + [str(counts["labels"].get(label, 0)) for label in LABELS]) + " |")
    lines += ["", f"Raw examples: {audit['raw_rows']}; retained: {audit['clean_rows']}; duplicate rows removed: {audit['duplicate_rows_removed']}; conflicting/invalid rows excluded: {audit['rejected_rows']}.",
              f"Split seed: {audit['split_seed']}. Selection metric: validation `{config['selection_metric']}`.",
              "Preprocessing: " + audit["preprocessing"], "Leakage checks: " + audit["leakage_checks"], "",
              "## Model comparison", "",
              "| Model | Seed | Accuracy | Weighted precision | Weighted recall | Weighted F1 | Macro F1 |", "|---|---:|---:|---:|---:|---:|---:|"]
    for _, value in runs:
        score = value["test_metrics"]
        lines.append("| " + " | ".join([value["model"], str(value["seed"])] + [number(score[key]) for key in
                     ("accuracy", "weighted_precision", "weighted_recall", "weighted_f1", "macro_f1")]) + " |")
    for model_name in ("naive_bayes", "svm", "mbert"):
        lines += ["", "## " + {"naive_bayes": "Naive Bayes + TF-IDF", "svm": "Linear SVM + TF-IDF", "mbert": "mBERT"}[model_name], ""]
        selected = [(folder, value) for folder, value in runs if value["model"] == model_name]
        if not selected:
            lines += ["No completed run yet. No accuracy, precision, recall, F1, or confusion matrix is available."]
            for status_file in sorted((root / model_name).glob("seed_*/status.json")):
                status = read_json(status_file)
                lines += ["", f"Status for {status_file.parent.name}: `{status.get('status')}`; optimizer steps {status.get('step', 'unavailable')}/{status.get('total_steps', 'unavailable')} at report generation."]
            continue
        for folder, value in selected:
            lines += [f"### Seed {value['seed']}", ""]
            selection = read_json(folder / "selection.json")
            lines += ["Selection details:", "", "```json", json.dumps(selection, indent=2), "```", ""]
            for split in ("test", "validation"):
                scores = read_json(folder / f"{split}_metrics.json")
                lines += [f"#### {split.title()} overall metrics", "", "| Metric | Value |", "|---|---:|"]
                lines += [f"| {key} | {number(value)} |" for key, value in scores.items()]
                if model_name == "svm":
                    lines += ["", "Log loss and probability ROC-AUC: not computed because LinearSVC does not produce calibrated probabilities."]
                report = read_json(folder / f"{split}_classification_report.json")
                lines += ["", f"#### {split.title()} per-class metrics", "",
                          "| Class / average | Precision | Recall | F1 | Support |", "|---|---:|---:|---:|---:|"]
                for label in LABELS + ["macro avg", "weighted avg"]:
                    row = report[label]
                    lines.append("| " + " | ".join([label, number(row["precision"]), number(row["recall"]), number(row["f1-score"]), str(int(row["support"]))]) + " |")
                matrix = read_csv(folder / f"{split}_confusion_matrix.csv")
                lines += ["", f"#### {split.title()} confusion matrix (counts)", "",
                          "Rows = actual; columns = predicted. Class order: negative, neutral, positive.", "",
                          "| Actual / predicted | Negative | Neutral | Positive |", "|---|---:|---:|---:|"]
                for row in matrix:
                    lines.append("| " + " | ".join([row["actual"]] + [row[label] for label in LABELS]) + " |")
                lines += ["", f"#### {split.title()} confusion matrix (row-normalized)", "",
                          "| Actual / predicted | Negative | Neutral | Positive |", "|---|---:|---:|---:|"]
                for row in matrix:
                    counts = [int(row[label]) for label in LABELS]
                    total = sum(counts)
                    lines.append("| " + " | ".join([row["actual"]] + [number(count / total if total else 0.0) for count in counts]) + " |")
                timing = read_json(folder / f"{split}_timing.json")
                lines += ["", f"{split.title()} inference time: {number(timing['inference_seconds'])} seconds; throughput: {number(timing['examples_per_second'])} examples/second.",
                          f"[Full metrics JSON]({link(folder / f'{split}_metrics.json')}) | [All predictions]({link(folder / f'{split}_predictions.csv')}) | [Errors]({link(folder / f'{split}_errors.csv')})", "",
                          f"![{model_name} seed {value['seed']} {split} confusion matrix]({link(folder / f'{split}_confusion_matrix.png')})", ""]
            bootstrap_file = folder / "test_bootstrap.json"
            if bootstrap_file.exists():
                bootstrap = read_json(bootstrap_file)
                lines += ["#### Test confidence intervals", "", bootstrap["method"],
                          f"Resamples: {bootstrap['n_resamples']}; bootstrap RNG seed: {bootstrap['seed']}.", "",
                          "| Metric | 95% lower | 95% upper |", "|---|---:|---:|"]
                for key, interval in bootstrap["95_percent_intervals"].items():
                    lines.append(f"| {key} | {number(interval[0])} | {number(interval[1])} |")
            training_seconds = value.get("training_seconds", value.get("training_seconds_including_search"))
            lines += ["", "#### Training details", "", f"Training time: {number(training_seconds)} seconds" + (" (including baseline hyperparameter search)." if model_name != "mbert" else ".")]
            if (folder / "training_history.csv").exists():
                history = read_csv(folder / "training_history.csv")
                lines += ["", "| Epoch | Mean training loss | Validation accuracy | Validation macro F1 | Validation weighted F1 | Elapsed seconds |", "|---|---:|---:|---:|---:|---:|"]
                for row in history:
                    lines.append("| " + " | ".join([row[key] for key in ("epoch", "train_loss", "validation_accuracy", "validation_macro_f1", "validation_weighted_f1", "elapsed_seconds")]) + " |")
            if (folder / "training_metadata.json").exists():
                lines += ["", "```json", (folder / "training_metadata.json").read_text(encoding="utf-8"), "```"]
            lines += ["", f"[Recorded config]({link(folder / 'config.json')}) | [Run environment]({link(folder / 'environment.json')})", ""]
    lines += ["## Training-seed summary", "", "Single-run standard deviation is unavailable; it is not evidence of zero variability.", ""]
    for row in summary:
        lines += [f"### {row['model']}: {row['n_runs']} completed run(s)", "", "| Metric | Mean | Sample standard deviation |", "|---|---:|---:|"]
        lines += [f"| {key} | {number(row[key + '_mean'])} | {number(row[key + '_std'])} |" for key in FIELDS]
        lines.append("")
    lines += ["## Paired model comparisons", "", "Weighted F1 differences use matched test-example bootstrap resampling for fixed seed-42 runs.", "",
              "| Left model vs right model | Difference (left - right) | 95% lower | 95% upper |", "|---|---:|---:|---:|"]
    for key, value in comparisons.items():
        interval = value["paired_bootstrap_95_percent_interval"]
        lines.append(f"| {key} | {number(value['weighted_f1_difference_left_minus_right'])} | {number(interval[0])} | {number(interval[1])} |")
    lines += ["", "Intervals condition on these fitted models/test examples and do not account for training-seed or split uncertainty. No significance or state-of-the-art claim is implied.", "",
              "## Reproducibility", "", "Frozen split SHA-256 checksums:", "", "```json", json.dumps(audit["split_sha256"], indent=2), "```", "",
              "Regenerate and print this file with `python run_research.py report` in the research environment. Training commands also regenerate it after completion."]
    content = "\n".join(lines) + "\n"
    (ROOT / "METRICS.md").write_text(content, encoding="utf-8")
    return content


def paired_comparison(left, right, samples=1000):
    if [row["group_id"] for row in left] != [row["group_id"] for row in right]:
        raise ValueError("Pairwise comparison requires identical test examples/order")
    if [row["true_label"] for row in left] != [row["true_label"] for row in right]:
        raise ValueError("Mismatched ground truth")
    y = np.array([LABEL2ID[row["true_label"]] for row in left])
    a = np.array([LABEL2ID[row["predicted_label"]] for row in left])
    b = np.array([LABEL2ID[row["predicted_label"]] for row in right])
    rng = np.random.default_rng(42)
    groups = [np.flatnonzero(y == label) for label in range(3)]
    score = lambda target, pred: f1_score(target, pred, labels=[0, 1, 2], average="weighted", zero_division=0)
    deltas = []
    for _ in range(samples):
        ix = np.concatenate([rng.choice(group, len(group), replace=True) for group in groups if len(group)])
        deltas.append(float(score(y[ix], a[ix]) - score(y[ix], b[ix])))
    return {"weighted_f1_difference_left_minus_right": float(score(y, a) - score(y, b)),
            "paired_bootstrap_95_percent_interval": np.quantile(deltas, [0.025, 0.975]).tolist(),
            "note": "Conditional test-example uncertainty for these fitted runs; no seed-level significance claim."}


def report(config):
    root = path(config["output_dir"])
    runs = []
    for file in sorted(root.glob("*/seed_*/complete.json")):
        value = read_json(file)
        runs.append((file.parent, value))
    if not runs:
        raise ValueError("No completed experiments to report")
    fingerprints = [run[1]["dataset_sha256"] for run in runs]
    if any(item != fingerprints[0] for item in fingerprints):
        raise ValueError("Cannot compare models trained with different dataset splits")
    rows = [{"model": value["model"], "seed": value["seed"], **{key: value["test_metrics"][key] for key in FIELDS}} for _, value in runs]
    write_csv(root / "comparison.csv", rows)
    summary = []
    for model in sorted({row["model"] for row in rows}):
        selected = [row for row in rows if row["model"] == model]
        item = {"model": model, "n_runs": len(selected)}
        for key in FIELDS:
            values = [row[key] for row in selected]
            item[key + "_mean"] = float(np.mean(values))
            item[key + "_std"] = float(np.std(values, ddof=1)) if len(values) > 1 else None
        summary.append(item)
    write_json(root / "summary.json", summary)
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    figure, axis = plt.subplots(figsize=(8, 4.5))
    indices = np.arange(len(summary))
    for offset, metric, label in ((-0.18, "weighted_f1", "Weighted F1"), (0.18, "macro_f1", "Macro F1")):
        values = [row[metric + "_mean"] for row in summary]
        errors = [row[metric + "_std"] or 0 for row in summary]
        axis.bar(indices + offset, values, width=0.36, yerr=errors, capsize=4, label=label)
    axis.set_xticks(indices, [row["model"] for row in summary])
    axis.set_ylim(0, 1)
    axis.set_ylabel("F1 score (0-1)")
    axis.set_title("Custom held-out split; error bars: training-seed sample SD")
    axis.legend()
    figure.tight_layout()
    figure.savefig(root / "comparison.png", dpi=220)
    plt.close(figure)
    # A fixed seed is used for example-level pairwise comparisons; no best-test-seed selection.
    reference_runs = [(folder, value) for folder, value in runs if value["seed"] == 42]
    comparisons = {}
    for (left_folder, left), (right_folder, right) in itertools.combinations(reference_runs, 2):
        comparisons[f"{left['model']} vs {right['model']}"] = paired_comparison(
            read_csv(left_folder / "test_predictions.csv"), read_csv(right_folder / "test_predictions.csv"), config["bootstrap_samples"])
    write_json(root / "paired_comparisons.json", comparisons)
    headers = ["Model", "Seed", "Accuracy", "Weighted P", "Weighted R", "Weighted F1", "Macro F1"]
    lines = ["# Measured sentiment classification results", "",
             "These are measured results on a custom deduplicated split of the downloaded SentiMix train/development files.",
             "They are not a reproduction of the exact Hinglish-24k corpus, paper split, or official SentiMix test benchmark.", "",
             "| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    for row in rows:
        lines.append("| " + " | ".join([row["model"], str(row["seed"])] + [f"{row[key]:.4f}" for key in
                     ("accuracy", "weighted_precision", "weighted_recall", "weighted_f1", "macro_f1")]) + " |")
    lines += ["", "## Reporting limits", "",
              "Only completed runs are included. A single transformer seed is preliminary; run additional seeds on the same frozen split before drawing conclusions.",
              "Bootstrap intervals capture test-example uncertainty, not training-seed or dataset-split variability.",
              "Model selection uses validation weighted F1. The test set is evaluated after selection, and must not guide further tuning.",
              "No identical normalized texts or tweet IDs cross splits; author/topic/near-duplicate independence is not guaranteed.",
              "Do not claim a novel method, publication readiness, state-of-the-art performance, or significance without additional evidence.", "",
              "Per-run directories contain confusion matrices (CSV/PNG), per-class metrics, predictions, errors, confidence intervals, configurations, and environment metadata."]
    (root / "results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    # Publication-friendly table; escape identifiers and keep metrics on a 0-1 scale.
    latex = [r"\begin{tabular}{lrrrrr}", r"\hline", r"Model & Seed & Accuracy & Precision$_w$ & Recall$_w$ & F1$_w$ \\", r"\hline"]
    for row in rows:
        latex.append(row["model"].replace("_", r"\_") + " & " + str(row["seed"]) + " & " + " & ".join(
            f"{row[key]:.4f}" for key in ("accuracy", "weighted_precision", "weighted_recall", "weighted_f1")) + r" \\")
    latex += [r"\hline", r"\end{tabular}"]
    (root / "comparison.tex").write_text("\n".join(latex) + "\n", encoding="utf-8")
    print(write_metrics_markdown(config, runs, summary, comparisons), flush=True)
