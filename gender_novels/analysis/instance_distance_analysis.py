from gender_novels.corpus import Corpus
from statistics import median, mean

import numpy as np
import matplotlib.pyplot as plt
from gender_novels.analysis.analysis import male_instance_dist, female_instance_dist, pronoun_instance_dist
from gender_novels import common
import pandas as pnds
from scipy import stats
from pprint import pprint

import seaborn as sns
sns.set()

#def process_medians(lst1 ,lst2):
 #   return

#TO-DO - get medians, means, max and min instance distances per novel per gender


def run_distance_analysis(corpus):
    """
    Takes in a corpus of novels. Return a dictionary with each novel mapped to an array of 3 lists:
     - median, mean, min, and max distances between male pronoun instances
     - median, mean, min, and max distances between female pronoun instances
     - for each of the above stats, the difference between male and female values. (male stat- female stat for all stats)
        POSITIVE DIFFERENCE VALUES mean there is a LARGER DISTANCE BETWEEN MALE PRONOUNS and therefore
        HIGHER FEMALE FREQUENCY.
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

        diffs = {}
        for stat in range(0, 4):
            stat_diff = list(male_stats.values())[stat] - list(female_stats.values())[stat]
            diffs[list(male_stats.keys())[stat]] = stat_diff

        novel.text = ""
        novel._word_counts_counter = None
        results[novel] = {'male': male_stats, 'female': female_stats, 'difference': diffs}

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
    :return: dictionary of stats
    """
    if len(distance_results) == 0:
        return {'median': 0, 'mean': 0, 'min': 0, 'max': 0}
    else:
        return {'median': median(distance_results), 'mean': mean(distance_results), 'min': min(distance_results),
                'max': max(distance_results)}

def results_by_author_gender(results, metric):
    """
    takes in a dictionary of results and a specified metric from run_distance_analysis, returns a dictionary:
     - key = 'male' or 'female' (indicating male or female author)
      - value  = list of lists. Each list has 3 elements: median/mean/max/min male pronoun distance, female pronoun
       distance, and the difference (whether it is median, mean, min, or max depends on the specified metric)
       order = [male distance, female distance, difference]
    :param results dictionary, a metric ('median', 'mean', 'min', 'max')
    :return: dictionary
    """
    data = {'male': [], "female": []}
    metric_indexes = {"median": 0, "mean": 2, "min": 3, "max": 4}
    try:
        stat = metric_indexes[metric]
    except:
        print("Not valid metric name. Valid names: 'median', 'mean', 'min', 'max'")
    for novel in list(results.keys()):
        if novel.author_gender == "male":
            data['male'].append([results[novel]['male'][metric], results[novel]['female'][metric],
                                 results[novel]['difference'][metric]])
        else:
            data['female'].append([results[novel]['male'][metric], results[novel]['female'][metric],
                                   results[novel]['difference'][metric]])
    return data

