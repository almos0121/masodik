import numpy as np
from scipy.stats import norm
from matplotlib import pyplot as plt
import pandas as pd
from hatodikgyak import Option
from hatodikgyak import GBrownianPath
K = 360

expiry = "20221215"

C = Option('C',K,expiry,1)
P = Option('P',K,expiry,-1)

S = 124.35
t= 0.23
vola = 0.45
r = 0

a = C.calcPrice(S,t,vola,r) + P.calcPrice(S,t,vola,r) - S #putcall paritas
# print(a)

spots = range(250,500,5)
prices = [C.calcPrice(s,1, vola, r) for s in spots]
pays = [C.calcPayoff(s) for s in spots]

# plt.plot(spots,pays, spots, prices)
# plt.show()

# print(opt.calcPayoff(139))
# print(opt.calcPrice(110,0.5,0.4,0.3))


#option profit calculator

#creating options
opt_c = Option("C",380, None, 1)
opt_p = Option("P",380, None, 1)
print(opt_p)

opt_c.vola = 0.3
opt_p.vola = 0.3

a = opt_c.calcPrice(362,1/12, opt_c.vola, 0.1)
# opt_p.calcPrice(362,1/12)
b = opt_c.calcVola(a,362,1/12,0.1) #nem jó volat ad vissza, mi a baj? A vola_hi-t kellett alakítgatni
print(a)
print(b)

#Generating Brownian Path

gb = GBrownianPath()

sigma = 0.35
N=250
S0=100
spots1 = gb.generate(S0,0.,sigma,1,N)
times = np.arange(0,1,1/N)
plt.plot(times,spots1)
# plt.show()

opt = Option("C", S0, None, 1)

vola = 0.3
prices = []
deltas = []

#kiszámlom minden egyes pontban az opció árát

for (t,S) in zip(times, spots1): #Ez a zip párokon iterál végig (t,S) párok az ábrázoláshoz
    price = opt.calcPrice(S,1-t, vola,0)
    delta = opt.calcDelta(S, 1-t, vola, 0)
    prices.append(price)
    deltas.append(delta)


plt.plot(times,np.array(prices))
plt.show()

df = pd.DataFrame({"time":times, "spot": spots1})
#2022,11,08
K=100
def calcPrice(row): #time és spotból árat számol
    opt = Option("C", K, None, 1 )
    vola = 0.3
    return opt.calcPrice(row.spot, 1-row.time,vola,0)

df['price']= df.apply(calcPrice, axis=1)

print(df)