import csv
import hashlib
import importlib.metadata
import json
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / "tmp" / "matplotlib"))


def path(value):
    p = Path(value)
    return p if p.is_absolute() else ROOT / p


def sha256(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


def write_json(file, value):
    file = Path(file)
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False), encoding="utf-8")


def read_json(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


def write_csv(file, rows, fields=None):
    rows = list(rows)
    file = Path(file)
    file.parent.mkdir(parents=True, exist_ok=True)
    fields = fields or (list(rows[0]) if rows else [])
    with file.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(file):
    with Path(file).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def environment():
    packages = {}
    for package in ("numpy", "scikit-learn", "torch", "transformers", "emoji", "matplotlib"):
        try:
            packages[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            packages[package] = None
    return {"timestamp_utc": datetime.now(timezone.utc).isoformat(), "python": sys.version,
            "platform": platform.platform(), "packages": packages}


def evaluation_splits(config):
    splits = config.get("evaluation_splits", ["validation", "test"])
    if splits not in (["validation"], ["validation", "test"]):
        raise ValueError("evaluation_splits must be ['validation'] or ['validation', 'test']")
    return splits


def load_splits(config, required_splits=None):
    folder = path(config["prepared_dir"])
    audit = read_json(folder / "audit.json")
    if audit["lowercase"] != config.get("lowercase", False) or audit["split_seed"] != config["split_seed"]:
        raise ValueError("Configuration preprocessing/split seed does not match the frozen dataset")
    result = {}
    for split in required_splits or ("train", "validation", "test"):
        file = folder / f"{split}.csv"
        if sha256(file) != audit["split_sha256"][split]:
            raise ValueError(f"Prepared {split} changed; restore the recorded split or prepare a new experiment.")
        result[split] = read_csv(file)
    return result, audit


def new_run(config, name, seed):
    folder = path(config["output_dir"]) / name / f"seed_{seed}"
    if folder.exists() and any(folder.iterdir()):
        raise FileExistsError(f"Run already exists: {folder}. Use a new output_dir to avoid overwriting research results.")
    folder.mkdir(parents=True, exist_ok=True)
    write_json(folder / "config.json", config)
    write_json(folder / "environment.json", environment())
    return folder
