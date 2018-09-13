import unittest

def count_to_ten():
    '''
    Counts to ten.
    
    >>> x = tests.count_to_ten()
    >>> x
    10
    '''
    return 10


class Count(unittest.TestCase):
    def test_count(self):
        self.assertEqual(1 + 2, 3)


class Imports(unittest.TestCase):
    '''
    Tests if the gender_novels and dh_testers modules are installed

    SR: I don't quite trust pip to install a package from git. With this test,
    students can examine if their installation was successful with 'python setup.py test'
    It seems like running this test does not require dh_testers itself.
    Test procedure:
    remove 'dh_testers' from requirements.txt
    pip uninstall dh_testers
    python setup.py test
    This results correctly in 'AssertionError: dh_testers could not be loaded.'
    '''

    def test_imports(self):
        import importlib
        for package in ['gender_novels', 'dh_testers']:
            try:
                importlib.import_module(package)
                self.
                self.assertTrue(True, f'{package} loaded successfully.')
            except ModuleNotFoundError:
                self.fail(f'{package} could not be loaded.')



if __name__ == '__main__':
    from dh_testers.testRunner import main_test
    main_test()
