def get_p_and_ttest_value(list_a,list_b):

    '''
    Takes in two lists and returns t-test and p value
    can be used to establish correlation between author gender and word usage
    also used for null hypothesis testing

    :param list_a:
    :param list_b:
    :return: (ttest value , p value)
    '''

    ttest_p_value = stats.ttest_ind(list_a, list_b, equal_var=False)
    return ttest_p_value
