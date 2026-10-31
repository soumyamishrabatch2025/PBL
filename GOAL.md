# Research Goal: State-of-the-Art Hinglish Sentiment Classification

## 1. Primary Objective
Publish a peer-reviewed research paper that significantly outperforms the baseline paper **"Code-Mix Sentiment Analysis on Hinglish Tweets" (Garg et al., arXiv:2601.05091v1)** in classification performance, linguistic nuance, methodological innovation, and empirical rigor.

---

## 2. Target Metrics & Benchmarks

| Metric / Dimension | Baseline Paper (mBERT) | Current Repo State (HingBERT v2) | Research Target |
|---|---|---|---|
| **Weighted F1** | ~0.6700 | 0.6686 (Val, Seed 42) | **$\ge$ 0.7200 – 0.7500+** |
| **Macro F1** | Not emphasized | 0.6724 (Val, Seed 42) | **$\ge$ 0.7250+** |
| **Neutral Class F1** | 0.6000 | 0.6044 | **$\ge$ 0.6800+** |
| **Negative Class F1** | 0.7100 | 0.6912 | **$\ge$ 0.7400+** |
| **Positive Class F1** | 0.7000 | 0.7216 | **$\ge$ 0.7500+** |
| **Model Diversity** | mBERT only | mBERT, HingBERT, Word+Char SVM | HingBERT, Hing-RoBERTa, MuRIL, Ensemble |
| **Multi-Dataset Eval** | 1 merged split (unverified duplicate IDs) | SentiMix (clean split) + SAIL-2017 (clean split) | SentiMix + SAIL-2017 + Cross-Corpus Generalization |
| **Statistical Rigor** | 1 seed, no significance test | Stratified bootstrap, seed 42 completed | Multi-seed (mean $\pm$ std), Bootstrap $p < 0.01$ |

---

## 3. Core Technical Innovations
1. **Domain-Specialized Encoders**:
   - Evaluate `l3cube-pune/hing-roberta` (byte-level BPE pre-trained on Romanized code-mixed Hindi).
   - Evaluate `google/muril-base-cased` (specifically pre-trained on Indian languages, transliterated text, and cross-script pairs).
2. **Neutral Bottleneck Resolution**:
   - Address the prominent neutral confusion boundary using **Focal Loss** ($\gamma \in [1.5, 2.0]$) and adaptive class-cost weighting to force gradients to distinguish subtle subjective opinion markers from objective neutral observations.
3. **Probability-Level Soft-Voting Ensemble**:
   - Combine out-of-fold calibrated probabilities from diverse model families (HingBERT + Hing-RoBERTa + MuRIL + Word+Char SVM) to boost robust classification and minimize calibration error.
4. **Cross-Dataset Validation & Out-of-Domain Generalization**:
   - Test models across both **SentiMix** and **SAIL-2017** benchmarks.
   - Demonstrate cross-domain generalization (train on SentiMix $\rightarrow$ zero-shot test on SAIL-2017) to provide an empirical contribution rarely presented in current Hinglish literature.

---

## 4. Target Publication Venues
- **ACL / EMNLP / COLING Workshops**: Workshop on Computational Approaches to Code-Switching (CALCS), Workshop on Multilingual Representation Learning (MRL), or Workshop on Indic NLP.
- **IEEE / ACM Conferences / Journals**: IEEE Transactions on Computational Social Systems (TCSS), IEEE Access, or ACM Transactions on Asian and Low-Resource Language Information Processing (TALLIP).
