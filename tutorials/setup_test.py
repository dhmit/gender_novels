import sys
import importlib


def unboxing_test():
    """ This function should be run at the end of the unboxing tutorial to test
    if the install worked properly. It checks for a) is Python 3.6+ installed
    and b) if the python packages in requirements.txt can be imported. (For the
    moment, the names are hard-coded. I'm sure there are ways around the
    differences between pip name ("ipython") and import name ("IPython")--but
    I'm tired right now and wanted to push a draft. :return:
    """

    print("\nChecking if Python is corretly set up for the \"Gender in the" \
            "19th Century Novel\" project.")

    python_version = sys.version_info
    if python_version.major == 3 and python_version.minor >= 6:
        print("\nCheck: Python Version 3.6 or 3.7 -- Passed.")
    else:
        # I wasn't sure what error to properly raise here
        raise AssertionError("""\nCheck: Python Version 3.6 or 3.7 -- Failed.
            Your current Python version is: {}.{}".format(
            python_version.major, python_version.minor)
        """)

    packages = [
        {'pip_name': 'gender-guesser',  'python_name': 'gender_guesser'},
        {'pip_name': 'ipython',         'python_name': 'IPython'}
    ]
    for package in packages:
        try:
            importlib.import_module(package['python_name'])
            print("Check: Package {} available -- Passed.".format(
                            package['python_name']))
        except ModuleNotFoundError:
            raise ModuleNotFoundError("Check: Package {} available -- Failed."
                            "Try running \"pip3 install {}\"".format(
                            package['python_name'], package['pip_name']
                            ))

    print("\nYou are ready to go. Have fun!")

if __name__ == '__main__':
    unboxing_test()
