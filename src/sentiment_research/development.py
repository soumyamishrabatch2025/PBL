"""Validation-only development, preflight checks, and blinded review materials."""
import json
import random
import sys
from collections import Counter
from pathlib import Path

import numpy as np

from . import LABELS
from .common import ROOT, evaluation_splits, load_splits, path, read_csv, read_json, write_csv, write_json

MARKER = "<!-- DEVELOPMENT_RESULTS_START -->"


def stop_if_requested(config):
    """Honor a user stop request after a completed run, including an already-running CLI."""
    if len(sys.argv) < 2 or sys.argv[1] not in ("train", "all"):
        return
    root = path(config["output_dir"])
    control = root / "training_control.json"
    if not control.exists():
        return
    request = read_json(control)
    model, seed = request.get("model"), request.get("stop_after_seed")
    if model not in ("hingbert", "hingbert_focal", "hingroberta", "hingroberta_focal", "muril", "mbert", "svm", "svm_word_char", "naive_bayes") or not isinstance(seed, int):
        raise ValueError("Invalid run-boundary stop request")
    # Restrict a model-specific request to a command that actually trains that model.
    if "--models" in sys.argv and model not in sys.argv:
        return
    if (root / model / f"seed_{seed}" / "complete.json").exists():
        write_json(root / "stop_acknowledgement.json", {"status": "stopped_after_requested_run",
                   "model": model, "completed_seed": seed, "reason": request.get("reason"),
                   "remaining_requested_seeds_started": False})
        print(f"User stop request honored: {model} seed {seed} completed; no later seeds will start.", flush=True)
        raise SystemExit(0)


