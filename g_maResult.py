

class MAResult():
    def __init__(self, df_trades, pairname, params):
        self.pairname = pairname
        self.df_trades = df_trades
        self.params = params
        
    def result_obj(self):
        d = {
            'pair': self.pairname,
            'num_trades': self.df_trades.shape[0],
            'total_gain': self.df_trades.gain.sum(),
            'mean_gain': self.df_trades.gain.mean(),
            'min_gain': self.df_trades.gain.min(),
            'max_gain': self.df_trades.gain.max()
        }

        for k,v in self.params.items():
            d[k] = v

        return d