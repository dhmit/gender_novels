import string
from pathlib import Path

from gender_novels import common

class Novel(common.FileLoaderMixin):
    """ The Novel class loads and holds the full text and
    metadata (author, title, publication date) of a novel

    >>> from gender_novels import novel
    >>> novel_metadata = {'author': 'Austen, Jane', 'title': 'Persuasion',
    ...                   'corpus_name': 'sample_novels', 'date': '1818',
    ...                   'filename': 'austen_persuasion.txt'}
    >>> austen = novel.Novel(novel_metadata)
    >>> type(austen.text)
    <class 'str'>
    >>> len(austen.text)
    467018
    """

    def __init__(self, novel_metadata_dict):

        if not hasattr(novel_metadata_dict, 'items'):
            raise ValueError(
                'novel_metadata_dict must be a dictionary or support .items()')

        # Check that the essential attributes for the novel exists.
        for key in ('author', 'date', 'title', 'corpus_name', 'filename'):
            if key not in novel_metadata_dict:
                raise ValueError(
                    f'novel_metadata_dict must have an entry for "{key}"')

        self.author = novel_metadata_dict['author']
        self.data = novel_metadata_dict['date']
        self.title = novel_metadata_dict['title']
        self.corpus_name = novel_metadata_dict['corpus_name']
        self.filename = novel_metadata_dict['filename']

        # optional attributes
        self.country_publication = novel_metadata_dict.get(
            'country_publication', None)
        self.author_gender = novel_metadata_dict.get('author_gender', None)
        self.notes = novel_metadata_dict.get('notes', None)

        if 'text' in novel_metadata_dict:
            self.text = novel_metadata_dict['text']
        else:
            self.text = self._load_novel_text()

    def _load_novel_text(self):
        """Loads the text of a novel and removes boilerplate at the beginning and end

        Currently only supports boilerplate removal for Project Gutenberg ebooks.

        :rtype: str
        """

        file_path = Path('corpora', self.corpus_name, 'texts', self.filename)

        try:
            text = self.load_file(file_path)
        except FileNotFoundError:
            err = "Could not find the novel text file "
            err += "at the expected location ({file_path})."
            raise FileNotFoundError(err)

        # Extract Project Gutenberg Boilerplate
        if text.find('*** START OF THIS PROJECT GUTENBERG EBOOK') > -1:
            end_intro_boilerplate = text.find(
                '*** START OF THIS PROJECT GUTENBERG EBOOK')
            # second set of *** indicates start
            start_novel = text.find('***', end_intro_boilerplate + 5) + 3
            end_novel = text.find('*** END OF THIS PROJECT GUTENBERG EBOOK')
            text = text[start_novel:end_novel]

        return text

    def get_tokenized_text(self):
        """
        Tokenizes the text and returns it as a list of tokens

        This is a very simple way of tokenizing the text. We will replace it soon with a
        better implementation that uses either regex or nltk
        E.g. this version doesn't handle dashes or contractions

        >>> from gender_novels import novel
        >>> novel_metadata = {'author': 'Austen, Jane', 'title': 'Persuasion', 'date': '1818',
        ...                   'corpus_name': 'sample_novels', 'filename': 'austen_persuasion.txt',
        ...                   'text': '?!All-kinds %$< of pun*ct(uatio)n {a}nd sp+ecial cha/rs'}
        >>> austin = novel.Novel(novel_metadata)
        >>> tokenized_text = austin.get_tokenized_text()
        >>> tokenized_text
        ['allkinds', 'of', 'punctuation', 'and', 'special', 'chars']

        :rtype: list
        """

        # Excluded characters: !"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~
        excluded_characters = set(string.punctuation)
        cleaned_text = ''
        for character in self.text:
            if character not in excluded_characters:
                cleaned_text += character

        tokenized_text = cleaned_text.lower().split()
        return tokenized_text

    def find_quoted_text(self):
        """
        Finds all of the quoted statements in the novel text

        >>> from gender_novels import novel
        >>> test_text = '"This is a quote" and also "This is my quote"'
        >>> novel_metadata = {'author': 'Austen, Jane', 'title': 'Persuasion',
        ...                   'corpus_name': 'sample_novels', 'date': '1818',
        ...                   'filename': 'austen_persuasion.txt', 'text' : test_text}
        >>> test_novel = novel.Novel(novel_metadata)
        >>> test_novel.find_quoted_text()
        ['"This is a quote"', '"This is my quote"']

        //TODO: Make this test pass
        >>> test_novel.text = 'Test case: "Miss A.E.--," [...] "a quote."'
        >>> test_novel.find_quoted_text()
        ['"Miss A.E.-- a quote."']

        //TODO: Make this test pass
        //TODO: One approach would be to find the shortest possible closed quote.
        >>> test_novel.text = 'Test case: "Open quote. [...] "Closed quote."'
        >>> test_novel.find_quoted_text()
        ['"Closed quote."']

        //TODO(Redlon & Murray): Add and statements so that a broken up quote is treated as a
        //TODO(Redlon & Murray): single quote
        //TODO: Look for more complicated test cases in our existing novels.

        :return: list of complete quotation strings
        """
        text_list = self.text.split()
        quotes = []
        current_quote = []
        quote_in_progress = False
        quote_is_paused = False

        for word in text_list:
            if word[0] == "\"":
                quote_in_progress = True
                quote_is_paused = False
                current_quote.append(word)
            elif quote_in_progress:
                if not quote_is_paused:
                    current_quote.append(word)
                if word[-1] == "\"":
                    if word[-2] != ',':
                        quote_in_progress = False
                        quote_is_paused = False
                        quotes.append(' '.join(current_quote))
                        current_quote = []
                    else:
                        quote_is_paused = True


        return quotes

    def get_count_of_word(self, word):
        """
        Returns the number of instances of str word in the text.  N.B.: Not case-sensitive.
        >>> from gender_novels import novel
        >>> summary = "Hester was convicted of adultery. "
        >>> summary += "which made her very sad, and then Arthur was also sad, and everybody was "
        >>> summary += "sad and then Arthur died and it was very sad.  Sadness."
        >>> novel_metadata = {'author': 'Hawthorne, Nathaniel', 'title': 'Scarlet Letter',
        ...                   'corpus_name': 'sample_novels', 'date': 'long long ago',
        ...                   'filename': None, 'text': summary}
        >>> scarlett = novel.Novel(novel_metadata)
        >>> scarlett.get_count_of_word("sad")
        4

        :param word: word to be counted in text
        :return: int
        """
        word = word.lower()
        count = 0
        words = self.get_tokenized_text()
        for w in words:
            if (w == word):
                count += 1
        return count

    def words_associated(self, wlist):
        """
        Returns a dictionary of the words found after each word in wlist
       Throws an error if wlist is not a list
       Note: dictionary keys are always all lowercase

        >>> from gender_novels import novel
        >>> summary = "She took a lighter out of her purse and handed it over to him."
        >>> summary += " He lit his cigarette and took a deep drag from it, and then began "
        >>> summary += "his speech which ended in a proposal. Her tears drowned the ring."
        >>> summary += " TBH i know nothing about this story."
        >>> novel_metadata = {'author': 'Hawthorne, Nathaniel', 'title': 'Scarlet Letter',
        ...                   'corpus_name': 'sample_novels', 'date': 'long long ago',
        ...                   'filename': None, 'text': summary}
        >>> scarlett = novel.Novel(novel_metadata)
        >>> scarlett.words_associated(["his", "her"])
        {'his': ['cigarette', 'speech'], 'her': ['purse', 'tears']}

        :param wlist:
        :return: dict{ word : [lst_of_following_words]}
        """

        check = [0] * len(wlist)
        dictionary = {}
        text = self.get_tokenized_text()
        for w in wlist:
            wlist[wlist.index(w)] = w.lower()
            dictionary[w.lower()] = []

        for word in text:
            if word in wlist:
                check[wlist.index(word)] = 1
            elif 1 in check:
                index = check.index(1)
                dictionary[wlist[index]].append(word)
                check[index] = 0

        return dictionary



if __name__ == '__main__':
    from dh_testers.testRunner import main_test
    main_test()
