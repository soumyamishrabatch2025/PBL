"""Full transformer fine-tuning with validation-only checkpoint selection."""
import math
import gc
import os
import random
import time
from pathlib import Path

import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset
from transformers import (AutoModelForSequenceClassification, AutoTokenizer,
                          DataCollatorWithPadding, get_linear_schedule_with_warmup)

from . import LABEL2ID, LABELS
from .common import ROOT, evaluation_splits, load_splits, new_run, write_csv, write_json
from .evaluation import evaluate, metrics


class EncodedDataset(Dataset):
    def __init__(self, rows, tokenizer, max_length):
        self.tokens = tokenizer([row["text"] for row in rows], truncation=True, max_length=max_length)
        self.labels = [int(row["label_id"]) for row in rows]
        self.truncated = sum(len(ids) == max_length for ids in self.tokens["input_ids"])

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, index):
        return {**{key: value[index] for key, value in self.tokens.items()}, "labels": self.labels[index]}


def resolve_model(settings):
    """Prefer an existing cached pretrained snapshot; otherwise download locally."""
    from huggingface_hub import snapshot_download
    source = settings["model_name"]
    if Path(source).is_dir():
        return str(Path(source).resolve())
    try:
        return snapshot_download(source, revision=settings.get("revision", "main"), local_files_only=True)
    except OSError:
        return snapshot_download(source, revision=settings.get("revision", "main"),
                                 cache_dir=ROOT / ".hf-cache", allow_patterns=["*.json", "*.txt", "*.safetensors"])