def preflight(config):
    """Validate the source/tokenizer/hardware without loading or training weights."""
    import torch
    from safetensors import safe_open
    from transformers import AutoConfig, AutoTokenizer
    from .transformer import resolve_model

    expected_models = {
        "hingbert": "l3cube-pune/hing-bert",
        "hingbert_focal": "l3cube-pune/hing-bert",
        "hingroberta": "l3cube-pune/hing-roberta",
        "hingroberta_focal": "l3cube-pune/hing-roberta",
        "muril": "google/muril-base-cased",
    }
    run_name = config["transformer"].get("run_name", "hingbert")
    if run_name in expected_models:
        if config["transformer"]["model_name"] != expected_models[run_name]:
            raise ValueError(f"Preflight requires the fresh {expected_models[run_name]} pretrained checkpoint")
    elif config["transformer"]["model_name"] != "l3cube-pune/hing-bert":
        raise ValueError("This preflight requires the fresh l3cube-pune/hing-bert pretrained checkpoint")
    if evaluation_splits(config) != ["validation"]:
        raise ValueError("Development must evaluate validation only")
    splits, audit = load_splits(config, ["train", "validation"])
    source = resolve_model(config["transformer"])
    architecture = AutoConfig.from_pretrained(source, local_files_only=True)
    if any("SequenceClassification" in name for name in architecture.architectures or []):
        raise ValueError("Source is an existing classifier, not a fresh pretrained base")
    tokenizer = AutoTokenizer.from_pretrained(source, local_files_only=True)
    tokenizer([row["text"] for row in splits["train"][:3]], truncation=True,
              max_length=config["transformer"]["max_length"])
    weights_st = Path(source) / "model.safetensors"
    weights_bin = Path(source) / "pytorch_model.bin"
    if weights_st.exists():
        with safe_open(weights_st, framework="pt", device="cpu") as handle:
            keys = list(handle.keys())
    elif weights_bin.exists():
        state = torch.load(weights_bin, map_location="cpu", weights_only=True)
        keys = list(state.keys())
    else:
        keys = []
    if any(key.startswith("classifier.") for key in keys):
        raise ValueError("Unexpected pretrained classification head")
    gpu = torch.cuda.get_device_properties(0) if torch.cuda.is_available() else None
    result = {"model": config["transformer"]["model_name"], "run_name": run_name, "source": source,
              "snapshot_commit": Path(source).name, "source_architectures": architecture.architectures,
              "tokenizer_check": "passed", "fresh_three_class_head": True,
              "optimizer_steps_executed": 0, "training_started": False,
              "train_rows": len(splits["train"]), "validation_rows": len(splits["validation"]),
              "test_loaded": False, "cuda_available": gpu is not None,
              "gpu": gpu.name if gpu else None,
              "gpu_vram_gb": gpu.total_memory / 2**30 if gpu else None,
              "gpu_free_vram_gb": torch.cuda.mem_get_info()[0] / 2**30 if gpu else None,
              "dataset_sha256": audit["split_sha256"]}
    write_json(path(config["output_dir"]) / f"preflight_{run_name}.json", result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def audit_packet(config):
    splits, audit = load_splits(config, ["validation"])
    old_run = path(config["baseline_output_dir"]) / "mbert/seed_42"
    if read_json(old_run / "complete.json")["dataset_sha256"] != audit["split_sha256"]:
        raise ValueError("Baseline predictions use a different frozen dataset")
    predictions = read_csv(old_run / "validation_predictions.csv")
    if [row["group_id"] for row in predictions] != [row["group_id"] for row in splits["validation"]]:
        raise ValueError("Validation examples/order do not match baseline predictions")
    folder = path(config["output_dir"]) / "neutral_review"
    if folder.exists() and any(folder.iterdir()):
        raise FileExistsError("Review packet already exists; preserve annotator work")
    rng = random.Random(42)
    strata = {
        "neutral_boundary_error": [row for row in predictions if row["true_label"] != row["predicted_label"]
                                   and "neutral" in (row["true_label"], row["predicted_label"])],
        "polarity_error": [row for row in predictions if row["true_label"] != row["predicted_label"]
                           and "neutral" not in (row["true_label"], row["predicted_label"])],
        "correct_control": [row for row in predictions if row["true_label"] == row["predicted_label"]],
    }
    selected = []
    for name, count in (("neutral_boundary_error", 100), ("polarity_error", 50), ("correct_control", 50)):
        selected += [(name, row) for row in rng.sample(strata[name], min(count, len(strata[name])))]
    if len(selected) < 200:
        used = {row["group_id"] for _, row in selected}
        remaining = [(name, row) for name, rows in strata.items() for row in rows if row["group_id"] not in used]
        selected += rng.sample(remaining, 200 - len(selected))
    rng.shuffle(selected)
    key, blinded = [], []
    for index, (stratum, row) in enumerate(selected, 1):
        case_id = f"VR{index:03d}"
        blinded.append({"case_id": case_id, "text": row["text"], "review_label": "", "confidence": "",
                        "reason_tags": "", "needs_context": "", "notes": ""})
        key.append({"case_id": case_id, "tweet_id": row["tweet_id"], "group_id": row["group_id"],
                    "original_label": row["true_label"], "model_prediction": row["predicted_label"], "stratum": stratum})
    write_csv(folder / "reviewer_A.csv", blinded)
    write_csv(folder / "reviewer_B.csv", blinded)
    write_csv(folder / "answer_key.csv", key)
    write_csv(folder / "adjudication.csv", [{"case_id": row["case_id"], "final_label": "", "rationale": ""} for row in blinded])
    write_json(folder / "manifest.json", {"examples": len(blinded), "sampling_seed": 42, "source_split": "validation",
               "stratum_counts": dict(Counter(name for name, _ in selected)), "dataset_sha256": audit["split_sha256"],
               "annotation_status": "Pending two independent human reviewers; no labels have been changed."})
    (folder / "README.md").write_text(
        "# Neutral boundary review\n\n200 validation examples selected using the original mBERT validation predictions. "
        "The packet deliberately oversamples mistakes; its label-disagreement rate is not an unbiased estimate of dataset label noise.\n\n"
        "Distribute only reviewer_A.csv and reviewer_B.csv to their assigned independent reviewers, not the whole folder. "
        "Hide answer_key.csv, INITIAL_NOTES.md and the sampling manifest until both finish. "
        "Use positive, negative, neutral, or uncertain. Record confidence and relevant tags (negation, sarcasm, mixed sentiment, "
        "spelling/slang, missing context, possible labeling ambiguity). Do not force uncertain examples into neutral. "
        "Neutral means no clear positive/negative attitude; mixed polarity is not automatically neutral.\n\n"
        "After independent annotation, calculate agreement and adjudicate disagreements in adjudication.csv. "
        "No corrected gold labels or agreement scores are claimed yet. No test examples were used. "
        "Any label changes require a separately versioned experiment; do not silently edit the frozen splits.\n", encoding="utf-8")
    print("Prepared 200-example blinded validation review packet:", folder, flush=True)


def development_report(config):
    if evaluation_splits(config) != ["validation"]:
        raise ValueError("Development reporting requires validation-only runs")
    root = path(config["output_dir"])
    runs = [(file.parent, read_json(file)) for file in sorted(root.glob("*/seed_*/complete.json"))]
    audit = read_json(path(config["prepared_dir"]) / "audit.json")
    for folder, value in runs:
        if value.get("evaluation_splits") != ["validation"] or "test_metrics" in value:
            raise ValueError(f"Unexpected test evaluation in development run {folder}")
        if value["dataset_sha256"] != audit["split_sha256"]:
            raise ValueError("Cannot compare development results across different splits")
    lines = ["## Development experiments: validation only", "",
             "Experiment: `" + config["experiment"] + "`. These scores are used for model selection and are NOT fresh test results.",
             "The original test results above remain historical baseline measurements. Final generalization needs an untouched, deduplicated evaluation set.", "",
             "### Validation comparison", "",
             "| Model | Run group | Seed | Accuracy | Weighted precision | Weighted recall | Weighted F1 | Macro F1 |", "|---|---|---:|---:|---:|---:|---:|---:|"]
    comparison = []
    baseline_root = path(config["baseline_output_dir"])
    for model in ("naive_bayes", "svm", "mbert"):
        folder = baseline_root / model / "seed_42"
        if (folder / "validation_metrics.json").exists():
            if read_json(folder / "complete.json")["dataset_sha256"] != audit["split_sha256"]:
                raise ValueError("Historical validation baseline uses a different dataset")
            comparison.append({"model": model, "run_group": "historical baseline", "seed": 42, **read_json(folder / "validation_metrics.json")})
    for folder, value in runs:
        comparison.append({"model": value["model"], "run_group": "phase 2", "seed": value["seed"], **value["evaluation_metrics"]["validation"]})
    fields = ("accuracy", "weighted_precision", "weighted_recall", "weighted_f1", "macro_f1")
    for row in comparison:
        lines.append("| " + " | ".join([row["model"], row["run_group"], str(row["seed"])] + [f"{row[key]:.10f}" for key in fields]) + " |")
    write_csv(root / "validation_comparison.csv", comparison)
    for folder, value in runs:
        lines += ["", f"### {value['model']} — seed {value['seed']}", "", "#### Validation metrics", "",
                  "| Metric | Value |", "|---|---:|"]
        for key, number in value["evaluation_metrics"]["validation"].items():
            lines.append(f"| {key} | {number:.10f} |" if isinstance(number, float) else f"| {key} | {number} |")
        rows = read_csv(folder / "validation_per_class.csv")
        lines += ["", "#### Validation class results", "", "| Class | Precision | Recall | F1 | Support |", "|---|---:|---:|---:|---:|"]
        for row in rows:
            lines.append("| " + " | ".join([row["label"], row["precision"], row["recall"], row["f1-score"], row["support"]]) + " |")
        lines += ["", "#### Validation confusion matrix", "", "Rows = actual; columns = predicted.", "",
                  "| Actual / predicted | Negative | Neutral | Positive |", "|---|---:|---:|---:|"]
        matrix = read_csv(folder / "validation_confusion_matrix.csv")
        for row in matrix:
            lines.append("| " + " | ".join([row["actual"]] + [row[label] for label in LABELS]) + " |")
        lines += ["", "#### Row-normalized validation confusion matrix", "",
                  "| Actual / predicted | Negative | Neutral | Positive |", "|---|---:|---:|---:|"]
        for row in matrix:
            counts = [int(row[label]) for label in LABELS]
            total = sum(counts)
            lines.append("| " + " | ".join([row["actual"]] + [f"{count/total:.10f}" if total else "0" for count in counts]) + " |")
        for title, file in (("Selection", "selection.json"), ("Inference timing", "validation_timing.json"),
                            ("Training metadata", "training_metadata.json")):
            if (folder / file).exists():
                lines += ["", f"#### {title}", "", "```json", (folder / file).read_text(encoding="utf-8"), "```"]
        seconds = value.get("training_seconds", value.get("training_seconds_including_search"))
        lines += ["", f"Training/search elapsed seconds: {seconds}."]
        if (folder / "training_history.csv").exists():
            lines += ["", "#### Epoch history", "", "```csv", (folder / "training_history.csv").read_text(encoding="utf-8"), "```"]
        relative = folder.relative_to(ROOT).as_posix()
        lines += ["", f"![{value['model']} validation confusion matrix]({relative}/validation_confusion_matrix.png)", "",
                  f"[Predictions]({relative}/validation_predictions.csv) | [Errors]({relative}/validation_errors.csv) | [Config]({relative}/config.json)", ""]
    if runs:
        lines += ["### Development training-seed variability", "",
                  "Validation scores were used for checkpoint/model selection; these are descriptive seed statistics, not unbiased final-test estimates.", "",
                  "| Model | Runs | Weighted F1 mean | Sample SD | Macro F1 mean | Sample SD |", "|---|---:|---:|---:|---:|---:|"]
        for model in sorted({value["model"] for _, value in runs}):
            scores = [value["evaluation_metrics"]["validation"] for _, value in runs if value["model"] == model]
            cells = [model, str(len(scores))]
            for key in ("weighted_f1", "macro_f1"):
                values = [row[key] for row in scores]
                cells += [f"{np.mean(values):.10f}", f"{np.std(values, ddof=1):.10f}" if len(values) > 1 else "Not available"]
            lines.append("| " + " | ".join(cells) + " |")
    for status in sorted(root.glob("*/seed_*/status.json")):
        if not (status.parent / "complete.json").exists():
            state = read_json(status)
            lines += ["", f"Pending: {status.parent.parent.name}/{status.parent.name}: {state.get('status')}, step {state.get('step', 0)}/{state.get('total_steps', 'unknown')}."]
            history_file = status.parent / "training_history.csv"
            if history_file.exists():
                lines += ["", "Interim epoch measurements (validation, not a final completed run):", "",
                          "| Epoch | Mean training loss | Validation accuracy | Validation macro F1 | Validation weighted F1 |", "|---|---:|---:|---:|---:|"]
                for row in read_csv(history_file):
                    lines.append("| " + " | ".join(row[key] for key in ("epoch", "train_loss", "validation_accuracy", "validation_macro_f1", "validation_weighted_f1")) + " |")
    pred_files = {m: root / m / "seed_42/validation_predictions.csv" for m in ("hingbert", "hingroberta", "hingroberta_focal", "muril")
                  if (root / m / "seed_42/validation_predictions.csv").exists()}
    if len(pred_files) >= 2:
        from sklearn.metrics import accuracy_score, f1_score
        from . import LABEL2ID
        preds = {}
        for m, p in pred_files.items():
            rows = read_csv(p)
            preds[m] = np.array([[float(r["p_negative"]), float(r["p_neutral"]), float(r["p_positive"])] for r in rows])
        y_true = np.array([LABEL2ID[r["true_label"]] for r in read_csv(next(iter(pred_files.values())))])

        combos = []
        if "hingbert" in preds and "hingroberta" in preds:
            combos.append(("Dual-Encoder (BERT + RoBERTa CE)", 0.5 * preds["hingbert"] + 0.5 * preds["hingroberta"]))
        if "hingbert" in preds and "hingroberta_focal" in preds:
            combos.append(("Dual-Encoder (BERT + RoBERTa Focal)", 0.5 * preds["hingbert"] + 0.5 * preds["hingroberta_focal"]))
        if "hingbert" in preds and "hingroberta_focal" in preds and "muril" in preds:
            combos.append(("Tri-Encoder (BERT + RoBERTa Focal + MuRIL)", 0.45 * preds["hingbert"] + 0.45 * preds["hingroberta_focal"] + 0.10 * preds["muril"]))
        if "hingbert" in preds and "hingroberta" in preds and "hingroberta_focal" in preds and "muril" in preds:
            combos.append(("Quad-Encoder (BERT + RoBERTa CE + Focal + MuRIL)", 0.35 * preds["hingbert"] + 0.25 * preds["hingroberta"] + 0.30 * preds["hingroberta_focal"] + 0.10 * preds["muril"]))

        lines += ["", "### Multi-model probability ensembles", "",
                  "Calibrated soft-voting combining prediction probability distributions across architectures on the frozen validation set (1,700 examples):", "",
                  "| Ensemble Strategy | Accuracy | Macro F1 | Weighted F1 | Negative F1 | Neutral F1 | Positive F1 |",
                  "|---|---:|---:|---:|---:|---:|---:|"]
        for name, prob in combos:
            yp = prob.argmax(1)
            acc = accuracy_score(y_true, yp)
            mf1 = f1_score(y_true, yp, average="macro")
            wf1 = f1_score(y_true, yp, average="weighted")
            cf1 = f1_score(y_true, yp, average=None)
            lines.append(f"| {name} | {acc:.10f} | {mf1:.10f} | {wf1:.10f} | {cf1[0]:.4f} | {cf1[1]:.4f} | {cf1[2]:.4f} |")

    lines += ["", "### Neutral review", "",
              "The blinded 200-example validation packet is under `" + (root / "neutral_review").relative_to(ROOT).as_posix() + "`. Human annotation/agreement remain pending; no gold labels were changed.", "",
              "No new test metrics or selection-set confidence intervals are claimed for these development runs."]
    content = "\n".join(lines) + "\n"
    (root / "development_metrics.md").write_text(content, encoding="utf-8")
    target = ROOT / "METRICS.md"
    existing = target.read_text(encoding="utf-8") if target.exists() else "# All model metrics\n"
    target.write_text(existing.split(MARKER)[0].rstrip() + "\n\n" + MARKER + "\n\n" + content, encoding="utf-8")
    print(content, flush=True)
    stop_if_requested(config)
    return comparison
