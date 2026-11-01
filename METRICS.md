# All model metrics

Generated: 2026-10-31T13:19:36+05:30

Experiment: `sentimix_custom_split_v1`. Only measured results from completed runs are reported.
Accuracy, precision, recall, F1, and ROC-AUC use a 0-1 scale. MCC and kappa range from -1 to 1; log loss is nonnegative and lower is better, with no fixed upper bound. Counts and seconds are explicit.
In single-label multiclass classification, weighted recall and micro precision/recall/F1 equal accuracy; balanced accuracy equals macro recall. These repeated values are expected.
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
| mbert | 42 | 0.6235294118 | 0.6246229018 | 0.6235294118 | 0.6240270480 | 0.6277489654 |
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

### Seed 42

Selection details:

```json
{
  "selection_split": "validation",
  "metric": "weighted_f1",
  "best_epoch": 2,
  "best_score": 0.6201218034225114
}
```

#### Test overall metrics

| Metric | Value |
|---|---:|
| n_examples | 1700 |
| accuracy | 0.6235294118 |
| balanced_accuracy | 0.6267832215 |
| matthews_correlation | 0.4319626872 |
| cohen_kappa | 0.4319243875 |
| macro_precision | 0.6288093123 |
| macro_recall | 0.6267832215 |
| macro_f1 | 0.6277489654 |
| weighted_precision | 0.6246229018 |
| weighted_recall | 0.6235294118 |
| weighted_f1 | 0.6240270480 |
| micro_precision | 0.6235294118 |
| micro_recall | 0.6235294118 |
| micro_f1 | 0.6235294118 |
| log_loss | 0.8182491287 |
| macro_roc_auc_ovr | 0.8047189771 |

#### Test per-class metrics

| Class / average | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| negative | 0.6422764228 | 0.6332665331 | 0.6377396569 | 499 |
| neutral | 0.5474006116 | 0.5602503912 | 0.5537509667 | 639 |
| positive | 0.6967509025 | 0.6868327402 | 0.6917562724 | 562 |
| macro avg | 0.6288093123 | 0.6267832215 | 0.6277489654 | 1700 |
| weighted avg | 0.6246229018 | 0.6235294118 | 0.6240270480 | 1700 |

#### Test confusion matrix (counts)

Rows = actual; columns = predicted. Class order: negative, neutral, positive.

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 316 | 161 | 22 |
| neutral | 135 | 358 | 146 |
| positive | 41 | 135 | 386 |

#### Test confusion matrix (row-normalized)

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 0.6332665331 | 0.3226452906 | 0.0440881764 |
| neutral | 0.2112676056 | 0.5602503912 | 0.2284820031 |
| positive | 0.0729537367 | 0.2402135231 | 0.6868327402 |

Test inference time: 2.2576556000 seconds; throughput: 752.9935035172 examples/second.
[Full metrics JSON](outputs/sentimix_custom_split_v1/mbert/seed_42/test_metrics.json) | [All predictions](outputs/sentimix_custom_split_v1/mbert/seed_42/test_predictions.csv) | [Errors](outputs/sentimix_custom_split_v1/mbert/seed_42/test_errors.csv)

![mbert seed 42 test confusion matrix](outputs/sentimix_custom_split_v1/mbert/seed_42/test_confusion_matrix.png)

#### Validation overall metrics

| Metric | Value |
|---|---:|
| n_examples | 1700 |
| accuracy | 0.6205882353 |
| balanced_accuracy | 0.6246889251 |
| matthews_correlation | 0.4284767440 |
| cohen_kappa | 0.4284388797 |
| macro_precision | 0.6229156999 |
| macro_recall | 0.6246889251 |
| macro_f1 | 0.6237546269 |
| weighted_precision | 0.6197547502 |
| weighted_recall | 0.6205882353 |
| weighted_f1 | 0.6201218034 |
| micro_precision | 0.6205882353 |
| micro_recall | 0.6205882353 |
| micro_f1 | 0.6205882353 |
| log_loss | 0.8390264284 |
| macro_roc_auc_ovr | 0.7949127888 |

#### Validation per-class metrics

| Class / average | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| negative | 0.6324110672 | 0.6412825651 | 0.6368159204 | 499 |
| neutral | 0.5608974359 | 0.5477308294 | 0.5542359462 | 639 |
| positive | 0.6754385965 | 0.6850533808 | 0.6802120141 | 562 |
| macro avg | 0.6229156999 | 0.6246889251 | 0.6237546269 | 1700 |
| weighted avg | 0.6197547502 | 0.6205882353 | 0.6201218034 | 1700 |

#### Validation confusion matrix (counts)

Rows = actual; columns = predicted. Class order: negative, neutral, positive.

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 320 | 150 | 29 |
| neutral | 133 | 350 | 156 |
| positive | 53 | 124 | 385 |

#### Validation confusion matrix (row-normalized)

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 0.6412825651 | 0.3006012024 | 0.0581162325 |
| neutral | 0.2081377152 | 0.5477308294 | 0.2441314554 |
| positive | 0.0943060498 | 0.2206405694 | 0.6850533808 |

Validation inference time: 2.2536159000 seconds; throughput: 754.3432756217 examples/second.
[Full metrics JSON](outputs/sentimix_custom_split_v1/mbert/seed_42/validation_metrics.json) | [All predictions](outputs/sentimix_custom_split_v1/mbert/seed_42/validation_predictions.csv) | [Errors](outputs/sentimix_custom_split_v1/mbert/seed_42/validation_errors.csv)

![mbert seed 42 validation confusion matrix](outputs/sentimix_custom_split_v1/mbert/seed_42/validation_confusion_matrix.png)

#### Test confidence intervals

Stratified test-example bootstrap; excludes training-seed/split uncertainty
Resamples: 1000; bootstrap RNG seed: 42.

| Metric | 95% lower | 95% upper |
|---|---:|---:|
| accuracy | 0.6011764706 | 0.6464852941 |
| macro_f1 | 0.6053747754 | 0.6506471820 |
| weighted_f1 | 0.6015049139 | 0.6470889928 |

