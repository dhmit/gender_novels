import matplotlib.pyplot as plt
import seaborn as sns
from gender_novels.corpus import Corpus

def plt_pubyears(years):
    '''
    Creates a histogram displaying the frequency of books that were published within a 20 year 
    period
    :param years: list
    RETURNS a pyplot histogram
    '''
    sns.set(style='darkgrid')
    ax1=plt.subplot2grid((1,1),(0,0))
    bins=[num for num in range(min(years),max(years)+5,5)]
    plt.hist(years,bins,histtype='bar',rwidth=.8,color='red')
    plt.xlabel('Year')
    plt.ylabel('Frequency')
    plt.title('Publication Year Concentration')
    plt.xticks([i for i in range(min(years),max(years)+10,10)])
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)
    plt.show()

def plt_pubcountries(pub_country):
    '''
    Creates a bar graph displaying the frequency of books that were published in each country
    :param pub_country: list
    :return:
    '''
    sns.set(style='darkgrid')
    ax1=plt.subplot2grid((1,1),(0,0))
    country_counter={}
    x=[]
    y=[]
    for country in pub_country:
        if country in country_counter:
            country_counter[country]+=1
        else:
            country_counter[country]=1
    for i in country_counter:
        x.append(i)
        y.append(country_counter[i])

    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)
    plt.bar(x,y,color='red')
    plt.xlabel('Countries')
    plt.ylabel('Frequency')
    plt.title('Country of Publication')
    plt.show()

if __name__ == '__main__':
    pub_year=[]
    pub_country=[]
    corpus=Corpus('sample_novels')
    for novel in corpus.novels:
        pub_year.append(novel.date)
        pub_country.append(novel.country_publication)
    
