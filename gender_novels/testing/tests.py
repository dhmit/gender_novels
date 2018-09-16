import unittest

def count_to_ten():
    '''
    Counts to ten.

    >>> from gender_novels.testing import tests
    >>> x = tests.count_to_ten()
    >>> x
    10
    '''
    return 10


class Count(unittest.TestCase):
    def test_count(self):
        self.assertEqual(1 + 2, 3)


class Imports(unittest.TestCase):
    """
    Tests if the gender_novels and dh_testers modules are installed
    """
    def test_imports(self):
        import importlib
        for package in ['gender_novels', 'dh_testers']:
            try:
                importlib.import_module(package)
                self.assertTrue(True, f'{package} loaded successfully.')
            except ModuleNotFoundError:
                self.fail(f'{package} could not be loaded.')


if __name__ == '__main__':
    from dh_testers.testRunner import main_test
    main_test()