#### Training details

Training time: 3657.9305866000 seconds.

| Epoch | Mean training loss | Validation accuracy | Validation macro F1 | Validation weighted F1 | Elapsed seconds |
|---|---:|---:|---:|---:|---:|
| 1 | 0.9529077915361996 | 0.6088235294117647 | 0.6125832292967125 | 0.6098896049056327 | 886.8528256000136 |
| 2 | 0.7882532666852596 | 0.6205882352941177 | 0.6237546268974073 | 0.6201218034225114 | 2254.9470131999697 |
| 3 | 0.6383065755711235 | 0.6176470588235294 | 0.621242130023396 | 0.6180200429280878 | 3657.9269811999984 |

```json
{
  "pretrained_model": "bert-base-multilingual-cased",
  "resolved_snapshot": "C:\\Users\\Soumya\\.cache\\huggingface\\hub\\models--bert-base-multilingual-cased\\snapshots\\3f076fdb1ab68d5b2880cb87a0886f315b8146f8",
  "snapshot_commit": "3f076fdb1ab68d5b2880cb87a0886f315b8146f8",
  "device": "cuda",
  "gpu": "NVIDIA GeForce RTX 4050 Laptop GPU",
  "effective_batch_size": 8,
  "mixed_precision": true,
  "optimizer_steps": 5100,
  "parameter_count": 177855747,
  "length_at_limit_counts": {
    "train": 144,
    "validation": 21,
    "test": 22
  },
  "determinism": "Fixed RNG seeds; cuDNN deterministic; exact cross-device reproducibility is not guaranteed."
}
```

[Recorded config](outputs/sentimix_custom_split_v1/mbert/seed_42/config.json) | [Run environment](outputs/sentimix_custom_split_v1/mbert/seed_42/environment.json)

## Training-seed summary

Single-run standard deviation is unavailable; it is not evidence of zero variability.

### mbert: 1 completed run(s)

| Metric | Mean | Sample standard deviation |
|---|---:|---:|
| accuracy | 0.6235294118 | Not available |
| weighted_precision | 0.6246229018 | Not available |
| weighted_recall | 0.6235294118 | Not available |
| weighted_f1 | 0.6240270480 | Not available |
| macro_precision | 0.6288093123 | Not available |
| macro_recall | 0.6267832215 | Not available |
| macro_f1 | 0.6277489654 | Not available |
| balanced_accuracy | 0.6267832215 | Not available |
| matthews_correlation | 0.4319626872 | Not available |
| cohen_kappa | 0.4319243875 | Not available |

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
| mbert vs naive_bayes | -0.0034176962 | -0.0254157098 | 0.0208564636 |
| mbert vs svm | 0.0097926657 | -0.0159222688 | 0.0348725692 |
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

<!-- DEVELOPMENT_RESULTS_START -->

## Development experiments: validation only

Experiment: `sentimix_development_v2`. These scores are used for model selection and are NOT fresh test results.
The original test results above remain historical baseline measurements. Final generalization needs an untouched, deduplicated evaluation set.

### Validation comparison

| Model | Run group | Seed | Accuracy | Weighted precision | Weighted recall | Weighted F1 | Macro F1 |
|---|---|---:|---:|---:|---:|---:|---:|
| naive_bayes | historical baseline | 42 | 0.6029411765 | 0.6042657426 | 0.6029411765 | 0.6033628766 | 0.6074811674 |
| svm | historical baseline | 42 | 0.5988235294 | 0.5961825086 | 0.5988235294 | 0.5968067944 | 0.6021864648 |
| mbert | historical baseline | 42 | 0.6205882353 | 0.6197547502 | 0.6205882353 | 0.6201218034 | 0.6237546269 |
| hingbert | phase 2 | 42 | 0.6688235294 | 0.6699365350 | 0.6688235294 | 0.6686182265 | 0.6723957753 |
| hingroberta | phase 2 | 42 | 0.6670588235 | 0.6651472445 | 0.6670588235 | 0.6641395807 | 0.6701609474 |
| hingroberta_focal | phase 2 | 42 | 0.6758823529 | 0.6773864996 | 0.6758823529 | 0.6762287332 | 0.6812698754 |
| muril | phase 2 | 42 | 0.6452941176 | 0.6458613922 | 0.6452941176 | 0.6413626726 | 0.6468157089 |
| svm | phase 2 | 42 | 0.6023529412 | 0.5995341236 | 0.6023529412 | 0.6004071178 | 0.6057801052 |
| svm_word_char | phase 2 | 42 | 0.6252941176 | 0.6245887981 | 0.6252941176 | 0.6248693692 | 0.6296955580 |

### hingbert — seed 42

#### Validation metrics

| Metric | Value |
|---|---:|
| n_examples | 1700 |
| accuracy | 0.6688235294 |
| balanced_accuracy | 0.6712827821 |
| matthews_correlation | 0.5003026722 |
| cohen_kappa | 0.4998102927 |
| macro_precision | 0.6751647073 |
| macro_recall | 0.6712827821 |
| macro_f1 | 0.6723957753 |
| weighted_precision | 0.6699365350 |
| weighted_recall | 0.6688235294 |
| weighted_f1 | 0.6686182265 |
| micro_precision | 0.6688235294 |
| micro_recall | 0.6688235294 |
| micro_f1 | 0.6688235294 |
| log_loss | 0.7747237014 |
| macro_roc_auc_ovr | 0.8292386269 |

#### Validation class results

| Class | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| negative | 0.7262693156732892 | 0.6593186372745491 | 0.6911764705882353 | 499.0 |
| neutral | 0.6015503875968993 | 0.6071987480438185 | 0.6043613707165109 | 639.0 |
| positive | 0.6976744186046512 | 0.7473309608540926 | 0.7216494845360825 | 562.0 |

#### Validation confusion matrix

Rows = actual; columns = predicted.

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 329 | 151 | 19 |
| neutral | 88 | 388 | 163 |
| positive | 36 | 106 | 420 |

