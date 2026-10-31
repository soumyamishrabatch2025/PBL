import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from sentiment_research.data import assert_disjoint, clean_rows, normalize, parse_conll, prepare
from sentiment_research.common import load_splits, read_csv
from sentiment_research.evaluation import metrics
from sentiment_research.report import paired_comparison


class DataTests(unittest.TestCase):
    def test_preserves_negation_emoji_and_hashtag_words(self):
        text = normalize("@ user movie achhi nahi hai # boring 😢 https://example.com")
        self.assertIn("nahi", text)
        self.assertIn("boring", text)
        self.assertIn("EMOJI_", text)
        self.assertNotIn("example.com", text)

    def test_conflicting_labels_are_removed_not_arbitrarily_resolved(self):
        rows = [{"tweet_id": str(i), "raw_text": text, "label": label, "source_file": "fixture"}
                for i, (text, label) in enumerate([("same", "positive"), ("SAME", "negative"),
                                                 ("great", "positive"), ("great", "positive")])]
        clean, rejected, audit = clean_rows(rows)
        self.assertEqual(len(clean), 1)
        self.assertEqual(len(rejected), 2)
        self.assertEqual(audit["duplicate_rows_removed"], 1)

    def test_id_overlap_is_detected_even_with_different_text(self):
        with self.assertRaises(ValueError):
            assert_disjoint({"train": [{"tweet_id": "1", "group_id": "a"}],
                             "test": [{"tweet_id": "1", "group_id": "b"}]})

    def test_normalized_text_overlap_is_detected(self):
        with self.assertRaises(ValueError):
            assert_disjoint({"train": [{"tweet_id": "1", "group_id": "a"}],
                             "test": [{"tweet_id": "2", "group_id": "a"}]})

    def test_preparation_reproducibility_and_tamper_detection(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1] / "tmp") as temp:
            folder = Path(temp)
            for name in ("train_14k_split_conll.txt", "dev_3k_split_conll.txt"):
                lines = []
                for label in ("positive", "negative", "neutral"):
                    for i in range(20):
                        lines += [f"meta\t{name}-{label}-{i}\t{label}", f"{name}{label}{i}\tEng", ""]
                (folder / name).write_text("\n".join(lines), encoding="utf-8")
            config = {"data_dir": str(folder), "prepared_dir": str(folder / "one"), "lowercase": False,
                      "test_fraction": 0.1, "validation_fraction": 0.1, "split_seed": 42}
            first = prepare(config)
            splits, _ = load_splits(config)
            assert_disjoint(splits)
            config["prepared_dir"] = str(folder / "two")
            second = prepare(config)
            self.assertEqual(first["split_sha256"], second["split_sha256"])
            (folder / "two/train.csv").write_text("tampered", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_splits(config)

    def test_malformed_raw_labels_fail_loudly(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1] / "tmp") as temp:
            file = Path(temp) / "bad.txt"
            file.write_text("meta\t123\tSafe\nhello\tEng\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                parse_conll(file)


class MetricTests(unittest.TestCase):
    def test_known_multiclass_metrics(self):
        result = metrics([0, 0, 1, 1, 2, 2], [0, 1, 1, 1, 2, 0])
        self.assertAlmostEqual(result["accuracy"], 4 / 6)
        self.assertAlmostEqual(result["weighted_recall"], result["accuracy"])
        self.assertAlmostEqual(result["macro_f1"], (0.5 + 0.8 + 2 / 3) / 3)

    def test_pairwise_comparison_rejects_different_examples(self):
        a = [{"group_id": "a", "true_label": "positive", "predicted_label": "positive"}]
        b = [{**a[0], "group_id": "b"}]
        with self.assertRaises(ValueError):
            paired_comparison(a, b, samples=10)


if __name__ == "__main__":
    unittest.main()
