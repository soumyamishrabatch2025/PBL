# Automated improvement experiments

Implementation and preparation do not establish a performance improvement. New
transformer runs are queued, not trained. Historical results and source datasets
are preserved. Independent human annotations are not fabricated.

`src/sentiment_research/improvements.py` prepares versioned SentiMix, SAIL, pooled,
and matched old-preprocessing control datasets under `data/research/automated_v3`.
It repairs tokenized URL/mention fragments, preserves sentiment cues, hashes inputs
and outputs, excludes conflicting training groups, and removes normalized-text
duplicates. Across both corpora, test texts have priority over validation and
training; validation texts have priority over training. Labels are never rewritten.
Exclusions are recorded. Test labels are not used for exclusion decisions.
Near-duplicate semantic matches and shared authors are not guaranteed disjoint.

Ten configurations in `configs/automated_v3` isolate four loss choices, compare
matched preprocessing, compare learning rates 1e-5/2e-5/3e-5, and compare SentiMix,
SAIL, pooled, and corpus-balanced pooled training. Three epochs maximum, patience
one, and validation weighted F1 select checkpoints. Corpus balancing samples each
corpus with equal expected mass, using inverse corpus size per-example weights.
All runs evaluate validation only. Additional seeds use the same frozen settings.
SAIL-only scores are on SAIL validation; pooled scores are on SentiMix validation,
so those two rows must not be interpreted as a matched corpus ablation.

Run from the repository root with `.venv-research/Scripts/python.exe`:

```powershell
python scripts/audit_automated_data.py
python scripts/run_improvement_experiments.py
python scripts/run_improvement_experiments.py --train --experiments preprocess_control loss_ce loss_weighted_ce loss_focal loss_weighted_focal
python scripts/run_improvement_experiments.py --train --experiments lr_1e-05 lr_3e-05 corpus_sail corpus_pooled pooled_balanced
```

The runner prints the queue unless `--train` is supplied, runs sequentially, skips
completed runs, and refuses to overwrite interrupted runs. Training is not resumable
from optimizer state; use a new output directory to restart an interrupted run.

`scripts/evaluate_transfer.py` evaluates an unchanged local checkpoint on another
prepared corpus. It defaults to validation, requires matching preprocessing, and
requires `--allow-test` to release test evaluation. Example after training:

```powershell
python scripts/evaluate_transfer.py --checkpoint outputs/automated_v3/loss_ce/hingroberta_focal/seed_42/checkpoint --config configs/automated_v3/corpus_sail.json --output outputs/automated_v3/transfer_sentimix_to_sail
```

`scripts/calibrated_ensemble.py` fits temperatures on 40% of existing validation
predictions, chooses simplex weights on 30%, and diagnoses on the remaining 30%.
It validates prediction identities, class order, and probability normalization and
saves metrics, class reports, predictions, and confusion matrices alongside an
equal-weight comparison. Base checkpoints already used the full validation set:
these are conditional development diagnostics, not training out-of-fold predictions
or independent test performance. Calibration is not presumed to improve F1.
Inputs, subset IDs, temperatures, and weights are recorded in selection.json.

`outputs/automated_v3/data_checks.json` records hash checks, text disjointness,
and training/validation tokenizer lengths. Keep length 128 unless training-only
truncation diagnostics justify a separately documented longer-length experiment.

Annotation may begin now: follow `ANNOTATION_GUIDE.md`. Review is independent of
this automated queue. Final publication needs a frozen protocol, seed variability,
and a defensible untouched evaluation source; the historical SentiMix test has
already been exposed. Do not compare its custom-split score directly with a paper's
different dataset/split as evidence of superiority.
