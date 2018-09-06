import sys
import importlib

def unboxing_test():
    """ This function should be run at the end of the unboxing tutorial to test if the install worked properly.

    It checks for a) is Python 3.6+ installed and b) is the gender-guesser library installed

    :return:
    """

    all_tests_passed = True

    print("\nChecking if Python is corretly set up for the \"Gender in the 19th Century Novel\" project.")

    python_version = sys.version_info
    if python_version.major == 3 and python_version.minor >= 6:
        print("\nCheck: Python Version 3.6 or 3.7 -- Passed.")
    else:
        print("\nCheck: Python Version 3.6 or 3.7 -- Failed. Your current Python version is: {}.{}".format(
            python_version.major, python_version.minor)
        )
        all_tests_passed = False

    libraries = [
        {'pip_name': 'gender-guesser', 'python_name': 'gender_guesser'}
    ]
    for library in libraries:
        try:
            importlib.import_module(library['python_name'])
            print("Check: {} library available -- Passed.".format(library['python_name']))
        except ModuleNotFoundError:
            print("Check: {} library available -- Passed. Try running \"pip3 install {}\"".format(
                library['python_name'], library['pip_name']
            ))
            all_tests_passed = False

    if all_tests_passed:
        print("\nYou are ready to go. Have fun!")
    else:
        print("\nYou need to either update Python or install the gender-guesser library.")



if __name__ == '__main__':
    unboxing_test()