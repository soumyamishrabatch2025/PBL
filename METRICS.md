# All model metrics

Generated: 2026-10-31T12:22:12+05:30

Experiment: `sentimix_custom_split_v1`. Only measured results from completed runs are reported.
Scores are on a 0-1 scale unless stated otherwise; MCC and kappa range from -1 to 1. Counts and seconds are explicit.
Values are rounded to 10 decimal places here; linked JSON artifacts retain full numerical precision.

## Dataset and evaluation protocol

Custom deduplicated split of the SentiMix training/development sources, not the paper's exact Hinglish-24k or official benchmark test set.

| Split | Examples | Negative | Neutral | Positive |
|---|---:|---:|---:|---:|
| train | 13593 | 3993 | 5111 | 4489 |
| validation | 1700 | 499 | 639 | 562 |
| test | 1700 | 499 | 639 | 562 |

Raw examples: 17000; retained: 16993; duplicate rows removed: 3; conflicting/invalid rows excluded: 4.
Split seed: 42. Selection metric: validation `weighted_f1`.
Preprocessing: NFKC, HTML unescape, URL/mention placeholders, hashtag text retained, emoji descriptions; negation and stop words retained.
Leakage checks: No identical casefolded normalized texts or tweet IDs cross splits. Near duplicates/authors/topics are not guaranteed disjoint.

## Model comparison

| Model | Seed | Accuracy | Weighted precision | Weighted recall | Weighted F1 | Macro F1 |
|---|---:|---:|---:|---:|---:|---:|
| naive_bayes | 42 | 0.6264705882 | 0.6291437971 | 0.6264705882 | 0.6274447442 | 0.6309055868 |
| svm | 42 | 0.6147058824 | 0.6140158375 | 0.6147058824 | 0.6142343823 | 0.6193533445 |

## Naive Bayes + TF-IDF

### Seed 42

Selection details:

```json
{
  "selection_split": "validation",
  "metric": "weighted_f1",
  "best_parameter": 1.0,
  "trials": [
    {
      "parameter": 0.1,
      "validation_selection_score": 0.5898459143721761
    },
    {
      "parameter": 0.5,
      "validation_selection_score": 0.5942368069480045
    },
    {
      "parameter": 1.0,
      "validation_selection_score": 0.6033628765924304
    }
  ]
}
```

#### Test overall metrics

| Metric | Value |
|---|---:|
| n_examples | 1700 |
| accuracy | 0.6264705882 |
| balanced_accuracy | 0.6284521010 |
| matthews_correlation | 0.4357035368 |
| cohen_kappa | 0.4354318672 |
| macro_precision | 0.6340900623 |
| macro_recall | 0.6284521010 |
| macro_f1 | 0.6309055868 |
| weighted_precision | 0.6291437971 |
| weighted_recall | 0.6264705882 |
| weighted_f1 | 0.6274447442 |
| micro_precision | 0.6264705882 |
| micro_recall | 0.6264705882 |
| micro_f1 | 0.6264705882 |
| log_loss | 0.8532258477 |
| macro_roc_auc_ovr | 0.7870149566 |

#### Test per-class metrics

| Class / average | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| negative | 0.6659574468 | 0.6272545090 | 0.6460268318 | 499 |
| neutral | 0.5509601182 | 0.5837245696 | 0.5668693009 | 639 |
| positive | 0.6853526221 | 0.6743772242 | 0.6798206278 | 562 |
| macro avg | 0.6340900623 | 0.6284521010 | 0.6309055868 | 1700 |
| weighted avg | 0.6291437971 | 0.6264705882 | 0.6274447442 | 1700 |

#### Test confusion matrix (counts)

Rows = actual; columns = predicted. Class order: negative, neutral, positive.

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 313 | 163 | 23 |
| neutral | 115 | 373 | 151 |
| positive | 42 | 141 | 379 |

#### Test confusion matrix (row-normalized)

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 0.6272545090 | 0.3266533066 | 0.0460921844 |
| neutral | 0.1799687011 | 0.5837245696 | 0.2363067293 |
| positive | 0.0747330961 | 0.2508896797 | 0.6743772242 |

