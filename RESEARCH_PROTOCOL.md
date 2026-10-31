# Experiment protocol

## Scope and question

Compare TF-IDF + Multinomial Naive Bayes, TF-IDF + Linear SVM, and fully fine-tuned mBERT on the same Hinglish sentiment examples. Determine how contextual fine-tuning performs against explicit classical baselines under a controlled, documented setup. This is a baseline study inspired by arXiv:2601.05091v1, not a claim of architectural novelty.

## Data and unit of evaluation

Use only the 14,000-example raw SentiMix training file and 3,000-example raw development file downloaded from a shared-task participant archive. Pool these raw examples, remove conflicting-label IDs and normalized texts, and deduplicate by normalized text and ID. Construct a new stratified 80/10/10 split with seed 42. A tweet is the unit of evaluation. Dataset provenance and exact exclusions/counts are written to `data/research/sentimix_custom_split_v1/audit.json`.

The original benchmark development set is not used as the benchmark test set. The protocol intentionally discards the original split boundaries to make a custom experiment, and it must be described as such. It cannot support claims about the original official SentiMix test-set performance or exact Hinglish-24k reproduction.

Normalize Unicode and HTML, replace URL and user mentions with placeholders, preserve hashtag words, and expand emoji into English descriptions. Preserve negation, stop words, and case. The TF-IDF vectorizer separately lowercases as an explicitly documented model-specific feature choice. No token vocabulary, IDF statistics, or model parameters are fitted on validation/test text.

## Primary outcome and selection

The primary outcome is held-out **weighted F1**. Also report accuracy, weighted precision/recall, macro F1, per-class precision/recall/F1/support, balanced accuracy, Matthews correlation, and Cohen's kappa. Report confusion matrix counts and row-normalized proportions.

Choose Naive Bayes alpha from [0.1, 0.5, 1.0] and SVM C from [0.5, 1.0, 2.0] using validation weighted F1 only. Fit each candidate's TF-IDF vocabulary/IDF on the training split only. Ties select the first candidate in the listed grid. Do not refit on validation after selection.

Use the paper's stated mBERT learning rate, epochs, effective batch size, weight decay, warmup steps and maximum length. Select the best epoch by validation weighted F1; ties retain the earlier epoch. Test predictions are generated only after selecting the checkpoint. No model or seed is chosen by its test score.

## Randomness and uncertainty

The initial run uses training seed 42. Additional mBERT seeds 43 and 44 use identical frozen train/validation/test examples and settings. Report all runs plus the arithmetic mean and sample standard deviation; do not report a single seed as a multi-run mean. Classical baselines need only one run because their procedures are deterministic or nearly deterministic here; repeating identical NB fits is not independent evidence.

For each fitted model, compute 1,000 stratified bootstrap resamples of its test predictions, keeping class supports fixed, and report percentile 95% intervals for accuracy, macro F1, and weighted F1. For fixed seed-42 model pairs, resample identical indices to obtain paired weighted-F1 difference intervals. These intervals quantify example uncertainty conditional on the fitted models, not training-seed uncertainty. No uncorrected multi-comparison p-value or significance claim is made.

## Limits and reporting

Exact normalized-text and ID leakage is checked. Near duplicates, shared authors, topics, time periods, and pretrained-corpus contamination are not ruled out. The observed results characterize this custom dataset/split, not unseen domains or all Hinglish text. Inference throughput depends on hardware, batching, and sequence length and is not directly compared to the reference paper's hardware.

Before publication, inspect errors by neutral ambiguity, negation, slang, sarcasm, mixed-language balance, and spelling variation. Mark any manually annotated subgroup analysis as post hoc unless defined beforehand. Cite original data/model authors and the inspiration paper. Review data redistribution terms before publishing raw text. A deployable codebase or a higher test score by itself does not establish a publishable contribution.

## Artifact map

The CLI writes raw-source hashes, exact split hashes, full configs, dependency versions, pretrained snapshot identifiers, seeds, timing, selected hyperparameters/epochs, validation scores, test predictions, per-class metrics, confusion matrices, bootstrap results, and model artifacts. `complete.json` distinguishes successful research runs from interrupted or failed attempts. Installed package versions are also exported to a lock file after environment setup.
