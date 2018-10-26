import doctest
import os

def test():
    """
    tests simple addition that we know is true
    :return: nothing, exits
    """
    if 2 + 2 == 4:
        exit(0)
    else:
        exit(1)


def file_passes(filename):
    """
    tests the doctests in the file given
    :param filename: the code file being tested
    :return: True if no failures, False if failures
    """
    (failure_count, test_count) = doctest.testfile(filename)
    if failure_count == 0:
        return True
    else:
        return False


def passes_tests():
    """
    Goes through each file in the gender_novels directory and tests the doctests.
    :return: nothing, exits(0) if the doctests all pass or exits(1) if at least
    one fails
    """
    passes = True
    list_of_files = os.listdir()
    for file in list_of_files:
        if not file_passes(file):
            passes = False
    if passes:
        exit(0)
    else:
        exit(1)


if __name__ == '__main__':
    passes_tests()
