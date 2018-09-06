import sys
import importlib

def unboxing_test():
    """ This function should be run at the end of the unboxing tutorial to test if the install worked properly.

    It checks for a) is Python 3.6+ installed and b) is the gender-guesser library installed

    :return:
    """

    print("\nChecking if Python is corretly set up for the \"Gender in the 19th Century Novel\" project.")

    python_version = sys.version_info
    if python_version.major == 3 and python_version.minor >= 6:
        print("\nCheck: Python Version 3.6 or 3.7 -- Passed.")
    else:
        # I wasn't sure what error to properly raise here
        raise AssertionError("\nCheck: Python Version 3.6 or 3.7 -- Failed. Your current Python version is: {}.{}".format(
            python_version.major, python_version.minor)
        )

    libraries = [
        {'pip_name': 'gender-guesser',  'python_name': 'gender_guesser'},
        {'pip_name': 'ipython',         'python_name': 'IPython'}
    ]
    for library in libraries:
        try:
            importlib.import_module(library['python_name'])
            print("Check: Package {} available -- Passed.".format(library['python_name']))
        except ModuleNotFoundError:
            raise ModuleNotFoundError("Check: Package {} available -- Failed. Try running \"pip3 install {}\"".format(
                library['python_name'], library['pip_name']
            ))

    print("\nYou are ready to go. Have fun!")



if __name__ == '__main__':
    unboxing_test()