#### Row-normalized validation confusion matrix

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 0.6593186373 | 0.3026052104 | 0.0380761523 |
| neutral | 0.1377151800 | 0.6071987480 | 0.2550860720 |
| positive | 0.0640569395 | 0.1886120996 | 0.7473309609 |

#### Selection

```json
{
  "selection_split": "validation",
  "metric": "weighted_f1",
  "best_epoch": 1,
  "best_score": 0.66861822648274
}
```

#### Inference timing

```json
{
  "inference_seconds": 2.468774500011932,
  "examples_per_second": 688.6007612245604
}
```

#### Training metadata

```json
{
  "pretrained_model": "l3cube-pune/hing-bert",
  "resolved_snapshot": "C:\\Users\\Soumya\\.cache\\huggingface\\hub\\models--l3cube-pune--hing-bert\\snapshots\\62cf31a13d65ae3b846456cede60c7d965e5fdd4",
  "snapshot_commit": "62cf31a13d65ae3b846456cede60c7d965e5fdd4",
  "device": "cuda",
  "gpu": "NVIDIA GeForce RTX 4050 Laptop GPU",
  "effective_batch_size": 8,
  "mixed_precision": true,
  "evaluation_splits": [
    "validation"
  ],
  "optimizer_steps": 5100,
  "parameter_count": 109484547,
  "length_at_limit_counts": {
    "train": 78,
    "validation": 11
  },
  "determinism": "Fixed RNG seeds; cuDNN deterministic; exact cross-device reproducibility is not guaranteed."
}
```

Training/search elapsed seconds: 1572.02426200005.

#### Epoch history

```csv
epoch,train_loss,validation_weighted_f1,validation_macro_f1,validation_accuracy,elapsed_seconds
1,0.8378697029584679,0.66861822648274,0.6723957752802763,0.6688235294117647,722.8169749000226
2,0.6511044103403119,0.6638714364148564,0.6695173895329457,0.668235294117647,1314.1094460000168
3,0.47382202462750816,0.6683786700971669,0.6721610984455363,0.6688235294117647,1572.015644500032

```

![hingbert validation confusion matrix](outputs/sentimix_development_v2/hingbert/seed_42/validation_confusion_matrix.png)

[Predictions](outputs/sentimix_development_v2/hingbert/seed_42/validation_predictions.csv) | [Errors](outputs/sentimix_development_v2/hingbert/seed_42/validation_errors.csv) | [Config](outputs/sentimix_development_v2/hingbert/seed_42/config.json)


### hingroberta — seed 42

#### Validation metrics

| Metric | Value |
|---|---:|
| n_examples | 1700 |
| accuracy | 0.6670588235 |
| balanced_accuracy | 0.6767293649 |
| matthews_correlation | 0.5021839676 |
| cohen_kappa | 0.5006922433 |
| macro_precision | 0.6677211441 |
| macro_recall | 0.6767293649 |
| macro_f1 | 0.6701609474 |
| weighted_precision | 0.6651472445 |
| weighted_recall | 0.6670588235 |
| weighted_f1 | 0.6641395807 |
| micro_precision | 0.6670588235 |
| micro_recall | 0.6670588235 |
| micro_f1 | 0.6670588235 |
| log_loss | 0.7946009394 |
| macro_roc_auc_ovr | 0.8373047436 |

#### Validation class results

| Class | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| negative | 0.6769759450171822 | 0.7895791583166333 | 0.72895467160037 | 499.0 |
| neutral | 0.6184668989547039 | 0.5555555555555556 | 0.5853256389117889 | 639.0 |
| positive | 0.7077205882352942 | 0.6850533807829181 | 0.6962025316455697 | 562.0 |

#### Validation confusion matrix

Rows = actual; columns = predicted.

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 394 | 86 | 19 |
| neutral | 144 | 355 | 140 |
| positive | 44 | 133 | 385 |

#### Row-normalized validation confusion matrix

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 0.7895791583 | 0.1723446894 | 0.0380761523 |
| neutral | 0.2253521127 | 0.5555555556 | 0.2190923318 |
| positive | 0.0782918149 | 0.2366548043 | 0.6850533808 |

#### Selection

```json
{
  "selection_split": "validation",
  "metric": "weighted_f1",
  "best_epoch": 2,
  "best_score": 0.6641395806929575
}
```

#### Inference timing

```json
{
  "inference_seconds": 8.826818700006697,
  "examples_per_second": 192.5948699953144
}
```

#### Training metadata

```json
{
  "pretrained_model": "l3cube-pune/hing-roberta",
  "resolved_snapshot": "C:\\Users\\Soumya\\.cache\\huggingface\\hub\\models--l3cube-pune--hing-roberta\\snapshots\\f714c4bdce6b008a2fbb84193eee99e651c59e15",
  "snapshot_commit": "f714c4bdce6b008a2fbb84193eee99e651c59e15",
  "device": "cuda",
  "gpu": "NVIDIA GeForce RTX 4050 Laptop GPU",
  "effective_batch_size": 8,
  "mixed_precision": true,
  "evaluation_splits": [
    "validation"
  ],
  "optimizer_steps": 5100,
  "parameter_count": 278045955,
  "length_at_limit_counts": {
    "train": 82,
    "validation": 11
  },
  "determinism": "Fixed RNG seeds; cuDNN deterministic; exact cross-device reproducibility is not guaranteed."
}
```

Training/search elapsed seconds: 4907.453885100025.

#### Epoch history

```csv
epoch,train_loss,validation_weighted_f1,validation_macro_f1,validation_accuracy,elapsed_seconds
1,0.8331669223919825,0.6638840752729638,0.6696881731245127,0.6664705882352941,811.1867168000317
2,0.6701856759230682,0.6641395806929575,0.6701609473859095,0.6670588235294118,2676.2138996000285
3,0.5168506266186238,0.6625464198750394,0.6686349029109682,0.6647058823529411,4907.195782400027

```

![hingroberta validation confusion matrix](outputs/sentimix_development_v2/hingroberta/seed_42/validation_confusion_matrix.png)

