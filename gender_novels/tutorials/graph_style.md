# How to Style Graphs

All graphs used on the website must follow these style parameters. Please use this tutorial to 
make your graphs match.


## Seaborn

We'll use a package called seaborn to make our graphs look nicer. Use pip to install seaborn in 
your coding environment:
```
pip install seaborn
```

or use PyCharm's package installer. 

For any files producing graphs, include an import statement

```angular2html
import seaborn as sns
```


## Style parameters

Seaborn gives you more control over the styling of your graph. For this project, we'll all use 
the same style codes. In order to do this, you must call the load_graph_settings method at the 
beginning of the file with this code:
```angular2html
from gender_novels.common import load_graph_settings
load_graph_settings()
```
This defaults to putting grid lines in the graph. If you don't want grid lines, call this instead:
```angular2html
from gender_novels.common import load_graph_settings
load_graph_settings(False)
```
## Other style requirements

Some style things must be set in the same method that makes the graph. 

These include:
```angular2html
opacity = 0.4
bar_width = 0.3
```
Now, matplotlib is very generous with its whitespace. To fix that, try: 
```angular2html  
fig.tight_layout() 
``` 
If you're not making a bar graph, omit bar_width. Remember that you must then use opacity and 
bar_width in your matplotlib method call. For example:
```angular2html
ax.bar(authors, num_she, bar_width, alpha=opacity, color='r', label="Number of 'she'")
```
Finally, you must call
```angular2html
sns.despine()
```
after making the graph and before showing it or exporting it as an image.

Here's an example of a plot with fake data and correct styling:
```python
# Here are the initial import and style statements
import seaborn as sns
from gender_novels.common import load_graph_settings
load_graph_settings()

# This is the fake data I'm using
num_she = [4000, 2500, 3000, 1000, 6000]
num_he = [7000, 2000, 4000, 2000, 2500]
authors = ["Dickens", "C. Bronte", "Eliot", "Hawthorne", "Austen"]
index = np.arange(5)

# Here are the extra style settings    
bar_width = 0.3
opacity = 0.4

# This is the matplotlib code that's making my barplot
f, ax = plt.subplots()
ax.bar(authors, num_she, bar_width, alpha=opacity, color='g', label="Number of 'she'")
ax.bar(index + bar_width, num_he, bar_width, alpha=opacity, color='b', label="Number of 'he'")
ax.legend(ncol=2, loc="upper right", frameon=True)
ax.set(ylim=(0, 8000), ylabel="",
           xlabel="Usage of 'he' and 'she'")

#I despine right before showing my plot
sns.despine()
plt.show()
```
