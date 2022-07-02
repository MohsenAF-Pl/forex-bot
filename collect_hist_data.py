import pandas as pd
import datetime as dt

from instrument import Instrument
import utils
from oanda_api import OandaAPI

INCREMENTS = {
    'M5' : 5,
    'H1' : 60,
    'H4' : 240
}

def create_file(pair, granularity, api):
    candle_count = 2000
    time_step = INCREMENTS[granularity] * candle_count

    # he's hard coding this part and idk y but you can change it using datetim
    end_date = utils.get_utc_dt_from_string('2022-06-28 23:59:59')
    date_from = utils.get_utc_dt_from_string('2018-01-01 00:00:00')

    candles_dfs = []

    date_to = date_from
    while date_to < end_date:
        date_to = date_from + dt.timedelta(minutes=time_step)
        if date_to > end_date:
            date_to = end_date
        print(date_from, date_to)
            # collect data
        date_from = date_to


def run_collection():
    pair_list = 'GBP,EUR,USD,CAD,JPY,NZD,CHF' #['EUR_USD', '...]
    api = OandaAPI()
    for g in INCREMENTS.keys():
        for i in Instrument.get_pairs_from_string(pair_list):
            print(g, i)
            create_file(i, g, api)


if __name__ == '__main__':
    run_collection()