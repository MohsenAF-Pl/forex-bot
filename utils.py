import datetime as dt
from dateutil.parser import *

def get_hist_data_filename(pair, granularity):
    return f"hist_data/{pair}_{granularity}.pkl"

def get_instruments_data_filename():
    return "instruments.pkl"

def time_utc():
    return dt.datetime.utcnow().replace(tzinfo=dt.tzinfo.utc)

def get_utc_dt_from_string(date_str):
    d = parse(date_str)
    return d.replace(tzinfo=dt.timezone.utc)

if __name__ == '__main__':
    pass