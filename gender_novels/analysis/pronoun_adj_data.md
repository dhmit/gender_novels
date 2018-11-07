#Pronoun Adjective Analysis

**The following Markdown file contains results from an analysis of adjectives associated with gendered pronouns. 
The results are additionally categorized based on characteristics of the novels such as author gender, date published, and location.**

The code used for this analysis can be found in [`pronoun_adjective_analysis.py`](https://github.com/dhmit/gender_novels/blob/master/gender_novels/analysis/pronoun_adjective_analysis.py).

The raw analysis returns a dictionary with each novel mapped to an array of 2 dictionaries:
* Each adjective and its number of occurrences associated with male pronouns
* Each adjective and its number of occurrences associated with female pronouns
 
For each novel, this analysis is conducted by iterating through the novel's tokenized text and considering windows of 10 
words. When the central word of a window is a gendered pronoun, any adjectives also in the window are added to a dictionary.
If there are additionally any opposite-gendered pronouns also in the window then the adjectives are discarded (as they are 
technically associated with both gender pronouns in that case).


##Top 20 Adjectives Associated with Each Gender
**These were obtained by calculating the difference between adjective associations with male pronouns, and with female 
pronouns:** 
> number of male pronoun associations - number of female pronoun associations = difference value

Adjectives with the highest positive difference values demonstrate the strongest male pronoun association, and adjectives 
with the highest negative difference values demonstrate the strongest female pronoun association.
####Top 20 Adjectives Associated with Female Pronouns

| Adjective  | Difference |
| ---------  | ------|
|Beautiful|-6606|
|Pretty| -4348|
|Sweet|-4119|
|Lady|-3058|
|Lovely|-2205|
|Dear|-1926|
|Soft|-1922|
|Happy|-1527|
|Queen|-1198|
|Girlish|-1027|
|Delicate|-987|
|Graceful|-945|
|Bright|-932|
|Rosy|-771|
|Alone|-755|
|Pale|-697|
|Down|-665|
|Childish|-657|
|Slim|-645|

####Top 20 Adjectives Associated with Male Pronouns
| Adjective  | Difference |
| ---------  | ------|
| Old        |53565  |
| Good  | 48647|
|   Last         |   48647    |
|  Great          |  40234     |
|  First          |  28948     |
|  Young          |  26771     |
|  Little          |  25935     |
|  More          |  25071     |
|   Few         |   20510    |
|   Much         | 19362      |
|   Many         |  19283     |
|   New         |   18025    |
|  Long          |   17929    |
|   Big         |  17520     |
|   Right         |   15763    |
|    Best        |   14032    |
|   Dead         |   12470    |
|   Certain         |   11966    |
|   Better         |   11782    |
|   Sure         |   11643    |
|Able| 10700|
