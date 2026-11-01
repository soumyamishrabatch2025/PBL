import importlib.util
import sys
import unittest
from pathlib import Path
import tempfile
from unittest.mock import patch

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from sentiment_research.improvements import normalize_v2
from sentiment_research.transformer import FocalLoss
from sentiment_research.common import write_csv, write_json

spec = importlib.util.spec_from_file_location('calibrated', Path(__file__).resolve().parents[1] / 'scripts/calibrated_ensemble.py')
ensemble = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ensemble)


class ImprovementTests(unittest.TestCase):
    def test_new_report_sections_preserve_previous_experiments(self):
        from sentiment_research import development
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1] / 'tmp') as temp:
            root = Path(temp)
            out = root / 'outputs/new'
            out.mkdir(parents=True)
            write_json(root/'data/audit.json', {'split_sha256': {}})
            original = '# Historical results\n<!-- DEVELOPMENT_RESULTS_START -->\nold results\n'
            (root/'METRICS.md').write_text(original)
            config = {'output_dir': str(out), 'prepared_dir': str(root/'data'),
                      'baseline_output_dir': str(root/'missing'), 'experiment': 'new',
                      'evaluation_splits': ['validation'],
                      'report_section': 'new_experiment'}
            with patch.object(development, 'ROOT', root):
                development.development_report(config)
                first = (root/'METRICS.md').read_text()
                development.development_report(config)
            final = (root/'METRICS.md').read_text()
            self.assertEqual(first, final)
            self.assertTrue(final.startswith(original.rstrip()))
            self.assertEqual(final.count('<!-- new_experiment_START -->'), 1)

    def test_fragment_cleanup_preserves_sentiment(self):
        result = normalize_v2('USER _ abc nahi achha 😂 https //t.co/abc #Bad!!!')
        self.assertIn('nahi achha', result)
        self.assertIn('EMOJI_', result)
        self.assertIn('Bad!!!', result)
        self.assertNotIn('t.co', result)
        self.assertNotIn('_ abc', result)
        self.assertNotIn('_ abc', normalize_v2('@ _ abc nahi'))

    def test_zero_gamma_matches_cross_entropy_and_gradients(self):
        logits = torch.tensor([[1., 2., 3.], [2., -1., .5]], requires_grad=True)
        labels = torch.tensor([0, 2])
        a = FocalLoss(0)(logits, labels)
        b = torch.nn.functional.cross_entropy(logits, labels)
        self.assertTrue(torch.allclose(a, b))
        self.assertTrue(torch.allclose(torch.autograd.grad(a, logits, retain_graph=True)[0],
                                       torch.autograd.grad(b, logits)[0]))

    def test_focal_alpha_weights_each_target(self):
        logits = torch.zeros((2,3), requires_grad=True)
        labels = torch.tensor([0,1])
        plain = FocalLoss(2)(logits, labels)
        weighted = FocalLoss(2, torch.tensor([1., 3., 1.]))(logits, labels)
        self.assertTrue(torch.allclose(weighted, 2 * plain))

    def test_temperature_scaling_is_normalized_and_identity_at_one(self):
        p = np.array([[.1,.2,.7],[0.,.5,.5]])
        scaled = ensemble.temperature_scale(p, 1.)
        np.testing.assert_allclose(scaled, p, atol=1e-10)
        np.testing.assert_allclose(ensemble.temperature_scale(p, 3.).sum(1), 1.)

    def test_alignment_rejects_reordered_predictions(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1] / 'tmp') as temp:
            a, b = Path(temp)/'a.csv', Path(temp)/'b.csv'
            rows = [dict(tweet_id=str(i),group_id=str(i),text='x',true_label='neutral',
                         p_negative=.1,p_neutral=.8,p_positive=.1) for i in range(2)]
            write_csv(a, rows)
            write_csv(b, rows[::-1])
            with self.assertRaisesRegex(ValueError, 'identities'):
                ensemble.load_aligned([a,b])


if __name__ == '__main__':
    unittest.main()
