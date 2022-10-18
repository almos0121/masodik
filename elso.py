import numpy as np
from scipy.stats import norm
from matplotlib import pyplot as plt

from hatodikgyak import Option
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

plt.plot(spots,pays, spots, prices)
plt.show()

# print(opt.calcPayoff(139))
# print(opt.calcPrice(110,0.5,0.4,0.3))


#option profit calculator
