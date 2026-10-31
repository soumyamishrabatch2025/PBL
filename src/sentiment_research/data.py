"""Parse raw CoNLL, remove label conflicts and duplicates, freeze a custom split."""
import hashlib
import html
import re
import unicodedata
from collections import Counter, defaultdict

import emoji
from sklearn.model_selection import train_test_split

from . import LABEL2ID
from .common import path, sha256, write_csv, write_json


def normalize(text, lowercase=False):
    text = unicodedata.normalize("NFKC", html.unescape(text))
    text = re.sub(r"https?\s*:\s*/\s*/\s*\S+|https?://\S+|www\.\S+", " URL ", text, flags=re.I)
    text = re.sub(r"@\s*[\w_]+", " USER ", text)
    text = re.sub(r"#\s*(\w+)", r"\1", text)
    text = emoji.demojize(text, language="en", delimiters=(" EMOJI_", " "))
    text = " ".join(text.split()).strip()
    return text.lower() if lowercase else text


def parse_conll(file):
    rows, current, tokens = [], None, []

    def flush():
        if current is not None:
            if not tokens:
                raise ValueError(f"Empty tweet {current['tweet_id']} in {file}")
            rows.append({**current, "raw_text": " ".join(tokens), "source_file": file.name})

    with file.open(encoding="utf-8-sig") as stream:
        for number, line in enumerate(stream, 1):
            line = line.rstrip("\r\n")
            if not line.strip():
                continue
            fields = line.split("\t")
            if fields[0] == "meta":
                flush()
                if len(fields) != 3 or fields[2].lower() not in LABEL2ID:
                    raise ValueError(f"Invalid metadata at {file}:{number}: {line!r}")
                current = {"tweet_id": fields[1], "label": fields[2].lower()}
                tokens = []
            else:
                if current is None or len(fields) != 2:
                    raise ValueError(f"Invalid token row at {file}:{number}: {line!r}")
                tokens.append(fields[0])
    flush()
    return rows


def clean_rows(rows, lowercase=False):
    id_labels = defaultdict(set)
    for row in rows:
        id_labels[row["tweet_id"]].add(row["label"])
    conflicting_ids = {key for key, labels in id_labels.items() if len(labels) > 1}
    groups = defaultdict(list)
    rejected = []
    for row in rows:
        text = normalize(row["raw_text"], lowercase)
        if row["tweet_id"] in conflicting_ids or not any(c.isalpha() for c in text):
            rejected.append({**row, "reason": "conflicting_id" if row["tweet_id"] in conflicting_ids else "empty_text"})
            continue
        key = text.casefold()
        groups[key].append({**row, "text": text, "label_id": LABEL2ID[row["label"]],
                            "group_id": hashlib.sha256(key.encode("utf-8")).hexdigest()})
    clean, duplicate_count, conflict_groups = [], 0, 0
    seen_ids = set()
    for key in sorted(groups):
        group = sorted(groups[key], key=lambda row: (row["tweet_id"], row["source_file"]))
        if len({row["label"] for row in group}) > 1:
            conflict_groups += 1
            rejected.extend({**row, "reason": "conflicting_text"} for row in group)
            continue
        # Same ID with different surface forms must still occur only once.
        eligible = [row for row in group if row["tweet_id"] not in seen_ids]
        if eligible:
            clean.append(eligible[0])
        seen_ids.update(row["tweet_id"] for row in group)
        duplicate_count += len(group) - bool(eligible)
    return clean, rejected, {"duplicate_rows_removed": duplicate_count,
                             "conflicting_text_groups": conflict_groups,
                             "conflicting_ids": sorted(conflicting_ids)}


def assert_disjoint(splits):
    for field in ("tweet_id", "group_id"):
        sets = {name: {row[field] for row in rows} for name, rows in splits.items()}
        names = list(sets)
        for i, left in enumerate(names):
            for right in names[i + 1:]:
                if sets[left] & sets[right]:
                    raise ValueError(f"Leakage: overlapping {field} between {left} and {right}")


def prepare(config):
    folder = path(config["prepared_dir"])
    if folder.exists() and any(folder.iterdir()):
        raise FileExistsError(f"Prepared dataset already exists: {folder}; use a new prepared_dir.")
    raw_dir = path(config["data_dir"])
    files = [raw_dir / "train_14k_split_conll.txt", raw_dir / "dev_3k_split_conll.txt"]
    raw = [row for file in files for row in parse_conll(file)]
    clean, rejected, details = clean_rows(raw, config.get("lowercase", False))
    val_fraction, test_fraction = config["validation_fraction"], config["test_fraction"]
    if not (0 < val_fraction < 1 and 0 < test_fraction < 1 and val_fraction + test_fraction < 1):
        raise ValueError("Validation and test fractions must be positive and sum to less than one.")
    train_val, test = train_test_split(clean, test_size=test_fraction, random_state=config["split_seed"],
                                      stratify=[row["label"] for row in clean])
    train, validation = train_test_split(train_val, test_size=val_fraction / (1 - test_fraction),
                                         random_state=config["split_seed"], stratify=[row["label"] for row in train_val])
    splits = {"train": train, "validation": validation, "test": test}
    assert_disjoint(splits)
    folder.mkdir(parents=True, exist_ok=True)
    for name, rows in splits.items():
        write_csv(folder / f"{name}.csv", sorted(rows, key=lambda row: row["group_id"]))
    fields = ["tweet_id", "label", "raw_text", "source_file", "reason"]
    write_csv(folder / "rejected.csv", [{k: row[k] for k in fields} for row in rejected], fields)
    audit = {"protocol": "Custom stratified 80/10/10 by default; NOT the official SentiMix benchmark split or Hinglish-24k.",
             "raw_rows": len(raw), "clean_rows": len(clean), "rejected_rows": len(rejected), **details,
             "raw_sha256": {file.name: sha256(file) for file in files},
             "split_seed": config["split_seed"], "lowercase": config.get("lowercase", False),
             "split_counts": {name: {"rows": len(rows), "labels": dict(Counter(row["label"] for row in rows))}
                              for name, rows in splits.items()},
             "split_sha256": {name: sha256(folder / f"{name}.csv") for name in splits},
             "preprocessing": "NFKC, HTML unescape, URL/mention placeholders, hashtag text retained, emoji descriptions; negation and stop words retained.",
             "leakage_checks": "No identical casefolded normalized texts or tweet IDs cross splits. Near duplicates/authors/topics are not guaranteed disjoint."}
    write_json(folder / "audit.json", audit)
    print(audit, flush=True)
    return audit
