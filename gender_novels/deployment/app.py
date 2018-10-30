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


@app.route('/books.html')
def render_corpus_data():
    return render_template('books.html')


@app.route('/team.html')
def render_team():
    return render_template('team.html')


@app.route('/web-scraping.html')
def render_web_scraping():
    return render_template('web-scraping.html')


@app.route('/metadata.html')
def render_metadata():
    return render_template('metadata.html')


@app.route('/visualizations.html')
def render_visualizations():
    return render_template('visualizations.html')


@app.route('/grammar.html')
def render_grammar():
    return render_template('grammar.html')


if __name__ == '__main__':
    # Open a web browser on the landing page
    import webbrowser
    webbrowser.open('http://127.0.0.1:8021/', new=2)
    app.run(host='127.0.0.1', port='8021')