Test inference time: 0.2187271000 seconds; throughput: 7772.2422141474 examples/second.
[Full metrics JSON](outputs/sentimix_custom_split_v1/naive_bayes/seed_42/test_metrics.json) | [All predictions](outputs/sentimix_custom_split_v1/naive_bayes/seed_42/test_predictions.csv) | [Errors](outputs/sentimix_custom_split_v1/naive_bayes/seed_42/test_errors.csv)

![naive_bayes seed 42 test confusion matrix](outputs/sentimix_custom_split_v1/naive_bayes/seed_42/test_confusion_matrix.png)

#### Validation overall metrics

| Metric | Value |
|---|---:|
| n_examples | 1700 |
| accuracy | 0.6029411765 |
| balanced_accuracy | 0.6059762677 |
| matthews_correlation | 0.4004309007 |
| cohen_kappa | 0.4002834739 |
| macro_precision | 0.6095045628 |
| macro_recall | 0.6059762677 |
| macro_f1 | 0.6074811674 |
| weighted_precision | 0.6042657426 |
| weighted_recall | 0.6029411765 |
| weighted_f1 | 0.6033628766 |
| micro_precision | 0.6029411765 |
| micro_recall | 0.6029411765 |
| micro_f1 | 0.6029411765 |
| log_loss | 0.8535041074 |
| macro_roc_auc_ovr | 0.7808514243 |

#### Validation per-class metrics

| Class / average | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| negative | 0.6439232409 | 0.6052104208 | 0.6239669421 | 499 |
| neutral | 0.5220030349 | 0.5383411581 | 0.5300462250 | 639 |
| positive | 0.6625874126 | 0.6743772242 | 0.6684303351 | 562 |
| macro avg | 0.6095045628 | 0.6059762677 | 0.6074811674 | 1700 |
| weighted avg | 0.6042657426 | 0.6029411765 | 0.6033628766 | 1700 |

#### Validation confusion matrix (counts)

Rows = actual; columns = predicted. Class order: negative, neutral, positive.

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 302 | 172 | 25 |
| neutral | 127 | 344 | 168 |
| positive | 40 | 143 | 379 |

#### Validation confusion matrix (row-normalized)

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 0.6052104208 | 0.3446893788 | 0.0501002004 |
| neutral | 0.1987480438 | 0.5383411581 | 0.2629107981 |
| positive | 0.0711743772 | 0.2544483986 | 0.6743772242 |

Validation inference time: 0.2587137000 seconds; throughput: 6570.9701497893 examples/second.
[Full metrics JSON](outputs/sentimix_custom_split_v1/naive_bayes/seed_42/validation_metrics.json) | [All predictions](outputs/sentimix_custom_split_v1/naive_bayes/seed_42/validation_predictions.csv) | [Errors](outputs/sentimix_custom_split_v1/naive_bayes/seed_42/validation_errors.csv)

![naive_bayes seed 42 validation confusion matrix](outputs/sentimix_custom_split_v1/naive_bayes/seed_42/validation_confusion_matrix.png)

#### Test confidence intervals

Stratified test-example bootstrap; excludes training-seed/split uncertainty
Resamples: 1000; bootstrap RNG seed: 42.

| Metric | 95% lower | 95% upper |
|---|---:|---:|
| accuracy | 0.6035294118 | 0.6500000000 |
| macro_f1 | 0.6083857447 | 0.6541846455 |
| weighted_f1 | 0.6048796435 | 0.6509387645 |

#### Training details

Training time: 6.9318572000 seconds (including baseline hyperparameter search).

[Recorded config](outputs/sentimix_custom_split_v1/naive_bayes/seed_42/config.json) | [Run environment](outputs/sentimix_custom_split_v1/naive_bayes/seed_42/environment.json)


## Linear SVM + TF-IDF

### Seed 42

Selection details:

```json
{
  "selection_split": "validation",
  "metric": "weighted_f1",
  "best_parameter": 0.5,
  "trials": [
    {
      "parameter": 0.5,
      "validation_selection_score": 0.5968067944095132
    },
    {
      "parameter": 1.0,
      "validation_selection_score": 0.5866460516620667
    },
    {
      "parameter": 2.0,
      "validation_selection_score": 0.5737291135299419
    }
  ]
}
```