def results_by_date(results, metric):
    """
    takes in a dictionary of results and a specified metric from run_distance_analysis, returns a dictionary:
     - key = date range
      - value  = list of lists. Each list has 3 elements: median/mean/max/min male pronoun distance, female pronoun
       distance, and the difference (whether it is median, mean, min, or max depends on the specified metric)
       order = [male distance, female distance, difference]
    :param results dictionary, a metric ('median', 'mean', 'min', 'max')
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
            date_to_1810.append([results[k]['male'][metric], results[k]['female'][metric],
                                 results[k]['difference'][metric]])
        elif k.date < 1820:
            date_1810_to_1819.append([results[k]['male'][metric], results[k]['female'][metric],
                                        results[k]['difference'][metric]])
        elif k.date < 1830:
            date_1820_to_1829.append([results[k]['male'][metric], results[k]['female'][metric],
                                        results[k]['difference'][metric]])
        elif k.date < 1840:
            date_1830_to_1839.append([results[k]['male'][metric], results[k]['female'][metric],
                                        results[k]['difference'][metric]])
        elif k.date < 1850:
            date_1840_to_1849.append([results[k]['male'][metric], results[k]['female'][metric],
                                        results[k]['difference'][metric]])
        elif k.date < 1860:
            date_1850_to_1859.append([results[k]['male'][metric], results[k]['female'][metric],
                                        results[k]['difference'][metric]])
        elif k.date < 1870:
            date_1860_to_1869.append([results[k]['male'][metric], results[k]['female'][metric],
                                      results[k]['difference'][metric]])
        elif k.date < 1880:
            date_1870_to_1879.append([results[k]['male'][metric], results[k]['female'][metric],
                                        results[k]['difference'][metric]])
        elif k.date < 1890:
            date_1880_to_1889.append([results[k]['male'][metric], results[k]['female'][metric],
                                        results[k]['difference'][metric]])
        elif k.date < 1900:
            date_1890_to_1899.append([results[k]['male'][metric], results[k]['female'][metric],
                                        results[k]['difference'][metric]])
        else:
            date_1900_on.append([results[k]['male'][metric], results[k]['female'][metric],
                                 results[k]['difference'][metric]])

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
    takes in a dictionary of results and a specified metric from run_distance_analysis, returns a dictionary:
     - key = location
      - value  = list of lists. Each list has 3 elements: median/mean/max/min male pronoun distance, female pronoun
       distance, and the difference (whether it is median, mean, min, or max depends on the specified metric)
       order = [male distance, female distance, difference]
    :param results dictionary, a metric ('median', 'mean', 'min', 'max')
    :return: dictionary """
    data = {}
    metric_indexes = {"median": 0, "mean": 2, "min": 3, "max": 4}
    try:
        stat = metric_indexes[metric]
    except:
        print("Not valid metric name. Valid names: 'median', 'mean', 'min', 'max'")

    location_UK = []
    location_US = []
    location_other = []

    for k in list(results.keys()):
        if k.country_publication in ["United Kingdom", "England", "Scotland", "Wales"]:
            location_UK.append([results[k]['male'][metric], results[k]['female'][metric],
                                 results[k]['difference'][metric]])
        elif k.country_publication == 'United States':
            location_US.append([results[k]['male'][metric], results[k]['female'][metric],
                                 results[k]['difference'][metric]])
        else:
            location_other.append([results[k]['male'][metric], results[k]['female'][metric],
                                 results[k]['difference'][metric]])

    data['location_UK'] = location_UK
    data['location_US'] = location_US
    data['location_other'] = location_other

    return data

def get_highest_distances(corpus_name, num):
    """
    Returns 3 lists.
        - Novels with the largest median male instance distance
        - Novels with the largest median female instance distance
        - Novels with the largest difference between median male & median female instance distances
    each list contains tuples, where each tuple has a novel and the median male/female/difference instance distance
    :param corpus_name:
    :param num: number of top distances to get
    :return: 3 lists of tuples.
    """
    try:
        raw_results = common.load_pickle("instance_distance_raw_analysis_" + corpus_name)
    except IOError:
        print("No raw results available for this corpus")
    male_medians = []
    female_medians = []
    difference_medians = []

    for novel in list(raw_results.keys()):
        male_medians.append((raw_results[novel]['male']['median'], novel))
        female_medians.append((raw_results[novel]['female']['median'], novel))
        difference_medians.append((raw_results[novel]['difference']['median'], novel))

    male_top = sorted(male_medians, reverse=True)[0:num]
    female_top = sorted(female_medians, reverse=True)[0:num]
    diff_top = sorted(difference_medians)[0:num]

    return male_top, female_top, diff_top


def get_p_vals(corpus_name):
    """
    ANOVA test for independence of:
        - male vs female authors' median distance between female instances
        - UK vs. US vs. other country authors' median distance between female instances
        - Date ranges authors' median distance between female instances
    :param corpus_name:
    :return: data-frame with 3 p-values, one for each category comparison
    """

    try:
        r1 = common.load_pickle("median_instance_distances_by_location_" + corpus_name)
        r2 = common.load_pickle("median_instance_distances_by_author_gender_" + corpus_name)
        r3 = common.load_pickle("median_instance_distances_by_date_" + corpus_name)
    except IOError:
        print("results not available")

    names = ["location", "male_vs_female_authors", "date"]
    median_distance_between_female_pronouns_pvals = []

    location_medians = []
    author_gender_medians = []
    date_medians = []

    med = [location_medians, author_gender_medians, date_medians]
    res = [r1, r2, r3]

    for r in range(0, 3):
        for key in list(res[r].keys()):
            medians = []
            for el in list(res[r][key]):
                medians.append(el[1])
            med[r].append(medians)
    _, location_pval = stats.f_oneway(location_medians[0], location_medians[1])
    _, author_gender_pval = stats.f_oneway(author_gender_medians[0], author_gender_medians[1])
    _, date_pval = stats.f_oneway(*date_medians)
    median_distance_between_female_pronouns_pvals = [location_pval, author_gender_pval, date_pval]

    return pnds.DataFrame({ "names": names, "pvals": median_distance_between_female_pronouns_pvals})

