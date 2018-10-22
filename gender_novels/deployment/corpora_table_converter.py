import pandas as pd

def corpora_table_converter():
    temp = pd.read_csv('../corpora/sample_novels/sample_novels.csv')
    temp.to_html('../deployment/static/html/corpora_table.html')

corpora_table_converter()
