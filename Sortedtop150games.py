import pandas as pd

df = pd.read_csv('allgames.csv', usecols=['Game Name', 'Game Link', 'Developer Name', 'Publisher Name', 'Game Genre', 'Platform',
                                          'Style Genre','Release Date', 'Price', 'Rating', 'Positive Review', 'Review'])

df.to_excel('allgames.xlsx', index=False)
df['Positive Review'] = df['Positive Review'].str.rstrip('%').astype('float') / 100.0

df_sorted = df[df['Review'] >= 1000].sort_values(['Rating', 'Positive Review', 'Review'], ascending=False)

df_new = df_sorted.iloc[:150]

df_new.to_csv('top150games.csv', index=False)

df_new.to_excel('top150games.xlsx', index=False)

