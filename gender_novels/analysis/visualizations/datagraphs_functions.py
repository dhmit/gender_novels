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
    sns.set_style('darkgrid')
    ax1=plt.subplot2grid((1,1),(0,0))
    bins=[num for num in range(min(years),max(years)+5,5)]
    plt.hist(years,bins,histtype='bar',rwidth=.8,color='plum')
    plt.xlabel('Year', size=13,weight='bold',color='slategray')
    plt.ylabel('Frequency',size=13,weight='bold',color='slategray')
    plt.title('Publication Year Concentration',size=15,weight='bold',color='slategray')
    plt.yticks(size=11,color='slategray')
    plt.xticks([i for i in range(min(years),max(years)+9,10)],size=11,color='slategray')
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(60)
    plt.show()

def plt_pubcountries(pub_country):
    '''
    Creates a bar graph displaying the frequency of books that were published in each country
    :param pub_country: list
    RETURNS a pyplot bargraph
    '''
    sns.set_style('darkgrid')
    ax1=plt.subplot2grid((1,1),(0,0))
    country_counter={}
    for country in pub_country:
        country_counter[country]=country_counter.setdefault(country,0)+1
    x=[country for country in country_counter]
    y=[country_counter[key] for key in country_counter]
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(15)
    plt.bar(x,y,color='plum')
    plt.xlabel('Countries',size=13,weight='bold',color='slategray')
    plt.ylabel('Frequency',size=13,weight='bold',color='slategray')
    plt.title('Country of Publication',size=15,color='slategray',weight='bold')
    plt.xticks(color='slategray',size=12)
    plt.yticks(color='slategray',size=12)
    plt.show()

def plt_gender_breakdown(pub_gender):
    gendercount={}
    for i in pub_gender:
        gendercount[i]=gendercount.setdefault(i,0)+1
    total=0
    for i in gendercount:
        total+=gendercount[i]
    slices=[gendercount[i]/total for i in gendercount]
    genders=[i for i in gendercount]
    labelgenders=[]
    for i in range(len(genders)):
        labelgenders.append(genders[i]+': ' + str(round(slices[i],2)*100)+'%')
    colors=['slateblue','mediumpurple','plum']
    plt.pie(slices,colors=colors,labels=labelgenders)
    plt.title('Gender Breakdown',size=15,color='slategray',weight='bold')
    plt.legend()
    plt.show()
