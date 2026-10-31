import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from sentiment_research.baselines import build_baseline
from sentiment_research.common import evaluation_splits, load_splits, sha256, write_csv, write_json


class DevelopmentTests(unittest.TestCase):
    def test_user_stop_request_waits_for_completed_run_and_does_not_interrupt_it(self):
        from sentiment_research.development import stop_if_requested
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1] / "tmp") as temp:
            root = Path(temp)
            write_json(root / "training_control.json", {"model": "hingbert", "stop_after_seed": 42,
                                                       "reason": "Finish first seed, then review"})
            config = {"output_dir": str(root)}
            with patch.object(sys, "argv", ["run_research.py", "train", "--models", "hingbert"]):
                stop_if_requested(config)  # In-progress run is not interrupted.
                write_json(root / "hingbert/seed_42/complete.json", {"model": "hingbert", "seed": 42})
                with self.assertRaises(SystemExit) as result:
                    stop_if_requested(config)
                self.assertEqual(result.exception.code, 0)
            self.assertFalse((root / "hingbert/seed_43").exists())
            self.assertTrue((root / "stop_acknowledgement.json").exists())
            with patch.object(sys, "argv", ["run_research.py", "report"]):
                stop_if_requested(config)  # Ordinary report regeneration remains available.

    def test_transformer_identity_checks_reject_mislabeled_or_old_classifier_sources(self):
        from sentiment_research.transformer import train_transformer
        config = {"transformer": {"run_name": "hingbert", "model_name": "l3cube-pune/hing-bert"}}
        with self.assertRaisesRegex(ValueError, "run name"):
            train_transformer(config, model_name="mbert")
        config["transformer"]["model_name"] = "models/hingbert"
        with self.assertRaisesRegex(ValueError, "pretrained"):
            train_transformer(config, model_name="hingbert")

    def test_validation_mode_does_not_open_test_file(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1] / "tmp") as temp:
            folder = Path(temp)
            for split in ("train", "validation"):
                write_csv(folder / f"{split}.csv", [{"text": "good", "label_id": 2}])
            write_json(folder / "audit.json", {"lowercase": False, "split_seed": 42,
                       "split_sha256": {split: sha256(folder / f"{split}.csv") for split in ("train", "validation")}})
            config = {"prepared_dir": str(folder), "split_seed": 42, "lowercase": False}
            # There is deliberately no test.csv or test checksum.
            splits, _ = load_splits(config, ["train", "validation"])
            self.assertEqual(set(splits), {"train", "validation"})

    def test_evaluation_policy_rejects_test_only_or_unknown_splits(self):
        self.assertEqual(evaluation_splits({"evaluation_splits": ["validation"]}), ["validation"])
        for splits in (["test"], ["train"], [], ["validation", "anything"]):
            with self.assertRaises(ValueError):
                evaluation_splits({"evaluation_splits": splits})

    def test_character_and_word_vocabulary_use_training_only(self):
        settings = {"ngram_range": [1, 2], "min_df": 1, "max_features": 100,
                    "char_min_df": 1, "char_max_features": 200, "char_ngram_range": [3, 5]}
        model = build_baseline(settings, "svm_word_char", 1.0)
        model.fit(["good accha movie", "bad bekaar movie", "neutral movie update"], [2, 0, 1])
        before = {name: dict(transformer.vocabulary_) for name, transformer in model.named_steps["features"].transformer_list}
        prediction = model.predict(["zzzzvalidationsecretzzzz"])
        after = {name: dict(transformer.vocabulary_) for name, transformer in model.named_steps["features"].transformer_list}
        self.assertEqual(before, after)
        self.assertNotIn("zzzzvalidationsecretzzzz", after["word"])
        self.assertEqual(len(prediction), 1)
        self.assertTrue(any("acc" in feature for feature in after["character"]))

    def test_development_report_preserves_historical_metrics_and_labels_split(self):
        from sentiment_research import development
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1] / "tmp") as temp:
            root = Path(temp)
            out = root / "outputs/development"
            out.mkdir(parents=True)
            data = root / "data"
            data.mkdir()
            write_json(data / "audit.json", {"split_sha256": {"train": "a", "validation": "b", "test": "c"}})
            original = "# Historical test results\n\nAccuracy = 0.6264705882\n"
            (root / "METRICS.md").write_text(original)
            config = {"output_dir": str(out), "prepared_dir": str(data), "baseline_output_dir": str(root / "missing"),
                      "evaluation_splits": ["validation"], "experiment": "fixture"}
            with patch.object(development, "ROOT", root):
                development.development_report(config)
                first = (root / "METRICS.md").read_text()
                development.development_report(config)
            final = (root / "METRICS.md").read_text()
            self.assertTrue(final.startswith(original.rstrip()))
            self.assertEqual(first, final)
            self.assertEqual(final.count(development.MARKER), 1)
            self.assertIn("NOT fresh test results", final)


if __name__ == "__main__":
    unittest.main()
