"""
Run all tests.
"""
import unittest

from app_tests import AppTests
from utils.utils_tests import UtilsTests
from database.models_tests import ModelsTests
from database.queries_tests import QueriesTests
from database.db_utils_tests import DbUtilsTests
from views.access.access_tests import AccessTests
from views.scraper.scraper_tests import ScraperTests
from views.replacement.replacement_tests import ReplacementTests
from views.authentication.authentication_tests import AuthenticationTests
from betsscrapers.pipelines_tests import PipelinesTests


def run_tests():
    """
    Run unittests.
    """

    suites = []
    testcases = [
        DbUtilsTests,
        ModelsTests,
        QueriesTests,
        AppTests,
        UtilsTests,
        AuthenticationTests,
        AccessTests,
        ReplacementTests,
        ScraperTests,
        PipelinesTests,
    ]
    for testcase in testcases:
        suites.append(unittest.TestLoader().loadTestsFromTestCase(testcase))
    suite = unittest.TestSuite(suites)
    unittest.TextTestRunner(verbosity=2, failfast=True).run(suite)


if __name__ == "__main__":
    run_tests()
