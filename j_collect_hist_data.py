import pandas as pd
import datetime as dt
import time
from c_instrument import Instrument
import toolbox
from d_oandaApi import OandaApi


INCREMENTS = {
    'M5': 5,
    'M15': 15,
    'M30': 30,
    # 'H1': 60,
    # 'H4': 240
}


def get_candles_df(json_response):

    prices = ['mid', 'bid', 'ask']
    ohlc = ['o', 'h', 'l', 'c']
    
    our_data = []
    for candle in json_response['candles']:
        if candle['complete'] == False:
            continue
        new_dict = {}
        new_dict['time'] = candle['time']
        new_dict['volume'] = candle['volume']
        for price in prices:
            for oh in ohlc:
                new_dict[f"{price}_{oh}"] = candle[price][oh]
        our_data.append(new_dict)
    return pd.DataFrame.from_dict(our_data)


def create_file(pair, granularity, api):
    candle_count = 2000
    time_step = INCREMENTS[granularity] * candle_count

    end_date = toolbox.get_utc_dt_from_string('2022-11-19 00:00:00')
    date_from = toolbox.get_utc_dt_from_string('2020-01-01 00:00:00')

    candle_dfs = []
    
    date_to = date_from
    
    start = time.time()
    while date_to < end_date:
        
        date_to = date_from + dt.timedelta(minutes=time_step)
        if date_to > end_date:
            date_to = end_date

        code, json_data = api.fetch_candles(pair,
                        granularity=granularity,
                        date_from=date_from,
                        date_to=date_to
                        )

        if code == 200 and len(json_data['candles']) > 0:
            candle_dfs.append(get_candles_df(json_data))
        elif code != 200:
            print('ERROR', pair, granularity, date_from, date_to)
            break

        date_from = date_to
        
    end = time.time()
    try:
        final_df = pd.concat(candle_dfs)
    except:
        final_df = pd.DataFrame(data={'error': code})
    final_df.drop_duplicates(subset='time', inplace=True)
    final_df.sort_values(by='time', inplace=True)
    final_df.to_pickle(toolbox.get_hist_data_filename(pair, granularity))
    
    print(f"{pair}  {granularity}  {final_df.iloc[0].time}  {final_df.iloc[-1].time}")
    print(f"duration: {end-start}")

def run_collection():
    pair_list = 'XAU,GBP,EUR,USD,CAD,JPY,NZD,CHF'
    api = OandaApi()
    for g in INCREMENTS.keys():
        for i in Instrument.get_pairs_from_string(pair_list):
            print(g, i)
            create_file(i, g, api)


if __name__ == '__main__':
    run_collection()