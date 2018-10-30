from flask import Flask, render_template

app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True


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


if __name__ == '__main__':
    # Open a web browser on the landing page
    import webbrowser
    webbrowser.open('http://127.0.0.1:8021/', new=2)
    app.run(host='127.0.0.1', port='8021')

