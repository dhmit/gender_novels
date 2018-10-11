from flask import Flask, render_template

app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['DEBUG'] = True


print(app.config)


@app.route('/')
def render_index():
    return render_template('gender_novels.html')
<<<<<<< HEAD

@app.route('/')
def md_convert():
    """
    Converts file written in markdown to html
    TODO (Xu): Find or create method
    """


=======
>>>>>>> upstream/master




@app.route('/team/')
def render_team():
    """
    Renders the team page
    TODO (Backend Developer): Implement this route
    """
    return render_template('team.html')

@app.route('/projects/')
def render_projects():
    """
    Renders the projects page
    TODO (Xu): Implement this route with list of projects
    """
    return "Check out our Projects!"

if __name__ == '__main__':
    # open a webbrowser on the landing page
    import webbrowser
    webbrowser.open('http://127.0.0.1:8021/', new=2)
    app.run(host='127.0.0.1', port='8021')

