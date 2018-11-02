# Gendered Pronoun Frequency Analyses
Several analyses of gendered pronouns in 19th century novels were conducted. First, the average frequency of male and female pronouns in a 19th century novel was analyzed. Second, the portion of subject pronouns that are female pronouns were analyzed and compared with the the portion of all pronouns that are female pronouns. Lastly, the proportion of female pronouns that are subject pronouns and the proportion of male pronouns that are subject pronouns were analyzed. 

## Analysis #1 - Frequency of Gendered Pronouns

Code from gender_pronoun_freq_analysis.py was used to determine the average proportion of the total number of pronouns in a given novel are female for each novel in the Gutenberg corpus. Then, results were binned by author gender, date published, and location of publication.

#### Overall
Below shows the average portion of the total number of pronouns in a given novel that are of each type 

- Female: 0.3316965406100648
- Male: 0.6683034593899352

On average, a novel in the corpus contains 33.2% female pronouns and 66.8% male pronouns. This 
result has not been tested for statistical significance.

#### By Author Gender
Below shows the average portion of the total number of pronouns in a given novel that are female sorted by author gender

- Male author: 0.24629771231950348
- Female author: 0.5278310846986431

On average, a novel by a male author in the corpus contains 24.6% female pronouns and a novel by a female author contains 52.8% female pronouns. This difference has been shown to be statistically significant at the p = 0.05 level by an independent t test.

#### By Date
- To 1810: 0.34781540605241895
- 1810 to 1819: 0.3671624206360133
- 1820 to 1829: 0.2252711618751344
- 1830 to 1839: 0.2251260105848198
- 1840 to 1849: 0.28394620417062355
- 1850 to 1859: 0.3456395654881602
- 1860 to 1869: 0.37898031072838706
- 1870 to 1879: 0.40327449636757995
- 1880 to 1889: 0.35059668822071316
- 1890 to 1899: nan
- 1900 on: 0.3306238344961748

#### By Publication Location
- United Kingdom: 0.3296691014458057
- United States: 0.34049641567218975
- Other: 0.33074660134105593

No patterns or significant difference was found between categories for publication date or publication location.

## Analysis #2 - Frequency of Gendered Subject Pronouns

Code from gender\_pronoun\_freq\_analysis.py was used to determine the average proportion of the 
total number of subject pronouns in a given novel that are female for each novel in the Gutenberg corpus. Then, results were binned by author gender, date published, and location of publication. Then, these data were compared with the data from Analysis #1 to determine if there is a difference in gender pronoun usage for subject vs object pronouns.

#### Overall
Below shows the average portion of the total number of subject pronouns in a given novel that are of each type 

- Female: 0.3249333651095546
- Male: 0.6750666348904454

On average, a novel in corpus contains 32.5% female pronouns and 67.5% male pronouns. This result has not been tested for statistical significance.

This result was then compared with the overall results for Analysis #1. No significant difference was found at the p = 0.05 level. 

#### By Author Gender
Below shows the average portion of the total number of pronouns in a given novel that are female sorted by author gender

- Male author: 0.2396835584145625
- Female author: 0.5200247331303264

On average, a novel by a male author in the corpus contains 24.0% female pronouns and a novel by a female author contains 52.0% female pronouns. This difference was shown to be statistically significant at the p = 0.05 level with an independent t test.

The results for female authors and male authors were compared with the results in Analysis #1. No significant difference was found at the p = 0.05 level. This implies that female and male authors do not use gendered pronouns any more or less frequently in the subject than they do overall.

#### By Date
- To 1810: 0.33783961142849517
- 1810 to 1819: 0.3662508165201387
- 1820 to 1829: 0.21716377261817688
- 1830 to 1839: 0.21330989562709954
- 1840 to 1849: 0.27465265338555933
- 1850 to 1859: 0.3394959997449575
- 1860 to 1869: 0.3666638420872048
- 1870 to 1879: 0.3957279988341315
- 1880 to 1889: 0.34070830032030436
- 1890 to 1899: nan
- 1900 on: 0.3242795909487435}

#### By Publication Location
- United Kingdom: 0.3249127349860628
- United States: 0.3336792546216914
- Other: 0.32374106776656686

As in Analysis #1, no patterns or significant differences were found for date of publication or publication location.

