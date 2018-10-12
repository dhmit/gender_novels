from flask import Flask, render_template

app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['DEBUG'] = True


print(app.config)


@app.route('/')
def render_gender_novels():
    return render_template('landing_page.html')


@app.route('/<string:text>/')
def render_base_text(text):
    """
    Renders subpage with base.html template that describes our gender novels research
    :param text: placeholder in base.html written as {{ text }} for words that will vary based on subpage
    :return: subpage with {{ text }} substituted with actual text such as the About page

    TODO (Xu): Figure out how to link other html files to base.html
    """
    return render_template('base.html', text = text)


if __name__ == '__main__':
    # open a webbrowser on the landing page
    import webbrowser
    webbrowser.open('http://127.0.0.1:8021/', new=2)
    app.run(host='127.0.0.1', port='8021')

