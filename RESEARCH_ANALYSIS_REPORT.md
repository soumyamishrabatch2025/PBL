# Research analysis and manuscript preparation report

**Evidence snapshot:** 2026-11-01T08:41:34+05:30 (Asia/Calcutta).

**Purpose:** a verified basis for writing the paper, not a claim that the study is submission-ready.

11 completed fitted runs were found. Saved metrics and confusion matrices were independently recomputed from predictions; all matched within numerical tolerance. Dataset files matched their recorded hashes. Training was neither stopped nor modified to produce this report.

## 1. Executive assessment

The project is a reproducible empirical study of three-class Hindi-English sentiment classification using classical models, pretrained encoders, loss reweighting, and probability ensembles. It does not introduce a new BERT architecture or pretrain a language model from scratch.

The strongest full-validation result currently documented is a selected four-model ensemble: accuracy 68.71%, macro F1 0.6908, weighted F1 0.6857. These are development-set selection scores, not an independent final-test estimate. The best historical test weighted F1 among the three initially tested models belongs to Naive Bayes (0.6274); paired intervals do not establish a clear advantage over mBERT or SVM.

The newest matched cross-entropy comparison shows that increasing neutral-class weight does not improve overall weighted or macro F1 for seed 42. This negative result is useful evidence. Human annotation was explicitly skipped by the user; no human agreement, relabeling, or noise-reduction result exists.

## 2. Paper framing and research questions

**Suggested title:** Domain-Specific Encoders and Loss Reweighting for Hinglish Sentiment Classification: A Controlled Empirical Study.

**Defensible contribution:** transparent data provenance, versioned preprocessing, matched classical controls, encoder comparison, neutral-boundary analysis, and explicit separation of development selection from final evaluation. Whether this contribution is novel enough for a venue requires a fuller literature review.

- RQ1: Does combining character and word features improve a matched linear SVM?
- RQ2: How do multilingual and Hindi-English domain-adapted encoders compare under the recorded training protocol?
- RQ3: Does neutral-class weighting improve the precision/recall tradeoff and overall performance?
- RQ4: Do probability ensembles improve development performance over individual encoders?
- Future RQ5: Does pooled or cross-corpus training generalize to SAIL? No completed evidence yet.

## 3. Data provenance and dataset versions

