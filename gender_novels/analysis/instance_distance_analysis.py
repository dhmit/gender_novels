from gender_novels.corpus import Corpus
from statistics import median

import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns
#sns.set()

#def process_medians(lst1 ,lst2):
 #   return


def instance_dist(novel, word):
    """
    >>> from gender_novels import novel
    >>> summary = "Hester was her convicted of adultery. "
    >>> summary += "which made her very sad, and then her Arthur was also sad, and her everybody was "
    >>> summary += "sad and then Arthur her died and it was very sad. her Sadness."
    >>> novel_metadata = {'author': 'Hawthorne, Nathaniel', 'title': 'Scarlet Letter',
    ...                   'corpus_name': 'sample_novels', 'date': '1966',
    ...                   'filename': None, 'text': summary}
    >>> scarlett = novel.Novel(novel_metadata)
    >>> instance_dist(scarlett, "her")
    [6, 5, 6, 7, 7]

    :param:novel to analyze, gendered word
    :return: list of distances between instances of gendered word

    """
    output = []
    count = 0
    start = False
    text = novel.get_tokenized_text()

    for element in text:
        if not start:
            if element == word:
                start = True
        else:
            count += 1
            if element == word:
                output.append(count)
                count = 0
    return output


def instance_stats(book, medians1, medians2, title):

    fig, ax = plt.subplots()

    index = np.arange(len(book))
    bar_width = 0.35

    opacity = 0.4
    error_config = {'ecolor': '0.3'}

    medians_she = tuple(medians2)
    medians_he = tuple(medians1)
    book = tuple(book)

    rects1 = ax.bar(index, medians_he, bar_width,
                    alpha=opacity, color='b',
                    error_kw=error_config,
                    label='he')

    rects2 = ax.bar(index + bar_width, medians_she, bar_width,
                    alpha=opacity, color='r',
                    error_kw=error_config,
                    label='she')

    ax.set_xlabel('Book')
    ax.set_ylabel('Median Values')
    ax.set_title('Distance between Word Instances by Book and Author')
    ax.set_xticks(index + bar_width / 2)
    plt.xticks(fontsize=8, rotation=90)
    ax.set_xticklabels(book)
    ax.legend()

    fig.tight_layout()
    #plt.show()
    filepng = "visualizations/" + title + ".png"
    filepdf = "visualizations/" + title + ".pdf"
    plt.savefig(filepng, bbox_inches='tight')
    plt.savefig(filepdf, bbox_inches='tight')

if __name__ == '__main__':
    corpus = Corpus('sample_novels')
    novels = corpus._load_novels()

    num = 0


    #while num <10:
    medians_he = []
    medians_she = []
    books = []
    for novel in novels[num * 10:num * 10 + 9]:
        result_he = instance_dist(novel, "he")
        result_she = instance_dist(novel, "she")
        try:
            medians_he.append(median(result_he))
        except:
            medians_he.append(0)
        try:
            m_she = median(result_she)
            medians_she.append(m_she if m_she < 500 else 500)
        except:
            medians_she.append(0)
        books.append(novel.title[0:20] + "\n" + novel.author)
    instance_stats(books, medians_he, medians_she, "inst_dist" + str(num))
    num += 1

