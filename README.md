# Hinglish sentiment classification research

A reproducible experimental project inspired by **Code-Mix Sentiment Analysis on Hinglish Tweets**, arXiv:2601.05091v1. It trains the three models discussed in that paper: TF-IDF + Multinomial Naive Bayes, TF-IDF + linear SVM, and fully fine-tuned multilingual BERT (`bert-base-multilingual-cased`).

## What this experiment measures

The paper's exact cleaned **Hinglish-24k** dataset and example-level split were not provided. This project uses the downloaded raw **SentiMix Hindi-English training and development files (14,000 + 3,000 tweets)**, removes normalized duplicates and conflicting labels, and makes a custom stratified **80%/10%/10% train/validation/test split** with seed 42. This is a related controlled experiment, not an exact replication of the paper or an official SentiMix test-set result.

The other cited GitHub CSV is **not merged**: all 14,000 training IDs already occur in it. Existing four-class hate-speech datasets, notebooks, and saved HingBERT models are not used or modified.

## Setup on Windows

Use Python 3.12 and an NVIDIA GPU for practical full mBERT training. The supplied setup script creates `.venv-research` separately from the existing `.venv` and installs the CUDA 12.6 PyTorch wheel. A compatible NVIDIA driver is sufficient; a separate CUDA toolkit is not required for these wheels.

```powershell
powershell -ExecutionPolicy Bypass -File scripts/setup.ps1
.\.venv-research\Scripts\python.exe run_research.py doctor
```

