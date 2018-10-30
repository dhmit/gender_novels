from flask import Flask, render_template

app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['DEBUG'] = True


print(app.config)

"""
These function calls render the individual pages of the overall website so that the
landing page is able to link to them through the navbar
"""


@app.route('/')
def render_overview():
    return render_template('home.html')


@app.route('/copyright.html')
def render_copyright():
    return render_template('copyright.html')


@app.route('/corpora.html')
def render_corpora():
    return render_template('corpora.html')


@app.route('/team.html')
def render_team():
    return render_template('team.html')


@app.route('/web-scraping.html')
def render_web_scraping():
    return render_template('web-scraping.html')


@app.route('/metadata.html')
def render_metadata():
    return render_template('metadata.html')


@app.route('/info/<fn>')
def render_markdown_any(fn):
    import markdown2
    from gender_novels.common import BASE_PATH
    try:
        with open(BASE_PATH / 'deployment' / 'static' / 'markdowns' / (fn + '.md')) as fh:
            md_in = fh.read()
    except FileNotFoundError:
        md_in = '**boo**'
    md_in = md_in.replace('(images/', '(/static/markdowns/images/')
    markdown_html = markdown2.markdown(md_in)
    title_parts = fn.split('_')
    title = ' '.join([title_word.capitalize() for title_word in title_parts])

    return render_template('blank_markdown.html', title=title, markdown_html=markdown_html)



if __name__ == '__main__':
    # Open a web browser on the landing page
    import webbrowser
    webbrowser.open('http://127.0.0.1:8021/', new=2)
    app.run(host='127.0.0.1', port='8021')

