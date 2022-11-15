import numpy as np
from scipy.stats import norm
from matplotlib import pyplot as plt
import pandas as pd

from hatodikgyak import Option
from hatodikgyak import GBrownianPath

filename = "KO.csv"
df = pd.read_csv(filename)

# print(df.describe()) #adott oszlopok mutatószámai
# print(df.columns)
# print(df[:6])



#open interest: Összesen mennxi kontraktust nyitottak meg
#mid: Best bid és Best Offer átlag
#symbolból leolvasható a dátum a C/P és a strike is
#hibák a BS modellel --> Sok feltétel nem teljesül (normalitás, folytonosság, zero tranzakciós költségek stb.), de limiteket jól a dvissza

#CALC TIME TO EXPIRY

df['date']=pd.to_datetime(df['date'])
df['expiry'] = pd.to_datetime(df["expiry"])
df["daysToExp"] = (df.expiry-df.date).dt.days
df = df.set_index("date")

# print(df[:6])

#PLOT FORWARD PRICE VS TIME

# df.groupby(df.index).forward_price.median().plot()
# plt.show()
#index valami nap, minden napra van több opció
#median azért, mert lehetnek outlierek

#CALC IMPLIED VOLA AND GREEKS

def calcVolaMid(row):
    opt = Option(row.cp_flag, row.strike, row.expiry, 1)
    if row.forward_price * row.daysToExp * row.mid > 0:
        return opt.calcVola(row.forward_price,row.daysToExp/365, row.mid)
    else:
        return np.nan

#Adatbázis szűkítése
df0 = df[df.index < "2018-03-01"]

df0.loc[:,'implied_vola_mid'] = df0.apply(calcVolaMid, axis=1) #sorokra alkalmazza a fv-t
print(df0)

# symbol = "KO 180323C48000"
# df = df0[df0.symbol == symbol]

dates = df0.index.unique()
df_ = df0[df0.index == dates[23]]
df_ = df0[df0.daysToExp == 102]
date = df_.index[0]
df_ = df_[df_.last_date == date]
df_.groupby(df_.strike).implied_vola_mid.median().plot()
plt.show()