def box_plots(inst_data, my_pal, title, x="N/A"):
    """
    Takes in a frequency dictionaries and exports its values as a bar-and-whisker graph
    :param freq_dict: dictionary of frequencies grouped up
    :param my_pal: palette to be used
    :param title: title of exported graph
    :param x: name of x-vars
    :return:
    """
    plt.clf()
    groups = []
    val = []
    for k, v in inst_data.items():
        temp1 = []
        for el in v:
            if el[1] <= 60:
                temp1.append(el[1])
        temp2 = [k.replace("_", " ").capitalize()]*len(temp1)
        val.extend(temp1)
        groups.extend(temp2)
    df = pnds.DataFrame({x: groups, 'Median Female Instance Distance': val})
    df = df[[x, 'Median Female Instance Distance']]
    sns.boxplot(x=df[x], y=df['Median Female Instance Distance'],
                palette=my_pal).set_title(title)
    plt.xticks(rotation=90)
    # plt.show()

    filepng = "visualizations/" + title + ".png"
    filepdf = "visualizations/" + title + ".pdf"
    plt.savefig(filepng, bbox_inches='tight')
    plt.savefig(filepdf, bbox_inches='tight')



def run_analysis(corpus_name):
    """
    Run instance distance analyses on a particular corpus and saves results as pickle files.
    Comment out sections of code or analyses that have already been run or are unnecessary.
    :param corpus_name:
    :return:
    """
    """
    print('loading corpus')
    corpus = Corpus(corpus_name)
    novels = corpus.novels

    print('running analysis')
    results = run_distance_analysis(novels)

    print('storing results')
    store_raw_results(results, corpus_name)

    r = common.load_pickle("instance_distance_raw_analysis_"+corpus_name)
    r2 = results_by_location(r, "mean")
    r3 = results_by_author_gender(r, "mean")
    r4 = results_by_date(r, "median")
    r5 = results_by_location(r, "median")
    r6 = results_by_author_gender(r, "median")
    r7 = results_by_date(r, "median")

    common.store_pickle(r2, "mean_instance_distances_by_location_"+corpus_name)
    common.store_pickle(r3, "mean_instance_distances_by_author_gender_"+corpus_name)
    common.store_pickle(r4, "mean_instance_distances_by_date_"+corpus_name)

    common.store_pickle(r5, "median_instance_distances_by_location_"+corpus_name)
    common.store_pickle(r6, "median_instance_distances_by_author_gender_"+corpus_name)
    common.store_pickle(r7, "median_instance_distances_by_date_"+corpus_name)

    pvals = get_p_vals("gutenberg")
    common.store_pickle(pvals, "instance_distance_comparison_pvals")

    male_top_twenty, female_top_twenty, diff_top_twenty = get_highest_distances("gutenberg", 20)
    top_twenties = {'male_pronoun_top_twenty': male_top_twenty, 'female_pronoun_top_twenty': female_top_twenty,
                    "difference_top_twenty": diff_top_twenty}
    common.store_pickle(top_twenties, "instance_distance_top_twenties")
    """
    inst_data = common.load_pickle("median_instance_distances_by_author_gender_gutenberg")
    box_plots(inst_data, "Blues", "Median Female Instance Distance by Author Gender", x="Author Gender")

    inst_data = common.load_pickle("median_instance_distances_by_location_gutenberg")
    box_plots(inst_data, "Blues", "Median Female Instance Distance by Location", x="Location")

    inst_data = common.load_pickle("median_instance_distances_by_date_gutenberg")
    box_plots(inst_data, "Blues", "Median Female Instance Distance by Date", x="Date")


if __name__ == '__main__':
    print("running")
    run_analysis("gutenberg")


