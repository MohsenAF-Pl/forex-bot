import pandas as pd
import xlsxwriter


def add_pair_sheets(ma_test_results, writer):

    for p in ma_test_results.pair.unique():
        temp_df = ma_test_results[ma_test_results.pair==p]
        temp_df.to_excel(writer, sheet_name=p, index=False)

def create_excel(ma_test_result):
    filename = 'ma_results.xlsx'
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')

    ma_test_result = ma_test_result[['pair', 'num_trades', 'total_gain', 'mashort', 'malong']].copy()
    ma_test_result['cross'] = 'ma_' + ma_test_result.mashort.map(str) + '_' + ma_test_result.malong.map(str)

    ma_test_result.sort_values(by=['pair', 'total_gain'], ascending=[True, False], inplace=True)
    add_pair_sheets(ma_test_result, writer)
    writer.save()


if __name__ == '__main__':
    df = pd.read_pickle('./data/ma_test_result.pkl')
    create_excel(df)




"""
we added this function to the f_maSim.py and idk the reason but we made the
funtion in here and then added this to that file
"""