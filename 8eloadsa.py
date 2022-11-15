import sys

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
#return-ok az idő függvényeként vannak ábrázolva 2008 és 2022 között
#hozamok szórása lehet az egész intervallumon
#rolling window vola --> Egy intervallumot csúsztatunk és mindenhol nézünk vola-t, majd ezt tudjuk akár ábrázolni is
#adj close --> osztalék nélküli + split eseten

#https://fred.stlouisfed.org/series/T10Y2Y
#zero spot yield curve - kockázatmentes
def get_daily_risk_free_rate():
    df = pd.read_csv('DTB3.csv')
    df.index = pd.to_datetime(df['DATE'])
    df = df[['DTB3']]
    df.columns = ['risk_free']
    msk = df['risk_free'] != '.'
    df = df[msk]
    df = df.astype(float)
    df = df / 252 #daily rate lesz belőle
    return df
# df_rfree = get_daily_risk_free_rate()
# print(df_rfree)

# sys.exit()

filename = "BRK-B.csv"

df = pd.read_csv(filename)


#print(df.dtypes) #melyik oszlop milyen típusú

df['ret_log_daily'] = np.log(df['Adj Close']/df['Adj Close'].shift(1)) #loghozamok
df.index = df['Date']
df.index = pd.to_datetime(df['Date']) #dátumformátumra állítva
# print(df)
# df['ret_log_daily'].plot()
# plt.show()

df_risk_free = get_daily_risk_free_rate()

df_joined = df.join(df_risk_free) #indexen joinolta össze, ez most így a dátum miatt jó
df_joined['ret_log_daily_exc'] = df_joined['ret_log_daily'] - df_joined['risk free'] #nt elküldi az övét, a töbit onnan









#rolling volatility (meg kell adni, hogy az ablak mekkora, 1 és 2 év)
# df['vol_rolling_1y'] = df['ret_log_daily'].rolling(252).std()
# df['vol_rolling_2y'] = df['ret_log_daily'].rolling(504).std()

# df[['vol_rolling_1y' ,'vol_rolling_2y']].plot()
# plt.show()
#ÁTLAGOS HOZAMOK ROLLING WINDOW-al + VOLA
t_day_in_year = 252
vol_windows_in_year = [0.25, 1,3,10]
cols_vol, cols_ret = [], []
for year in vol_windows_in_year:
    col_vol = 'vol_' + str(year) + 'y'
    col_ret = 'ret_yearly_' + str(year) + 'y'
    cols_vol.append(col_vol)
    cols_ret.append(col_ret)
    df[col_vol] = np.sqrt(t_day_in_year) * df['ret_log_daily'].rolling(int(year * t_day_in_year)).std() #évesítéssel
    df[col_ret] = t_day_in_year * df['ret_log_daily'].rolling(int(year * t_day_in_year)).mean()


# ========= ÁBRÁZOLÁS =========
df['ret_log_daily'].plot()
df[cols_vol].plot()
df[['ret_yearly_1y', 'vol_1y']].plot()
plt.show()

#stilizált tények --> Volatilitás klasztereződik
#heteroszkedasztikus returnok --> változik az eloszlása a hozamoknak






