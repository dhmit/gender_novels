from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['DEBUG'] = True


print(app.config)


@app.route('/')
def render_gender_novels():
    # Reads the CSV of the corpora, translates it to HTML, then saves it in corpora_table.html
    # temp = pd.read_csv("../../gender_novels/corpora/sample_novels/sample_novels.csv")
    # temp.to_html("templates/corpora_table.html")

    return render_template('gender_novels.html', corpora_table="Corpora table goes here")


if __name__ == '__main__':
    # open a webbrowser on the landing page
    import webbrowser
    webbrowser.open('http://127.0.0.1:8021/', new=2)
    app.run(host='127.0.0.1', port='8021')

