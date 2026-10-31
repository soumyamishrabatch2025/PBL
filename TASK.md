# Research Task Tracker

Last Updated: 2026-10-31

---

## Phase 1: Baseline Replication & Research Harness
- [x] **Task 1.1**: Deduplicate and clean raw SentiMix sources (14,000 train + 3,000 dev $\rightarrow$ 16,993 valid tweets).
- [x] **Task 1.2**: Create frozen, stratified 80/10/10 split with strict data leakage prevention (`sentimix_custom_split_v1`).
- [x] **Task 1.3**: Train and evaluate TF-IDF + Multinomial Naive Bayes (Test Weighted F1: 0.6274).
- [x] **Task 1.4**: Train and evaluate TF-IDF + Linear SVM (Test Weighted F1: 0.6142).
- [x] **Task 1.5**: Train and evaluate Multilingual BERT (`bert-base-multilingual-cased`) (Test Weighted F1: 0.6240).
- [x] **Task 1.6**: Generate comparative baseline metrics, confusion matrices, and bootstrap confidence intervals in `METRICS.md`.

---

## Phase 2: Validation-Only Development & Data Expansion
- [x] **Task 2.1**: Implement matched word-only SVM control with expanded C grid (Val Weighted F1: 0.6004).
- [x] **Task 2.2**: Implement spelling-robust Word + Character n-gram SVM (Val Weighted F1: 0.6249, outperforming mBERT).
- [x] **Task 2.3**: Fine-tune domain-specific `l3cube-pune/hing-bert` (Seed 42) (Val Weighted F1: 0.6686, Macro F1: 0.6724).
- [x] **Task 2.4**: Generate 200-sample blinded neutral-boundary review packet under `outputs/sentimix_development_v2/neutral_review/`.
- [x] **Task 2.5**: Ingest, sanitize, and verify SAIL-2017 benchmark dataset (`data/dataset/sail2017_csv/`).

---

## Phase 3: High-Performance Indic Encoders (Complete)
- [x] **Task 3.1**: Implement preflight and model architecture support for `l3cube-pune/hing-roberta`.
- [x] **Task 3.2**: Fine-tune and evaluate Hing-RoBERTa (Seed 42) on frozen validation set (Val Accuracy: 66.71%, Val Macro F1: 67.02%, Val ROC-AUC: 0.8373).
- [x] **Task 3.3**: Implement model architecture support and preflight for Google's MuRIL (`google/muril-base-cased`).
- [x] **Task 3.4**: Fine-tune and evaluate MuRIL (Seed 42) on frozen validation set (Val Accuracy: 64.53%, Val Macro F1: 64.68%, Val ROC-AUC: 0.8016).
- [x] **Task 3.5**: Compare HingBERT, Hing-RoBERTa, and MuRIL performance and error patterns; evaluate initial multi-model ensembles (Tri-model ensemble: **68.12% Accuracy**, **68.45% Macro F1**, **67.90% Weighted F1**).

---

## Phase 4: Neutral-Class Bottleneck Mitigation
- [ ] **Task 4.1**: Implement Focal Loss ($\gamma \in [1.5, 2.0]$) in transformer classification training pipeline.
- [ ] **Task 4.2**: Implement cost-sensitive class re-weighting targeting Neutral class errors.
- [ ] **Task 4.3**: Benchmark Focal Loss model against standard Cross-Entropy (Target: Neutral F1 $> 0.68$).

---

## Phase 5: Multi-Model Probability Ensembling
- [ ] **Task 5.1**: Build probability calibration and soft-voting ensemble module.
- [ ] **Task 5.2**: Generate ensemble predictions combining HingBERT + Hing-RoBERTa + MuRIL.
- [ ] **Task 5.3**: Evaluate ensemble against single best model (Target: Weighted F1 $> 0.72$).

---

## Phase 6: Multi-Dataset Benchmark (SAIL-2017 & Generalization)
- [ ] **Task 6.1**: Run baseline and top transformer architectures on SAIL-2017 benchmark.
- [ ] **Task 6.2**: Cross-corpus generalization experiment: SentiMix-trained models tested zero-shot on SAIL-2017.

---

## Phase 7: Scientific Rigor & Manuscript Preparation
- [ ] **Task 7.1**: Complete multi-seed runs (Seeds 42, 43, 44) for top architectures to report mean $\pm$ std dev.
- [ ] **Task 7.2**: Compute paired bootstrap significance tests ($p < 0.01$) against the reference paper's baseline.
- [ ] **Task 7.3**: Produce publication-ready LaTeX tables, confusion matrix figures, and final comparative analysis.
