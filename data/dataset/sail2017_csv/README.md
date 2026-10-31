# SAIL-2017 CSV files

Use `sanitized/train.csv`, `sanitized/validation.csv`, and `sanitized/test.csv` for experiments. The `raw/` CSVs preserve the alternate raw source version; combining raw and sanitized would duplicate examples.

| Version | Train | Validation | Test |
|---|---:|---:|---:|
| Sanitized | 10,068 | 1,260 | 1,261 |
| Raw | 10,080 | 1,260 | 1,261 |

Columns: `text` (original tweet), `label` (sentiment), `label_id` (negative=0, neutral=1, positive=2). Files are UTF-8, comma-separated, with CSV quoting for text. Existing split membership and row order are preserved. No text normalization, deduplication, merging, or label correction was performed. The label is not part of the text input.

The source files under the supplied Downloads folder are unchanged. `conversion_manifest.json` records source/output hashes, counts, and transformations. If inspecting CSVs with spreadsheet software, import the text column as text: literal leading equals signs are preserved for NLP use.