#### Test overall metrics

| Metric | Value |
|---|---:|
| n_examples | 1700 |
| accuracy | 0.6147058824 |
| balanced_accuracy | 0.6206093298 |
| matthews_correlation | 0.4198732603 |
| cohen_kappa | 0.4197934079 |
| macro_precision | 0.6183710749 |
| macro_recall | 0.6206093298 |
| macro_f1 | 0.6193533445 |
| weighted_precision | 0.6140158375 |
| weighted_recall | 0.6147058824 |
| weighted_f1 | 0.6142343823 |
| micro_precision | 0.6147058824 |
| micro_recall | 0.6147058824 |
| micro_f1 | 0.6147058824 |

Log loss and probability ROC-AUC: not computed because LinearSVC does not produce calibrated probabilities.

#### Test per-class metrics

| Class / average | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| negative | 0.6506717850 | 0.6793587174 | 0.6647058824 | 499 |
| neutral | 0.5486443381 | 0.5383411581 | 0.5434439179 | 639 |
| positive | 0.6557971014 | 0.6441281139 | 0.6499102334 | 562 |
| macro avg | 0.6183710749 | 0.6206093298 | 0.6193533445 | 1700 |
| weighted avg | 0.6140158375 | 0.6147058824 | 0.6142343823 | 1700 |

#### Test confusion matrix (counts)

Rows = actual; columns = predicted. Class order: negative, neutral, positive.

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 339 | 133 | 27 |
| neutral | 132 | 344 | 163 |
| positive | 50 | 150 | 362 |

#### Test confusion matrix (row-normalized)

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 0.6793587174 | 0.2665330661 | 0.0541082164 |
| neutral | 0.2065727700 | 0.5383411581 | 0.2550860720 |
| positive | 0.0889679715 | 0.2669039146 | 0.6441281139 |

Test inference time: 0.1036903000 seconds; throughput: 16394.9761903063 examples/second.
[Full metrics JSON](outputs/sentimix_custom_split_v1/svm/seed_42/test_metrics.json) | [All predictions](outputs/sentimix_custom_split_v1/svm/seed_42/test_predictions.csv) | [Errors](outputs/sentimix_custom_split_v1/svm/seed_42/test_errors.csv)

![svm seed 42 test confusion matrix](outputs/sentimix_custom_split_v1/svm/seed_42/test_confusion_matrix.png)

#### Validation overall metrics

| Metric | Value |
|---|---:|
| n_examples | 1700 |
| accuracy | 0.5988235294 |
| balanced_accuracy | 0.6062116455 |
| matthews_correlation | 0.3977764492 |
| cohen_kappa | 0.3972834608 |
| macro_precision | 0.5995589846 |
| macro_recall | 0.6062116455 |
| macro_f1 | 0.6021864648 |
| weighted_precision | 0.5961825086 |
| weighted_recall | 0.5988235294 |
| weighted_f1 | 0.5968067944 |
| micro_precision | 0.5988235294 |
| micro_recall | 0.5988235294 |
| micro_f1 | 0.5988235294 |

Log loss and probability ROC-AUC: not computed because LinearSVC does not produce calibrated probabilities.

#### Validation per-class metrics

| Class / average | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| negative | 0.6107011070 | 0.6633266533 | 0.6359269933 | 499 |
| neutral | 0.5341296928 | 0.4898278560 | 0.5110204082 | 639 |
| positive | 0.6538461538 | 0.6654804270 | 0.6596119929 | 562 |
| macro avg | 0.5995589846 | 0.6062116455 | 0.6021864648 | 1700 |
| weighted avg | 0.5961825086 | 0.5988235294 | 0.5968067944 | 1700 |

#### Validation confusion matrix (counts)

Rows = actual; columns = predicted. Class order: negative, neutral, positive.

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 331 | 137 | 31 |
| neutral | 159 | 313 | 167 |
| positive | 52 | 136 | 374 |

