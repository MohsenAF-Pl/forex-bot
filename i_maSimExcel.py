from curses import termname
import pandas as pd
import xlsxwriter



def get_line_chart(book, start_row, end_row, labels_col, data_col, title, sheetname):
    chart = book.add_chart({'type': 'line'})
    chart.add_series({
        'categories': [sheetname, start_row, labels_col, end_row, labels_col],
        'values': [sheetname, start_row, data_col, end_row, data_col],
        'line': {'color': 'blue'}
    })

    chart.set_title({'name': title})
    chart.set_legend({'none': True})

    return chart

def add_chart(pairname, cross, df, writer):
    workbook = writer.book
    worksheet = writer.sheets[pairname]

    chart = get_line_chart(workbook, 1, df.shape[0], 8, 9, f"Cum. Gains for {pairname} {cross}", pairname)
    chart.set_size({'x_scale': 2.5, 'y_scale': 2.5})
    worksheet.insert_chart('K1', chart)


def add_pair_charts(ma_test_result, all_trades, writer):
    cols = ['time', 'cum_gain']
    df_temp = ma_test_result.drop_duplicates(subset=['pair'])
    # print(df_temp.head(5))

    for index, row in df_temp.iterrows():
        # print('index: ', index)
        # print('row: ', row.cross, row.pair)
        temp_all_trades = all_trades[(all_trades.cross == row.cross) & (all_trades.pair == row.pair)].copy()
        
        temp_all_trades['cum_gain'] = temp_all_trades.gain.cumsum()
        # print(temp_all_trades.tail())
        temp_all_trades[cols].to_excel(writer, sheet_name=row.pair, startrow=0, startcol=7)
        add_chart(row.pair, row.cross, temp_all_trades, writer)

def add_pair_sheets(ma_test_results, writer):

    for p in ma_test_results.pair.unique():
        temp_df = ma_test_results[ma_test_results.pair==p]
        temp_df.to_excel(writer, sheet_name=p, index=False)

def create_excel(ma_test_result, all_trades):
    filename = 'ma_results.xlsx'
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')

    ma_test_result = ma_test_result[['pair', 'num_trades', 'total_gain', 'mashort', 'malong']].copy()
    ma_test_result['cross'] = 'ma_' + ma_test_result.mashort.map(str) + '_' + ma_test_result.malong.map(str)
    ma_test_result.sort_values(by=['pair', 'total_gain'], ascending=[True, False], inplace=True)

    all_trades['cross'] = 'ma_' + all_trades.mashort.map(str) + '_' + all_trades.malong.map(str)
    all_trades['time'] = [x.replace(tzinfo=None) for x in all_trades.time]


    add_pair_sheets(ma_test_result, writer)
    add_pair_charts(ma_test_result, all_trades, writer)
    writer.save()


if __name__ == '__main__':
    ma_test_result = pd.read_pickle('./data/ma_test_result.pkl')
    all_trades = pd.read_pickle('./data/all_trades.pkl')
    create_excel(ma_test_result, all_trades)




"""
we added this function to the f_maSim.py and idk the reason but we made the
funtion in here and then added this to that file
"""