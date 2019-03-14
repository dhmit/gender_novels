import doctest
import os
from pathlib import Path
BASE_PATH = Path(os.path.abspath(os.path.dirname(__file__)))

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


def get_list_of_files(file_list):
    """
    Makes a list of files from a list of files and/or directories with files
    in it
    :param file_list: a list of files and/or directories
    :return: a list of all the files in those directories
    """
    for item in file_list:
        if os.path.isdir(item):
            file_list.remove(item)
            file_list += get_list_of_files(item)
    return file_list


def passes_tests():
    """
    Goes through each file in the gender_novels directory and tests the doctests.
    :return: nothing, exits(0) if the doctests all pass or exits(1) if at least
    one fails
    """
    passes = True
    list_of_files = os.listdir(BASE_PATH)
    list_of_files = get_list_of_files(list_of_files)
    for file in list_of_files:
        if not file_passes(file):
            passes = False
    if passes:
        exit(0)
    else:
        exit(1)


if __name__ == '__main__':
    passes_tests()
