# Gendered Pronoun Frequency Analyses
Several analyses of gendered pronouns in 19th century novels were conducted. First, the average frequency of male and female pronouns in a 19th century novel was analyzed. Second, the portion of subject pronouns that are female pronouns were analyzed and compared with the the portion of all pronouns that are female pronouns. Lastly, the proportion of female pronouns that are subject pronouns and the proportion of male pronouns that are subject pronouns were analyzed. 

## Analysis #1 - Frequency of Gendered Pronouns

Code from gender\_pronoun\_freq\_analysis.py was used to determine the average proportion of the total number of 
pronouns in a given novel are female for each novel in the Gutenberg corpus. Then, results were binned by author gender, date published, and location of publication.

#### Overall
Below shows the average portion of the total number of pronouns in a given novel that are of each type 

- Female: 0.332
- Male: 0.668

On average, a novel in the corpus contains 33.2% female pronouns and 66.8% male pronouns. This 
result has not been tested for statistical significance.

#### By Author Gender
Below shows the average portion of the total number of pronouns in a given novel that are female sorted by author gender

- Male author: 0.246
- Female author: 0.528

On average, a novel by a male author in the corpus contains 24.6% female pronouns and a novel by a female author contains 52.8% female pronouns. This difference has been shown to be statistically significant at the p = 0.05 level by an independent t test.

#### By Date
- To 1810: 0.348
- 1810 to 1819: 0.367
- 1820 to 1829: 0.225
- 1830 to 1839: 0.225
- 1840 to 1849: 0.284
- 1850 to 1859: 0.346
- 1860 to 1869: 0.379
- 1870 to 1879: 0.403
- 1880 to 1889: 0.351
- 1890 to 1899: `NaN`
- 1900 on: 0.331

#### By Publication Location
- United Kingdom: 0.330
- United States: 0.340
- Other: 0.331

No patterns or significant difference was found between categories for publication date or publication location.

## Analysis #2 - Frequency of Gendered Subject Pronouns

Code from gender\_pronoun\_freq\_analysis.py was used to determine the average proportion of the 
total number of subject pronouns in a given novel that are female for each novel in the Gutenberg corpus. Then, results were binned by author gender, date published, and location of publication. Then, these data were compared with the data from Analysis #1 to determine if there is a difference in gender pronoun usage for subject vs object pronouns.

#### Overall
Below shows the average portion of the total number of subject pronouns in a given novel that are of each type 

- Female: 0.325
- Male: 0.675

On average, a novel in corpus contains 32.5% female pronouns and 67.5% male pronouns. This result has not been tested for statistical significance.

This result was then compared with the overall results for Analysis #1. No significant difference was found at the p = 0.05 level. 

#### By Author Gender
Below shows the average portion of the total number of pronouns in a given novel that are female sorted by author gender

- Male author: 0.240
- Female author: 0.520

On average, a novel by a male author in the corpus contains 24.0% female pronouns and a novel by a female author contains 52.0% female pronouns. This difference was shown to be statistically significant at the p = 0.05 level with an independent t test.

The results for female authors and male authors were compared with the results in Analysis #1. No significant difference was found at the p = 0.05 level. This implies that female and male authors do not use gendered pronouns any more or less frequently in the subject than they do overall.

#### By Date
- To 1810: 0.338
- 1810 to 1819: 0.366
- 1820 to 1829: 0.217
- 1830 to 1839: 0.213
- 1840 to 1849: 0.275
- 1850 to 1859: 0.340
- 1860 to 1869: 0.367
- 1870 to 1879: 0.396
- 1880 to 1889: 0.341
- 1890 to 1899: `NaN`
- 1900 on: 0.324

#### By Publication Location
- United Kingdom: 0.325
- United States: 0.334
- Other: 0.324

As in Analysis #1, no patterns or significant differences were found for date of publication or publication location.

## Analysis #3 - Frequency of Each Type of Gendered Pronoun that are Subject Pronouns

Code from gender\_pronoun\_freq\_analysis.py was used to determine the average proportion of the total number of 
pronouns of a given gender that are subject pronouns for each novel in the Gutenberg corpus. Then, results were binned by author gender, date published, and location of publication.

This analysis is separated into two parts, 3a and 3b. 3a is the analysis of female pronouns and 3b is the analysis of male pronouns.

#### Overall
Below are the average proportion of the pronouns of the given gender that are subject pronouns.

- Male: 0.744
- Female: 0.470

On average, for a given novel in the corpus, about 74% of the male pronouns are subject pronouns and about 47% of the female pronouns are subject pronouns. This difference was shown to be statistically significant at the p = 0.05 level.

### 3a - Female Pronouns
The following are the average proportions of female pronouns in a given novel that are subject pronouns.

#### By Author Gender

- Male: 0.464
- Female: 0.483

No significant difference at the p = 0.05 level was found for these categories.

#### By Publication Date

- Before 1810: 0.406
- 1810 to 1819: 0.398
- 1820 to 1829: 0.367
- 1830 to 1839: 0.387
- 1840 to 1849:  0.413
- 1850 to 1859: 0.431
- 1860 to 1869: 0.429
- 1870 to 1879: 0.454
- 1880 to 1889: 0.460
- 1890 to 1899: `NaN`
- 1900 to 1922: 0.477

#### By Publication Location

- United Kingdom 0.463
- United States: 0.470
- Other: 0.471

No patterns or significant differences were found for any of the above categories.

### 3b - Male Pronouns
The following are the average proportions of male pronouns in a given novel that are subject pronouns.

#### Author Gender
- Male: 0.748
- Female: 0.734
 
#### By Publication Date
 
- Before 1810: 0.714
- 1810 to 1819: 0.692
- 1820 to 1829: 0.721
- 1830 to 1839: 0.728
- 1840 to 1849: 0.702
- 1850 to 1859: 0.714
- 1860 to 1869: 0.708
- 1870 to 1879: 0.722
- 1880 to 1889: 0.732
- 1890 to 1899: `NaN`
- 1900 to 1922': 0.749
 
#### By Publication Location
 
- United Kingdom 0.725
- United States: 0.743
- Neither: 0.746

No patterns or significant differences were found for any of these categories.

## Discussion of Results

Analysis #1 shows that female authors use female pronouns more often than male authors. 

Analysis #2 shows that female authors use female subject pronouns more often than male authors, which is to be expected based off the results of Analysis #1. No significant difference was found between the results of Analysis #1 and Analysis #2. This implies that the proportion of subject pronouns that are one gender or another is the same as the proportion when considering all pronouns.

Analysis #3 shows that male pronouns are used more often in the subject than female pronouns. It was also found that there is no significant difference in male/female subject pronoun frequencies by author gender. 

The comparison between Analysis #1 and Analysis #2 and the results of Analysis #3 seem to present conflicting conclusions. The comparison between #1 and #2 seems to imply that pronouns of a particular gender are used in the subject at the same rate that they are used overall. Analysis #3 presents that most male pronouns are subject pronouns and most female pronouns are object pronouns. 

This may suggest that most protagonists in this literature are males. Thus, it would be logical that male pronouns would be used more often, and since the male is the main character, when thost pronouns are used they would be subject pronouns. However, one would expect male and female authors to then show a difference in Analysis #3b as in Analysis #1. Since this is not the case, it seems that female authors do include more female characters, but they must be supporting characters that receive action instead of do the action. Pronoun frequencies alone cannot support this conclusion, and more research is needed on this subject.

Overall, female authors from this time period use female pronouns more often on average than male authors. Male pronouns are used more often in the subject than the object, and female pronouns are used more often in the object than the subject. This result does not vary based on author gender.
