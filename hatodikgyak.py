import numpy as np
from scipy.stats import norm
#ár a vola-nak mon növő függvénye
#Most árhoz kell megmondani a volatilitást --> invertálni kell kb a CalcPrice functiont --> Iteratív módon kellene, beletszünk valamit és kisebb vagy nagyobb lesz

class Option:

    def __init__(self, right:str, strike:float, expiry:str, pos:int):
        self.right = right #call vagy put az opció
        self.pos = pos #long, short és hány db
        self.strike = strike
        self.expiry = expiry
        self.vola = np.nan

    def calcPrice(self, S: float, timeToExp: float, vola: float, rate:float):
        if not np.isnan(vola):
            IV = vola
        else:
            IV = self.vola if not np.isnan(self.vola) else self.initVola
        if np.isnan(IV):
            print("Vola is not set!")
            return np.nan
        t = timeToExp
        if t > 0:
            d1 = (np.log(S / self.strike) + (rate + IV ** 2 / 2) * t) / (IV * np.sqrt(t))
            d2 = d1 - IV * np.sqrt(t)
            if self.right == 'C':
                return (S * norm.cdf(d1) - norm.cdf(d2) * self.strike * np.exp(-rate * t)) * self.pos
            else:
                return (norm.cdf(-d2) * self.strike * np.exp(-rate * t) - S * norm.cdf(-d1)) * self.pos
        elif t == 0:
            return self.calcPayoff(S)
        else:
            print("expired!")
            return np.nan
    def initVola(self):
        self.vola = 0.2

    def calcPayoff(self, spot:float) -> float:
        if self.right == "C":
            return max(spot-self.strike,0)*self.pos
        elif self.right == "P":
            return max(self.strike - spot,0)*self.pos
        else:
            print("Wrong option type")
            return None
    def calcVola(self, price : float,S: float, time: float, rate:float ):
        #kezdőérték fontos, szigmákkal körül kellene lőni az árat
        vola_hi = 0.5
        while self.calcPrice(S, vola_hi, time, rate) < price:
            vola_hi *= 2
        vola_low = vola_hi / 2
        while abs(vola_hi - vola_low) > 0.0001:
            vola = 0.5 * (vola_low + vola_hi)
            price_update = self.calcPrice(S, time, vola, rate)
            if price_update < price:
                vola_low = vola
            else:
                vola_hi = vola
        return vola #ez kvázi a vola átlag

    def calcDelta(self, S, timeToExp, vola, rate=0):
        if not np.isnan(vola):
            IV = vola
        else:
            IV = self.vola if not np.isnan(self.vola) else self.initVola
        if np.isnan(IV):
            print("Vola is not set!")
            return np.nan
        t = timeToExp
        if t > 0:
            d1 = (np.log(S / self.strike) + (rate + IV ** 2 / 2) * t) / (IV * np.sqrt(t))
            if self.right == 'C':
                return norm.cdf(d1) * self.pos
            else:
                return (norm.cdf(d1) - 1) * self.pos
        else:
            print("expired!")
            return np.nan


class GBrownianPath:

    def __init__(self):
        pass

    def generate (self,S0,mu,sigma,T,N):
        #dS 7 mu*S*dt + sigma*S*dWt
        dt = T/N
        X = np.exp((mu-sigma**2/2)*dt+sigma*np.random.normal(0,np.sqrt(dt),N))
        return S0 * np.cumprod(X)

