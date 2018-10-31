from flask import Flask, render_template

app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True


print(app.config)

# These function calls render the individual pages of the overall website so that the
# landing page is able to link to them through the navbar


@app.route('/')
def render_overview():
    return render_markdown_any('gender_novels_overview', title='Gender in Novels, 1770–1922')


# Still necessary because team.html is partly static HTML and partly converted markdown HTML
@app.route('/info/team.html')
def render_team():
    return render_template('team.html')


# Still necessary because corpus-notes.html is composed of 2 separate MD files
@app.route('/info/corpus-notes.html')
def render_corpus_notes():
    return render_template('corpus-notes.html')


@app.route('/info/<fn>')
def render_markdown_any(fn, title=None):
    import markdown2
    from gender_novels.common import BASE_PATH

    try:
        with open(BASE_PATH / 'deployment' / 'static' / 'markdowns' / (fn + '.md')) as fh:
            md_in = fh.read()
    except FileNotFoundError:
        md_in = '**boo**'
    md_in = md_in.replace('(images/', '(/static/markdowns/images/')
    markdown_html = markdown2.markdown(md_in)
    if title is None:
        title_parts = fn.split('_')
        title = ' '.join([title_word.capitalize() for title_word in title_parts])
        # Gender in Novels, 1770-1922 is the desired title and this automatic naming
        # system would override that
        if title == "Gender Novels Overview":
            title = "Gender in Novels, 1770–1922"

    return render_template('blank_markdown.html', title=title, markdown_html=markdown_html)


@app.route('/markdowns/<fn>/')
def render_no_slash(fn, title=None):
    return render_markdown_any(fn, title)


if __name__ == '__main__':
    # Open a web browser on the landing page
    import webbrowser
    webbrowser.open('http://127.0.0.1:8021/', new=1)
    app.run(host='127.0.0.1', port='8021')
