from matplotlib.pyplot import axis
import pandas as pd
import utils
import instrument
import ma_result
from ma_excel import create_excel
pd.set_option('display.max_columns', None)

def is_trade(row):
    if row.DIFF >= 0 and row.DIFF_PREV < 0:
        return 1
    if row.DIFF <= 0 and row.DIFF_PREV > 0:
        return -1
    return 0


def get_ma_col(ma):
    return f"MA_{ma}"


def evaluate_pair(i_pair, mashort, malong, price_data):

    price_data['DIFF'] = price_data[get_ma_col(mashort)] - price_data[get_ma_col(malong)]
    price_data['DIFF_PREV'] = price_data.DIFF.shift(1)
    price_data['IS_TRADE'] = price_data.apply(is_trade, axis=1)

    df_trades = price_data[price_data.IS_TRADE != 0].copy()
    df_trades['DELTA'] = (df_trades.mid_c.diff() / i_pair.pipLocation).shift(-1)
    df_trades['GAIN'] = df_trades['DELTA']*df_trades['IS_TRADE']

    # print(f"{i_pair.name} {mashort} {malong} trades:{df_trades.shape[0]} gain:{df_trades['GAIN'].sum():.0f}")

    return ma_result.MAResult(
        df_trades=df_trades,
        pairname=i_pair.name,
        params={'mashort':mashort, 'malong':malong}
    )

def get_price_data(pairname, granularity):
    df = pd.read_pickle(utils.get_hist_data_filename(pairname, granularity))

    non_cols = ['time', 'volume']
    mod_cols = [x for x in df.columns if x not in non_cols]
    df[mod_cols] = df[mod_cols].apply(pd.to_numeric)

    return df[['time', 'mid_c']]

def process_data(ma_short, ma_long, price_data):
    ma_list = set(ma_long + ma_short)

    for ma in ma_list:
        price_data[get_ma_col(ma)] = price_data.mid_c.rolling(window=ma).mean()

    return price_data


def process_results(results):
    results_list = [r.result_ob() for r in results]
    final_df = pd.DataFrame.from_dict(results_list)

    final_df.to_pickle('ma_test.result.pkl')

    print(final_df.shape, final_df.num_trades.sum())

    # return final_df

    create_excel(final_df)

def get_test_pairs(pair_str):
    # gets the available pairs to trade from the instrument.py 
    existing_pairs = instrument.Instrument.get_instruments_dict().keys()

    pairs = pair_str.split(',')

    # ['GBP', ' ERU', ' USD', ' CAD', ' JPY', ' NZD', ' CHF']
    test_list = []
    for p1 in pairs:
        for p2 in pairs:
            pair = f"{p1}_{p2}"
            if pair in existing_pairs:
                test_list.append(pair)
    
    print(test_list)
    return test_list



def run():

    currencies = 'GBP,EUR,USD,CAD,JPY,NZD,CHF' #['EUR_USD', '...]
    granularity = 'H1'
    ma_short = [4, 8, 16, 20, 32, 64]
    ma_long = [4, 8, 16, 20, 32, 50, 64, 96, 128, 256]
    test_pairs = get_test_pairs(currencies)
    
    

    results = []
    for pairname in test_pairs:
        print('running...', pairname)
        for _malong in ma_long:
            i_pair = instrument.Instrument.get_instruments_dict()[pairname]

            price_data = get_price_data(pairname, granularity)
            price_data = process_data(ma_short, ma_long, price_data)

            for _mashort in  ma_short:
                if _mashort >= _malong:
                    continue
                results.append(evaluate_pair(i_pair, _mashort, _malong, price_data.copy()))
    
    process_results(results)


if __name__ == '__main__':
    run()