Sources: [PyTorch installation](https://pytorch.org/get-started/locally/), [mBERT model card](https://huggingface.co/google-bert/bert-base-multilingual-cased).

## Run experiments

All paths in a config are relative to this project root. Raw data are already under `data/raw/hinglish_24k_sources/sentimix/`. See the source README there for provenance and download links.

On another machine, run `python scripts/download_data.py` to download and checksum-verify the exact raw files used here.

```powershell
# Prepare once. The command refuses to overwrite an existing frozen dataset.
.\.venv-research\Scripts\python.exe run_research.py prepare

# Fit both baselines; hyperparameters are chosen using validation weighted F1.
.\.venv-research\Scripts\python.exe run_research.py train --models naive_bayes svm

# Train all mBERT parameters. First complete run, or add more seeds separately.
.\.venv-research\Scripts\python.exe run_research.py train --models mbert --seeds 42
.\.venv-research\Scripts\python.exe run_research.py train --models mbert --seeds 43 44

# Compare every completed run on the identical held-out split.
.\.venv-research\Scripts\python.exe run_research.py report

# Alternatively, prepare and train all three models in one command on a fresh experiment.
.\.venv-research\Scripts\python.exe run_research.py all
```

Settings live in `configs/research.json`. mBERT uses 3 epochs, learning rate 2e-5, AdamW, weight decay 0.01, 500 warmup steps, and maximum length 128, matching the paper's stated values. A microbatch of 4 with accumulation of 2 gives effective batch size 8. Mixed precision, dynamic padding, and gradient checkpointing help fit a 6 GB GPU. Select the best epoch using validation weighted F1, then evaluate the test set once. Bias and LayerNorm weights have no weight decay. Checkpoints store the model and tokenizer, not optimizer/resume state.

For an interactive entry point, open `notebooks/research_pipeline.ipynb`. It invokes the same isolated Python environment and skips completed runs; it does not duplicate training logic.

### Deliberate differences from the reference paper

- Raw corpus and custom split differ; direct performance ranking against the paper's 0.67 is not justified.
- Preprocessing preserves case for cased mBERT, negation, stop words, hashtag words, and sentiment-bearing emoji descriptions. The paper lowercases and removes some words/hashtags, but does not specify enough detail to reproduce its exact procedure.
- The exact SVM variant, TF-IDF settings, and NB smoothing were not specified. Here they are explicit and tuned on validation only.
- Both weighted F1 (paper-aligned primary selection metric) and macro F1 (equal class importance) are reported.
- Identical normalized texts and tweet IDs cannot cross splits. Near duplicates, authors, and topics may still overlap; this is not a cross-domain/author-independent experiment.

## Results and artifacts

`outputs/sentimix_custom_split_v1/` contains only actual measured results after training:

The root-level **`METRICS.md`** collects every completed model's test and validation metrics, class-level scores, raw/normalized confusion matrices, confidence intervals, training details, and seed summaries in one file. `report` and completed `train` commands regenerate it and print its contents. In-progress models are explicitly marked pending.

- `results.md`, `comparison.csv`, and `comparison.tex`: model comparison and table for a manuscript.
- `summary.json`: mean and sample standard deviation over completed seeds; a one-run standard deviation is null, not zero.
- `paired_comparisons.json`: paired stratified bootstrap intervals for weighted-F1 differences on fixed seed-42 runs.
- Each `<model>/seed_<seed>/` contains metrics JSON, per-class CSV, raw and normalized confusion matrices (CSV/PNG), test predictions, misclassified examples, and bootstrap confidence intervals.
- Baselines store `model.joblib`; mBERT stores `checkpoint/`, epoch history, training status, and the resolved pretrained snapshot identifier.
- Configurations, dependency versions, source/split checksums, and timing measurements support reproducibility.
- `complete.json` is written only after a successful evaluation. Failed or interrupted runs are never included in comparison tables.

Reported metrics: accuracy, balanced accuracy, macro/weighted/micro precision, recall and F1, Matthews correlation, Cohen's kappa, and class support. Naive Bayes and mBERT additionally report log loss and macro one-vs-rest ROC-AUC from probabilities. Linear SVM probabilities are not invented or approximated, so probability metrics are absent for it. Confusion matrix rows are actual classes and columns are predicted classes, ordered negative/neutral/positive.

The 95% bootstrap intervals condition on the fitted model and held-out examples. They do not quantify training-seed or split uncertainty. Multi-seed results on one split are useful but are not independent test datasets.

Runs refuse to overwrite existing results. To change preprocessing or splitting, copy the config and give `experiment`, `prepared_dir`, and `output_dir` new names. To change model hyperparameters on the same frozen split, use a new `output_dir`, and do not use observed test performance to select hyperparameters. An interrupted run has to be restarted under a new output directory; automatic optimizer-state resumption is not implemented.

## Phase 2 development

See `DEVELOPMENT_PROTOCOL.md` and `configs/development.json`. The fresh HingBERT classifier and word+character SVM use validation-only evaluation. Their results are appended to a separate development section in root `METRICS.md`; historical test measurements are preserved.

```powershell
.\.venv-research\Scripts\python.exe run_research.py preflight --config configs/development.json
.\.venv-research\Scripts\python.exe run_research.py audit-packet --config configs/development.json
.\.venv-research\Scripts\python.exe run_research.py train --config configs/development.json --models svm
.\.venv-research\Scripts\python.exe run_research.py train --config configs/development.json --models svm_word_char
.\.venv-research\Scripts\python.exe run_research.py train --config configs/development.json --models hingbert --seeds 42 43 44
.\.venv-research\Scripts\python.exe run_research.py report --config configs/development.json
```

The preflight checks metadata/tokenization/hardware without training. The blinded review packet needs two independent human annotators; packet creation does not imply label corrections or completed human review. A new untouched evaluation set is still required for final publication claims after model selection.

An active user-requested `outputs/sentimix_development_v2/training_control.json` stops the training CLI cleanly after HingBERT seed 42 finishes. Further seeds are deferred until review; the stop request must be cleared deliberately before an authorized continuation. It does not interrupt the current run or block the `report` command.

## Prediction

Only load saved model artifacts you trust.

```powershell
.\.venv-research\Scripts\python.exe run_research.py predict --model-path outputs/sentimix_custom_split_v1/svm/seed_42/model.joblib --text "movie achhi nahi thi"
.\.venv-research\Scripts\python.exe run_research.py predict --model-path outputs/sentimix_custom_split_v1/mbert/seed_42/checkpoint --text "movie bahut achhi thi"
```

## Validation

```powershell
.\.venv-research\Scripts\python.exe -m unittest discover -s tests -v
```

Tests cover label-conflict handling, ID/text leakage checks, reproducible splitting, split tamper detection, preservation of sentiment cues, known metric values, and rejection of invalid pairwise comparisons.

## Using this work in a research paper

Describe the exact corpus, exclusions, preprocessing, split seed, model-selection rules, hyperparameter search, and hardware. Cite the original SentiMix dataset and the reference paper. Report at least several transformer training seeds; do not select the best test seed. Review the saved error examples and the data audit before interpreting results. A baseline replication/controlled comparison alone does not establish a novel research contribution or guarantee publication.

Potential follow-up studies include original-versus-deromanized inputs, dual-view fusion, and controlled spelling-variation robustness. They require their own preregistered validation choices, ablations, and a fresh test protocol if the current test has informed development. They are not claimed as implemented here.

Dataset reference: [Patwa et al., SemEval-2020 Task 9](https://aclanthology.org/2020.semeval-1.100/). Reference paper: [Garg et al., arXiv:2601.05091](https://arxiv.org/abs/2601.05091).