## Analysis #3 - Frequency of Each Type of Gendered Pronoun that are Subject Pronouns

Code from gender_pronoun_freq_analysis.py was used to determine the average proportion of the total number of pronouns of a given gender that are subject pronouns for each novel in the Gutenberg corpus. Then, results were binned by author gender, date published, and location of publication.

This analysis is separated into two parts, 3a and 3b. 3a is the analysis of female pronouns and 3b is the analysis of male pronouns.

#### Overall
Below are the average proportion of the pronouns of the given gender that are subject pronouns.

- Male: 0.7435803117885973
- Female: 0.47034502270823825

On average, for a given novel in the corpus, about 74% of the male pronouns are subject pronouns and about 47% of the female pronouns are subject pronouns. This difference was shown to be statistically significant at the p = 0.05 level.

### 3a - Female Pronouns
The following are the average proportions of female pronouns in a given novel that are subject pronouns.

#### By Author Gender

- Male: 0.46431348982611936
- Female: 0.48263033001365574

No significant difference at the p = 0.05 level was found for these categories.

#### By Publication Date

- Before 1810: 0.40593066860442656
- 1810 to 1819: 0.3980949313580052
- 1820 to 1829: 0.36732936643896047
- 1830 to 1839: 0.3870903875197253
- 1840 to 1849:  0.4125675471862482
- 1850 to 1859: 0.4305920464371955
- 1860 to 1869: 0.42854803292323124
- 1870 to 1879: 0.45428441744767106
- 1880 to 1889: 0.4595701652307482
- 1890 to 1899: nan
- 1900 to 1922: 0.4768451673889129

#### By Publication Location

- United Kingdom 0.4630172431252677
- United States: 0.4696709249314243
- Other: 0.47138430899539147

No patterns or significant differences were found for any of the above categories.

### 3b - Male Pronouns
The following are the average proportions of male pronouns in a given novel that are subject pronouns.

#### Author Gender
- Male: 0.748109887456545
- Female: 0.7340411441916729
 
#### By Publication Date
 
- Before 1810: 0.7142577291819735
- 1810 to 1819: 0.6921965414568333
- 1820 to 1829: 0.7211259397016647
- 1830 to 1839: 0.7280032001021189
- 1840 to 1849: 0.7023337333868066
- 1850 to 1859: 0.7142664883064364
- 1860 to 1869: 0.7083737635176948
- 1870 to 1879: 0.722426298524636
- 1880 to 1889: 0.7319186466452987
- 1890 to 1899: nan
- 1900 to 1922': 0.7485333414947651
 
#### By Publication Location
 
- United Kingdom 0.7246609392902305
- United States: 0.7430083975098364
- Neither: 0.7461029074849881

No patterns or significant differences were found for any of these categories.

## Discussion of Results

Analysis #1 shows that female authors use female pronouns more often than male authors. 

Analysis #2 shows that female authors use female subject pronouns more often than male authors, which is to be expected based off the results of Analysis #1. No significant difference was found between the results of Analysis #1 and Analysis #2. This implies that the proportion of subject pronouns that are one gender or another is the same as the proportion when considering all pronouns.

Analysis #3 shows that male pronouns are used more often in the subject than female pronouns. It was also found that there is no significant difference in male/female subject pronoun frequencies by author gender. 

The comparison between Analysis #1 and Analysis #2 and the results of Analysis #3 seem to present conflicting conclusions. The comparison between #1 and #2 seems to imply that pronouns of a particular gender are used in the subject at the same rate that they are used overall. Analysis #3 presents that most male pronouns are subject pronouns and most female pronouns are object pronouns. 

This may suggest that most protagonists in this literature are males. Thus, it would be logical that male pronouns would be used more often, and since the male is the main character, when thost pronouns are used they would be subject pronouns. However, one would expect male and female authors to then show a difference in Analysis #3b as in Analysis #1. Since this is not the case, it seems that female authors do include more female characters, but they must be supporting characters that receive action instead of do the action. Pronoun frequencies alone cannot support this conclusion, and more research is needed on this subject.

Overall, female authors from this time period use female pronouns more often on average than male authors. Male pronouns are used more often in the subject than the object, and female pronouns are used more often in the object than the subject. This result does not vary based on author gender.