#### Validation confusion matrix (row-normalized)

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 0.6633266533 | 0.2745490982 | 0.0621242485 |
| neutral | 0.2488262911 | 0.4898278560 | 0.2613458529 |
| positive | 0.0925266904 | 0.2419928826 | 0.6654804270 |

Validation inference time: 0.0994528000 seconds; throughput: 17093.5358278762 examples/second.
[Full metrics JSON](outputs/sentimix_custom_split_v1/svm/seed_42/validation_metrics.json) | [All predictions](outputs/sentimix_custom_split_v1/svm/seed_42/validation_predictions.csv) | [Errors](outputs/sentimix_custom_split_v1/svm/seed_42/validation_errors.csv)

![svm seed 42 validation confusion matrix](outputs/sentimix_custom_split_v1/svm/seed_42/validation_confusion_matrix.png)

#### Test confidence intervals

Stratified test-example bootstrap; excludes training-seed/split uncertainty
Resamples: 1000; bootstrap RNG seed: 42.

| Metric | 95% lower | 95% upper |
|---|---:|---:|
| accuracy | 0.5917647059 | 0.6370588235 |
| macro_f1 | 0.5962607769 | 0.6408317836 |
| weighted_f1 | 0.5915694192 | 0.6359810501 |

#### Training details

Training time: 13.8241962000 seconds (including baseline hyperparameter search).

[Recorded config](outputs/sentimix_custom_split_v1/svm/seed_42/config.json) | [Run environment](outputs/sentimix_custom_split_v1/svm/seed_42/environment.json)


## mBERT

No completed run yet. No accuracy, precision, recall, F1, or confusion matrix is available.

Status for seed_42: `training`; optimizer steps 700/5100 at report generation.
## Training-seed summary

Single-run standard deviation is unavailable; it is not evidence of zero variability.

### naive_bayes: 1 completed run(s)

| Metric | Mean | Sample standard deviation |
|---|---:|---:|
| accuracy | 0.6264705882 | Not available |
| weighted_precision | 0.6291437971 | Not available |
| weighted_recall | 0.6264705882 | Not available |
| weighted_f1 | 0.6274447442 | Not available |
| macro_precision | 0.6340900623 | Not available |
| macro_recall | 0.6284521010 | Not available |
| macro_f1 | 0.6309055868 | Not available |
| balanced_accuracy | 0.6284521010 | Not available |
| matthews_correlation | 0.4357035368 | Not available |
| cohen_kappa | 0.4354318672 | Not available |

### svm: 1 completed run(s)

| Metric | Mean | Sample standard deviation |
|---|---:|---:|
| accuracy | 0.6147058824 | Not available |
| weighted_precision | 0.6140158375 | Not available |
| weighted_recall | 0.6147058824 | Not available |
| weighted_f1 | 0.6142343823 | Not available |
| macro_precision | 0.6183710749 | Not available |
| macro_recall | 0.6206093298 | Not available |
| macro_f1 | 0.6193533445 | Not available |
| balanced_accuracy | 0.6206093298 | Not available |
| matthews_correlation | 0.4198732603 | Not available |
| cohen_kappa | 0.4197934079 | Not available |

## Paired model comparisons

Weighted F1 differences use matched test-example bootstrap resampling for fixed seed-42 runs.

| Left model vs right model | Difference (left - right) | 95% lower | 95% upper |
|---|---:|---:|---:|
| naive_bayes vs svm | 0.0132103619 | -0.0035895571 | 0.0315201486 |

Intervals condition on these fitted models/test examples and do not account for training-seed or split uncertainty. No significance or state-of-the-art claim is implied.

## Reproducibility

Frozen split SHA-256 checksums:

```json
{
  "train": "1dd320f3e341d8a23146238ab46c1be60c5efef9196b879f5d378ea7df452708",
  "validation": "eebe157bedbcb7d08499e95098ffccf2495615b02d2e797606c1e004e930b34b",
  "test": "45fa015f13478db77c72cdf730db46abf1bd4c29f8f95cd7779e393cd86cc954"
}
```

Regenerate and print this file with `python run_research.py report` in the research environment. Training commands also regenerate it after completion.
