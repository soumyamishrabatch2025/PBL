# Annotation handoff

The packet is ready now. Annotation can run in parallel with automated experiments.
Use two independent people who understand Hindi-English code mixing.

Reviewer A: `outputs/sentimix_development_v2/neutral_review/reviewer_A.csv`

Reviewer B: `outputs/sentimix_development_v2/neutral_review/reviewer_B.csv`

Each reviewer fills their own 200-row file without seeing the other review, the
answer key, original labels, model predictions, or sampling notes. Preserve case_id,
text, row order, and the CSV columns. Save UTF-8 CSV.

- review_label: negative, neutral, positive, or uncertain.
- confidence: low, medium, or high.
- reason_tags: optional semicolon-separated tags such as sarcasm, mixed_sentiment,
  missing_context, spelling, or unclear_target.
- needs_context: yes or no.
- notes: short explanation when uncertain or mixed.

Judge the overall sentiment expressed in the visible text. Neutral means no clear
positive or negative opinion, not automatically a mixture of both. Preserve an
uncertain judgment when the text cannot support a confident interpretation.
Do not infer missing tweet context or use a model to supply independent judgments.

Return both completed files before adjudication. Agreement is calculated before
discussion; disagreements and uncertain cases are then reviewed together. Any
corrections create a new dataset version and never silently change frozen labels.
This error-enriched packet cannot estimate overall dataset label noise directly.
