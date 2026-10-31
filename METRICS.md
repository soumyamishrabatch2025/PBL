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
