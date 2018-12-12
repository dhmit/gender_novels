# Digital Humanities Lab Python Style Guide

## General Coding Guidelines

Generally, the Digital Humanities Lab will follow Python's PEP 8 style conventions, which you can learn about in the [Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/).

Use a linter such as [Pylint](https://www.pylint.org/) to check that your code is PEP 8 compliant and bug free.

### Naming Conventions

Variable names and module names use underscores. 
*    use: `this_novel`
*    not: `thisNovel`
*    not: `thisnovel`
    
Class Names use uppercase "CamelCase". So class for notes on 
novels could be `NovelNotes`.

Don’t use short but obscure variable names – use variables long enough to describe exactly what is happening:
*    not: `x`
*    but: `novel_character`

Don't reuse variables if the type of thing they contain changes.
For instance, avoid:
```python
character = NovelCharacter('Hamlet')
# 20 lines below
character = 'a'
```

Call the first one: `current_character` and the second one `letter` or something like that.

Use named return values not anonymous lists.  So don’t get in the habit of returning a list or tuple of 10 elements where each one means something different. You shouldn’t need to be writing code like: `returnedList[3][0][7]`.
Instead use dicts and named values: `returnedDict['parseFailuresList'][0]['path']`.  Or better, return an Object of a new (but documented) class you’ve made for passing a lot of data.  collections.namedtuple can be a great ally.

### Formatting Conventions

The lab prefers single quotes `'` versus double quotes to enclose strings. 

Code alignment is acceptable when it benefits readability. You can ignore pylint warnings for statements like this:
```python 
example = [
    {'attribute1': 10,     'attribute2': 42  },
    {'attribute1': 999999, 'attribute2': 3000}
]

Multi-line comments begin on their own lines: 
```
```python
def hi(name):
    '''
    Method that greets 'name'.
    '''
```

Place spaces around mathematical operations:
*    yes: `n = float((j + 3) % 2)`
*    no : `n = float((j+3)%2)`

### Other Coding Conventions

**Private Variables:** Don’t overuse private ( `_name` ) variables, methods, etc. Generally speaking, what you think now should be kept private will eventually become public.  Never refer to private methods within public documentation.  That’s extremely confusing (you can do it in a #_DOCS_HIDE block though, especially if it speeds up testing). If you think that your method is too complex for “normal” users to use, put it in a separate module and explain that it is for advanced users. This practice is much better than assuming someone else won’t want to subclass/reference etc. your code. Never use _private variables or methods as an excuse to avoid documenting or testing.

**Avoid Complex method chains or list comprehensions** Python, 
like every other programming language, allows you to write "cute" code that does a massive amount of complex work in a single line. Let's say we want to count the number of times that the word "he" appears in the Jane Austen novels in our corpus. Avoid implementing this as a one-liner:
```python
sum([open(file_name, 'r').read().lower().split().count('he') 
    for file_name in files if file_name.startswith('austen')])
```
Instead, split the code up into multiple statements so someone else can follow what's going on.
```python
count_he = 0
for file_name in files:
    if file_name.startswith('austen'):
        text = open(file_name).read()
        word_list = text.lower().split()
        count_he += word_list.count('he')
```
Note: You are not allowed to use nested list comprehensions.

**Maximum method length is 50 lines.** If your method is longer than 50 lines, undoubtedly it is multiple methods masquerading as one. Break it up.  Similarly it’s usually also the case for something has many nested for loops.  Pylint will enforce no more than five nested loops.

**Don't print.** If something is necessary for debugging, use the global DEBUG. We will add a more sophisticated debugging system in the future.
```python
if DEBUG:
    print("Setting up an environment")
```



## New Modules

Start each module with

```python
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------
# Name:         stemmer.py
# Purpose:      The reduces words to their root form.
#
# Authors:      <every contributor to this file>
#
# Copyright:    Copyright © 2018 MIT SHASS DH Lab
# License:      BSD, see license.txt
#---------------------------------------------------------------------
```

Don’t create a property that simply sets or retrieves a private attribute without doing any other manipulations. This is not Java – expose the attribute.


## Testing and Documentation
// talk to Myke
// add dhmit testers to requirements

//Use doctests to demonstrate usage. Many simple methods can get away with just doctests.
//Unit tests are for tests that require a lot of setup or might have output that changes every time, e.g. output between these two numbers or ordered randomly. 

### Write documentation and tests first, then write code

Writing tests first ensures that you’ve thought about the interface to your module/class/method – what will go in and what you expect to get out.  The first test should be something so simple that you can predict the output directly. 
If you want to count the number of male and female authors in a corpus, you might write something like this:

```python
def count_authors_by_gender(self, gender):
    """ 
    This function returns the number of authors with the specified gender (male, female, 
    unknown)

    >>> c = Corpus('sample_novels')
    >>> c.count_authors_by_gender('male'), c.count_authors_by_gender('female')
    (2, 2)
    
    Accepted inputs are 'male', 'female', and 'unknown' but no abbreviations.
    >>> c.count_authors_by_gender('m')
    Traceback (most recent call last):
    ValueError: Gender must be "male", "female", or "unknown" but not m.
    
    :rtype: int
    """
```
When writing code this way, with the test first and the code later, you’ll immediately start to think of things that could go wrong that you’ll want to check: What happens if the user enters abbreviations, for example `m` for male or `f` for female? Check that. Do all novels have an `author_gender` attribute? Check that. After a few weeks of coding this way, you will find that you code **faster** by writing the tests first than the other way around.

**Note**: You are allowed to submit a pull request that only contains documentation and tests for code even before you have written the code. That way, another student in your group can then implement the code. However, you cannot submit code without tests and documentation.

Don’t use `@param`, etc. alone to describe the type of parameters or return values. Explain their type and function in clear English.

### Testing
// check with Myke

As I said before, don’t add tests that take more than 15 seconds to run.  That’s 15 seconds that everyone will have to wait before their test of the complete system will have to wait.  The typical culprits for slow tests are corpus.parse() calls.  See if you can make a simpler hierarchy that loads faster and accomplishes the same results. We use Bach chorale bwv66.6 a lot since it is a very short piece with a lot of interesting cases (pickup notes, etc.)

### Documentation
The PyCharm spell-checker is not very good but it will definitely catch blatant errors, so use it. Don’t commit code (even inline comments) with typos or grammatical errors.  Several of our programmers use screen readers and it is annoying and reduces comprehension to not have words read back properly.
Feel free to use a bit of humor or colloquial language in documentation if it helps get the point across, but keep your work professional.  Remember that the docs are designed to be read by humans, not computers.  Keep them interesting enough that they don’t close the window before they get to the method that is relevant to them.