[Predictions](outputs/sentimix_development_v2/hingroberta/seed_42/validation_predictions.csv) | [Errors](outputs/sentimix_development_v2/hingroberta/seed_42/validation_errors.csv) | [Config](outputs/sentimix_development_v2/hingroberta/seed_42/config.json)


### hingroberta_focal — seed 42

#### Validation metrics

| Metric | Value |
|---|---:|
| n_examples | 1700 |
| accuracy | 0.6758823529 |
| balanced_accuracy | 0.6809769402 |
| matthews_correlation | 0.5115155797 |
| cohen_kappa | 0.5112260935 |
| macro_precision | 0.6823848481 |
| macro_recall | 0.6809769402 |
| macro_f1 | 0.6812698754 |
| weighted_precision | 0.6773864996 |
| weighted_recall | 0.6758823529 |
| weighted_f1 | 0.6762287332 |
| micro_precision | 0.6758823529 |
| micro_recall | 0.6758823529 |
| micro_f1 | 0.6758823529 |
| log_loss | 0.7723553525 |
| macro_roc_auc_ovr | 0.8304936028 |

#### Validation class results

| Class | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| negative | 0.7195357833655706 | 0.7454909819639278 | 0.7322834645669292 | 499.0 |
| neutral | 0.6024279210925645 | 0.621283255086072 | 0.6117103235747303 | 639.0 |
| positive | 0.7251908396946565 | 0.6761565836298933 | 0.6998158379373849 | 562.0 |

#### Validation confusion matrix

Rows = actual; columns = predicted.

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 372 | 111 | 16 |
| neutral | 114 | 397 | 128 |
| positive | 31 | 151 | 380 |

#### Row-normalized validation confusion matrix

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 0.7454909820 | 0.2224448898 | 0.0320641283 |
| neutral | 0.1784037559 | 0.6212832551 | 0.2003129890 |
| positive | 0.0551601423 | 0.2686832740 | 0.6761565836 |

#### Selection

```json
{
  "selection_split": "validation",
  "metric": "weighted_f1",
  "best_epoch": 2,
  "best_score": 0.6762287332376239
}
```

#### Inference timing

```json
{
  "inference_seconds": 13.665729300002567,
  "examples_per_second": 124.3987761414007
}
```

#### Training metadata

```json
{
  "pretrained_model": "l3cube-pune/hing-roberta",
  "resolved_snapshot": "C:\\Users\\Soumya\\.cache\\huggingface\\hub\\models--l3cube-pune--hing-roberta\\snapshots\\f714c4bdce6b008a2fbb84193eee99e651c59e15",
  "snapshot_commit": "f714c4bdce6b008a2fbb84193eee99e651c59e15",
  "device": "cuda",
  "gpu": "NVIDIA GeForce RTX 4050 Laptop GPU",
  "effective_batch_size": 8,
  "mixed_precision": true,
  "evaluation_splits": [
    "validation"
  ],
  "loss_function": "focal",
  "focal_gamma": 2.0,
  "class_weights": [
    1.0,
    1.25,
    1.0
  ],
  "optimizer_steps": 5100,
  "parameter_count": 278045955,
  "length_at_limit_counts": {
    "train": 82,
    "validation": 11
  },
  "determinism": "Fixed RNG seeds; cuDNN deterministic; exact cross-device reproducibility is not guaranteed."
}
```

Training/search elapsed seconds: 4497.107249399996.

#### Epoch history

```csv
epoch,train_loss,validation_weighted_f1,validation_macro_f1,validation_accuracy,elapsed_seconds
1,0.37154968371270186,0.6705776976314136,0.6743248862263588,0.67,1038.8121955000097
2,0.28330543723248147,0.6762287332376239,0.6812698753596814,0.6758823529411765,2676.730864299985
3,0.20714875426833215,0.6711868306085927,0.6761915612251626,0.6711764705882353,4496.884617000003

```

![hingroberta_focal validation confusion matrix](outputs/sentimix_development_v2/hingroberta_focal/seed_42/validation_confusion_matrix.png)

[Predictions](outputs/sentimix_development_v2/hingroberta_focal/seed_42/validation_predictions.csv) | [Errors](outputs/sentimix_development_v2/hingroberta_focal/seed_42/validation_errors.csv) | [Config](outputs/sentimix_development_v2/hingroberta_focal/seed_42/config.json)


### muril — seed 42

#### Validation metrics

| Metric | Value |
|---|---:|
| n_examples | 1700 |
| accuracy | 0.6452941176 |
| balanced_accuracy | 0.6560328911 |
| matthews_correlation | 0.4728675800 |
| cohen_kappa | 0.4696183021 |
| macro_precision | 0.6462842400 |
| macro_recall | 0.6560328911 |
| macro_f1 | 0.6468157089 |
| weighted_precision | 0.6458613922 |
| weighted_recall | 0.6452941176 |
| weighted_f1 | 0.6413626726 |
| micro_precision | 0.6452941176 |
| micro_recall | 0.6452941176 |
| micro_f1 | 0.6452941176 |
| log_loss | 0.8384013649 |
| macro_roc_auc_ovr | 0.8015634115 |

#### Validation class results

| Class | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| negative | 0.6167471819645732 | 0.7675350701402806 | 0.6839285714285714 | 499.0 |
| neutral | 0.6127819548872181 | 0.5101721439749609 | 0.5567890691716482 | 639.0 |
| positive | 0.7093235831809872 | 0.6903914590747331 | 0.6997294860234445 | 562.0 |

#### Validation confusion matrix

Rows = actual; columns = predicted.

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 383 | 97 | 19 |
| neutral | 173 | 326 | 140 |
| positive | 65 | 109 | 388 |

#### Row-normalized validation confusion matrix

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 0.7675350701 | 0.1943887776 | 0.0380761523 |
| neutral | 0.2707355243 | 0.5101721440 | 0.2190923318 |
| positive | 0.1156583630 | 0.1939501779 | 0.6903914591 |

#### Selection

```json
{
  "selection_split": "validation",
  "metric": "weighted_f1",
  "best_epoch": 2,
  "best_score": 0.6413626726404213
}
```

#### Inference timing

```json
{
  "inference_seconds": 13.401106800010893,
  "examples_per_second": 126.8551937813538
}
```

