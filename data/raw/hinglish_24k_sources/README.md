# Dataset sources for arXiv:2601.05091v1

Downloaded on 2026-10-26 for the paper "Code-Mix Sentiment Analysis on Hinglish Tweets".

## Files

- `behele/data.csv`: 17,000 rows; columns `ID`, `Tweet`, `Sentiment Polarity`. Labels: neutral 6,364; positive 5,634; negative 5,002.
  Source cited as reference [17]: https://github.com/saanvibehele/hinglish-sentiment-analysis
  Direct download: https://raw.githubusercontent.com/saanvibehele/hinglish-sentiment-analysis/main/data-main/data.csv
- `behele/README.md`: original source README.
- `sentimix/train_14k_split_conll.txt`: 14,000 training examples. Labels: neutral 5,264; positive 4,634; negative 4,102.
- `sentimix/dev_3k_split_conll.txt`: 3,000 development examples. Labels: neutral 1,128; positive 982; negative 890.
  SentiMix participant archive: https://github.com/JunKong5/Semveal2020-task9
  Direct training download: https://raw.githubusercontent.com/JunKong5/Semveal2020-task9/master/sentimix/dataprocess/hindi/data/train_14k_split_conll.txt
  Direct development download: https://raw.githubusercontent.com/JunKong5/Semveal2020-task9/master/sentimix/dataprocess/hindi/data/dev_3k_split_conll.txt
  Original dataset description: https://aclanthology.org/2020.semeval-1.100/
- `verification.json`: downloaded file sizes, SHA-256 checksums, parsed example counts, label counts, and tweet-ID overlap.

## Important reproduction limits

These are the accessible source datasets, not a verified release of the paper's final Hinglish-24k corpus. The paper reports 24,111 cleaned examples from a GitHub source of approximately 11,000 examples and the SentiMix training set. The currently cited GitHub CSV instead contains 17,000 rows. The supplied paper provides no direct download for its final cleaned corpus or exact example-level splits.

All 14,000 SentiMix training IDs already occur in the GitHub CSV. Combining these two files naively would duplicate those tweet IDs. None of the 3,000 development IDs occurs in the CSV. Source counts must not be added and presented as independent examples. Text in the CSV has also been processed differently from the tokenized source files.

No merging, cleaning, relabeling, or resplitting was performed. Existing project datasets were left untouched. Only the SentiMix training and development sets were downloaded; this folder does not include the SentiMix test set.

## Format

In the SentiMix CoNLL files, each example starts with `meta<TAB>tweet_id<TAB>sentiment`, followed by token/language-tag lines. Blank lines separate examples. Labels are `positive`, `negative`, and `neutral`.

## Attribution and terms

Cite both the source paper and original dataset authors when using these data. The cited GitHub repository does not expose a license file in its downloaded tree; no new license or redistribution rights are asserted here. The participant archive is a mirror, not an organizer-hosted release.
