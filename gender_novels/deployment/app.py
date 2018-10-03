from flask import Flask, render_template

app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['DEBUG'] = True


print(app.config)


@app.route('/')
def render_index():
    return render_template('index.html')

@app.route('/team')
def render_team():
    """
    Renders the team page

    TODO (Backend Developer): Implement this route

    """


if __name__ == '__main__':
    app.run(host='127.0.0.1', port='8021')

    # open a webbrowser on the landing page
    import webbrowser
    webbrowser.open('http://127.0.0.1:8021/', new=2)