#### Training metadata

```json
{
  "pretrained_model": "google/muril-base-cased",
  "resolved_snapshot": "C:\\Users\\Soumya\\Code\\PBL\\.hf-cache\\models--google--muril-base-cased\\snapshots\\afd9f36c7923d54e97903922ff1b260d091d202f",
  "snapshot_commit": "afd9f36c7923d54e97903922ff1b260d091d202f",
  "device": "cuda",
  "gpu": "NVIDIA GeForce RTX 4050 Laptop GPU",
  "effective_batch_size": 8,
  "mixed_precision": true,
  "evaluation_splits": [
    "validation"
  ],
  "optimizer_steps": 5100,
  "parameter_count": 237558531,
  "length_at_limit_counts": {
    "train": 100,
    "validation": 16
  },
  "determinism": "Fixed RNG seeds; cuDNN deterministic; exact cross-device reproducibility is not guaranteed."
}
```

Training/search elapsed seconds: 2906.4881979000056.

#### Epoch history

```csv
epoch,train_loss,validation_weighted_f1,validation_macro_f1,validation_accuracy,elapsed_seconds
1,0.9618902465308431,0.6111258290065237,0.6124903746478765,0.6111764705882353,550.8396276000421
2,0.7897208876179376,0.6413626726404213,0.6468157088745548,0.6452941176470588,1529.8508841000148
3,0.6827418172209502,0.6398362258248942,0.6433878021827856,0.6388235294117647,2906.410220400023

```

![muril validation confusion matrix](outputs/sentimix_development_v2/muril/seed_42/validation_confusion_matrix.png)

[Predictions](outputs/sentimix_development_v2/muril/seed_42/validation_predictions.csv) | [Errors](outputs/sentimix_development_v2/muril/seed_42/validation_errors.csv) | [Config](outputs/sentimix_development_v2/muril/seed_42/config.json)


### svm — seed 42

#### Validation metrics

| Metric | Value |
|---|---:|
| n_examples | 1700 |
| accuracy | 0.6023529412 |
| balanced_accuracy | 0.6094027729 |
| matthews_correlation | 0.4026646768 |
| cohen_kappa | 0.4022749130 |
| macro_precision | 0.6032106138 |
| macro_recall | 0.6094027729 |
| macro_f1 | 0.6057801052 |
| weighted_precision | 0.5995341236 |
| weighted_recall | 0.6023529412 |
| weighted_f1 | 0.6004071178 |
| micro_precision | 0.6023529412 |
| micro_recall | 0.6023529412 |
| micro_f1 | 0.6023529412 |

#### Validation class results

| Class | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| negative | 0.6177024482109228 | 0.657314629258517 | 0.6368932038834951 | 499.0 |
| neutral | 0.5338983050847458 | 0.49295774647887325 | 0.5126118795768918 | 639.0 |
| positive | 0.6580310880829016 | 0.6779359430604982 | 0.6678352322524101 | 562.0 |

#### Validation confusion matrix

Rows = actual; columns = predicted.

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 328 | 145 | 26 |
| neutral | 152 | 315 | 172 |
| positive | 51 | 130 | 381 |

#### Row-normalized validation confusion matrix

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 0.6573146293 | 0.2905811623 | 0.0521042084 |
| neutral | 0.2378716745 | 0.4929577465 | 0.2691705790 |
| positive | 0.0907473310 | 0.2313167260 | 0.6779359431 |

#### Selection

```json
{
  "selection_split": "validation",
  "metric": "weighted_f1",
  "best_parameter": 0.1,
  "trials": [
    {
      "parameter": 0.1,
      "validation_selection_score": 0.6004071178313838
    },
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
    },
    {
      "parameter": 5.0,
      "validation_selection_score": 0.5653121873934244
    }
  ]
}
```

#### Inference timing

```json
{
  "inference_seconds": 0.5919392999494448,
  "examples_per_second": 2871.9160902903222
}
```

Training/search elapsed seconds: 56.121831300028134.

![svm validation confusion matrix](outputs/sentimix_development_v2/svm/seed_42/validation_confusion_matrix.png)

[Predictions](outputs/sentimix_development_v2/svm/seed_42/validation_predictions.csv) | [Errors](outputs/sentimix_development_v2/svm/seed_42/validation_errors.csv) | [Config](outputs/sentimix_development_v2/svm/seed_42/config.json)


### svm_word_char — seed 42

#### Validation metrics

| Metric | Value |
|---|---:|
| n_examples | 1700 |
| accuracy | 0.6252941176 |
| balanced_accuracy | 0.6307783636 |
| matthews_correlation | 0.4356989661 |
| cohen_kappa | 0.4356495034 |
| macro_precision | 0.6287651746 |
| macro_recall | 0.6307783636 |
| macro_f1 | 0.6296955580 |
| weighted_precision | 0.6245887981 |
| weighted_recall | 0.6252941176 |
| weighted_f1 | 0.6248693692 |
| micro_precision | 0.6252941176 |
| micro_recall | 0.6252941176 |
| micro_f1 | 0.6252941176 |

#### Validation class results

| Class | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| negative | 0.654368932038835 | 0.6753507014028056 | 0.6646942800788954 | 499.0 |
| neutral | 0.5575079872204473 | 0.5461658841940532 | 0.5517786561264822 | 639.0 |
| positive | 0.6744186046511628 | 0.6708185053380783 | 0.6726137377341659 | 562.0 |

#### Validation confusion matrix

Rows = actual; columns = predicted.

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 337 | 138 | 24 |
| neutral | 132 | 349 | 158 |
| positive | 46 | 139 | 377 |

#### Row-normalized validation confusion matrix

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 0.6753507014 | 0.2765531062 | 0.0480961924 |
| neutral | 0.2065727700 | 0.5461658842 | 0.2472613459 |
| positive | 0.0818505338 | 0.2473309609 | 0.6708185053 |

#### Selection

