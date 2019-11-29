"""
Run all tests.
"""
import unittest

from shared.utils.utils_tests import UtilsTests
from shared.database.models_tests import ModelsTests
from shared.database.queries_tests import QueriesTests
from shared.database.db_utils_tests import DbUtilsTests
from views.authentication.authentication_tests import AuthenticationTests
from views.upload.upload_tests import UploadTests
from views.history.history_tests import HistoryTests
from services.dictionary_tests import DictionaryTests


def run_tests():
    """
    Run unittests.
    """

    suites = []
    testcases = [
        DbUtilsTests,
        ModelsTests,
        QueriesTests,
        UtilsTests,
        AuthenticationTests,
        UploadTests,
        HistoryTests,
        DictionaryTests,
    ]
    for testcase in testcases:
        suites.append(unittest.TestLoader().loadTestsFromTestCase(testcase))
    suite = unittest.TestSuite(suites)
    unittest.TextTestRunner(verbosity=2, failfast=True).run(suite)


if __name__ == "__main__":
    run_tests()