def train_transformer(config, seed=42, model_name="mbert"):
    settings = config["transformer"]
    if model_name != settings.get("run_name", "mbert"):
        raise ValueError("Transformer run name does not match the selected pretrained model configuration")
    if model_name == "hingbert" and settings["model_name"] != "l3cube-pune/hing-bert":
        raise ValueError("Fresh HingBERT runs require the pretrained l3cube-pune/hing-bert checkpoint")
    if settings["epochs"] < 1 or settings["batch_size"] < 1 or settings["gradient_accumulation_steps"] < 1:
        raise ValueError("Epochs, batch size, and accumulation steps must be positive")
    evaluated = evaluation_splits(config)
    splits, audit = load_splits(config, ["train", *evaluated])
    # Download/tokenizer failures do not reserve a run directory.
    source = resolve_model(settings)
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.set_num_threads(min(4, os.cpu_count() or 1))
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = AutoTokenizer.from_pretrained(source, local_files_only=True)
    datasets = {name: EncodedDataset(rows, tokenizer, settings["max_length"]) for name, rows in splits.items()}
    collator = DataCollatorWithPadding(tokenizer, pad_to_multiple_of=8 if device.type == "cuda" else None)
    generator = torch.Generator().manual_seed(seed)
    loaders = {name: DataLoader(data, batch_size=settings["batch_size"] if name == "train" else settings["eval_batch_size"],
                                shuffle=name == "train", collate_fn=collator, num_workers=settings["num_workers"],
                                pin_memory=device.type == "cuda", generator=generator if name == "train" else None)
               for name, data in datasets.items()}
    model = AutoModelForSequenceClassification.from_pretrained(source, num_labels=3,
                                                               id2label=dict(enumerate(LABELS)), label2id=LABEL2ID,
                                                               local_files_only=True)
    model.to(device)
    if settings["gradient_checkpointing"]:
        model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
    use_amp = bool(settings["mixed_precision"] and device.type == "cuda")
    # Adam moments consume less peak memory with foreach disabled on a 6 GB GPU.
    decay, no_decay = [], []
    for name, parameter in model.named_parameters():
        (no_decay if "bias" in name or "LayerNorm.weight" in name else decay).append(parameter)
    optimizer = torch.optim.AdamW([{"params": decay, "weight_decay": settings["weight_decay"]},
                                   {"params": no_decay, "weight_decay": 0.0}],
                                  lr=settings["learning_rate"], foreach=False)
    accumulation = settings["gradient_accumulation_steps"]
    steps_per_epoch = math.ceil(len(loaders["train"]) / accumulation)
    total_steps = settings["epochs"] * steps_per_epoch
    scheduler = get_linear_schedule_with_warmup(optimizer, settings["warmup_steps"], total_steps)
    scaler = torch.amp.GradScaler("cuda", enabled=use_amp)
    folder = new_run(config, model_name, seed)
    write_json(folder / "data_audit.json", audit)
    write_json(folder / "status.json", {"status": "training", "step": 0, "total_steps": total_steps})
    write_json(folder / "training_metadata.json", {"pretrained_model": settings["model_name"],
               "resolved_snapshot": source, "snapshot_commit": Path(source).name,
               "device": str(device), "gpu": torch.cuda.get_device_name(0) if device.type == "cuda" else None,
               "effective_batch_size": settings["batch_size"] * accumulation, "mixed_precision": use_amp,
               "evaluation_splits": evaluated,
               "optimizer_steps": total_steps, "parameter_count": sum(p.numel() for p in model.parameters()),
               "length_at_limit_counts": {name: data.truncated for name, data in datasets.items()},
               "determinism": "Fixed RNG seeds; cuDNN deterministic; exact cross-device reproducibility is not guaranteed."})

    def predict(loader):
        model.eval()
        probabilities = []
        start = time.perf_counter()
        with torch.inference_mode():
            for batch in loader:
                inputs = {key: value.to(device) for key, value in batch.items() if key != "labels"}
                with torch.autocast(device_type=device.type, dtype=torch.float16, enabled=use_amp):
                    logits = model(**inputs).logits
                probabilities.append(logits.float().softmax(-1).cpu().numpy())
        return np.concatenate(probabilities), time.perf_counter() - start

    best_score, best_epoch, global_step = -1, None, 0
    history = []
    start = time.perf_counter()
    try:
        for epoch in range(1, settings["epochs"] + 1):
            model.train()
            optimizer.zero_grad(set_to_none=True)
            loss_sum, example_count = 0.0, 0
            for batch_index, batch in enumerate(loaders["train"]):
                batch = {key: value.to(device, non_blocking=True) for key, value in batch.items()}
                batch_size = batch["labels"].shape[0]
                # Correct normalization for a final partial accumulation window/batch.
                window_start = (batch_index // accumulation) * accumulation * settings["batch_size"]
                window_examples = min(accumulation * settings["batch_size"], len(datasets["train"]) - window_start)
                with torch.autocast(device_type=device.type, dtype=torch.float16, enabled=use_amp):
                    raw_loss = model(**batch).loss
                    loss = raw_loss * batch_size / window_examples
                scaler.scale(loss).backward()
                loss_sum += float(raw_loss.detach()) * batch_size
                example_count += batch_size
                if (batch_index + 1) % accumulation == 0 or batch_index + 1 == len(loaders["train"]):
                    scaler.unscale_(optimizer)
                    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                    old_scale = scaler.get_scale()
                    scaler.step(optimizer)
                    scaler.update()
                    # Do not advance the LR on a skipped overflow step.
                    if scaler.get_scale() >= old_scale:
                        scheduler.step()
                    optimizer.zero_grad(set_to_none=True)
                    global_step += 1
                    if global_step % settings["log_every_steps"] == 0:
                        status = {"status": "training", "epoch": epoch, "step": global_step,
                                  "total_steps": total_steps, "mean_train_loss": loss_sum / example_count,
                                  "elapsed_seconds": time.perf_counter() - start}
                        write_json(folder / "status.json", status)
                        print(status, flush=True)
            probabilities, _ = predict(loaders["validation"])
            validation = metrics([int(row["label_id"]) for row in splits["validation"]], probabilities.argmax(1), probabilities)
            score = validation[config["selection_metric"]]
            history.append({"epoch": epoch, "train_loss": loss_sum / example_count,
                            "validation_weighted_f1": validation["weighted_f1"],
                            "validation_macro_f1": validation["macro_f1"], "validation_accuracy": validation["accuracy"],
                            "elapsed_seconds": time.perf_counter() - start})
            write_csv(folder / "training_history.csv", history)
            if score > best_score:
                best_score, best_epoch = score, epoch
                model.save_pretrained(folder / "checkpoint", safe_serialization=True)
                tokenizer.save_pretrained(folder / "checkpoint")
            write_json(folder / "selection.json", {"selection_split": "validation", "metric": config["selection_metric"],
                                                   "best_epoch": best_epoch, "best_score": best_score})
            print("Epoch completed:", history[-1], flush=True)
            if device.type == "cuda":
                torch.cuda.empty_cache()
        training_seconds = time.perf_counter() - start
        # Release optimizer memory before loading/evaluating the selected checkpoint.
        del optimizer, scheduler, model, decay, no_decay, parameter, raw_loss, loss, batch
        if device.type == "cuda":
            torch.cuda.empty_cache()
        model = AutoModelForSequenceClassification.from_pretrained(folder / "checkpoint", local_files_only=True).to(device)
        results = {}
        for split in evaluated:
            probabilities, seconds = predict(loaders[split])
            result = evaluate(folder, splits[split], probabilities.argmax(1), probabilities, split,
                              config["bootstrap_samples"] if split == "test" else 0)
            results[split] = result
            write_json(folder / f"{split}_timing.json", {"inference_seconds": seconds,
                                                       "examples_per_second": len(splits[split]) / seconds})
        completion = {"model": model_name, "seed": seed, "best_epoch": best_epoch,
                      "training_seconds": training_seconds, "evaluation_metrics": results,
                      "evaluation_splits": evaluated, "dataset_sha256": audit["split_sha256"]}
        if "test" in results:
            completion["test_metrics"] = results["test"]
        write_json(folder / "complete.json", completion)
        write_json(folder / "status.json", {"status": "complete", "evaluation_metrics": results})
        print(model_name, results, flush=True)
        del model
        gc.collect()
        if device.type == "cuda":
            torch.cuda.empty_cache()
    except BaseException as error:
        write_json(folder / "status.json", {"status": "failed", "error": str(error), "step": global_step})
        raise
