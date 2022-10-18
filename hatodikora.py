import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.DataFrame(columns=['num','fib'])

row1 = {'num': 1, 'fib': 1}
row2 = {'num': 2, 'fib': 1}
new_df = pd.DataFrame([row1, row2])

df = pd.concat([df, new_df], axis=0, ignore_index=True)
#append régebben jobb volt, most már nem szeretik
#pd.concat, pd.marge, pd.join
#df = df.append({'num': 1, 'fib': 1}, ignore_index=True)
# print(df)

df2 = pd.DataFrame(range(1,21), columns= ['n'])
df2['fib'] = np.nan
# print(df2)
# df2.loc[df2['n']==1, 'fib'] = 1
# df2.loc[df2['n']==2, 'fib'] = 1
# msk = df2['n'] in [1, 2]
# df2.loc[msk, 'fib'] = 1

fib_lag1 = 0
fib_lag2 = 0
for ix, row in df2.iterrows():
    if ix in [0,1]:
        #row['fib'] = 1
        df2.loc[ix, 'fib'] = 1
    else:
        df2.loc[ix,'fib'] = df2.loc[ix-1, 'fib']+df2.loc[ix-2,'fib']
    # print(ix)
    # print(row)
    # print(row['n'])
# print(df2)

class VelSzamok():

    def __init__(self, n_rows, n_cols):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.value = np.random.random((self.n_rows, self.n_cols))

    def plot_column_averages(self, show=True):
        averages = self.value.mean(axis=0)
        plt.plot(averages)
        if show:
            plt.show()

        pass


# VelSzamok(5,2) egy 5*2-es veletlenszám legyen
a = VelSzamok(600,100)
# print(a.value)
a.plot_column_averages()