The reference paper is [Garg et al., Code-Mix Sentiment Analysis on Hinglish Tweets](https://arxiv.org/abs/2601.05091v1). Its final Hinglish-24k corpus and exact splits were not reconstructed here. This project is inspired by it, not an exact replication. Dataset or split differences prevent a direct superiority claim against its published score.

The local SentiMix source contains 14,000 training and 3,000 development examples from a participant mirror. The [original shared-task overview](https://aclanthology.org/2020.semeval-1.100/) describes the underlying sentiment task. We pool only these accessible source partitions, clean them, and construct a custom stratified split; this is not the official SentiMix benchmark test split.

The downloaded alternative Behele CSV is not an independent second corpus: all 14,000 SentiMix training IDs occur in it. It was not merged into the experiments. Existing four-class hate-speech data and classifier checkpoints are outside this sentiment study.

SAIL comes from the derived [babyshark-sail2017-stage2 release](https://huggingface.co/datasets/satyam-arora-iiit-hyderabad/babyshark-sail2017-stage2). Raw and sanitized files are overlapping alternatives, not independent data. The text-line sentiment field was separated into a label column; it is not fed to the model. This release must not be represented as an organizer-original archive or as having a verified redistribution license.

| Dataset version | Train | Validation | Test | Use |
|---|---:|---:|---:|---|
| sentimix_custom_split_v1 | 13593 | 1700 | 1700 | Historical/phase-2 experiments |
| sail2017_prepared_v1 | 10068 | 1260 | 1261 | Prepared only / incomplete benchmark |
| automated_v3/sentimix | 13588 | 1700 | 1700 | New development version |
| automated_v3/sentimix_control | 13588 | 1700 | 1700 | New development version |
| automated_v3/sail | 10022 | 1259 | 1261 | New development version |
| automated_v3/pooled | 23610 | 1700 | 1700 | New development version |

Original SentiMix cleaning removed three duplicate rows and four rows in two conflicting-text groups, leaving 16,993 examples. Seed 42 creates 13,593/1,700/1,700 examples. Validation and test each contain negative=499, neutral=639, positive=562.

The new automated version removes 52 rows across SentiMix and SAIL partitions after stronger normalization and global overlap/conflict filtering. It keeps test text ahead of validation and training, and validation ahead of training. Training conflicts are excluded; labels are not corrected. Exclusion decisions do not use test sentiment labels. SAIL validation loses one overlap with its test partition. Pooled training is deduplicated across corpora.

No normalized-text overlap within the audited splits is not proof of semantic, near-duplicate, author, topic, or pretraining-corpus independence. Automated-v3 scores must not be pooled with historical scores as identical-dataset experiments. The matched old-preprocessing control is prepared but not yet completed.

### Dataset fingerprints

| Version | Split | SHA-256 |
|---|---|---|
| sentimix_custom_split_v1 | train | `1dd320f3e341d8a23146238ab46c1be60c5efef9196b879f5d378ea7df452708` |
| sentimix_custom_split_v1 | validation | `eebe157bedbcb7d08499e95098ffccf2495615b02d2e797606c1e004e930b34b` |
| sentimix_custom_split_v1 | test | `45fa015f13478db77c72cdf730db46abf1bd4c29f8f95cd7779e393cd86cc954` |
| sail2017_prepared_v1 | train | `1e9e1c288069d5b1e0b60b025a4d7105e60e31dc597b4c951aa8740391aeb6ac` |
| sail2017_prepared_v1 | validation | `54eff505525fa2bc1de14fb751adf573aefc1174a2af840a8c73e05d6d69e0b9` |
| sail2017_prepared_v1 | test | `affd18b4a88b8c051dfab11158793e1d7576b3e205f7a70eecd2e3f2f13a1785` |
| automated_v3/sentimix | train | `24991a164c4bce254b5cb74be79a27f1f7fa865cb05354432b5232c7aa974eb2` |
| automated_v3/sentimix | validation | `cc8f08b2c015b59672e5fd8ac399d000028e2258a22ae37c44142528af222979` |
| automated_v3/sentimix | test | `93756f9971cc3f6717a01564480ceab66cec330fdd86f220cdca4cddecfda390` |
| automated_v3/sentimix_control | train | `b1851590012529688a8ae22a8d2eba2cbc9a053de02dab16e7859e7f0bc54a06` |
| automated_v3/sentimix_control | validation | `6e408cf7772dc2dbf6bedba457ea92d6c37c0b63e3d4dee425c6d42dab23d6a8` |
| automated_v3/sentimix_control | test | `a1ee066d49726f9440df813fc6d987bc4fdf112b7b04b7e285704ac330b71b75` |
| automated_v3/sail | train | `d8a752479b8aab5f3abaf6c102ee015715cb8d384f3f2a6653dceacbf1e31697` |
| automated_v3/sail | validation | `14bd53c86e3f3c50748436ca741fd1b622a2d9d9b2615536c67d219f810c79ce` |
| automated_v3/sail | test | `e03c9eee6b3791eabd8152fdc935ae5449959da440f693ac69aac81d4c0feafa` |
| automated_v3/pooled | train | `750bdcf0b912243e7bdfd4bab93fdf2543960de53cb8a5fceda104bd3e1f7fde` |
| automated_v3/pooled | validation | `cc8f08b2c015b59672e5fd8ac399d000028e2258a22ae37c44142528af222979` |
| automated_v3/pooled | test | `93756f9971cc3f6717a01564480ceab66cec330fdd86f220cdca4cddecfda390` |

## 4. Methods and implementation

Labels are negative=0, neutral=1, positive=2. Baseline preprocessing uses Unicode NFKC, HTML unescaping, URL/mention placeholders, retained hashtag words, emoji descriptions, and whitespace normalization. Negation and stop words are retained. Transformer inputs preserve case; TF-IDF vectorizers lowercase independently. V2 preprocessing additionally repairs tokenized URLs and anonymized USER underscore fragments. No automatic sentiment-label correction is performed.

### Classical baselines

Word TF-IDF uses unigrams/bigrams, minimum document frequency 2, at most 60,000 features, and sublinear term frequency. Multinomial NB selects alpha from [0.1,0.5,1.0]. The original LinearSVC selects C from [0.5,1,2]. Matched development SVMs both search [0.1,0.5,1,2,5]; the word+character model adds char_wb 3–5 grams with a 100,000-feature cap, then L2-normalizes concatenated features. Vocabulary and IDF are fitted on training only.

### Pretrained encoders

[HingBERT](https://huggingface.co/l3cube-pune/hing-bert) is a BERT-family checkpoint adapted to romanized Hindi-English text. [Hing-RoBERTa](https://huggingface.co/l3cube-pune/hing-roberta) is **XLM-RoBERTa-based**; do not call this particular checkpoint an ordinary English RoBERTa or assume byte-level BPE from its short name. [MuRIL](https://arxiv.org/abs/2103.10730) is pretrained for Indian languages including translated/transliterated training signals. Model families differ in parameter count and tokenizer, so this is a comparison of available systems, not a controlled pretraining-only causal experiment.

All encoder parameters are fine-tuned with a newly initialized three-class classification head; no extra transformer layers are added. The old four-class hate-speech HingBERT classifier is not reused.

Default transformer settings: AdamW; learning rate 2e-5; weight decay 0.01 excluding bias/normalization parameters; 500 warmup steps; length 128; microbatch 4; accumulation 2 (effective batch 8); at most 3 epochs; gradient clipping 1.0; mixed precision and gradient checkpointing. mBERT evaluation batch is 16, later encoders use 8. Best checkpoint is selected by validation weighted F1. Automated-v3 adds patience-one early stopping. Hardware recorded: NVIDIA RTX 4050 Laptop GPU, approximately 6 GB VRAM. All completed runs in this snapshot use seed 42.

### Loss definitions

For correct-class probability p_y, the implemented loss is `mean[-alpha_y * (1-p_y)^gamma * log(p_y)]`. Standard CE sets gamma=0 and alpha=1; neutral-weighted CE uses [1,1.25,1] in negative/neutral/positive order; focal-only uses gamma=2 and alpha=1; weighted focal combines gamma=2 with [1,1.25,1]. Target weights multiply per-example losses before the batch mean, rather than dividing by the sum of target weights. The focal mechanism follows [Lin et al.](https://arxiv.org/abs/1708.02002); applying it here is not a new loss invention.

The historical focal run changed both gamma and class weights; it cannot isolate their individual effects. The automated four-arm loss ablation is designed to do so but is incomplete.

### Metrics and uncertainty

Accuracy is correct/N. Per-class precision=TP/(TP+FP), recall=TP/(TP+FN), and F1 is their harmonic mean. Macro F1 averages three class F1 scores equally; weighted F1 weights by class support. Weighted recall equals accuracy in this single-label setting. Confusion matrices below use actual rows and predicted columns ordered negative, neutral, positive. Probability models additionally supply log loss and macro one-vs-rest AUC; uncalibrated SVM has no such probability metrics.

Historical test intervals use 1,000 stratified example-bootstrap resamples and describe uncertainty conditional on fitted runs. They exclude seed/split uncertainty. Validation-selection scores and weight-search scores are not unbiased generalization estimates. No significance comparison against a published aggregate paper score is valid without matched examples/predictions.

## 5. Completed results, separated by protocol

### A. Historical custom test, original preprocessing

| Model / experiment | N | Accuracy (%) | Weighted precision | Weighted recall | Weighted F1 | Macro F1 |
|---|---:|---:|---:|---:|---:|---:|
| mbert | 1700 | 62.35 | 0.6246 | 0.6235 | 0.6240 | 0.6277 |
| naive_bayes | 1700 | 62.65 | 0.6291 | 0.6265 | 0.6274 | 0.6309 |
| svm | 1700 | 61.47 | 0.6140 | 0.6147 | 0.6142 | 0.6194 |

These are the initial measured custom-test results. Later development has occurred after this test was exposed. Do not describe it as a newly untouched final test for the current selected system.

### B. Historical and phase-2 validation on the original frozen data

| Model / experiment | N | Accuracy (%) | Weighted precision | Weighted recall | Weighted F1 | Macro F1 |
|---|---:|---:|---:|---:|---:|---:|
| mbert | 1700 | 62.06 | 0.6198 | 0.6206 | 0.6201 | 0.6238 |
| naive_bayes | 1700 | 60.29 | 0.6043 | 0.6029 | 0.6034 | 0.6075 |
| svm | 1700 | 59.88 | 0.5962 | 0.5988 | 0.5968 | 0.6022 |
| hingbert | 1700 | 66.88 | 0.6699 | 0.6688 | 0.6686 | 0.6724 |
| hingroberta | 1700 | 66.71 | 0.6651 | 0.6671 | 0.6641 | 0.6702 |
| hingroberta_focal | 1700 | 67.59 | 0.6774 | 0.6759 | 0.6762 | 0.6813 |
| muril | 1700 | 64.53 | 0.6459 | 0.6453 | 0.6414 | 0.6468 |
| svm | 1700 | 60.24 | 0.5995 | 0.6024 | 0.6004 | 0.6058 |
| svm_word_char | 1700 | 62.53 | 0.6246 | 0.6253 | 0.6249 | 0.6297 |

### C. Automated-v3 validation, revised training version

| Model / experiment | N | Accuracy (%) | Weighted precision | Weighted recall | Weighted F1 | Macro F1 |
|---|---:|---:|---:|---:|---:|---:|
| automated_v3_loss_ce | 1700 | 68.06 | 0.6824 | 0.6806 | 0.6813 | 0.6853 |
| automated_v3_loss_weighted_ce | 1700 | 67.94 | 0.6845 | 0.6794 | 0.6809 | 0.6847 |

Run-directory names such as `hingroberta_focal` are reused as backbone identifiers in automated-v3, even for CE runs. The experiment name, focal_gamma, and class_weights determine the actual loss. Do not label every such directory a focal-loss experiment.

### Matched neutral-weighting tradeoff

| Loss | Neutral precision | Neutral recall | Neutral F1 | Positive F1 |
|---|---:|---:|---:|---:|
| CE | 0.6105 | 0.6354 | 0.6227 | 0.7166 |
| Neutral-weighted CE | 0.6009 | 0.6620 | 0.6299 | 0.7061 |

Neutral weighting increases neutral recall and F1 while decreasing neutral precision and positive F1. It therefore changes the class tradeoff rather than improving overall F1. This observation is descriptive for one seed.

### D. Ensemble evidence

The recorded selected weights [0.15,0.15,0.40,0.30] for HingBERT / Hing-RoBERTa CE / Hing-RoBERTa weighted focal / MuRIL reproduce accuracy 68.71%, macro F1 0.6908, weighted F1 0.6857, and neutral F1 0.6167. Input IDs, text, labels, and ordering were verified. The original script searched simplex weights at step 0.05 to maximize macro F1 on this same validation set. This report recomputes the recorded winner, not an independent re-run of the entire search.

Historical ensembles are uncalibrated probability averages, not training out-of-fold predictions. A later diagnostic fits temperatures on 680 validation rows and ensemble weights on 510, then diagnoses on 510 other rows. Base checkpoints had already used all validation examples for checkpoint selection, so even its diagnostic split is not independently untouched.

| 510-row development diagnostic | Accuracy (%) | Macro F1 | Weighted F1 |
|---|---:|---:|---:|
| Calibrated tuned | 69.02 | 0.6960 | 0.6913 |
| Equal uncalibrated | 70.20 | 0.7058 | 0.7008 |

Calibration did not outperform equal weighting in this diagnostic. These subset scores must not be ranked directly against full-validation scores.

#### Selected full-validation ensemble: class evidence

| Class | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| negative | 0.703097 | 0.773547 | 0.736641 | 499 |
| neutral | 0.635158 | 0.599374 | 0.616747 | 639 |
| positive | 0.728102 | 0.709964 | 0.718919 | 562 |

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 386 | 98 | 15 |
| neutral | 122 | 383 | 134 |
| positive | 41 | 122 | 399 |

### E. Historical paired uncertainty

| Comparison | Weighted F1 difference | Paired bootstrap 95% interval |
|---|---:|---|
| mbert vs naive_bayes | -0.0034 | [-0.0254, 0.0209] |
| mbert vs svm | 0.0098 | [-0.0159, 0.0349] |
| naive_bayes vs svm | 0.0132 | [-0.0036, 0.0315] |

All displayed paired intervals contain zero. The historical test evidence does not establish a clear difference for these fitted runs.

## 6. Interpretation and claim boundaries

- The matched word+character SVM improves validation weighted F1 over the matched word-only SVM. Attribute this comparison to the matched feature experiment, not to the original SVM with a different C grid.
- On original-data validation, HingBERT outperforms local mBERT in weighted F1; MuRIL is weaker than the two Hinglish-adapted encoders in this run. This is seed-42 development evidence, not a universal ranking.
- Historical weighted focal improves Hing-RoBERTa development scores and neutral F1, but gamma and neutral weighting changed simultaneously. Do not claim focal loss alone caused the improvement.
- Neutral remains the weakest class in key original-data encoder/ensemble results. Confusion matrices quantify this; causes such as sarcasm or annotation noise remain hypotheses without systematic human validation.
- New CE vs weighted CE isolates neutral reweighting under the same automated-v3 data/settings. Overall F1 does not improve. Examine per-class recall and precision to explain the tradeoff; a class-level increase is not an overall gain.
- The selected ensemble is strongest among the full original-validation systems discussed here, but weights are tuned on that same set. Do not call it a fresh-test result, calibrated system, production-ready model, or state of the art.
- An apparent gain from historical Hing-RoBERTa to automated CE cannot isolate preprocessing: retained training examples and early-stopping protocol also changed. Await the matched preprocessing control.

## 7. Ongoing and uncompleted work at snapshot

| Experiment / artifact | State | Details |
|---|---|---|
| loss_ce | complete | Included above |
| loss_weighted_ce | complete | Included above |
| loss_focal | training | epoch 2, step 2300/5097 |
| loss_weighted_focal | not started | No completed evidence |
| preprocess_control | not started | No completed evidence |
| lr_1e-05 | not started | No completed evidence |
| lr_3e-05 | not started | No completed evidence |
| corpus_sail | not started | No completed evidence |
| corpus_pooled | not started | No completed evidence |
| pooled_balanced | not started | No completed evidence |
| Earlier SAIL benchmark | incomplete | A status file is not a completed training result |
| Cross-corpus evaluation | not completed | Evaluation utility exists; no measured result in this snapshot |
| Seeds 43 and 44 | not completed | Do not report mean ± SD across seeds |
| Independent human annotation | skipped by user | No label corrections or agreement scores |

The running queue remains authorized and active; this snapshot does not stop it. Current progress is not an accuracy estimate. New results after this timestamp require an updated report.

## 8. Manuscript-ready material

### Draft abstract (development study; revise after final evaluation)

> We investigate three-class sentiment classification of Hindi-English code-mixed social-media text using classical TF-IDF models and pretrained multilingual and domain-adapted encoders. We construct a versioned custom split from accessible SentiMix source partitions, document duplicate and label-conflict handling, and compare models using common evaluation artifacts. On the original 1,700-example development partition, a validation-selected ensemble achieves macro F1 0.6908 and weighted F1 0.6857. A matched feature experiment supports character n-grams as a useful addition to a word-based SVM. In a revised-data comparison, neutral-class weighting does not improve overall F1 over standard cross-entropy for seed 42. We report class-level errors and distinguish development selection from generalization. These results are preliminary because repeated validation use, single-seed training, and the absence of an independent final evaluation limit conclusions.

### Recommended section structure

1. Introduction: code mixing, romanization variability, neutral-boundary difficulty, and the specific empirical questions.
2. Related work: SentiMix, the reference paper, HingCorpus/HingBERT/Hing-RoBERTa, MuRIL, focal loss, and recent task-specific comparisons. Establish novelty through additional verified reading; do not invent citations.
3. Data: provenance, accessible-source limitations, custom split, label distribution, overlap policy, and version fingerprints.
4. Methods: classical features, actual encoder families, fine-tuning, loss equation, checkpoint selection, and ensemble weight selection.
5. Experimental setup: hardware, exact settings, seed, metrics, data versions, comparison groups, and evaluation exposure.
6. Results: historical test separately, original-data validation, new loss ablation, and conditional ensemble diagnostic.
7. Discussion: neutral tradeoffs, capacity/tokenizer confounds, negative findings, and resource limits.
8. Limitations/ethics: validation reuse, one seed, incomplete transfer study, social-media bias and potentially sensitive content, unresolved data permissions, and no human annotation study.
9. Conclusion: observed findings only; final evaluation and cross-corpus validation as pending work.

### Tables and figures to reuse

- Dataset-size and class-distribution table; exact version for each result.
- Original-data validation table, historical test table, and automated-v3 ablation table as separate objects.
- Per-class F1 table and confusion matrices for HingBERT, Hing-RoBERTa, weighted focal, and newest CE arms.
- Training histories from each run; show selected checkpoint rather than automatically using the final epoch.
- Ensemble weights, search objective, and same-set selection warning.
- Historical bootstrap intervals as conditional uncertainty; no manufactured seed SD or p-values.

### Remaining submission requirements

Freeze the final method using development evidence. Identify a defensible evaluation source, audit overlap with every training/development source, document annotation compatibility, and evaluate the frozen method and a matched baseline. Existing SAIL test data may support transfer evaluation only after appropriate provenance/overlap/protocol checks; preparation alone does not establish an unbiased benchmark. Additional seeds strengthen the key comparison if resources allow. Resolve data-use terms, complete the literature-based novelty argument, and format for the chosen venue. Drafting can start now; acceptance and state-of-the-art performance are not established.

## 9. Reproducibility and engineering notes

Use `.venv-research/Scripts/python.exe`, `run_research.py`, the recorded run config, exact dataset audit, selection.json, checkpoint, and prediction CSV. Model-cache commit IDs and parameter counts are recorded in each training_metadata.json. `requirements-lock.txt` records the project environment. Checkpoints do not save optimizer/resume state. An interrupted run must restart under a new output directory; it is not an exact mid-epoch resume.

The automated queue initially stopped after CE completed because reporting rejected an incompatible historical baseline dataset. Training artifacts survived. Baseline-report paths were corrected, the CE report was recovered, and the queue restarted while skipping its completed run. This was a reporting interruption, not an additional model result. The completed CE run config retains the earlier reporting path for provenance; its training settings were not changed.

Repository .gitignore excludes outputs, prepared data, caches, and checkpoints. Sharing code alone will not share measured evidence: package permitted manifests/results and provide a data-access/preparation procedure. Do not redistribute restricted tweet content or checkpoints without confirming applicable terms.

### Primary references checked for this report

- [Reference paper: Garg et al. (2026), Code-Mix Sentiment Analysis on Hinglish Tweets](https://arxiv.org/abs/2601.05091v1).
- [Patwa et al. (2020), SemEval-2020 Task 9 overview](https://aclanthology.org/2020.semeval-1.100/).
- [HingBERT model card](https://huggingface.co/l3cube-pune/hing-bert) and [Hing-RoBERTa model card](https://huggingface.co/l3cube-pune/hing-roberta).
- [Khanuja et al. (2021), MuRIL](https://arxiv.org/abs/2103.10730).
- [Lin et al., Focal Loss for Dense Object Detection](https://arxiv.org/abs/1708.02002).
- [Derived SAIL release](https://huggingface.co/datasets/satyam-arora-iiit-hyderabad/babyshark-sail2017-stage2); identify and cite the original SAIL task paper before submission.

## Appendix A. Full verified metrics and class-level evidence

### automated_v3_loss_ce / hingroberta_focal / seed 42

Artifacts: `outputs\automated_v3\loss_ce\hingroberta_focal\seed_42`. Selection: `{"selection_split": "validation", "metric": "weighted_f1", "best_epoch": 2, "best_score": 0.6813063270073157}`.

Checkpoint source: `l3cube-pune/hing-roberta`; resolved revision `f714c4bdce6b008a2fbb84193eee99e651c59e15`; parameters 278045955.

#### validation

| Metric | Value |
|---|---:|
| n_examples | 1700 |
| accuracy | 0.68058824 |
| balanced_accuracy | 0.68373076 |
| matthews_correlation | 0.51790280 |
| cohen_kappa | 0.51776249 |
| macro_precision | 0.68718631 |
| macro_recall | 0.68373076 |
| macro_f1 | 0.68530169 |
| weighted_precision | 0.68235252 |
| weighted_recall | 0.68058824 |
| weighted_f1 | 0.68130633 |
| micro_precision | 0.68058824 |
| micro_recall | 0.68058824 |
| micro_f1 | 0.68058824 |
| log_loss | 0.81005263 |
| macro_roc_auc_ovr | 0.83397424 |

| Class | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| negative | 0.723926 | 0.709419 | 0.716599 | 499 |
| neutral | 0.610526 | 0.635368 | 0.622699 | 639 |
| positive | 0.727106 | 0.706406 | 0.716606 | 562 |

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 354 | 130 | 15 |
| neutral | 99 | 406 | 134 |
| positive | 36 | 129 | 397 |

### automated_v3_loss_weighted_ce / hingroberta_focal / seed 42

Artifacts: `outputs\automated_v3\loss_weighted_ce\hingroberta_focal\seed_42`. Selection: `{"selection_split": "validation", "metric": "weighted_f1", "best_epoch": 2, "best_score": 0.6809480496085302}`.

Checkpoint source: `l3cube-pune/hing-roberta`; resolved revision `f714c4bdce6b008a2fbb84193eee99e651c59e15`; parameters 278045955.

#### validation

| Metric | Value |
|---|---:|
| n_examples | 1700 |
| accuracy | 0.67941176 |
| balanced_accuracy | 0.68102998 |
| matthews_correlation | 0.51590474 |
| cohen_kappa | 0.51501795 |
| macro_precision | 0.69025392 |
| macro_recall | 0.68102998 |
| macro_f1 | 0.68466051 |
| weighted_precision | 0.68453542 |
| weighted_recall | 0.67941176 |
| weighted_f1 | 0.68094805 |
| micro_precision | 0.67941176 |
| micro_recall | 0.67941176 |
| micro_f1 | 0.67941176 |
| log_loss | 0.81456343 |
| macro_roc_auc_ovr | 0.83430889 |

| Class | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| negative | 0.735294 | 0.701403 | 0.717949 | 499 |
| neutral | 0.600852 | 0.661972 | 0.629933 | 639 |
| positive | 0.734615 | 0.679715 | 0.706100 | 562 |

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 350 | 135 | 14 |
| neutral | 92 | 423 | 124 |
| positive | 34 | 146 | 382 |

### sentimix_custom_split_v1 / mbert / seed 42

Artifacts: `outputs\sentimix_custom_split_v1\mbert\seed_42`. Selection: `{"selection_split": "validation", "metric": "weighted_f1", "best_epoch": 2, "best_score": 0.6201218034225114}`.

Checkpoint source: `bert-base-multilingual-cased`; resolved revision `3f076fdb1ab68d5b2880cb87a0886f315b8146f8`; parameters 177855747.

#### validation

| Metric | Value |
|---|---:|
| n_examples | 1700 |
| accuracy | 0.62058824 |
| balanced_accuracy | 0.62468893 |
| matthews_correlation | 0.42847674 |
| cohen_kappa | 0.42843888 |
| macro_precision | 0.62291570 |
| macro_recall | 0.62468893 |
| macro_f1 | 0.62375463 |
| weighted_precision | 0.61975475 |
| weighted_recall | 0.62058824 |
| weighted_f1 | 0.62012180 |
| micro_precision | 0.62058824 |
| micro_recall | 0.62058824 |
| micro_f1 | 0.62058824 |
| log_loss | 0.83902643 |
| macro_roc_auc_ovr | 0.79491279 |

| Class | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| negative | 0.632411 | 0.641283 | 0.636816 | 499 |
| neutral | 0.560897 | 0.547731 | 0.554236 | 639 |
| positive | 0.675439 | 0.685053 | 0.680212 | 562 |

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 320 | 150 | 29 |
| neutral | 133 | 350 | 156 |
| positive | 53 | 124 | 385 |

#### test

| Metric | Value |
|---|---:|
| n_examples | 1700 |
| accuracy | 0.62352941 |
| balanced_accuracy | 0.62678322 |
| matthews_correlation | 0.43196269 |
| cohen_kappa | 0.43192439 |
| macro_precision | 0.62880931 |
| macro_recall | 0.62678322 |
| macro_f1 | 0.62774897 |
| weighted_precision | 0.62462290 |
| weighted_recall | 0.62352941 |
| weighted_f1 | 0.62402705 |
| micro_precision | 0.62352941 |
| micro_recall | 0.62352941 |
| micro_f1 | 0.62352941 |
| log_loss | 0.81824913 |
| macro_roc_auc_ovr | 0.80471898 |

| Class | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| negative | 0.642276 | 0.633267 | 0.637740 | 499 |
| neutral | 0.547401 | 0.560250 | 0.553751 | 639 |
| positive | 0.696751 | 0.686833 | 0.691756 | 562 |

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 316 | 161 | 22 |
| neutral | 135 | 358 | 146 |
| positive | 41 | 135 | 386 |

Conditional 95% example-bootstrap intervals: accuracy [0.601176, 0.646485]; macro_f1 [0.605375, 0.650647]; weighted_f1 [0.601505, 0.647089].

### sentimix_custom_split_v1 / naive_bayes / seed 42

Artifacts: `outputs\sentimix_custom_split_v1\naive_bayes\seed_42`. Selection: `{"selection_split": "validation", "metric": "weighted_f1", "best_parameter": 1.0, "trials": [{"parameter": 0.1, "validation_selection_score": 0.5898459143721761}, {"parameter": 0.5, "validation_selection_score": 0.5942368069480045}, {"parameter": 1.0, "validation_selection_score": 0.6033628765924304}]}`.

#### validation

| Metric | Value |
|---|---:|
| n_examples | 1700 |
| accuracy | 0.60294118 |
| balanced_accuracy | 0.60597627 |
| matthews_correlation | 0.40043090 |
| cohen_kappa | 0.40028347 |
| macro_precision | 0.60950456 |
| macro_recall | 0.60597627 |
| macro_f1 | 0.60748117 |
| weighted_precision | 0.60426574 |
| weighted_recall | 0.60294118 |
| weighted_f1 | 0.60336288 |
| micro_precision | 0.60294118 |
| micro_recall | 0.60294118 |
| micro_f1 | 0.60294118 |
| log_loss | 0.85350411 |
| macro_roc_auc_ovr | 0.78085142 |

| Class | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| negative | 0.643923 | 0.605210 | 0.623967 | 499 |
| neutral | 0.522003 | 0.538341 | 0.530046 | 639 |
| positive | 0.662587 | 0.674377 | 0.668430 | 562 |

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 302 | 172 | 25 |
| neutral | 127 | 344 | 168 |
| positive | 40 | 143 | 379 |

#### test

| Metric | Value |
|---|---:|
| n_examples | 1700 |
| accuracy | 0.62647059 |
| balanced_accuracy | 0.62845210 |
| matthews_correlation | 0.43570354 |
| cohen_kappa | 0.43543187 |
| macro_precision | 0.63409006 |
| macro_recall | 0.62845210 |
| macro_f1 | 0.63090559 |
| weighted_precision | 0.62914380 |
| weighted_recall | 0.62647059 |
| weighted_f1 | 0.62744474 |
| micro_precision | 0.62647059 |
| micro_recall | 0.62647059 |
| micro_f1 | 0.62647059 |
| log_loss | 0.85322585 |
| macro_roc_auc_ovr | 0.78701496 |

| Class | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| negative | 0.665957 | 0.627255 | 0.646027 | 499 |
| neutral | 0.550960 | 0.583725 | 0.566869 | 639 |
| positive | 0.685353 | 0.674377 | 0.679821 | 562 |

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 313 | 163 | 23 |
| neutral | 115 | 373 | 151 |
| positive | 42 | 141 | 379 |

Conditional 95% example-bootstrap intervals: accuracy [0.603529, 0.650000]; macro_f1 [0.608386, 0.654185]; weighted_f1 [0.604880, 0.650939].

### sentimix_custom_split_v1 / svm / seed 42

Artifacts: `outputs\sentimix_custom_split_v1\svm\seed_42`. Selection: `{"selection_split": "validation", "metric": "weighted_f1", "best_parameter": 0.5, "trials": [{"parameter": 0.5, "validation_selection_score": 0.5968067944095132}, {"parameter": 1.0, "validation_selection_score": 0.5866460516620667}, {"parameter": 2.0, "validation_selection_score": 0.5737291135299419}]}`.

#### validation

| Metric | Value |
|---|---:|
| n_examples | 1700 |
| accuracy | 0.59882353 |
| balanced_accuracy | 0.60621165 |
| matthews_correlation | 0.39777645 |
| cohen_kappa | 0.39728346 |
| macro_precision | 0.59955898 |
| macro_recall | 0.60621165 |
| macro_f1 | 0.60218646 |
| weighted_precision | 0.59618251 |
| weighted_recall | 0.59882353 |
| weighted_f1 | 0.59680679 |
| micro_precision | 0.59882353 |
| micro_recall | 0.59882353 |
| micro_f1 | 0.59882353 |

| Class | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| negative | 0.610701 | 0.663327 | 0.635927 | 499 |
| neutral | 0.534130 | 0.489828 | 0.511020 | 639 |
| positive | 0.653846 | 0.665480 | 0.659612 | 562 |

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 331 | 137 | 31 |
| neutral | 159 | 313 | 167 |
| positive | 52 | 136 | 374 |

#### test

| Metric | Value |
|---|---:|
| n_examples | 1700 |
| accuracy | 0.61470588 |
| balanced_accuracy | 0.62060933 |
| matthews_correlation | 0.41987326 |
| cohen_kappa | 0.41979341 |
| macro_precision | 0.61837107 |
| macro_recall | 0.62060933 |
| macro_f1 | 0.61935334 |
| weighted_precision | 0.61401584 |
| weighted_recall | 0.61470588 |
| weighted_f1 | 0.61423438 |
| micro_precision | 0.61470588 |
| micro_recall | 0.61470588 |
| micro_f1 | 0.61470588 |

| Class | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| negative | 0.650672 | 0.679359 | 0.664706 | 499 |
| neutral | 0.548644 | 0.538341 | 0.543444 | 639 |
| positive | 0.655797 | 0.644128 | 0.649910 | 562 |

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 339 | 133 | 27 |
| neutral | 132 | 344 | 163 |
| positive | 50 | 150 | 362 |

Conditional 95% example-bootstrap intervals: accuracy [0.591765, 0.637059]; macro_f1 [0.596261, 0.640832]; weighted_f1 [0.591569, 0.635981].

### sentimix_development_v2 / hingbert / seed 42

Artifacts: `outputs\sentimix_development_v2\hingbert\seed_42`. Selection: `{"selection_split": "validation", "metric": "weighted_f1", "best_epoch": 1, "best_score": 0.66861822648274}`.

Checkpoint source: `l3cube-pune/hing-bert`; resolved revision `62cf31a13d65ae3b846456cede60c7d965e5fdd4`; parameters 109484547.

#### validation

| Metric | Value |
|---|---:|
| n_examples | 1700 |
| accuracy | 0.66882353 |
| balanced_accuracy | 0.67128278 |
| matthews_correlation | 0.50030267 |
| cohen_kappa | 0.49981029 |
| macro_precision | 0.67516471 |
| macro_recall | 0.67128278 |
| macro_f1 | 0.67239578 |
| weighted_precision | 0.66993653 |
| weighted_recall | 0.66882353 |
| weighted_f1 | 0.66861823 |
| micro_precision | 0.66882353 |
| micro_recall | 0.66882353 |
| micro_f1 | 0.66882353 |
| log_loss | 0.77472370 |
| macro_roc_auc_ovr | 0.82923863 |

| Class | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| negative | 0.726269 | 0.659319 | 0.691176 | 499 |
| neutral | 0.601550 | 0.607199 | 0.604361 | 639 |
| positive | 0.697674 | 0.747331 | 0.721649 | 562 |

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 329 | 151 | 19 |
| neutral | 88 | 388 | 163 |
| positive | 36 | 106 | 420 |

### sentimix_development_v2 / hingroberta / seed 42

Artifacts: `outputs\sentimix_development_v2\hingroberta\seed_42`. Selection: `{"selection_split": "validation", "metric": "weighted_f1", "best_epoch": 2, "best_score": 0.6641395806929575}`.

Checkpoint source: `l3cube-pune/hing-roberta`; resolved revision `f714c4bdce6b008a2fbb84193eee99e651c59e15`; parameters 278045955.

#### validation

| Metric | Value |
|---|---:|
| n_examples | 1700 |
| accuracy | 0.66705882 |
| balanced_accuracy | 0.67672936 |
| matthews_correlation | 0.50218397 |
| cohen_kappa | 0.50069224 |
| macro_precision | 0.66772114 |
| macro_recall | 0.67672936 |
| macro_f1 | 0.67016095 |
| weighted_precision | 0.66514724 |
| weighted_recall | 0.66705882 |
| weighted_f1 | 0.66413958 |
| micro_precision | 0.66705882 |
| micro_recall | 0.66705882 |
| micro_f1 | 0.66705882 |
| log_loss | 0.79460094 |
| macro_roc_auc_ovr | 0.83730474 |

| Class | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| negative | 0.676976 | 0.789579 | 0.728955 | 499 |
| neutral | 0.618467 | 0.555556 | 0.585326 | 639 |
| positive | 0.707721 | 0.685053 | 0.696203 | 562 |

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 394 | 86 | 19 |
| neutral | 144 | 355 | 140 |
| positive | 44 | 133 | 385 |

### sentimix_development_v2 / hingroberta_focal / seed 42

Artifacts: `outputs\sentimix_development_v2\hingroberta_focal\seed_42`. Selection: `{"selection_split": "validation", "metric": "weighted_f1", "best_epoch": 2, "best_score": 0.6762287332376239}`.

Checkpoint source: `l3cube-pune/hing-roberta`; resolved revision `f714c4bdce6b008a2fbb84193eee99e651c59e15`; parameters 278045955.

#### validation

| Metric | Value |
|---|---:|
| n_examples | 1700 |
| accuracy | 0.67588235 |
| balanced_accuracy | 0.68097694 |
| matthews_correlation | 0.51151558 |
| cohen_kappa | 0.51122609 |
| macro_precision | 0.68238485 |
| macro_recall | 0.68097694 |
| macro_f1 | 0.68126988 |
| weighted_precision | 0.67738650 |
| weighted_recall | 0.67588235 |
| weighted_f1 | 0.67622873 |
| micro_precision | 0.67588235 |
| micro_recall | 0.67588235 |
| micro_f1 | 0.67588235 |
| log_loss | 0.77235535 |
| macro_roc_auc_ovr | 0.83049360 |

| Class | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| negative | 0.719536 | 0.745491 | 0.732283 | 499 |
| neutral | 0.602428 | 0.621283 | 0.611710 | 639 |
| positive | 0.725191 | 0.676157 | 0.699816 | 562 |

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 372 | 111 | 16 |
| neutral | 114 | 397 | 128 |
| positive | 31 | 151 | 380 |

### sentimix_development_v2 / muril / seed 42

Artifacts: `outputs\sentimix_development_v2\muril\seed_42`. Selection: `{"selection_split": "validation", "metric": "weighted_f1", "best_epoch": 2, "best_score": 0.6413626726404213}`.

Checkpoint source: `google/muril-base-cased`; resolved revision `afd9f36c7923d54e97903922ff1b260d091d202f`; parameters 237558531.

#### validation

| Metric | Value |
|---|---:|
| n_examples | 1700 |
| accuracy | 0.64529412 |
| balanced_accuracy | 0.65603289 |
| matthews_correlation | 0.47286758 |
| cohen_kappa | 0.46961830 |
| macro_precision | 0.64628424 |
| macro_recall | 0.65603289 |
| macro_f1 | 0.64681571 |
| weighted_precision | 0.64586139 |
| weighted_recall | 0.64529412 |
| weighted_f1 | 0.64136267 |
| micro_precision | 0.64529412 |
| micro_recall | 0.64529412 |
| micro_f1 | 0.64529412 |
| log_loss | 0.83840136 |
| macro_roc_auc_ovr | 0.80156341 |

| Class | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| negative | 0.616747 | 0.767535 | 0.683929 | 499 |
| neutral | 0.612782 | 0.510172 | 0.556789 | 639 |
| positive | 0.709324 | 0.690391 | 0.699729 | 562 |

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 383 | 97 | 19 |
| neutral | 173 | 326 | 140 |
| positive | 65 | 109 | 388 |

### sentimix_development_v2 / svm / seed 42

Artifacts: `outputs\sentimix_development_v2\svm\seed_42`. Selection: `{"selection_split": "validation", "metric": "weighted_f1", "best_parameter": 0.1, "trials": [{"parameter": 0.1, "validation_selection_score": 0.6004071178313838}, {"parameter": 0.5, "validation_selection_score": 0.5968067944095132}, {"parameter": 1.0, "validation_selection_score": 0.5866460516620667}, {"parameter": 2.0, "validation_selection_score": 0.5737291135299419}, {"parameter": 5.0, "validation_selection_score": 0.5653121873934244}]}`.

#### validation

| Metric | Value |
|---|---:|
| n_examples | 1700 |
| accuracy | 0.60235294 |
| balanced_accuracy | 0.60940277 |
| matthews_correlation | 0.40266468 |
| cohen_kappa | 0.40227491 |
| macro_precision | 0.60321061 |
| macro_recall | 0.60940277 |
| macro_f1 | 0.60578011 |
| weighted_precision | 0.59953412 |
| weighted_recall | 0.60235294 |
| weighted_f1 | 0.60040712 |
| micro_precision | 0.60235294 |
| micro_recall | 0.60235294 |
| micro_f1 | 0.60235294 |

| Class | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| negative | 0.617702 | 0.657315 | 0.636893 | 499 |
| neutral | 0.533898 | 0.492958 | 0.512612 | 639 |
| positive | 0.658031 | 0.677936 | 0.667835 | 562 |

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 328 | 145 | 26 |
| neutral | 152 | 315 | 172 |
| positive | 51 | 130 | 381 |

### sentimix_development_v2 / svm_word_char / seed 42

Artifacts: `outputs\sentimix_development_v2\svm_word_char\seed_42`. Selection: `{"selection_split": "validation", "metric": "weighted_f1", "best_parameter": 0.1, "trials": [{"parameter": 0.1, "validation_selection_score": 0.6248693691945837}, {"parameter": 0.5, "validation_selection_score": 0.6009380738505451}, {"parameter": 1.0, "validation_selection_score": 0.5894263467822061}, {"parameter": 2.0, "validation_selection_score": 0.5810205747866936}, {"parameter": 5.0, "validation_selection_score": 0.5673205684133773}]}`.

#### validation

| Metric | Value |
|---|---:|
| n_examples | 1700 |
| accuracy | 0.62529412 |
| balanced_accuracy | 0.63077836 |
| matthews_correlation | 0.43569897 |
| cohen_kappa | 0.43564950 |
| macro_precision | 0.62876517 |
| macro_recall | 0.63077836 |
| macro_f1 | 0.62969556 |
| weighted_precision | 0.62458880 |
| weighted_recall | 0.62529412 |
| weighted_f1 | 0.62486937 |
| micro_precision | 0.62529412 |
| micro_recall | 0.62529412 |
| micro_f1 | 0.62529412 |

| Class | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| negative | 0.654369 | 0.675351 | 0.664694 | 499 |
| neutral | 0.557508 | 0.546166 | 0.551779 | 639 |
| positive | 0.674419 | 0.670819 | 0.672614 | 562 |

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 337 | 138 | 24 |
| neutral | 132 | 349 | 158 |
| positive | 46 | 139 | 377 |