```json
{
  "selection_split": "validation",
  "metric": "weighted_f1",
  "best_parameter": 0.1,
  "trials": [
    {
      "parameter": 0.1,
      "validation_selection_score": 0.6248693691945837
    },
    {
      "parameter": 0.5,
      "validation_selection_score": 0.6009380738505451
    },
    {
      "parameter": 1.0,
      "validation_selection_score": 0.5894263467822061
    },
    {
      "parameter": 2.0,
      "validation_selection_score": 0.5810205747866936
    },
    {
      "parameter": 5.0,
      "validation_selection_score": 0.5673205684133773
    }
  ]
}
```

#### Inference timing

```json
{
  "inference_seconds": 1.2514281999901868,
  "examples_per_second": 1358.447891787424
}
```

Training/search elapsed seconds: 204.75255269999616.

![svm_word_char validation confusion matrix](outputs/sentimix_development_v2/svm_word_char/seed_42/validation_confusion_matrix.png)

[Predictions](outputs/sentimix_development_v2/svm_word_char/seed_42/validation_predictions.csv) | [Errors](outputs/sentimix_development_v2/svm_word_char/seed_42/validation_errors.csv) | [Config](outputs/sentimix_development_v2/svm_word_char/seed_42/config.json)

### Development training-seed variability

Validation scores were used for checkpoint/model selection; these are descriptive seed statistics, not unbiased final-test estimates.

| Model | Runs | Weighted F1 mean | Sample SD | Macro F1 mean | Sample SD |
|---|---:|---:|---:|---:|---:|
| hingbert | 1 | 0.6686182265 | Not available | 0.6723957753 | Not available |
| hingroberta | 1 | 0.6641395807 | Not available | 0.6701609474 | Not available |
| hingroberta_focal | 1 | 0.6762287332 | Not available | 0.6812698754 | Not available |
| muril | 1 | 0.6413626726 | Not available | 0.6468157089 | Not available |
| svm | 1 | 0.6004071178 | Not available | 0.6057801052 | Not available |
| svm_word_char | 1 | 0.6248693692 | Not available | 0.6296955580 | Not available |

### Multi-model probability ensembles

Uncalibrated soft-voting combining prediction probability distributions across architectures on the frozen validation set (1,700 examples):

#### Phase 4 ensembles (heuristic weights)

| Ensemble Strategy | Accuracy | Macro F1 | Weighted F1 | Negative F1 | Neutral F1 | Positive F1 |
|---|---:|---:|---:|---:|---:|---:|
| Dual-Encoder (BERT + RoBERTa CE) | 0.6788 | 0.6823 | 0.6768 | 0.7315 | 0.6013 | 0.7142 |
| Dual-Encoder (BERT + RoBERTa Focal) | 0.6747 | 0.6792 | 0.6750 | 0.7099 | 0.6102 | 0.7175 |
| Tri-Encoder (BERT + RoBERTa Focal + MuRIL) | 0.6759 | 0.6802 | 0.6756 | 0.7164 | 0.6084 | 0.7158 |
| Quad-Encoder (BERT + RoBERTa CE + Focal + MuRIL) | 0.6806 | 0.6844 | 0.6792 | 0.7304 | 0.6069 | 0.7158 |

#### Phase 5 ensembles (grid search optimized, step=0.05)

Grid search over all (w_hingbert, w_rob_ce, w_rob_focal, w_muril) summing to 1.0 at 0.05 step, maximising Macro F1. Evaluated on frozen validation set (1,700 examples). HB=HingBERT, RC=RoBERTa CE, RF=RoBERTa Focal, MU=MuRIL.

| Ensemble Strategy | Weights (HB/RC/RF/MU) | Accuracy | Macro F1 | Weighted F1 | MCC | Kappa | ROC-AUC | Neg F1 | Neu F1 | Pos F1 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Tri-Equal (HB + RC + RF) | 0.33/0.33/0.33/0.00 | 0.6765 | 0.6803 | 0.6752 | 0.5138 | 0.5135 | 0.8419 | 0.7260 | 0.6039 | 0.7111 |
| Quad-Equal | 0.25/0.25/0.25/0.25 | 0.6841 | 0.6876 | 0.6822 | 0.5263 | 0.5255 | 0.8413 | 0.7395 | 0.6091 | 0.7143 |
| Quad-Tuned (prev best) | 0.35/0.25/0.30/0.10 | 0.6806 | 0.6844 | 0.6792 | 0.5202 | 0.5198 | 0.8424 | 0.7304 | 0.6069 | 0.7158 |
| **Grid-Search Best** | **0.15/0.15/0.40/0.30** | **0.6871** | **0.6908** | **0.6857** | **0.5302** | **0.5296** | **0.8396** | **0.7366** | **0.6167** | **0.7189** |

Grid-search best per-class breakdown (Macro F1 = 0.6908):

| Class | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| negative | 0.7031 | 0.7735 | 0.7366 | 499 |
| neutral | 0.6352 | 0.5994 | 0.6167 | 639 |
| positive | 0.7281 | 0.7100 | 0.7189 | 562 |

Top-10 grid configurations (sorted by Macro F1):

| HingBERT | RoBERTa CE | Focal | MuRIL | Macro F1 | Weighted F1 |
|---:|---:|---:|---:|---:|---:|
| 0.15 | 0.15 | 0.40 | 0.30 | 0.6908 | 0.6857 |
| 0.05 | 0.05 | 0.75 | 0.15 | 0.6905 | 0.6853 |
| 0.10 | 0.00 | 0.75 | 0.15 | 0.6897 | 0.6846 |
| 0.10 | 0.05 | 0.70 | 0.15 | 0.6896 | 0.6845 |
| 0.15 | 0.10 | 0.65 | 0.10 | 0.6894 | 0.6843 |
| 0.15 | 0.10 | 0.55 | 0.20 | 0.6893 | 0.6840 |
| 0.10 | 0.00 | 0.80 | 0.10 | 0.6891 | 0.6842 |
| 0.05 | 0.00 | 0.80 | 0.15 | 0.6891 | 0.6839 |
| 0.40 | 0.35 | 0.00 | 0.25 | 0.6888 | 0.6836 |
| 0.15 | 0.15 | 0.45 | 0.25 | 0.6888 | 0.6834 |

