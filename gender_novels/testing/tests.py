import unittest

def sum_to_num(max_number):
    """
    Returns the sum from 0 to max_number inclusive.

    >>> from gender_novels.testing import tests
    >>> x = tests.sum_to_num(3)
    >>> x
    6

    >>> x = tests.sum_to_num(100)
    >>> x
    5050
    """
    sum_result = 0
    for n in range(max_number + 1):
        sum_result += n
    return sum_result

def count_vowels(word):
    """
    >>> from gender_novels.testing import tests
    >>> tests.count_vowels('asdf')
    1

    note that y will not be counted as a vowel.  This
    behavior may change in future versions.

    :param word:
    :return:
    """
    # TODO(cuthbert): implement smart y code.
    total = 0
    for letter in word:
        if letter in 'aeiou':
            total += 1
    return total


class Count(unittest.TestCase):
    def test_sum_count(self):
        self.assertEqual(sum_to_num(10), 55)


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

class CorporaTestCases(unittest.TestCase):
    """
    Checks methods and novels associated with the corpus
    """
if __name__ == '__main__':
    from dh_testers.testRunner import main_test
    main_test()
