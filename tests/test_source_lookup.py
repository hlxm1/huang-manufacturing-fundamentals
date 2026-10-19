"""Regression tests for page mapping, indexed chapter routes and local OCR search."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT/'skills/huang-manufacturing-fundamentals/scripts/source_lookup.py'


class SourceLookupTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                              capture_output=True, encoding='utf-8')

    def test_page_boundaries(self):
        for printed, pdf in [(1, 11), (228, 238), (311, 321)]:
            result = self.run_cli('--page', printed)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout), {'book_page': printed, 'pdf_page': pdf})
        for invalid in [0, 312]:
            self.assertEqual(self.run_cli('--page', invalid).returncode, 2)

    def test_all_chapters_resolve_to_existing_files(self):
        skill = SCRIPT.parents[1]
        previous_end = 0
        for number in range(1, 10):
            result = self.run_cli('--chapter', number)
            self.assertEqual(result.returncode, 0, result.stderr)
            rows = json.loads(result.stdout)
            self.assertEqual(len(rows), 1)
            row = rows[0]
            self.assertEqual(row['book_start'], previous_end+1)
            self.assertEqual(row['pdf_start'], row['book_start']+10)
            self.assertTrue((skill/row['file']).is_file())
            previous_end = row['book_end']
        self.assertEqual(previous_end, 310)

    def test_topic_and_missing_topic(self):
        rows = json.loads(self.run_cli('--topic', '定位').stdout)
        self.assertIn(5, [r['chapter'] for r in rows])
        self.assertEqual(json.loads(self.run_cli('--topic', 'NO-SUCH-TOPIC').stdout), [])

    def test_local_ocr_search_and_front_matter(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            for number, content in [(4, '目录：尺寸链'), (238, '尺寸链关系：A0=A1-A2')]:
                (folder/f'page-{number:03d}.json').write_text(
                    json.dumps({'pdf_page': number, 'text': content}), encoding='utf-8')
            result = self.run_cli('--search', '尺寸链', '--ocr', folder)
            self.assertEqual(result.returncode, 0, result.stderr)
            rows = json.loads(result.stdout)
            self.assertEqual([r['book_page'] for r in rows], [None, 228])
            self.assertEqual(self.run_cli('--search', ' ', '--ocr', folder).returncode, 2)

    def test_invalid_render_and_wrong_source(self):
        self.assertEqual(self.run_cli('--page', 228, '--render', 'unused.png').returncode, 2)
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            fake_pdf = folder/'different.pdf'
            fake_pdf.write_bytes(b'not the indexed source')
            result = self.run_cli('--page', 228, '--pdf', fake_pdf, '--render', folder/'page.png')
            self.assertEqual(result.returncode, 2)
            self.assertIn('SHA-256', result.stderr)
            self.assertFalse((folder/'page.png').exists())


if __name__ == '__main__':
    unittest.main()
