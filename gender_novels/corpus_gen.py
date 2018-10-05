import csv
import gutenberg
import re
from pathlib import Path
import unittest

from gender_novels import common
from gender_novels import novel

# @TODO: A lot of things

# Not sure how things are going to work exactly, functions might not look like this in the end

def get_novel_text(novel_id):
    """
        For a given novel id returns the full text of that novel as a string
        @TODO: implement this function
        """
    pass

def get_publication_date(novel_id):
    """
        For a given novel with id novel_id this function attempts a variety of methods to try and
        find the publication date
        :param novel_id: int
        :return: int
        @TODO: implement this function
        """
    pass

def get_publication_date_from_copyright(novel_text):
    """
        Tries to extract the publication date from the copyright statement in the given text
        >>> novel_text = "This work blah blah blah blah COPYRIGHT, 1894 blah
        >>> novel_text += and they all died."
        >>> from gender_novels import corpus_gen
        >>> get_publication_date_from_copyright(novel_text)
        1894
        
        @TODO: should this function take the novel's text as a string or the id or?
        @TODO: should function also try to find publication years not prefaced with "copyright" at
            the risk of finding arbitrary 4-digit numbers?
        :param novel_text: string
        :return: int
        """
    match = re.search(r"(COPYRIGHT\,*\s*) (\d{4})", novel_text, flags = re.IGNORECASE)
    return match.group(2)

if __name__ == '__main__':
    from dh_testers.testRunner import main_test
    main_test()

