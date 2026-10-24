import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

BASE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('collector', BASE / 'tools/update_corpus.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
TRACKS = {'subtitles': {'en': [{'ext': 'json3', 'url': 'https://example.invalid/captions'}]}}


class RateLimitTests(unittest.TestCase):
    def test_http_429_exposes_retry_after_without_local_retry(self):
        error = HTTPError('https://example.invalid', 429, 'Too Many Requests', {'Retry-After': '1800'}, None)
        with patch.object(c.urllib.request, 'urlopen', side_effect=error), patch.object(c.time, 'sleep') as sleep:
            with self.assertRaises(c.CaptionRateLimited) as caught:
                c.fetch_json('https://example.invalid')
            self.assertEqual(caught.exception.retry_after, 1800)
            sleep.assert_not_called()

    def test_same_clip_retried_with_fresh_metadata_after_pause(self):
        fresh = dict(TRACKS, title='fresh')
        with patch.object(c, 'captions', side_effect=[c.CaptionRateLimited(1800), ([[0, 2, 'hello']], 'm')]) as captions, patch.object(c, 'info_of', return_value=fresh) as info, patch.object(c.time, 'sleep') as sleep, patch.object(c.time, 'time', return_value=0):
            self.assertEqual(c.captions_with_backoff('clip', TRACKS, 20, 10000)[1], 'm')
            sleep.assert_called_once_with(1800)
            info.assert_called_once_with('clip')
            self.assertEqual(captions.call_args.args, (fresh,))

    def test_persistent_limit_stops_after_three_increasing_pauses(self):
        with patch.object(c, 'captions', side_effect=c.CaptionRateLimited()) as captions, patch.object(c, 'info_of', return_value=TRACKS), patch.object(c.time, 'sleep') as sleep, patch.object(c.time, 'time', return_value=0):
            with self.assertRaises(c.StopCollection): c.captions_with_backoff('clip', TRACKS, 20, 30000)
            self.assertEqual(captions.call_count, 4)
            self.assertEqual([call.args[0] for call in sleep.call_args_list], [1200, 2400, 4800])

    def test_deadline_prevents_another_request(self):
        with patch.object(c, 'captions', side_effect=c.CaptionRateLimited()), patch.object(c.time, 'sleep') as sleep, patch.object(c.time, 'time', return_value=100):
            with self.assertRaises(c.StopCollection): c.captions_with_backoff('clip', TRACKS, 20, 200)
            sleep.assert_not_called()

    def test_no_wait_mode_stops_immediately(self):
        with patch.object(c, 'captions', side_effect=c.CaptionRateLimited()), patch.object(c.time, 'sleep') as sleep:
            with self.assertRaises(c.StopCollection): c.captions_with_backoff('clip', TRACKS, 0, 9999999999)
            sleep.assert_not_called()

    def test_other_http_errors_remain_visible(self):
        error = HTTPError('https://example.invalid', 403, 'Forbidden', {}, None)
        with patch.object(c.urllib.request, 'urlopen', side_effect=error):
            with self.assertRaises(HTTPError): c.fetch_json('https://example.invalid')

    def test_collection_stops_without_losing_saved_clip_or_skipping_blocked_clip(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'tools').mkdir()
            (root / 'tools/channels.tsv').write_text('@channel\tconversation\tNZ\n', encoding='utf-8')
            saved = root / 'clips'
            segments = [[n, 1, 'Hello there.'] for n in range(25)]
            result = type('Result', (), {'stdout': 'first\t120\tFirst clip\nblocked\t120\tSecond clip\nthird\t120\tThird clip'})()
            args = ['collector', '--save-dir', str(saved), '--wait-when-blocked', '0']
            with patch.object(c, 'ROOT', str(root)), patch.object(c, 'load_records', return_value={}), patch.object(c.subprocess, 'run', return_value=result), patch.object(c, 'info_of', return_value=TRACKS) as info, patch.object(c, 'captions', side_effect=[(segments, 'm'), c.CaptionRateLimited()]), patch.object(c.time, 'sleep'), patch.object(sys, 'argv', args):
                c.main()
            self.assertTrue((saved / 'first.json').exists())
            self.assertEqual(json.loads((saved / 'skip.json').read_text()), [])
            self.assertEqual([call.args[0] for call in info.call_args_list], ['first', 'blocked'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
