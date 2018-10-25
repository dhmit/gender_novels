from gender_novels.corpus import Corpus
from statistics import median, mean

import numpy as np
import matplotlib.pyplot as plt
from gender_novels.analysis.analysis import male_instance_dist, female_instance_dist, pronoun_instance_dist
from gender_novels import common
#import seaborn as sns
#sns.set()

#def process_medians(lst1 ,lst2):
 #   return

#TO-DO - get medians, means, max and min instance distances per novel per gender


def run_distance_analysis(corpus):
    """
    Takes in a corpus of novels. Return a dictionary with each novel mapped to an array of 3 lists:
     - median, mean, min, and max distances between male pronoun instances
     - median, mean, min, and max distances between female pronoun instances
     - for each of the above stats, the difference between male and female values. (male stat- female stat for all stats.
        POSITIVE DIFFERENCE VALUES mean there is a HIGHER FEMALE FREQUENCY.
    dict order: [male, female]

    :param corpus:
    :return:dictionary where the key is a novel and the value is the results of distance analysis
    """
    results = {}
    for novel in corpus:
        print(novel.title, novel.author)
        male_results = male_instance_dist(novel)
        female_results = female_instance_dist(novel)

        male_stats = get_stats(male_results)
        female_stats = get_stats(female_results)

        diffs = []
        for stat in range(0, 4):
            stat_diff = male_stats[stat] - female_stats[stat]
            diffs.append(stat_diff)

        results[novel] = [male_stats, female_stats, diffs]

    return results


def store_raw_results(results, corpus_name):
    try:
        common.load_pickle("instance_distance_raw_analysis_" + corpus_name)
        x = input("results already stored. overwrite previous analysis? (y/n)")
        if x == 'y':
            common.store_pickle(results, "instance_distance_raw_analysis_" + corpus_name)
        else:
            pass
    except IOError:
        common.store_pickle(results, "instance_distance_raw_analysis_" + corpus_name)


def get_stats(distance_results):
    """
    list order: median, mean, min, max
    :param distance_results:
    :return: list
    """
    return [median(distance_results), mean(distance_results), min(distance_results), max(distance_results)]

def results_by_author_gender(results, metric):
    """
    takes in a dictionary of results and a specified metric from run_distance_analysis, returns a dictionary that maps
    'male' (male author) and 'female' (female author) to a list of difference values from novels written by an author of
    that gender. The dictionary bins difference values from one of the stats (median, mean, min, max) depending on which
    metric is specified in parameters
    :param results dictionary, a metric ('median', 'mean', 'min', 'max')
    :return: list of dictionaries, each with two keys: 'male' (male author) or 'female' (female author). Each key maps
    a list of difference stats for each novel.
    """
    data = {'male': [], "female": []}
    metric_indexes = {"median": 0, "mean": 2, "min": 3, "max": 4}
    try:
        stat = metric_indexes[metric]
    except:
        print("Not valid metric name. Valid names: 'median', 'mean', 'min', 'max'")
    for novel in list(results.keys()):
        if novel.author_gender == "male":
            data['male'].append(results[novel][2][stat])
        else:
            data['female'].append(results[novel][2][stat])
    return data

def results_by_date(results, metric):
    """
    takes in a dictionary of results and a specified metric from run_distance_analysis, returns a dictionary that maps
    different time periods to a list of difference values from novels written by an author of
    that gender. The dictionary bins difference values from one of the stats (median, mean, min, max) depending on which
    metric is specified in parameters
    :param results:
    :param metric: either 'median', 'mean', 'min', or 'max'
    :return: dictionary
    """
    data = {}
    metric_indexes = {"median": 0, "mean": 2, "min": 3, "max": 4}
    try:
        stat = metric_indexes[metric]
    except:
        print("Not valid metric name. Valid names: 'median', 'mean', 'min', 'max'")

    date_to_1810 = []
    date_1810_to_1819 = []
    date_1820_to_1829 = []
    date_1830_to_1839 = []
    date_1840_to_1849 = []
    date_1850_to_1859 = []
    date_1860_to_1869 = []
    date_1870_to_1879 = []
    date_1880_to_1889 = []
    date_1890_to_1899 = []
    date_1900_on = []

    for k in list(results.keys()):
        if k.date < 1810:
            date_to_1810.append(results[k][2][stat])
        elif k.date < 1820:
            date_1810_to_1819.append(results[k][2][stat])
        elif k.date < 1830:
            date_1820_to_1829.append(results[k][2][stat])
        elif k.date < 1840:
            date_1830_to_1839.append(results[k][2][stat])
        elif k.date < 1850:
            date_1840_to_1849.append(results[k][2][stat])
        elif k.date < 1860:
            date_1850_to_1859.append(results[k][2][stat])
        elif k.date < 1870:
            date_1860_to_1869.append(results[k][2][stat])
        elif k.date < 1880:
            date_1870_to_1879.append(results[k][2][stat])
        elif k.date < 1890:
            date_1880_to_1889.append(results[k][2][stat])
        elif k.date < 1900:
            date_1890_to_1899.append(results[k][2][stat])
        else:
            date_1900_on.append(results[k][2][stat])

    data['date_to_1810'] = date_to_1810
    data['date_1810_to_1819'] = date_1810_to_1819
    data['date_1820_to_1829'] = date_1820_to_1829
    data['date_1830_to_1839'] = date_1830_to_1839
    data['date_1840_to_1849'] = date_1840_to_1849
    data['date_1850_to_1859'] = date_1850_to_1859
    data['date_1860_to_1869'] = date_1860_to_1869
    data['date_1870_to_1879'] = date_1870_to_1879
    data['date_1880_to_1889'] = date_1880_to_1889
    data['date_1890_to_1899'] = date_1890_to_1899
    data['date_1900_on'] = date_1900_on

    return data

def results_by_location(results, metric):
    """

    :param results:
    :param metric:
    :return:
    """
    data = {}
    metric_indexes = {"median": 0, "mean": 2, "min": 3, "max": 4}
    try:
        stat = metric_indexes[metric]
    except:
        print("Not valid metric name. Valid names: 'median', 'mean', 'min', 'max'")

    location_England = []
    location_US = []
    location_other = []

    for k in list(results.keys()):
        if k.country_publication == 'England':
            location_England.append(results[k][2][stat])
        elif k.country_publication == 'United States':
            location_US.append(results[k][2][stat])
        else:
            location_other.append(results[k][2][stat])

    data = {}

    data['location_England'] = location_England
    data['location_US'] = location_US
    data['location_other'] = location_other

    return data

def run_gutenberg_analysis():
    print("loading corpus")
    corpus = Corpus('gutenberg')
    novels = corpus.novels

    print("running analysis")
    results = run_distance_analysis(novels)

    print("storing results")
    store_raw_results(results, "gutenberg")

if __name__ == '__main__':
    run_gutenberg_analysis()

    #median_by_author_gender = results_by_author_gender(results, 'median')
    #median_by_date = results_by_date(results, 'median')
    #print(median_by_author_gender)
    #print(median_by_date)
