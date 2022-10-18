import pandas as pd

df = pd.DataFrame()

df['a']=[1,2,3,4,5]
df['b']=[2,10,11,1,1]

df['c'] = df['a']+df['b']

print(df)