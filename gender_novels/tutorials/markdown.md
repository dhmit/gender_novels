# Introduction to Markdown

Markdown is a lightweight markup language, meaning that it can be written in any generic text editor, produces formatted text when rendered, and remains readable even in its raw form. Designed to be converted to HTML and other formats, Markdown is often used to format `readme` files and other technical documentation.

Because the original specification of Markdown contained ambiguities, there are several different flavors of Markdown. As most of the work we'll be doin will end up on GitHub, GitHub's "[Mastering Markdown](https://guides.github.com/features/mastering-markdown/)" and this [Markdown Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet) will be useful references.

## Headers

To organize text under headers, you'll use the hash symbol:

```
# H1
## H2
### H3
```

And so on.

These will be rendered like so:

# This is an H1
## This is an H2
### This is an H3

Typically, you should reserve the H1 heading for the title of a document, and then use H2s as the main points, with H3s nestled inside to break up the main points further.

## Lists

### Unordered

Unordered, bulleted lists can be created with an asterisk or hyphen symbol.

```
* Point 1
* Point 2
```

* Point 1
* Point 2

```
- Point 1
- Point 2
```

- Point 1
- Point 2

### Ordered

Use numbers to order your lists.

```
1. Point 1
2. Point 2
3. Point 3
```

1. Point 1
2. Point 2
3. Point 3

You can use `1.` as the number throughout your ordered list.

### Nested

To nest lists, indent with spaces.

```
* Point 1
* Point 2
  * Point 2a
  * Point 2b
```

* Point 1
* Point 2
  * Point 2a
  * Point 2b

```
1. Point 1
1. Point 2
1. Point 3
   1. Point 3a
   1. Point 3b
```

1. Point 1
1. Point 2
1. Point 3
   1. Point 3a
   1. Point 3b

## Emphasis

You can achieve **bold** and *italic* formatted text with either asterisks or underscores on either side of the word you wish to highlight.

```
**This is bold text**
__This is also bold text__

*This is italic text*
_This is also italic text_
```

**This is bold text**
__This is also bold text__

*This is italic text*
_This is also italic text_

## Links

You can add links to documents by putting the hyperlink text in square brackets, and the URL in parentheses.

```
[MIT](https://mit.edu/)
```

The rendered text will look like this:

[MIT](https://mit.edu/)

Be sure to use descriptive hyperlink text (avoid using "click here"), this will make your pages more search engine friendly.

## Images

You can add images to your markdown by using the format of `![Alt Text](url)`.

```
![Baby Bat](https://nyc3.digitaloceanspaces.com/robot/baby-bat.gif)
```

![Baby Bat](https://nyc3.digitaloceanspaces.com/robot/baby-bat.gif)

Including alt text that is helpful is important for accessibility, especially for those using screen readers.

Also, avoid hotlinking to images that you do not own.

## Block Quotes

If you need to include quotes within your markdown, you can indent them as block quotes.

```
> Nel mezzo del cammin di nostra vita
> mi ritrovai per una selva oscura,
> ché la diritta via era smarrita.
```

> Nel mezzo del cammin di nostra vita

> mi ritrovai per una selva oscura,

> ché la diritta via era smarrita.

## Tables

In many versions of Markdown, you can use tables, which make it possible to organize data in a readable way.

The columns of the table can be formatted to be aligned left, centered, or right, which can help to organize both textual and numeric data.

```
| Col 1 Header  | Col 2 Header | Col 3 |
| ------------- |:------------:| -----:|
| This          | This column  |  2304 |
| column is     | is centered, |   495 |
| left-aligned  | Col 3 is...  |    90 |
```

| Col 1 Header  | Col 2 Header | Col 3 |
| ------------- |:------------:| -----:|
| This          | This column  |  2304 |
| column is     | is centered, |   495 |
| left-aligned  | Col 3 is...  |    90 |

## Code

### Inline Code

You can include inline code by using backticks.

```
For your code to be Python 3 compliant,include parentheses with your `print()` statements.
```

For your code to be Python 3 compliant, be sure to include parentheses with your `print` statements, as in `print()`.

### Blocks of Code

You can use three backticks on either side of code to create blocks of unformatted code.


\```

print("meow")

\```


```
print("meow")
```

### Language Blocks

Many flavors of Markdown support highlighted code blocks for specific languages.

\```python

def meow:
    print("meow")

\```


```python
def meow:
    print("meow")
```

\```javascript

function meow(){
    console.log("meow");
}

\```

```javascript
function meow(){
    console.log("meow");
}
```
