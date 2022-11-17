import requests
import pandas as pd
import authentication
import toolbox

class OandaApi():

    def __init__(self):
        self.session = requests.Session()

    def fetch_instruments(self):
        url = f"{authentication.OANDA_URL}/accounts/{authentication.ACCOUNT_ID}/instruments"
        response = self.session.get(url, params=None, headers=authentication.SECURE_HEADER)
        return response.status_code, response.json()

    def get_instruments_df(self):
        code ,data = self.fetch_instruments()
        if code ==200:
            df = pd.DataFrame.from_dict(data['instruments'])
            return df[['name', 'type', 'displayName', 'pipLocation', 'marginRate']]
        else:
            return None

    def save_instruments(self):
        df = self.get_instruments_df()
        if df is not None:
            df.to_pickle(toolbox.get_instruments_data_filename())

    def fetch_candles(self, pair_name, count, granularity):
        url = f"{authentication.OANDA_URL}/instruments/{pair_name}/candles"

        params = dict(
            count = count,
            granularity = granularity,
            price = "MBA"
        )

        response = self.session.get(url, params=params, headers=authentication.SECURE_HEADER)

        return response.status_code, response.json()


if __name__ == '__main__':
    api = OandaApi()
    api.save_instruments()