# Basic Subject vs Object Pronoun Frequency Analysis

**This markdown file contains data from an analysis of feminine
and masculine subject pronouns vs object pronouns.**

The code used for this analysis can be found in 
gender\_pronoun\_freq\_analysis.py

Two analyses were conducted on this subject. The first compares
how often each gender's pronouns were used in the subject within
their gender, i.e., what portion of female pronouns are subject pronouns
and what portion of male pronouns are subject pronouns. The 
second analysis compares the frequency of masculine and 
feminine pronouns in subject pronouns, ie, what portion of 
subject pronouns are masculine vs feminine.

## First Analysis
This analysis first separated the pronouns into masculine 
and feminine pronouns and compared frequencies within these
categories.

### Overall
These frequencies are the portion of pronouns of a certain
gender that are subject pronouns. Thus, on average, approximately 72% of 
masculine pronouns in a given novel are subject pronouns while approximately 
45% of feminine pronouns are subject pronouns.

Male: 
0.7245

Female: 
0.4479

### Binned
The following are averages of the same frequency but binned 
over author gender, date published, and location.

#### Female pronouns:
The following are frequencies of female pronouns that are
 subject pronouns.

By author gender: 

Male author: 0.4420

Female author: 0.4580

By date: (`NaN` means no novels from this range available)

To 1810 : 0.4142

1810 to 1819 : 0.4463

1820 to 1829 : `NaN`

1830 to 1839 : 0.3511

1840 to 1849 : 0.4184

1850 to 1859 : 0.3905 

1860 to 1869 : 0.4769 

1870 to 1879 : 0.4756 

1880 to 1889 : 0.4207 

1890 to 1899 : `NaN`

1900 on : 0.4724

By location:

England: 0.4435 

United States: 0.4549 

Other: 0.4339

####Male Pronouns

By author gender:

Male author: 0.7287
 
Female author: 0.7194
 
By date:

To 1810: 0.7082

1810 to 1819: 0.7042 

1820 to 1829: `NaN`

1830 to 1839: 0.7046 

1840 to 1849: 0.6922 

1850 to 1859: 0.699 

1860 to 1869: 0.7268 

1870 to 1879: 0.7318 

1880 to 1889: 0.7297 

1890 to 1899: `NaN`

1900 on: 0.7313

By location:

England: 0.721

US: 0.73

Other: 0.7156
 
### Thoughts
We noticed no trends in the binning for this analysis. 
It did seem notable that about 72% of all male pronouns were
subject pronouns while only about 45% of female pronouns
were subject pronouns.

## Analysis 2

This analysis looked at the percentage of subject pronouns
that were male verses female. The following frequencies are
the portion of subject pronouns that are female.

### Overall
Overall: 0.3161

Thus, on average, about 32% of the subject pronouns in a given 
novel were feminine.

### Binned

#### By author gender:

Male author: 0.2352

Female author: 0.4334

#### By date:

To 1810: 0.445

1810 to 1819: 0.4164

1820 to 1829: `NaN`

1830 to 1839: 0.1

1840 to 1849: 0.316

1850 to 1859: 0.3855

1860 to 1869: 0.4284

1870 to 1879: 0.3847

1880 to 1889: 0.2193

1890 to 1899: `NaN` 

1900 on: 0.3134

#### By location:

England: 0.301

US: 0.3374

Other: 0.2969

### Thoughts
For this analysis, we found the overall comparison and the
comparison by author gender most noteworthy. We noticed no
trends in the date binning, though there is a strange deviancy
from the norm in the 1830's. We noticed no trend based on location.

## Overall Thoughts
Analysis #1 is probably the most useful of the two. The results
observed in analysis #2 are likely due to just the frequency of
male vs female pronoun use in general as observed in an earlier
analysis (see he\_she\_freq\_data.md).
