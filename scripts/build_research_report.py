"""Build a dated evidence snapshot from completed runs, without touching training."""
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

import numpy as np
from sklearn.metrics import classification_report, confusion_matrix

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from sentiment_research.common import ROOT, read_csv, read_json, sha256, write_json
from sentiment_research.evaluation import metrics
from sentiment_research import LABELS, LABEL2ID


def main():
    stamp = datetime.now(timezone(timedelta(hours=5, minutes=30))).isoformat(timespec='seconds')
    destination = ROOT / 'RESEARCH_ANALYSIS_REPORT.md'
    runs, evidence = [], {}

    def read(file):
        file = Path(file)
        evidence[str(file.relative_to(ROOT))] = sha256(file)
        return read_json(file)

    for complete in sorted((ROOT/'outputs').rglob('complete.json')):
        value = read(complete)
        folder = complete.parent
        config = read(folder/'config.json')
        verified = {}
        evaluation_metrics = value.get('evaluation_metrics')
        if evaluation_metrics is None:
            evaluation_metrics = {s: read(folder/f'{s}_metrics.json') for s in ['validation','test']
                                  if (folder/f'{s}_metrics.json').exists()}
            if value.get('test_metrics') != evaluation_metrics.get('test'):
                raise ValueError(f'Legacy completion metrics disagree: {folder}')
        for split, saved in evaluation_metrics.items():
            file = folder / f'{split}_predictions.csv'
            rows = read_csv(file)
            evidence[str(file.relative_to(ROOT))] = sha256(file)
            y = np.array([LABEL2ID[r['true_label']] for r in rows])
            yp = np.array([LABEL2ID[r['predicted_label']] for r in rows])
            probs = (np.array([[float(r['p_'+c]) for c in LABELS] for r in rows])
                     if 'p_negative' in rows[0] else None)
            calculated = metrics(y, yp, probs)
            for name, number in calculated.items():
                if name in saved and not np.isclose(number, saved[name], atol=1e-6, rtol=1e-6):
                    raise ValueError(f'Metric mismatch: {folder}/{split}/{name}')
            matrix = confusion_matrix(y, yp, labels=[0,1,2])
            recorded = read_csv(folder/f'{split}_confusion_matrix.csv')
            if matrix.tolist() != [[int(r[c]) for c in LABELS] for r in recorded]:
                raise ValueError(f'Confusion mismatch: {folder}/{split}')
            verified[split] = {'metrics': saved, 'confusion_matrix': matrix.tolist(),
                               'per_class': classification_report(y,yp,labels=[0,1,2],target_names=LABELS,
                                                                 output_dict=True,zero_division=0)}
        metadata = read(folder/'training_metadata.json') if (folder/'training_metadata.json').exists() else {}
        runs.append({'path': str(folder.relative_to(ROOT)), 'group': folder.relative_to(ROOT).parts[1],
                     'experiment': config['experiment'], 'model': value['model'], 'seed': value['seed'],
                     'config': config, 'completion': value, 'verified': verified, 'metadata': metadata,
                     'selection': read(folder/'selection.json')})
    statuses = []
    for file in sorted((ROOT/'outputs/automated_v3').rglob('status.json')):
        statuses.append({'path': str(file.relative_to(ROOT)), **read_json(file)})
    audits = {}
    for name in ['sentimix_custom_split_v1','sail2017_prepared_v1','automated_v3/sentimix',
                 'automated_v3/sentimix_control','automated_v3/sail','automated_v3/pooled']:
        audits[name] = read(ROOT/'data/research'/name/'audit.json')
        for split, expected in audits[name]['split_sha256'].items():
            file = ROOT/'data/research'/name/(split+'.csv')
            if sha256(file) != expected:
                raise ValueError(f'Dataset hash mismatch: {file}')
            evidence[str(file.relative_to(ROOT))] = expected
    paired = read(ROOT/'outputs/sentimix_custom_split_v1/paired_comparisons.json')
    lines = ['# Research analysis and manuscript preparation report', '',
             f'**Evidence snapshot:** {stamp} (Asia/Calcutta).', '',
             '**Purpose:** a verified basis for writing the paper, not a claim that the study is submission-ready.', '',
             f'{len(runs)} completed fitted runs were found. Saved metrics and confusion matrices were independently recomputed from predictions; all matched within numerical tolerance. Dataset files matched their recorded hashes. Training was neither stopped nor modified to produce this report.', '',
             '## 1. Executive assessment', '',
             'The project is a reproducible empirical study of three-class Hindi-English sentiment classification using classical models, pretrained encoders, loss reweighting, and probability ensembles. It does not introduce a new BERT architecture or pretrain a language model from scratch.', '',
             'The strongest full-validation result currently documented is a selected four-model ensemble: accuracy 68.71%, macro F1 0.6908, weighted F1 0.6857. These are development-set selection scores, not an independent final-test estimate. The best historical test weighted F1 among the three initially tested models belongs to Naive Bayes (0.6274); paired intervals do not establish a clear advantage over mBERT or SVM.', '',
             'The newest matched cross-entropy comparison shows that increasing neutral-class weight does not improve overall weighted or macro F1 for seed 42. This negative result is useful evidence. Human annotation was explicitly skipped by the user; no human agreement, relabeling, or noise-reduction result exists.', '',
             '## 2. Paper framing and research questions', '',
             '**Suggested title:** Domain-Specific Encoders and Loss Reweighting for Hinglish Sentiment Classification: A Controlled Empirical Study.', '',
             '**Defensible contribution:** transparent data provenance, versioned preprocessing, matched classical controls, encoder comparison, neutral-boundary analysis, and explicit separation of development selection from final evaluation. Whether this contribution is novel enough for a venue requires a fuller literature review.', '',
             '- RQ1: Does combining character and word features improve a matched linear SVM?',
             '- RQ2: How do multilingual and Hindi-English domain-adapted encoders compare under the recorded training protocol?',
             '- RQ3: Does neutral-class weighting improve the precision/recall tradeoff and overall performance?',
             '- RQ4: Do probability ensembles improve development performance over individual encoders?',
             '- Future RQ5: Does pooled or cross-corpus training generalize to SAIL? No completed evidence yet.', '',
             '## 3. Data provenance and dataset versions', '',
             'The reference paper is [Garg et al., Code-Mix Sentiment Analysis on Hinglish Tweets](https://arxiv.org/abs/2601.05091v1). Its final Hinglish-24k corpus and exact splits were not reconstructed here. This project is inspired by it, not an exact replication. Dataset or split differences prevent a direct superiority claim against its published score.', '',
             'The local SentiMix source contains 14,000 training and 3,000 development examples from a participant mirror. The [original shared-task overview](https://aclanthology.org/2020.semeval-1.100/) describes the underlying sentiment task. We pool only these accessible source partitions, clean them, and construct a custom stratified split; this is not the official SentiMix benchmark test split.', '',
             'The downloaded alternative Behele CSV is not an independent second corpus: all 14,000 SentiMix training IDs occur in it. It was not merged into the experiments. Existing four-class hate-speech data and classifier checkpoints are outside this sentiment study.', '',
             'SAIL comes from the derived [babyshark-sail2017-stage2 release](https://huggingface.co/datasets/satyam-arora-iiit-hyderabad/babyshark-sail2017-stage2). Raw and sanitized files are overlapping alternatives, not independent data. The text-line sentiment field was separated into a label column; it is not fed to the model. This release must not be represented as an organizer-original archive or as having a verified redistribution license.', '',
             '| Dataset version | Train | Validation | Test | Use |',
             '|---|---:|---:|---:|---|']
    for name, audit in audits.items():
        count = lambda s: audit.get('split_counts',{}).get(s,{}).get('rows',audit.get(s+'_rows','?'))
        lines.append(f'| {name} | {count("train")} | {count("validation")} | {count("test")} | '+
                     ('Historical/phase-2 experiments' if name=='sentimix_custom_split_v1' else
                      'Prepared only / incomplete benchmark' if name=='sail2017_prepared_v1' else 'New development version')+' |')
    lines += ['', 'Original SentiMix cleaning removed three duplicate rows and four rows in two conflicting-text groups, leaving 16,993 examples. Seed 42 creates 13,593/1,700/1,700 examples. Validation and test each contain negative=499, neutral=639, positive=562.', '',
              'The new automated version removes 52 rows across SentiMix and SAIL partitions after stronger normalization and global overlap/conflict filtering. It keeps test text ahead of validation and training, and validation ahead of training. Training conflicts are excluded; labels are not corrected. Exclusion decisions do not use test sentiment labels. SAIL validation loses one overlap with its test partition. Pooled training is deduplicated across corpora.', '',
              'No normalized-text overlap within the audited splits is not proof of semantic, near-duplicate, author, topic, or pretraining-corpus independence. Automated-v3 scores must not be pooled with historical scores as identical-dataset experiments. The matched old-preprocessing control is prepared but not yet completed.', '',
              '### Dataset fingerprints', '', '| Version | Split | SHA-256 |', '|---|---|---|']
    for name, audit in audits.items():
        for split, value in audit['split_sha256'].items():
            lines.append(f'| {name} | {split} | `{value}` |')
    lines += ['', '## 4. Methods and implementation', '',
              'Labels are negative=0, neutral=1, positive=2. Baseline preprocessing uses Unicode NFKC, HTML unescaping, URL/mention placeholders, retained hashtag words, emoji descriptions, and whitespace normalization. Negation and stop words are retained. Transformer inputs preserve case; TF-IDF vectorizers lowercase independently. V2 preprocessing additionally repairs tokenized URLs and anonymized USER underscore fragments. No automatic sentiment-label correction is performed.', '',
              '### Classical baselines', '',
              'Word TF-IDF uses unigrams/bigrams, minimum document frequency 2, at most 60,000 features, and sublinear term frequency. Multinomial NB selects alpha from [0.1,0.5,1.0]. The original LinearSVC selects C from [0.5,1,2]. Matched development SVMs both search [0.1,0.5,1,2,5]; the word+character model adds char_wb 3–5 grams with a 100,000-feature cap, then L2-normalizes concatenated features. Vocabulary and IDF are fitted on training only.', '',
              '### Pretrained encoders', '',
              '[HingBERT](https://huggingface.co/l3cube-pune/hing-bert) is a BERT-family checkpoint adapted to romanized Hindi-English text. [Hing-RoBERTa](https://huggingface.co/l3cube-pune/hing-roberta) is **XLM-RoBERTa-based**; do not call this particular checkpoint an ordinary English RoBERTa or assume byte-level BPE from its short name. [MuRIL](https://arxiv.org/abs/2103.10730) is pretrained for Indian languages including translated/transliterated training signals. Model families differ in parameter count and tokenizer, so this is a comparison of available systems, not a controlled pretraining-only causal experiment.', '',
              'All encoder parameters are fine-tuned with a newly initialized three-class classification head; no extra transformer layers are added. The old four-class hate-speech HingBERT classifier is not reused.', '',
              'Default transformer settings: AdamW; learning rate 2e-5; weight decay 0.01 excluding bias/normalization parameters; 500 warmup steps; length 128; microbatch 4; accumulation 2 (effective batch 8); at most 3 epochs; gradient clipping 1.0; mixed precision and gradient checkpointing. mBERT evaluation batch is 16, later encoders use 8. Best checkpoint is selected by validation weighted F1. Automated-v3 adds patience-one early stopping. Hardware recorded: NVIDIA RTX 4050 Laptop GPU, approximately 6 GB VRAM. All completed runs in this snapshot use seed 42.', '',
              '### Loss definitions', '',
              'For correct-class probability p_y, the implemented loss is `mean[-alpha_y * (1-p_y)^gamma * log(p_y)]`. Standard CE sets gamma=0 and alpha=1; neutral-weighted CE uses [1,1.25,1] in negative/neutral/positive order; focal-only uses gamma=2 and alpha=1; weighted focal combines gamma=2 with [1,1.25,1]. Target weights multiply per-example losses before the batch mean, rather than dividing by the sum of target weights. The focal mechanism follows [Lin et al.](https://arxiv.org/abs/1708.02002); applying it here is not a new loss invention.', '',
              'The historical focal run changed both gamma and class weights; it cannot isolate their individual effects. The automated four-arm loss ablation is designed to do so but is incomplete.', '',
              '### Metrics and uncertainty', '',
              'Accuracy is correct/N. Per-class precision=TP/(TP+FP), recall=TP/(TP+FN), and F1 is their harmonic mean. Macro F1 averages three class F1 scores equally; weighted F1 weights by class support. Weighted recall equals accuracy in this single-label setting. Confusion matrices below use actual rows and predicted columns ordered negative, neutral, positive. Probability models additionally supply log loss and macro one-vs-rest AUC; uncalibrated SVM has no such probability metrics.', '',
              'Historical test intervals use 1,000 stratified example-bootstrap resamples and describe uncertainty conditional on fitted runs. They exclude seed/split uncertainty. Validation-selection scores and weight-search scores are not unbiased generalization estimates. No significance comparison against a published aggregate paper score is valid without matched examples/predictions.', '',
              '## 5. Completed results, separated by protocol', '']
    def table(selected, split):
        lines.extend(['| Model / experiment | N | Accuracy (%) | Weighted precision | Weighted recall | Weighted F1 | Macro F1 |',
                      '|---|---:|---:|---:|---:|---:|---:|'])
        for run in selected:
            m = run['verified'][split]['metrics']
            title = run['experiment'] if run['group']=='automated_v3' else run['model']
            lines.append(f'| {title} | {m["n_examples"]} | {100*m["accuracy"]:.2f} | {m["weighted_precision"]:.4f} | {m["weighted_recall"]:.4f} | {m["weighted_f1"]:.4f} | {m["macro_f1"]:.4f} |')
    historical = [r for r in runs if r['group']=='sentimix_custom_split_v1']
    development = [r for r in runs if r['group']=='sentimix_development_v2']
    automated = [r for r in runs if r['group']=='automated_v3']
    lines += ['### A. Historical custom test, original preprocessing', '']
    table(historical, 'test')
    lines += ['', 'These are the initial measured custom-test results. Later development has occurred after this test was exposed. Do not describe it as a newly untouched final test for the current selected system.', '',
              '### B. Historical and phase-2 validation on the original frozen data', '']
    table(historical+development,'validation')
    lines += ['', '### C. Automated-v3 validation, revised training version', '']
    table(automated,'validation')
    lines += ['', 'Run-directory names such as `hingroberta_focal` are reused as backbone identifiers in automated-v3, even for CE runs. The experiment name, focal_gamma, and class_weights determine the actual loss. Do not label every such directory a focal-loss experiment.', '',
              '### D. Ensemble evidence', '']
    ce = next((r for r in automated if r['experiment']=='automated_v3_loss_ce'),None)
    weighted = next((r for r in automated if r['experiment']=='automated_v3_loss_weighted_ce'),None)
    if ce and weighted:
        # Insert the matched tradeoff before the ensemble subsection.
        lines[-2:-2] = ['### Matched neutral-weighting tradeoff', '',
                        '| Loss | Neutral precision | Neutral recall | Neutral F1 | Positive F1 |',
                        '|---|---:|---:|---:|---:|'] + [
            f'| {name} | {r["verified"]["validation"]["per_class"]["neutral"]["precision"]:.4f} | {r["verified"]["validation"]["per_class"]["neutral"]["recall"]:.4f} | {r["verified"]["validation"]["per_class"]["neutral"]["f1-score"]:.4f} | {r["verified"]["validation"]["per_class"]["positive"]["f1-score"]:.4f} |'
            for name,r in [('CE',ce),('Neutral-weighted CE',weighted)]] + ['',
            'Neutral weighting increases neutral recall and F1 while decreasing neutral precision and positive F1. It therefore changes the class tradeoff rather than improving overall F1. This observation is descriptive for one seed.', '']
    names = ['hingbert','hingroberta','hingroberta_focal','muril']
    arrays, ref, ensemble_rows = [], None, None
    for name in names:
        file = ROOT/f'outputs/sentimix_development_v2/{name}/seed_42/validation_predictions.csv'
        rows = read_csv(file)
        identity = [(r['tweet_id'],r['group_id'],r['text'],r['true_label']) for r in rows]
        if ref is not None and ref != identity:
            raise ValueError('Ensemble inputs are misaligned')
        ref, ensemble_rows = identity, rows
        arrays.append(np.array([[float(r['p_'+c]) for c in LABELS] for r in rows]))
    combined = sum(w*p for w,p in zip([.15,.15,.4,.3],arrays))
    combined /= combined.sum(1,keepdims=True)
    y = np.array([LABEL2ID[r['true_label']] for r in ensemble_rows])
    em = metrics(y,combined.argmax(1),combined)
    er = classification_report(y,combined.argmax(1),labels=[0,1,2],target_names=LABELS,output_dict=True,zero_division=0)
    lines += [f'The recorded selected weights [0.15,0.15,0.40,0.30] for HingBERT / Hing-RoBERTa CE / Hing-RoBERTa weighted focal / MuRIL reproduce accuracy {100*em["accuracy"]:.2f}%, macro F1 {em["macro_f1"]:.4f}, weighted F1 {em["weighted_f1"]:.4f}, and neutral F1 {er["neutral"]["f1-score"]:.4f}. Input IDs, text, labels, and ordering were verified. The original script searched simplex weights at step 0.05 to maximize macro F1 on this same validation set. This report recomputes the recorded winner, not an independent re-run of the entire search.', '',
              'Historical ensembles are uncalibrated probability averages, not training out-of-fold predictions. A later diagnostic fits temperatures on 680 validation rows and ensemble weights on 510, then diagnoses on 510 other rows. Base checkpoints had already used all validation examples for checkpoint selection, so even its diagnostic split is not independently untouched.', '',
              '| 510-row development diagnostic | Accuracy (%) | Macro F1 | Weighted F1 |', '|---|---:|---:|---:|']
    for method, filename in [('Calibrated tuned','development_diagnostic_metrics.json'),('Equal uncalibrated','equal_uncalibrated_diagnostic_metrics.json')]:
        m = read(ROOT/'outputs/automated_v3/calibrated_ensemble'/filename)
        lines.append(f'| {method} | {100*m["accuracy"]:.2f} | {m["macro_f1"]:.4f} | {m["weighted_f1"]:.4f} |')
    lines += ['', 'Calibration did not outperform equal weighting in this diagnostic. These subset scores must not be ranked directly against full-validation scores.', '',
              '#### Selected full-validation ensemble: class evidence', '',
              '| Class | Precision | Recall | F1 | Support |', '|---|---:|---:|---:|---:|']
    for label in LABELS:
        c=er[label]
        lines.append(f'| {label} | {c["precision"]:.6f} | {c["recall"]:.6f} | {c["f1-score"]:.6f} | {int(c["support"])} |')
    lines += ['', '| Actual / predicted | Negative | Neutral | Positive |', '|---|---:|---:|---:|']
    for label,counts in zip(LABELS,confusion_matrix(y,combined.argmax(1),labels=[0,1,2]).tolist()):
        lines.append('| '+label+' | '+' | '.join(map(str,counts))+' |')
    lines += ['',
              '### E. Historical paired uncertainty', '', '| Comparison | Weighted F1 difference | Paired bootstrap 95% interval |', '|---|---:|---|']
    for name, result in paired.items():
        lo,hi = result['paired_bootstrap_95_percent_interval']
        lines.append(f'| {name} | {result["weighted_f1_difference_left_minus_right"]:.4f} | [{lo:.4f}, {hi:.4f}] |')
    lines += ['', 'All displayed paired intervals contain zero. The historical test evidence does not establish a clear difference for these fitted runs.', '',
              '## 6. Interpretation and claim boundaries', '',
              '- The matched word+character SVM improves validation weighted F1 over the matched word-only SVM. Attribute this comparison to the matched feature experiment, not to the original SVM with a different C grid.',
              '- On original-data validation, HingBERT outperforms local mBERT in weighted F1; MuRIL is weaker than the two Hinglish-adapted encoders in this run. This is seed-42 development evidence, not a universal ranking.',
              '- Historical weighted focal improves Hing-RoBERTa development scores and neutral F1, but gamma and neutral weighting changed simultaneously. Do not claim focal loss alone caused the improvement.',
              '- Neutral remains the weakest class in key original-data encoder/ensemble results. Confusion matrices quantify this; causes such as sarcasm or annotation noise remain hypotheses without systematic human validation.',
              '- New CE vs weighted CE isolates neutral reweighting under the same automated-v3 data/settings. Overall F1 does not improve. Examine per-class recall and precision to explain the tradeoff; a class-level increase is not an overall gain.',
              '- The selected ensemble is strongest among the full original-validation systems discussed here, but weights are tuned on that same set. Do not call it a fresh-test result, calibrated system, production-ready model, or state of the art.',
              '- An apparent gain from historical Hing-RoBERTa to automated CE cannot isolate preprocessing: retained training examples and early-stopping protocol also changed. Await the matched preprocessing control.', '',
              '## 7. Ongoing and uncompleted work at snapshot', '', '| Experiment / artifact | State | Details |', '|---|---|---|']
    completed = {r['experiment'] for r in automated}
    plan = read(ROOT/'outputs/automated_v3/experiment_plan.json')
    for item in plan:
        config = read(ROOT/item['config'])
        matching = [s for s in statuses if f'/{item["name"]}/' in s['path'].replace('\\','/')]
        status = matching[0] if matching else {}
        done = config['experiment'] in completed
        detail = (f'epoch {status.get("epoch","?")}, step {status.get("step","?")}/{status.get("total_steps","?")}'
                  if not done and status else 'No completed evidence' if not done else 'Included above')
        lines.append(f'| {item["name"]} | {"complete" if done else status.get("status","not started")} | {detail} |')
    lines += ['| Earlier SAIL benchmark | incomplete | A status file is not a completed training result |',
              '| Cross-corpus evaluation | not completed | Evaluation utility exists; no measured result in this snapshot |',
              '| Seeds 43 and 44 | not completed | Do not report mean ± SD across seeds |',
              '| Independent human annotation | skipped by user | No label corrections or agreement scores |', '',
              'The running queue remains authorized and active; this snapshot does not stop it. Current progress is not an accuracy estimate. New results after this timestamp require an updated report.', '',
              '## 8. Manuscript-ready material', '',
              '### Draft abstract (development study; revise after final evaluation)', '',
              '> We investigate three-class sentiment classification of Hindi-English code-mixed social-media text using classical TF-IDF models and pretrained multilingual and domain-adapted encoders. We construct a versioned custom split from accessible SentiMix source partitions, document duplicate and label-conflict handling, and compare models using common evaluation artifacts. On the original 1,700-example development partition, a validation-selected ensemble achieves macro F1 0.6908 and weighted F1 0.6857. A matched feature experiment supports character n-grams as a useful addition to a word-based SVM. In a revised-data comparison, neutral-class weighting does not improve overall F1 over standard cross-entropy for seed 42. We report class-level errors and distinguish development selection from generalization. These results are preliminary because repeated validation use, single-seed training, and the absence of an independent final evaluation limit conclusions.', '',
              '### Recommended section structure', '',
              '1. Introduction: code mixing, romanization variability, neutral-boundary difficulty, and the specific empirical questions.',
              '2. Related work: SentiMix, the reference paper, HingCorpus/HingBERT/Hing-RoBERTa, MuRIL, focal loss, and recent task-specific comparisons. Establish novelty through additional verified reading; do not invent citations.',
              '3. Data: provenance, accessible-source limitations, custom split, label distribution, overlap policy, and version fingerprints.',
              '4. Methods: classical features, actual encoder families, fine-tuning, loss equation, checkpoint selection, and ensemble weight selection.',
              '5. Experimental setup: hardware, exact settings, seed, metrics, data versions, comparison groups, and evaluation exposure.',
              '6. Results: historical test separately, original-data validation, new loss ablation, and conditional ensemble diagnostic.',
              '7. Discussion: neutral tradeoffs, capacity/tokenizer confounds, negative findings, and resource limits.',
              '8. Limitations/ethics: validation reuse, one seed, incomplete transfer study, social-media bias and potentially sensitive content, unresolved data permissions, and no human annotation study.',
              '9. Conclusion: observed findings only; final evaluation and cross-corpus validation as pending work.', '',
              '### Tables and figures to reuse', '',
              '- Dataset-size and class-distribution table; exact version for each result.',
              '- Original-data validation table, historical test table, and automated-v3 ablation table as separate objects.',
              '- Per-class F1 table and confusion matrices for HingBERT, Hing-RoBERTa, weighted focal, and newest CE arms.',
              '- Training histories from each run; show selected checkpoint rather than automatically using the final epoch.',
              '- Ensemble weights, search objective, and same-set selection warning.',
              '- Historical bootstrap intervals as conditional uncertainty; no manufactured seed SD or p-values.', '',
              '### Remaining submission requirements', '',
              'Freeze the final method using development evidence. Identify a defensible evaluation source, audit overlap with every training/development source, document annotation compatibility, and evaluate the frozen method and a matched baseline. Existing SAIL test data may support transfer evaluation only after appropriate provenance/overlap/protocol checks; preparation alone does not establish an unbiased benchmark. Additional seeds strengthen the key comparison if resources allow. Resolve data-use terms, complete the literature-based novelty argument, and format for the chosen venue. Drafting can start now; acceptance and state-of-the-art performance are not established.', '',
              '## 9. Reproducibility and engineering notes', '',
              'Use `.venv-research/Scripts/python.exe`, `run_research.py`, the recorded run config, exact dataset audit, selection.json, checkpoint, and prediction CSV. Model-cache commit IDs and parameter counts are recorded in each training_metadata.json. `requirements-lock.txt` records the project environment. Checkpoints do not save optimizer/resume state. An interrupted run must restart under a new output directory; it is not an exact mid-epoch resume.', '',
              'The automated queue initially stopped after CE completed because reporting rejected an incompatible historical baseline dataset. Training artifacts survived. Baseline-report paths were corrected, the CE report was recovered, and the queue restarted while skipping its completed run. This was a reporting interruption, not an additional model result. The completed CE run config retains the earlier reporting path for provenance; its training settings were not changed.', '',
              'Repository .gitignore excludes outputs, prepared data, caches, and checkpoints. Sharing code alone will not share measured evidence: package permitted manifests/results and provide a data-access/preparation procedure. Do not redistribute restricted tweet content or checkpoints without confirming applicable terms.', '',
              '### Primary references checked for this report', '',
              '- [Reference paper: Garg et al. (2026), Code-Mix Sentiment Analysis on Hinglish Tweets](https://arxiv.org/abs/2601.05091v1).',
              '- [Patwa et al. (2020), SemEval-2020 Task 9 overview](https://aclanthology.org/2020.semeval-1.100/).',
              '- [HingBERT model card](https://huggingface.co/l3cube-pune/hing-bert) and [Hing-RoBERTa model card](https://huggingface.co/l3cube-pune/hing-roberta).',
              '- [Khanuja et al. (2021), MuRIL](https://arxiv.org/abs/2103.10730).',
              '- [Lin et al., Focal Loss for Dense Object Detection](https://arxiv.org/abs/1708.02002).',
              '- [Derived SAIL release](https://huggingface.co/datasets/satyam-arora-iiit-hyderabad/babyshark-sail2017-stage2); identify and cite the original SAIL task paper before submission.', '',
              '## Appendix A. Full verified metrics and class-level evidence', '']
    for run in runs:
        lines += [f'### {run["experiment"]} / {run["model"]} / seed {run["seed"]}', '',
                  f'Artifacts: `{run["path"]}`. Selection: `{json.dumps(run["selection"], ensure_ascii=False)}`.', '']
        if run['metadata']:
            meta=run['metadata']
            lines += [f'Checkpoint source: `{meta.get("pretrained_model")}`; resolved revision `{meta.get("snapshot_commit")}`; parameters {meta.get("parameter_count")}.', '']
        for split, result in run['verified'].items():
            lines += [f'#### {split}', '', '| Metric | Value |','|---|---:|']
            for name, value in result['metrics'].items():
                lines.append(f'| {name} | {value:.8f} |' if isinstance(value,float) else f'| {name} | {value} |')
            lines += ['', '| Class | Precision | Recall | F1 | Support |','|---|---:|---:|---:|---:|']
            for label in LABELS:
                c=result['per_class'][label]
                lines.append(f'| {label} | {c["precision"]:.6f} | {c["recall"]:.6f} | {c["f1-score"]:.6f} | {int(c["support"])} |')
            lines += ['', '| Actual / predicted | Negative | Neutral | Positive |','|---|---:|---:|---:|']
            for label, counts in zip(LABELS,result['confusion_matrix']):
                lines.append('| '+label+' | '+' | '.join(map(str,counts))+' |')
            file=ROOT/run['path']/f'{split}_bootstrap.json'
            if file.exists():
                ci=read(file)['95_percent_intervals']
                lines += ['', 'Conditional 95% example-bootstrap intervals: '+ '; '.join(f'{k} [{v[0]:.6f}, {v[1]:.6f}]' for k,v in ci.items())+'.']
            lines.append('')
    snapshot={'timestamp_ist':stamp,'verification':'All saved scalar metrics and confusion matrices matched recomputed predictions; all dataset hashes matched.',
              'runs':runs,'statuses':statuses,'datasets':audits,'ensemble_metrics':em,'ensemble_per_class':er,
              'source_sha256':evidence}
    write_json(ROOT/'reports/research_evidence_snapshot.json',snapshot)
    destination.write_text('\n'.join(lines).rstrip()+'\n',encoding='utf-8')
    print(f'Wrote {destination}; {len(runs)} runs; {sum(len(r["verified"]) for r in runs)} evaluations verified; {len(lines)} report elements')


if __name__=='__main__':
    main()
