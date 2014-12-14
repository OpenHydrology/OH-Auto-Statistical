import unittest
import autostatistical as astat
import os.path
import jinja2.exceptions
from tempfile import TemporaryDirectory
from datetime import date


class TestReport(unittest.TestCase):
    def test_template_exists(self):
        report = astat.Report("", {}, 'plain.md')
        self.assertTrue(os.path.isfile(report.template.filename))

    def test_template_does_not_exist(self):
        self.assertRaises(jinja2.exceptions.TemplateNotFound, astat.Report, "", {}, 'invalid template name.txt')

    def test_template_extension(self):
        report = astat.Report("", {}, 'plain.md')
        self.assertEqual(report.template_extension, '.md')

    def test_template_text(self):
        report = astat.Report("", {}, 'plain.md')
        text = report._get_content()
        self.assertEqual(text[0:26], '# Flood Estimation Report\n')

    def test_save_template(self):
        report = astat.Report("test", {}, 'plain.md')
        with TemporaryDirectory() as folder:
            report.save(folder)
            self.assertTrue(os.path.isfile(os.path.join(folder, 'test.' + date.today().isoformat() + '.md')))

    def test_save_template_invalid_folder(self):
        report = astat.Report("test", {}, 'plain.md')
        folder = '/nonexistingfolder'
        self.assertRaises(FileNotFoundError, report.save, folder)


class TestAnalysis(unittest.TestCase):
    def test_empty_result(self):
        analysis = astat.Analysis('./autostatistical/tests/data/17002.CD3')
        with TemporaryDirectory() as folder:
            analysis.folder = folder
            analysis.create_report()
            self.assertTrue(os.path.isfile(os.path.join(folder, '17002.' + date.today().isoformat() + '.md')))

    def test_result_date(self):
        analysis = astat.Analysis('./autostatistical/tests/data/17002.CD3')
        with TemporaryDirectory() as folder:
            analysis.folder = folder
            analysis.create_report()
            file_path = os.path.join(folder, '17002.' + date.today().isoformat() + '.md')
            with open(file_path) as f:
                for line in f:
                    if line.startswith("Date: "):
                        break
        self.assertEqual(line, "Date: " + date.today().strftime('%d/%m/%Y') + "\n")

    def test_results(self):
        analysis = astat.Analysis('./autostatistical/tests/data/17002.CD3')
        analysis.create_report()
