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
0.7245328833821589

Female: 
0.44787289273153363

### Binned
The following are averages of the same frequency but binned 
over author gender, date published, and location.

#### Female pronouns:
The following are frequencies of female pronouns that are
 subject pronouns.

By author gender: 

Male author: 0.441991212798621

Female author: 0.45798459814830395

By date: (`NaN` means no novels from this range available)

To 1810 : 0.41417750044585927 

1810 to 1819 : 0.4463033852965594 

1820 to 1829 : `NaN`

1830 to 1839 : 0.35106382978723405 

1840 to 1849 : 0.4184030235018519 

1850 to 1859 : 0.3905045204232324 

1860 to 1869 : 0.4768948491730092 

1870 to 1879 : 0.47558451497862986 

1880 to 1889 : 0.42070917410798475 

1890 to 1899 : `NaN`

1900 on : 0.47236646351007894

By location:

England: 0.44347747403902865 

United States: 0.4549392445507864 

Other: 0.43391869615013184

####Male Pronouns

By author gender:

Male author: 0.7287418763201214
 
Female author: 0.7194162706961524
 
By date:

To 1810: 0.708219281182348

1810 to 1819: 0.7041715628672149 

1820 to 1829: `NaN`

1830 to 1839: 0.7046263345195729 

1840 to 1849: 0.6922031669905926 

1850 to 1859: 0.6990460760450546 

1860 to 1869: 0.7267589702159075 

1870 to 1879: 0.7317825828658459 

1880 to 1889: 0.7296998576365381 

1890 to 1899: `NaN`

1900 on: 0.7312530130825822

By location:

England: 0.7209666004589768

US: 0.7300165752376145

Other: 0.7156454243312463
 
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
Overall: 0.31606923574399076

Thus, on average, about 32% of the subject pronouns in a given 
novel were feminine.

### Binned

#### By author gender:

Male author: 0.23516100081271119

Female author: 0.4333655569112226

#### By date:

To 1810: 0.44504635214783195

1810 to 1819: 0.41640324428305886

1820 to 1829: `NaN`

1830 to 1839: 0.09999999999999999

1840 to 1849: 0.31599450339367746

1850 to 1859: 0.3854980861034278

1860 to 1869: 0.42842988831401607

1870 to 1879: 0.3847251297708155

1880 to 1889: 0.2192833286434825

1890 to 1899: `NaN` 

1900 on: 0.31340014426057095

#### By location:

England: 0.3009783595291811

US: 0.3373807026583039

Other: 0.2969183860145596

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




