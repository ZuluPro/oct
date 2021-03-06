import os
import sys
import shutil
import unittest

from oct.core.exceptions import OctConfigurationError
from oct.utilities.commands import main


class ToolsTest(unittest.TestCase):

    def setUp(self):
        self.base_dir = os.path.dirname(os.path.realpath(__file__))
        self.output_file = '/tmp/oct-test-output.csv'
        self.results_file = os.path.join(self.base_dir, 'fixtures', 'results.sqlite')
        self.config_file = os.path.join(self.base_dir, 'fixtures', 'rebuild_config.json')
        self.bad_config = os.path.join(self.base_dir, 'fixtures', 'bad_rebuild_config.json')
        self.rebuild_project_dir = '/tmp/rebuild_results'
        self.rebuild_dir = '/tmp/rebuild_results/results/test'

        sys.argv = sys.argv[:1]
        sys.argv += ["new-project", self.rebuild_project_dir]
        main()
        os.makedirs(self.rebuild_dir)

    def test_convert_to_csv_success(self):
        """Convert sqlite result file to csv"""
        sys.argv = sys.argv[:1]
        sys.argv += ["results-to-csv", self.results_file, self.output_file]
        main()
        self.assertTrue(os.path.isfile(self.output_file))

    def test_convert_to_csv_errors(self):
        """Convert sqlite result file to csv error"""
        with self.assertRaises(OSError):
            sys.argv = sys.argv[:1]
            sys.argv += ["results-to-csv", "bad_result_file", "/tmp/bad_results_file"]
            main()

    def test_parser(self):
        """Call the main function for results_to_csv with sys.argv set
        """
        sys.argv = sys.argv[:1]
        sys.argv += ["results-to-csv", self.results_file, self.output_file, "-d", ";"]
        main()

    def test_rebuild_results(self):
        """OCT should be able to rebuild results from sqlite file
        """
        sys.argv = sys.argv[:1]
        sys.argv += ["rebuild-results", self.rebuild_dir, self.config_file, "-f", self.results_file]
        main()

        # try same rebuild
        sys.argv = sys.argv[:1]
        sys.argv += ["rebuild-results", self.rebuild_dir, self.config_file, "-f", self.results_file]
        main()

    def test_rebuild_results_error(self):
        """rebuild results command should correctly raise errors when bad configured"""
        sys.argv = sys.argv[:1]
        sys.argv += ['rebuild-results', self.rebuild_dir, self.bad_config]
        with self.assertRaises(OctConfigurationError):
            main()

    def test_download_armory(self):
        """From armory command should be able to download and start project from armory"""
        sys.argv = sys.argv[:1]
        sys.argv += ['from-armory', "/tmp/test-armory", "karec/armory-wordpress"]
        main()

    def test_download_armory_fail(self):
        """From armory command should be able to download and start project from armory"""
        sys.argv = sys.argv[:1]
        sys.argv += ['from-armory', "/tmp/test-armory", "karec/bad-rep"]
        main()

    def tearDown(self):
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
        if os.path.exists(self.rebuild_project_dir):
            shutil.rmtree(self.rebuild_project_dir)
