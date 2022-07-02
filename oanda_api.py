# this file creates a file containing candles of the available piars to trade

from pydoc import resolve
import requests
import pandas as pd
import credentials
import utils

class OandaAPI():

    def __init__(self):
        self.session = requests.Session()

    def fetch_instruments(self):
        url = f"{credentials.OANDA_URL}/accounts/{credentials.ACCOUNT_ID}/instruments"
        response = self.session.get(url, params=None, headers=credentials.SECURE_HEADER)
        return response.status_code, response.json()

    def get_instruments_df(self):
        code, data = self.fetch_instruments()
        if code == 200:
            df = pd.DataFrame.from_dict(data['instruments'])
            return df[['name', 'type', 'displayName', 'pipLocation', 'marginRate']]
        else:
            return None

    def save_instruments(self):
        df = self.get_instruments_df()
        if df is not None:
            df.to_pickle(utils.get_instruments_data_filename())

    def fetch_candles(self, pair_name, count=None, granularity="H1", date_from=None, date_to=None):
        url = f"{credentials.OANDA_URL}/instruments/{pair_name}/candles"

        params = dict(
            granularity = granularity,
            price = "MBA"
        )

        if date_from is not None and date_to is not None:
            params['to'] = int(date_to.timestamp())
            params['from'] = int(date_from.timestamp())
        elif count is not None:
            params['count'] = count
        else:
            params['count'] = 300

        response = self.session.get(url, params=params, headers=credentials.SECURE_HEADER)

        return response.status_code, response.json()


# apparently the limit of getting candles from oanda api is 5000  
if __name__ == "__main__":
    api = OandaAPI()
    # api.save_instruments()
    date_from = utils.get_utc_dt_from_string("2022-01-01 18:00:00")
    date_to = utils.get_utc_dt_from_string("2022-06-28 12:00:00")
    print(api.fetch_candles("EUR_USD", date_from=date_from, date_to=date_to))