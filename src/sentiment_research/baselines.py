import time

import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.preprocessing import Normalizer
from sklearn.svm import LinearSVC

from .common import evaluation_splits, load_splits, new_run, write_json
from .evaluation import evaluate, metrics


def build_baseline(settings, model_name, value, seed=42):
    word = TfidfVectorizer(ngram_range=tuple(settings["ngram_range"]), min_df=settings["min_df"],
                           max_features=settings["max_features"], sublinear_tf=True, lowercase=True)
    if model_name == "svm_word_char":
        chars = TfidfVectorizer(analyzer="char_wb", ngram_range=tuple(settings.get("char_ngram_range", [3, 5])),
                                min_df=settings.get("char_min_df", 2),
                                max_features=settings.get("char_max_features", 100000),
                                sublinear_tf=True, lowercase=True)
        return Pipeline([("features", FeatureUnion([("word", word), ("character", chars)], n_jobs=1)),
                         ("normalize", Normalizer()),
                         ("classifier", LinearSVC(C=value, random_state=seed, max_iter=10000))])
    if model_name not in ("naive_bayes", "svm"):
        raise ValueError(f"Unsupported baseline: {model_name}")
    classifier = MultinomialNB(alpha=value) if model_name == "naive_bayes" else LinearSVC(C=value, random_state=seed, max_iter=10000)
    return Pipeline([("tfidf", word), ("classifier", classifier)])


def train_baseline(config, model_name, seed=42):
    evaluated = evaluation_splits(config)
    splits, audit = load_splits(config, ["train", *evaluated])
    folder = new_run(config, model_name, seed)
    write_json(folder / "data_audit.json", audit)
    settings = config["baseline"]
    grid = settings["nb_alpha"] if model_name == "naive_bayes" else settings["svm_c"]
    trials, best, best_value, best_score = [], None, None, -1
    start = time.perf_counter()
    for value in grid:
        model = build_baseline(settings, model_name, value, seed)
        model.fit([row["text"] for row in splits["train"]], [int(row["label_id"]) for row in splits["train"]])
        predicted = model.predict([row["text"] for row in splits["validation"]])
        score = metrics([int(row["label_id"]) for row in splits["validation"]], predicted)[config["selection_metric"]]
        trials.append({"parameter": value, "validation_selection_score": score})
        print(model_name, "C/alpha", value, "validation weighted F1", score, flush=True)
        if score > best_score:
            best, best_value, best_score = model, value, score
    training_seconds = time.perf_counter() - start
    joblib.dump(best, folder / "model.joblib")
    write_json(folder / "selection.json", {"selection_split": "validation", "metric": config["selection_metric"],
                                           "best_parameter": best_value, "trials": trials})
    results = {}
    for split in evaluated:
        texts = [row["text"] for row in splits[split]]
        start = time.perf_counter()
        predicted = best.predict(texts)
        probabilities = best.predict_proba(texts) if model_name == "naive_bayes" else None
        seconds = time.perf_counter() - start
        result = evaluate(folder, splits[split], predicted, probabilities, split,
                          config["bootstrap_samples"] if split == "test" else 0)
        results[split] = result
        write_json(folder / f"{split}_timing.json", {"inference_seconds": seconds, "examples_per_second": len(texts) / seconds})
    completion = {"model": model_name, "seed": seed, "training_seconds_including_search": training_seconds,
                  "evaluation_metrics": results, "evaluation_splits": evaluated,
                  "dataset_sha256": audit["split_sha256"]}
    if "test" in results:
        completion["test_metrics"] = results["test"]
    write_json(folder / "complete.json", completion)
    print(model_name, result, flush=True)
