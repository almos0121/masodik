import pandas as pd
import numpy as np
import seaborn as sns
import scipy as sp

from util_function import asset_metrics
from matplotlib import pyplot as plt

def calc_2asset_mean_std(w1,w2,ret1,ret2,sd1,sd2,corr):
    ptf_return = w1*ret1+w2*ret2
    ptf_sd = w1**2*sd1**2+w2**2*sd2**2
    ptf_sd += 2*w1*w2*sd1*sd2*corr
    ptf_sd = np.sqrt(ptf_sd)
    return ptf_return, ptf_sd

def calc_nasset_mean(w, mean_return):
    return np.sum(w*mean_return)

def calc_nasset_std(w, cov_matrix):
    return np.sqrt(np.dot(np.dot(w,cov_matrix),w.transpose()))

def calc_nasset_mean_std(w,mean_return,cov_matrix):
    ret = calc_nasset_mean(w,mean_return)
    std = calc_nasset_std(w,cov_matrix)
    return ret, std

if __name__ == "__main__":
    price_hist_df = pd.read_csv("Price_history.csv", index_col=0)
    # one-liner list comp
    price_hist_df.columns = [colname.replace("_price","") for colname in price_hist_df.columns]
    price_hist_df.index = pd.to_datetime(price_hist_df.index)
    #price_hist_df.columns = ['BLK', 'KO', 'GE', 'ATVI', 'JPM']

    price_hist_df.fillna(method="ffill") # érték megadásával

    # 1. írjunk függvényt, ami kiszámolja a fontosabb eszközmetrikákat
    # - return
    # - várható return
    # - std (szórás) return
    # - cov return
    # - corr return

    ret_asset, mean_asset, std_asset, cov_asset, corr_asset = asset_metrics(price_hist_df)

    ret_asset_ext = ret_asset.copy()
    ret_asset_ext["Pre-2015"] = ret_asset_ext.index.year<2015


    # plt.scatter(ret_asset["BLK"], ret_asset["KO"])
    # plt.suptitle("BLK és KO hozamok")
    # plt.show()
    #
    # sns.pairplot(ret_asset_ext, hue="Pre-2015")
    # plt.show()

    # 2. feladat: portfolio 2 eszközből
    # - függvény (várh hozam, kock) 2 eszközre
    # - ábrázoljuk kül súlyozás mellet

    w1s = np.linspace(-1, 1, 11)

    twoassetptf_dict = {}
    for w1 in w1s:
        ptf_ret, ptf_std = calc_2asset_mean_std(w1,1-w1, mean_asset["BLK"],mean_asset["JPM"],
                             std_asset["BLK"],std_asset["JPM"],
                             corr_asset.loc["BLK","JPM"])
        twoassetptf_dict[w1] = (ptf_ret,ptf_std)

    twoassetptf_df = pd.DataFrame(twoassetptf_dict).transpose()
    twoassetptf_df.columns = ["Portfolio Return", "Portfolio Std. Dev."]

    twoassetptf_df.plot(x="Portfolio Std. Dev.", y = "Portfolio Return")

    # 3. feladat - n eszközre hozam, kock
    # - fuggveny

    calc_nasset_mean_std(np.array([1,0,0,0,0]), mean_asset, cov_asset)

    grid = np.array(np.meshgrid(w1s, w1s, w1s, w1s))
    grid = grid.reshape((4,-1)).transpose()
    grid = np.c_[grid, 1-grid.sum(axis=1)]


    nsasset_mean_std = []
    for i in range(grid.shape[0]):
        ret,std = calc_nasset_mean_std(grid[i], mean_asset, cov_asset)
        nsasset_mean_std.append((ret,std))

    nsasset_mean_std_df = pd.DataFrame(nsasset_mean_std)
    nsasset_mean_std_df.columns = ["Portfolio Return", "Portfolio Std. Dev."]
    nsasset_mean_std_df.plot.scatter(x="Portfolio Std. Dev.", y="Portfolio Return")
    pass

    # 4 optimalizáció
    # std dev minimalizálása adott hozamszint mellett
    # - constraintek megadása, feltételezések

    eff_frontier = {}
    for return_target in np.linspace(0.01, 0.2, 100):
        #return_target = 0.2
        cons = ({'type': 'eq', 'fun': lambda weight: return_target - calc_nasset_mean(weight,mean_asset)}, #return targe
                {'type': 'eq', 'fun': lambda weight: np.sum(weight)-1} #fully invested
                )
        #szokott még leverage feltétel is lenni

        bounds = []
        #Olyan határ kell, hogy ne legyen short position, tehát mindegyik sor pozitív
        for i in range(mean_asset.shape[0]):
            bounds.append((0, None)) #itt a felső határral is meg lehet adni

        res = sp.optimize.minimize(calc_nasset_std,
                             np.array([1,0,0,0,0]),
                             args=(cov_asset),
                             constraints=cons)

        #eredmeny = res.x


        if res.success:
            eff_frontier[return_target] = res.x
        #print(eff_frontier)

eff_frontier_df = pd.DataFrame(eff_frontier).transpose()
eff_frontier_df["Standard dev."] = eff_frontier_df.apply(lambda x: calc_nasset_std(np.array(x), cov_asset), axis=1)
eff_frontier_df.reset_index(inplace=True)
eff_frontier_df.plot(x="Standard dev.", y = "index")
print(eff_frontier_df)
plt.show()