Key finding: Heavy Focal weighting (0.40-0.80) combined with MuRIL (0.15-0.30) consistently outperforms older heuristic weights. The Focal Loss model is the strongest individual contributor to ensemble diversity and Neutral F1 improvement.

### Neutral review

The blinded 200-example validation packet is under `outputs/sentimix_development_v2/neutral_review`. Human annotation/agreement remain pending; no gold labels were changed.

No new test metrics or selection-set confidence intervals are claimed for these development runs.


<!-- AUTOMATED_DIAGNOSTIC_V3 -->
## Automated ensemble diagnostic (development only)

510 examples from the previously used validation set; not comparable to the full 1,700-row results. Base checkpoint selection already used these examples. Temperatures fitted on 680 other validation rows and weights tuned on 510 other rows. No fresh test result or confirmed improvement is claimed.

| Method | Accuracy | Macro F1 | Weighted F1 |
|---|---:|---:|---:|
| Calibrated tuned | 0.6902 | 0.6960 | 0.6913 |
| Equal uncalibrated | 0.7020 | 0.7058 | 0.7008 |

Equal weighting performs better on this diagnostic subset. New preprocessing/loss/corpus training experiments remain untrained; see AUTOMATED_EXPERIMENTS.md.

<!-- automated_v3_loss_ce_START -->

## Development experiments: validation only

Experiment: `automated_v3_loss_ce`. These scores are used for model selection and are NOT fresh test results.
The original test results above remain historical baseline measurements. Final generalization needs an untouched, deduplicated evaluation set.

### Validation comparison

| Model | Run group | Seed | Accuracy | Weighted precision | Weighted recall | Weighted F1 | Macro F1 |
|---|---|---:|---:|---:|---:|---:|---:|
| hingroberta_focal | phase 2 | 42 | 0.6805882353 | 0.6823525172 | 0.6805882353 | 0.6813063270 | 0.6853016917 |

### hingroberta_focal — seed 42

#### Validation metrics

| Metric | Value |
|---|---:|
| n_examples | 1700 |
| accuracy | 0.6805882353 |
| balanced_accuracy | 0.6837307646 |
| matthews_correlation | 0.5179028017 |
| cohen_kappa | 0.5177624932 |
| macro_precision | 0.6871863078 |
| macro_recall | 0.6837307646 |
| macro_f1 | 0.6853016917 |
| weighted_precision | 0.6823525172 |
| weighted_recall | 0.6805882353 |
| weighted_f1 | 0.6813063270 |
| micro_precision | 0.6805882353 |
| micro_recall | 0.6805882353 |
| micro_f1 | 0.6805882353 |
| log_loss | 0.8100526292 |
| macro_roc_auc_ovr | 0.8339742353 |

#### Validation class results

| Class | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| negative | 0.7239263803680982 | 0.7094188376753507 | 0.7165991902834008 | 499.0 |
| neutral | 0.6105263157894737 | 0.6353677621283255 | 0.6226993865030674 | 639.0 |
| positive | 0.7271062271062271 | 0.7064056939501779 | 0.7166064981949458 | 562.0 |

#### Validation confusion matrix

Rows = actual; columns = predicted.

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 354 | 130 | 15 |
| neutral | 99 | 406 | 134 |
| positive | 36 | 129 | 397 |

#### Row-normalized validation confusion matrix

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 0.7094188377 | 0.2605210421 | 0.0300601202 |
| neutral | 0.1549295775 | 0.6353677621 | 0.2097026604 |
| positive | 0.0640569395 | 0.2295373665 | 0.7064056940 |

#### Selection

```json
{
  "selection_split": "validation",
  "metric": "weighted_f1",
  "best_epoch": 2,
  "best_score": 0.6813063270073157
}
```

#### Inference timing

```json
{
  "inference_seconds": 2.625447499973234,
  "examples_per_second": 647.5086628155129
}
```

#### Training metadata

```json
{
  "pretrained_model": "l3cube-pune/hing-roberta",
  "resolved_snapshot": "C:\\Users\\Soumya\\.cache\\huggingface\\hub\\models--l3cube-pune--hing-roberta\\snapshots\\f714c4bdce6b008a2fbb84193eee99e651c59e15",
  "snapshot_commit": "f714c4bdce6b008a2fbb84193eee99e651c59e15",
  "device": "cuda",
  "gpu": "NVIDIA GeForce RTX 4050 Laptop GPU",
  "effective_batch_size": 8,
  "mixed_precision": true,
  "evaluation_splits": [
    "validation"
  ],
  "loss_function": "cross_entropy",
  "focal_gamma": 0.0,
  "class_weights": null,
  "optimizer_steps": 5097,
  "parameter_count": 278045955,
  "length_at_limit_counts": {
    "train": 81,
    "validation": 10
  },
  "determinism": "Fixed RNG seeds; cuDNN deterministic; exact cross-device reproducibility is not guaranteed."
}
```

Training/search elapsed seconds: 2854.45547679998.

#### Epoch history

```csv
epoch,train_loss,validation_weighted_f1,validation_macro_f1,validation_accuracy,elapsed_seconds
1,0.8179185051478671,0.667616443627051,0.6705875843525048,0.6652941176470588,836.4380622999743
2,0.6567644046831734,0.6813063270073157,0.6853016916604714,0.6805882352941176,1852.1819557999843
3,0.4997867239479602,0.6685660714589283,0.6738558868460593,0.6705882352941176,2854.4531110999524

```

![hingroberta_focal validation confusion matrix](outputs/automated_v3/loss_ce/hingroberta_focal/seed_42/validation_confusion_matrix.png)

[Predictions](outputs/automated_v3/loss_ce/hingroberta_focal/seed_42/validation_predictions.csv) | [Errors](outputs/automated_v3/loss_ce/hingroberta_focal/seed_42/validation_errors.csv) | [Config](outputs/automated_v3/loss_ce/hingroberta_focal/seed_42/config.json)

### Development training-seed variability

Validation scores were used for checkpoint/model selection; these are descriptive seed statistics, not unbiased final-test estimates.

