# Phase 2 & 3: Indic encoders, spelling-robust SVM, and ensembling

## Scope fixed before new training

The first three models have already exposed the custom test set. Phase 2 and 3 are therefore validation-only development. Use the exact frozen 13,593 training and 1,700 validation examples, retain their SHA-256 checksums, and do not load or evaluate test.csv. Preserve all historical test results and label new results as validation results in METRICS.md.

Final publication-level performance must be measured on a fresh untouched evaluation set, checked for normalized-text and ID overlap with every development source. No such set is claimed to exist yet.

## Experiments

- Matched word-only SVM control: retain the original word feature settings, but use the same C grid [0.1, 0.5, 1, 2, 5] as the character model. This separates the effect of adding character features from expanding the regularization search. The historical SVM searched [0.5, 1, 2], so its score alone is not a matched ablation.
- Word + character SVM: word unigrams/bigrams plus character-within-word 3-5 grams, each with sublinear TF-IDF and training-only vocabulary/IDF fitting. Feature caps are 60,000 word and 100,000 character features, minimum document frequency 2. L2-normalize the concatenated features. Choose C from [0.1, 0.5, 1, 2, 5] by validation weighted F1. Strict ties retain the first candidate. This deterministic baseline needs one seed-42 run.
- HingBERT: initialize from the pretrained `l3cube-pune/hing-bert` masked-language-model checkpoint and a newly initialized three-class head. Do not reuse the existing four-class hate-speech classifier. Use the same preprocessing and training/validation examples as the baseline study.
- Hing-RoBERTa: initialize from `l3cube-pune/hing-roberta` (byte-level BPE pre-trained on Romanized Hinglish) with a newly initialized 3-class classification head.
- MuRIL: initialize from `google/muril-base-cased` (pre-trained on Indian languages, transliterated text, and cross-lingual pairs) with a fresh classification head.
- Fixed transformer settings: 3 epochs, learning rate 2e-5, AdamW, weight decay 0.01 excluding bias/LayerNorm, 500 warmup steps, maximum length 128, microbatch 4, accumulation 2 (effective batch 8), evaluation batch 8, mixed precision, gradient checkpointing, and gradient clipping at 1.0. Release unused CUDA cache between epochs to reduce cached-memory pressure. No learning-rate search is conducted in this initial comparison.
- Multi-Model Ensembles: Calibrated soft-voting combining out-of-fold probability distributions from diverse Indic architectures (HingBERT, Hing-RoBERTa, MuRIL) to exploit complementary error patterns.
- Phase 4 Focal Loss: Target the persistent Neutral class bottleneck (~0.58-0.60 F1) using Focal Loss ($\gamma \in [1.5, 2.0]$) and cost-sensitive class re-weighting.

The user requested notice before HingBERT training. Preflight performs metadata, safe-tensor key, tokenizer and hardware checks with zero optimizer steps; it is not training.

## Neutral-boundary audit

Create a blinded 200-example packet using only the original mBERT validation predictions. Target 100 neutral-boundary errors, 50 polarity errors, and 50 correctly classified controls, with deterministic fallback sampling if a stratum is too small. Save the exact case IDs, source hashes, and actual sampling counts.

Independent reviewers A and B must annotate without seeing the original labels, model predictions, or sampling strata. Keep uncertain/missing-context cases explicit; do not automatically call mixed opinions neutral. Calculate agreement and adjudicate disagreements only after both reviewers finish. No labels are silently corrected or removed, and no human-agreement score is invented. This targeted audit cannot estimate the entire corpus's label-noise rate without accounting for sampling.

Human annotations remain pending until supplied. Preparing the packet does not count as completing an independent human annotation study. Any label corrections require a new dataset version and a separately documented experiment.

## Reporting

Save validation accuracy; macro/weighted/micro precision, recall and F1; per-class support; balanced accuracy; MCC; kappa; raw and normalized confusion matrices; predictions; and errors. HingBERT also supplies log loss and macro one-vs-rest ROC-AUC. Uncalibrated LinearSVC does not supply probability metrics.

Report validation selection/search scores and checkpoint epochs. Do not present selection-set bootstrap intervals or these validation scores as unbiased generalization estimates. Extend METRICS.md with a clearly separated development section; preserve the historical test section unchanged. Additional model/backbone searches or label-cleaning experiments require a newly recorded configuration and validation protocol.
