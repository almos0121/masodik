import pandas as pd
import numpy as np
import scipy as sp


#itt lényegében a korábbi fájlt teszük át

class PortfolioOptimizer:
    def __init__(self, asset_price_file_loc):
        self._asset_file_loc = asset_price_file_loc
        self._read_asset_file()
        self._calc_asset_metrics()

    def _read_asset_file(self):
        price_hist_df = pd.read_csv(self._asset_file_loc, index_col=0)
        # one-liner list comp
        price_hist_df.columns = [colname.replace("_price", "") for colname in price_hist_df.columns]
        price_hist_df.index = pd.to_datetime(price_hist_df.index)
        # price_hist_df.columns = ['BLK', 'KO', 'GE', 'ATVI', 'JPM']

        price_hist_df.fillna(method="ffill")  # érték megadásával
        self._price_hist_df = price_hist_df

    def _calc_asset_metrics(self):
        self._return_asset = self._price_hist_df / self._price_hist_df.diff(1)-1
        self._mean_asset = self._return_asset.mean()*12
        self._std_asset = self._return_asset.std() * np.sqrt(12)
        self._cov_asset = self._return_asset.cov() * 12
        self._corr_asset = self._return_asset.corr()

    def _calc_nasset_mean(self):
        return 2 #np.sum(w * mean_return)

    def _calc_nasset_std(self):
        return np.sqrt()

    def calc(self):
        return 1



if __name__ == "__main__":
    PO = PortfolioOptimizer("Price_history.csv")
    print(PO._corr_asset)