| Model | Runs | Weighted F1 mean | Sample SD | Macro F1 mean | Sample SD |
|---|---:|---:|---:|---:|---:|
| hingroberta_focal | 1 | 0.6813063270 | Not available | 0.6853016917 | Not available |

### Neutral review

The blinded 200-example validation packet is under `outputs/automated_v3/loss_ce/neutral_review`. Human annotation/agreement remain pending; no gold labels were changed.

No new test metrics or selection-set confidence intervals are claimed for these development runs.

<!-- automated_v3_loss_ce_END -->

<!-- automated_v3_loss_weighted_ce_START -->

## Development experiments: validation only

Experiment: `automated_v3_loss_weighted_ce`. These scores are used for model selection and are NOT fresh test results.
The original test results above remain historical baseline measurements. Final generalization needs an untouched, deduplicated evaluation set.

### Validation comparison

| Model | Run group | Seed | Accuracy | Weighted precision | Weighted recall | Weighted F1 | Macro F1 |
|---|---|---:|---:|---:|---:|---:|---:|
| hingroberta_focal | phase 2 | 42 | 0.6794117647 | 0.6845354195 | 0.6794117647 | 0.6809480496 | 0.6846605063 |

### hingroberta_focal — seed 42

#### Validation metrics

| Metric | Value |
|---|---:|
| n_examples | 1700 |
| accuracy | 0.6794117647 |
| balanced_accuracy | 0.6810299797 |
| matthews_correlation | 0.5159047384 |
| cohen_kappa | 0.5150179545 |
| macro_precision | 0.6902539250 |
| macro_recall | 0.6810299797 |
| macro_f1 | 0.6846605063 |
| weighted_precision | 0.6845354195 |
| weighted_recall | 0.6794117647 |
| weighted_f1 | 0.6809480496 |
| micro_precision | 0.6794117647 |
| micro_recall | 0.6794117647 |
| micro_f1 | 0.6794117647 |
| log_loss | 0.8145634333 |
| macro_roc_auc_ovr | 0.8343088924 |

#### Validation class results

| Class | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| negative | 0.7352941176470589 | 0.7014028056112225 | 0.717948717948718 | 499.0 |
| neutral | 0.6008522727272727 | 0.6619718309859155 | 0.6299329858525688 | 639.0 |
| positive | 0.7346153846153847 | 0.6797153024911032 | 0.7060998151571165 | 562.0 |

#### Validation confusion matrix

Rows = actual; columns = predicted.

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 350 | 135 | 14 |
| neutral | 92 | 423 | 124 |
| positive | 34 | 146 | 382 |

#### Row-normalized validation confusion matrix

| Actual / predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| negative | 0.7014028056 | 0.2705410822 | 0.0280561122 |
| neutral | 0.1439749609 | 0.6619718310 | 0.1940532081 |
| positive | 0.0604982206 | 0.2597864769 | 0.6797153025 |

#### Selection

```json
{
  "selection_split": "validation",
  "metric": "weighted_f1",
  "best_epoch": 2,
  "best_score": 0.6809480496085302
}
```

#### Inference timing

```json
{
  "inference_seconds": 12.776811399962753,
  "examples_per_second": 133.05354104271711
}
```

#### Training metadata

```json
{
  "pretrained_model": "l3cube-pune/hing-roberta",
  "resolved_snapshot": "C:\\Users\\Soumya\\.cache\\huggingface\\hub\\models--l3cube-pune--hing-roberta\\snapshots\\f714c4bdce6b008a2fbb84193eee99e651c59e15",
  "snapshot_commit": "f714c4bdce6b008a2fbb84193eee99e651c59e15",
  "device": "cuda",
  "gpu": "NVIDIA GeForce RTX 4050 Laptop GPU",
  "effective_batch_size": 8,
  "mixed_precision": true,
  "evaluation_splits": [
    "validation"
  ],
  "loss_function": "focal",
  "focal_gamma": 0.0,
  "class_weights": [
    1.0,
    1.25,
    1.0
  ],
  "optimizer_steps": 5097,
  "parameter_count": 278045955,
  "length_at_limit_counts": {
    "train": 81,
    "validation": 10
  },
  "determinism": "Fixed RNG seeds; cuDNN deterministic; exact cross-device reproducibility is not guaranteed."
}
```

Training/search elapsed seconds: 5040.21333649999.

#### Epoch history

```csv
epoch,train_loss,validation_weighted_f1,validation_macro_f1,validation_accuracy,elapsed_seconds
1,0.8940410999022479,0.6590852762163877,0.6610539166626489,0.6564705882352941,977.1152032000246
2,0.7219500922375053,0.6809480496085302,0.6846605063194677,0.6794117647058824,3164.5362082000356
3,0.5494139267393235,0.674693556440792,0.6789003750676862,0.6752941176470588,5040.1584706000285

```

![hingroberta_focal validation confusion matrix](outputs/automated_v3/loss_weighted_ce/hingroberta_focal/seed_42/validation_confusion_matrix.png)

[Predictions](outputs/automated_v3/loss_weighted_ce/hingroberta_focal/seed_42/validation_predictions.csv) | [Errors](outputs/automated_v3/loss_weighted_ce/hingroberta_focal/seed_42/validation_errors.csv) | [Config](outputs/automated_v3/loss_weighted_ce/hingroberta_focal/seed_42/config.json)

### Development training-seed variability

Validation scores were used for checkpoint/model selection; these are descriptive seed statistics, not unbiased final-test estimates.

| Model | Runs | Weighted F1 mean | Sample SD | Macro F1 mean | Sample SD |
|---|---:|---:|---:|---:|---:|
| hingroberta_focal | 1 | 0.6809480496 | Not available | 0.6846605063 | Not available |

### Neutral review

The blinded 200-example validation packet is under `outputs/automated_v3/loss_weighted_ce/neutral_review`. Human annotation/agreement remain pending; no gold labels were changed.

No new test metrics or selection-set confidence intervals are claimed for these development runs.

<!-- automated_v3_loss_weighted_ce_END -->
