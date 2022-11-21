import pandas as pd
from dateutil.parser import *
import toolbox
import c_instrument
import g_maResult
from i_maSimExcel import create_excel

pd.set_option('display.max_columns', None)

def is_trade(row):
    if row['diff'] >= 0 and row['diff_prev'] < 0:
        return 1
    if row['diff'] <= 0 and row['diff_prev'] > 0:
        return -1
    else:
        return 0

def get_ma_col(ma):
    return f"ma_{ma}"

def eavaluate_pair(i_pair, mashort, malong, price_data):

    price_data = price_data[['time', 'mid_c', get_ma_col(mashort), get_ma_col(malong)]].copy()

    price_data['diff'] = price_data[get_ma_col(mashort)] - price_data[get_ma_col(malong)]
    price_data['diff_prev'] = price_data['diff'].shift(1)
    price_data['is_trade'] = price_data.apply(is_trade, axis=1)

    df_trades = price_data[price_data['is_trade']!=0].copy()
    df_trades['delta'] = (df_trades['mid_c'].diff() / i_pair.pipLocation).shift(-1)
    df_trades['gain'] = df_trades['delta'] * df_trades['is_trade']

    df_trades['pair'] = i_pair.name
    df_trades['mashort'] = mashort
    df_trades['malong'] = malong

    del df_trades[get_ma_col(mashort)]
    del df_trades[get_ma_col(malong)]

    df_trades['time'] = [parse(x) for x in df_trades.time]
    df_trades['duration'] = df_trades.time.diff().shift(-1)
    df_trades['duration'] = [x.total_seconds() / 3600 for x in df_trades.duration]
    df_trades.dropna(inplace=True)

    # print(f"{i_pair.name} {mashort} {malong}  trades:{df_trades.shape[0]} gain:{df_trades['gain'].sum():.0f}")

    return g_maResult.MAResult(
        df_trades=df_trades,
        pairname=i_pair.name,
        params={'mashort':mashort, 'malong':malong}
    )

def get_price_data(pairname, granularity):
    df = pd.read_pickle(toolbox.get_hist_data_filename(pairname, granularity))

    non_cols = ['time', 'volume']
    mod_cols = [x for x in df.columns if x not in non_cols]
    df[mod_cols] = df[mod_cols].apply(pd.to_numeric)

    return df[['time', 'mid_c']]
    

def process_data(ma_short, ma_long, price_data):
    ma_list = set(ma_short + ma_long)

    for ma in ma_list:
        price_data[get_ma_col(ma)] = price_data.mid_c.rolling(window=ma).mean()

    return price_data

def store_trades(results):
    all_trades_df_list = [x.df_trades for x in results]
    all_trades_df = pd.concat(all_trades_df_list)
    all_trades_df.to_pickle('./data/all_trades.pkl')

    return all_trades_df

def process_results(results):
    results_list = [r.result_obj() for r in results]
    final_df = pd.DataFrame.from_dict(results_list)

    final_df.to_pickle('./data/ma_test_result.pkl')
    print(final_df.shape, final_df.num_trades.sum())

    return final_df


def get_test_pairs(pair_str):
    existing_pairs = c_instrument.Instrument.get_instrument_dict().keys()
    pairs = pair_str.split(',')

    test_list = []
    for p1 in pairs:
        for p2 in pairs:
            p = f"{p1}_{p2}"
            if p in existing_pairs:
                test_list.append(p)

    return test_list

def run():
    # pairname = 'GBP_JPY'
    currencies = 'XAU,GBP,EUR,USD,CAD,JPY,NZD,CHF'
    granularity = 'H1'
    ma_short = [8, 16, 32, 64]
    ma_long = [32, 64, 96, 128, 256]
    test_pairs = get_test_pairs(currencies)


    results = []

    for pairname in test_pairs:
        print('running..', pairname)
        i_pair = c_instrument.Instrument.get_instrument_dict()[pairname]

        price_data = get_price_data(pairname, granularity)
        price_data = process_data(ma_short, ma_long, price_data)
        for _malong in ma_long:
            for _mashort in ma_short:
                if _mashort >= _malong:
                    continue
                results.append(eavaluate_pair(i_pair, _mashort, _malong, price_data))

    final_df = process_results(results)
    all_trades_df = store_trades(results)
    create_excel(final_df, all_trades_df)


if __name__ == '__main__':
    run()
