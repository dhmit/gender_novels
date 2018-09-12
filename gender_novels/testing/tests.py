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
    def testCount(self):
        self.assertEqual(1 + 2, 3)

# class CountWrong(unittest.TestCase):
#     def testCount(self):
#         self.assertEqual(1 + 2, 4)


if __name__ == '__main__':
    from dh_testers.testRunner import main_test
    main_test()
