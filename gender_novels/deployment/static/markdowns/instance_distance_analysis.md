# Male/Female Instance Distance Analysis

The code used for this analysis can be found in [instance\_distance\_analysis.py](https://github\.com/dhmit/gender_novels/blob/master/gender_novels/analysis/instance_distance_analysis.py).

The raw analysis returns a dictionary with each novel mapped to an array of 3 lists:
* Median, mean, minimum, and maximum distances between male pronoun instances.
* Median, mean, minimum, and maximum distances between female pronoun instances.
* For each of the above stats, the difference between male and female values. (male stat- female stat for all stats). 
*positive difference values* mean there is a *larger distance between male pronouns than female pronouns* and therefore 
*higher female frequency*.
 
For example:
>A median female instance value of 14.0 vs a median male instance distance value of 10.0 means that female instances tend 
tend to occur every 14 words in the novels versus male instances occurring every 9 words in the novel. This would indicate 
a greater male presence in the novel.

> A mean difference value of 4.0 means that on average, the distance between male instances is 4 words longer than female 
instances.
 
##By Author Gender:
####Average Median Male Instance Distance:
Male Authors: 12.61

Female Authors: 13.79

####Average Median Female Instance Distance:
Male Authors: 72.30

Female Authors: 30.17

p-value = 0.0184

![](/static/markdowns/images/median_female_instance_distance_by_author_gender.png)

## By Decade:

**Average median female instance distance in each decade**

All dates before 1810 : 12.36

Dates 1810 to 1819 : 13.833

Dates 1820 to 1829 : 15.22 

Dates 1830 to 1839 : 17.14

Dates 1840 to 1849 : 14.53

Dates 1850 to 1859 : 14.43

Dates 1860 to 1869 : 14.56

Dates 1870 to 1879 : 13.70

Dates 1880 to 1889 : 23.49

Dates 1890 to 1899 : 41.92 

Dates 1900 on : 67.34

p-value = 0.942

![](/static/markdowns/images/median_female_instance_distance_by_date.png)

## By Location:
**Average median female instance distance in each location**

Published in England : 63.04

Published in US : 20.59

Published in other country : 62.02

p-value = 0.317

![](/static/markdowns/images/median_female_instance_distance_by_location.png)


##Novels With Greatest Instance Distances
####Top 10 novels with greatest median female instance distances:
1. *Don Hale with the Flying Squadron* by William Crispin
    Median female instance distance: 19713.5
    
2. *The Head of Kay's* by Pelham Grenville  
    Median female instance distance: 15962
    
3. *Teddy and Carrots: Two Merchants of Newpaper Row* James Otis  
    Median female instance distance: 9906
    
4. *The Outdoor Chums in the Big Woods* by Quincy Allen  
    Median female instance distance: 9804
    
5. *The Boy Scouts at the Canadian Border* by John Henry Goldfrap  
    Median female instance distance: 9507
    
6. *Our Young Aeroplane Scouts in Germany; or, Winning the Iron Cross* by Horace Porter  
    Median female instance distance: 8671
    
7. *The Keepers of the Trail: A Story of the Great Woods* by Joseph Alexander
    Median female instance distance: 7551.5
    
8. *Storm-Bound; or, A Vacation Among the Snow Drifts* by Captain Alan Douglas  
    Median female instance distance: 6335.5
    
9.  *Tom Slade's Double Dare* by Percy Keese Fitzhugh
    Median female instance distance: 5654

10. *The Wonder Island Boys: Conquest of the Savages* by Roger Thompson Finlay
    Median female instance distance: 5091 


####Top 10 novels with greatest median male instance distances:
1. *Marjorie's Busy Days* by Carolyn Wells  
    Median male instance distance: 43.5
    
2. *The Mary Frances Cook Book* by Jane Eayre Fryer  
    Median male instance distance: 39
    
3. *The Motor Girls on the Coast; or, The Waif From the Sea* by Margaret Penrose  
    Median male instance distance: 36
    
4. *The Adopting of Rosa Marie* by Carroll Watson Rankin  
    Median male instance distance: 34
    
5. *Ruth Fielding At College; or, The Missing Examination Papers* by Alice B. Emerson  
    Median male instance distance: 33.5
    
6. *Mary Jane in New England* by Clara Ingram Judson  
    Median male instance distance: 32
    
7. *Wanted: A Cook* by Alan Dale  
    Median male instance distance: 32
    
8. *The Armed Ship America* by James Otis  
    Median male instance distance: 31
    
9.  *The Mary Frances Garden Book; or, Adventures Among the Garden People* by Jane Eayre Fryer
    Median male instance distance: 31

10. *The Mary Frances Knitting and Crocheting Book* by Jane Eayre Fryer
    Median male instance distance: 30 
    
## Thoughts:
Overall, both male and female authors have greater median female instance distances than male instance distances. 
However, there is a significant difference between median female instance distance in novels written by female authors,
and those written by male authors. There is evidently no significant trend with relation to date or location of
publication. 

Looking at the list of top-10 novels in each measured category, it is important to note that the highest male instance distances
are far smaller than the highest female instance distance. The top 10 median male instance distances are in the range of 
30-45, while the top 10 median female instance distances are in the range of 5091-19713. This may indicate that even the female-centric novels still have a male
presence, while male-centric novels exclude female characters to a greater degree.
