import unittest
import autostatistical as astat
import autostatistical.template as templ
import os.path
import shutil
import jinja2.exceptions
from tempfile import TemporaryDirectory
from datetime import date
from appdirs import AppDirs


class TestReport(unittest.TestCase):
    empty_context = {'catchment': {'point': {}, 'descriptors': {'centroid_ngr': {}}},
                     'nrfa': {},
                     'qmed': {},
                     'gc': {'distr_params': {}}}

    def test_template_exists(self):
        report = astat.Report("", {}, 'normal.md')
        self.assertTrue(os.path.isfile(report.template.filename))

    def test_template_does_not_exist(self):
        self.assertRaises(jinja2.exceptions.TemplateNotFound, astat.Report, "", {}, 'invalid template name.txt')

    def test_template_extension(self):
        report = astat.Report("", {}, 'normal.md')
        self.assertEqual(report.template_extension, '.md')

    def test_template_text(self):
        report = astat.Report("", self.empty_context, 'normal.md')
        text = report._get_content()
        self.assertEqual(text[0:26], '# Flood Estimation Report\n')

    def test_save_template(self):
        report = astat.Report("test", self.empty_context, 'normal.md')
        with TemporaryDirectory() as folder:
            report.save(folder)
            self.assertTrue(os.path.isfile(
                os.path.join(folder, 'test.Flood estimation report.' + date.today().isoformat() + '.md')))

    def test_save_template_invalid_folder(self):
        report = astat.Report("test", self.empty_context, 'normal.md')
        folder = '/nonexistingfolder'
        self.assertRaises(FileNotFoundError, report.save, folder)

    def test_empty_result(self):
        analysis = astat.Analysis('./autostatistical/tests/data/17002.CD3')
        with TemporaryDirectory() as folder:
            analysis.folder = folder
            analysis.results.update(self.empty_context)
            analysis.create_report()
            self.assertTrue(os.path.isfile(
                os.path.join(folder, '17002.Flood estimation report.' + date.today().isoformat() + '.md')))

    def test_result_date(self):
        analysis = astat.Analysis('./autostatistical/tests/data/17002.CD3')
        with TemporaryDirectory() as folder:
            analysis.folder = folder
            analysis.results.update(self.empty_context)
            analysis.create_report()
            file_path = os.path.join(folder, '17002.Flood estimation report.' + date.today().isoformat() + '.md')
            with open(file_path) as f:
                for line in f:
                    if line.startswith("Date: "):
                        break
        self.assertEqual(line, "Date:          " + date.today().strftime('%d/%m/%Y') + "\n")

    def test_results(self):
        analysis = astat.Analysis('./autostatistical/tests/data/17002.CD3')
        analysis.run()
        analysis.create_report()

    def test_user_templates_empty(self):
        env = templ.TemplateEnvironment()
        loader = env.loader.loaders[0]
        self.assertEqual(loader.list_templates(), [])

    def test_user_template(self):
        folder = os.path.join(AppDirs("OH Auto Statistical", "Open Hydrology").user_data_dir,
                                'templates')
        os.makedirs(folder, exist_ok=True)
        filename = os.path.join(folder, 'normal.md')
        with open(filename, mode='w') as f:
            f.write("test template")
        env = templ.TemplateEnvironment()
        loader = env.loader.loaders[0]
        self.assertEqual(loader.list_templates(), ['normal.md'])
        self.assertEqual(env.get_template('normal.md').filename, filename)
        shutil.rmtree(AppDirs("OH Auto Statistical", "Open Hydrology").user_data_dir)

    def test_package_templates(self):
        env = templ.TemplateEnvironment()
        loader = env.loader.loaders[1]
        self.assertEqual(loader.list_templates(), ['normal.md'])