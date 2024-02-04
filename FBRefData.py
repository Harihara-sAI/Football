import pandas as pd
df = pd.read_html('https://fbref.com/en/comps/20/Bundesliga-Stats')
for idx,table in enumerate(df):
    print('''***************************''')
    print(idx)
    print(table)