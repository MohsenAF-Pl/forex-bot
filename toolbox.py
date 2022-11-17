def get_hist_data_filename(pair, granularity):
    return f"historical_data/{pair}_{granularity}.pkl"

def get_instruments_data_filename():
    return "./data/instruments.pkl"

if __name__ == '__main__':
    print(get_hist_data_filename("EUR_USD", "H1"))
    print(get_instruments_data_filename())
    