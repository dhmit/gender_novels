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
the same style codes. In order to do this, this code must be called sometime before you create 
your graph:
```angular2html
palette = "colorblind"
style_name = "white"
style_list = {'axes.edgecolor': '.6', 'grid.color': '.9', 'axes.grid': 'True',
                           'font.family': 'serif'}
sns.set_color_codes(palette)
sns.set_style(style_name,style_list)
```
This can be in a separate method. Enclosing this code in a set_style method is a great idea.
## Other style requirements

Some style things must be set in the same method that makes the graph. 

These include:
```angular2html
opacity = 0.4
bar_width = 0.3
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

That's all! Thanks for making your graph look great!
