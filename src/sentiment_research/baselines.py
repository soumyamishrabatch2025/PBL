import time

import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

from .common import load_splits, new_run, write_json
from .evaluation import evaluate, metrics


def train_baseline(config, model_name, seed=42):
    splits, audit = load_splits(config)
    folder = new_run(config, model_name, seed)
    write_json(folder / "data_audit.json", audit)
    settings = config["baseline"]
    grid = settings["nb_alpha"] if model_name == "naive_bayes" else settings["svm_c"]
    trials, best, best_value, best_score = [], None, None, -1
    start = time.perf_counter()
    for value in grid:
        classifier = MultinomialNB(alpha=value) if model_name == "naive_bayes" else LinearSVC(C=value, random_state=seed, max_iter=10000)
        model = Pipeline([("tfidf", TfidfVectorizer(ngram_range=tuple(settings["ngram_range"]),
                                                   min_df=settings["min_df"], max_features=settings["max_features"],
                                                   sublinear_tf=True, lowercase=True)), ("classifier", classifier)])
        model.fit([row["text"] for row in splits["train"]], [int(row["label_id"]) for row in splits["train"]])
        predicted = model.predict([row["text"] for row in splits["validation"]])
        score = metrics([int(row["label_id"]) for row in splits["validation"]], predicted)[config["selection_metric"]]
        trials.append({"parameter": value, "validation_selection_score": score})
        if score > best_score:
            best, best_value, best_score = model, value, score
    training_seconds = time.perf_counter() - start
    joblib.dump(best, folder / "model.joblib")
    write_json(folder / "selection.json", {"selection_split": "validation", "metric": config["selection_metric"],
                                           "best_parameter": best_value, "trials": trials})
    for split in ("validation", "test"):
        texts = [row["text"] for row in splits[split]]
        start = time.perf_counter()
        predicted = best.predict(texts)
        probabilities = best.predict_proba(texts) if model_name == "naive_bayes" else None
        seconds = time.perf_counter() - start
        result = evaluate(folder, splits[split], predicted, probabilities, split,
                          config["bootstrap_samples"] if split == "test" else 0)
        write_json(folder / f"{split}_timing.json", {"inference_seconds": seconds, "examples_per_second": len(texts) / seconds})
    write_json(folder / "complete.json", {"model": model_name, "seed": seed, "training_seconds_including_search": training_seconds,
                                          "test_metrics": result, "dataset_sha256": audit["split_sha256"]})
    print(model_name, result, flush=True)
